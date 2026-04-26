#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAIN_COMPOSE = ROOT / "docker-compose.yml"
ONPREM_OVERRIDE = ROOT / "ops" / "compose.onprem-check.yml"
DOTENV_PATH = ROOT / ".env"
BOT_SERVICE = "botpress"
LANG_SERVICE = "botpress-lang"


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


DOTENV = load_dotenv(DOTENV_PATH)


def env_value(name: str, default: str) -> str:
    return os.environ.get(name, DOTENV.get(name, default))


def local_http_url() -> str:
    return f"http://localhost:{env_value('BOTPRESS_PORT', '3000')}"


def run(cmd: list[str], *, env: dict[str, str] | None = None, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    merged_env.setdefault("COMPOSE_REMOVE_ORPHANS", "1")
    if env:
        merged_env.update(env)
    return subprocess.run(
        cmd,
        cwd=ROOT,
        env=merged_env,
        check=check,
        text=True,
        capture_output=capture,
    )


def compose(args: list[str], *, env: dict[str, str] | None = None, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["docker", "compose", *args], env=env, capture=capture, check=check)


def compose_with_override(args: list[str], *, env: dict[str, str] | None = None, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(
        [
            "docker",
            "compose",
            "-f",
            str(MAIN_COMPOSE),
            "-f",
            str(ONPREM_OVERRIDE),
            *args,
        ],
        env=env,
        capture=capture,
        check=check,
    )


def docker(args: list[str], *, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["docker", *args], capture=capture, check=check)


def compose_exec(service: str, shell_command: str, *, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    return compose(["exec", "-T", service, "sh", "-lc", shell_command], capture=capture, check=check)


def compose_logs(service: str, *, tail: int = 80, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    return compose(["logs", "--tail", str(tail), service], capture=capture, check=check)


def wait_for_http_ready(url: str, timeout_seconds: int = 30) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            request = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(request, timeout=3) as response:
                if 200 <= response.status < 400:
                    return True
        except (urllib.error.URLError, TimeoutError, ConnectionResetError, OSError, http.client.HTTPException):
            time.sleep(1)
    return False


def print_runtime_open_message() -> None:
    print(flush=True)
    print("Botpress v12 work-prep starter should be running.", flush=True)
    print(f"Open: {env_value('BOTPRESS_EXTERNAL_URL', local_http_url())}", flush=True)


def start(_: argparse.Namespace) -> int:
    compose(["up", "-d"])
    print_runtime_open_message()
    return 0


def stop(_: argparse.Namespace) -> int:
    compose(["down", "--remove-orphans"])
    print(flush=True)
    print("Botpress v12 work-prep starter stopped.", flush=True)
    return 0


def start_onprem_check(_: argparse.Namespace) -> int:
    compose_with_override(["up", "-d"], env={"BOTPRESS_LANG_OFFLINE": "true"})
    print(flush=True)
    print("Botpress started in strict on-prem check mode.", flush=True)
    print("Known Botpress-hosted runtime domains are mapped to localhost inside the containers.", flush=True)
    print(f"Open: {env_value('BOTPRESS_EXTERNAL_URL', local_http_url())}", flush=True)
    return 0


def download_language(args: argparse.Namespace) -> int:
    lang = args.language or env_value("BOTPRESS_BOOTSTRAP_LANGUAGE", "en")
    lang_dir = env_value("BOTPRESS_LANG_DIR", "/botpress/lang")
    lang_port = env_value("BOTPRESS_LANG_PORT", "3100")
    metadata_url = env_value(
        "BOTPRESS_LANG_REMOTE_METADATA_URL",
        "https://nyc3.digitaloceanspaces.com/botpress-public/embeddings/index.json",
    )

    compose(["up", "-d", LANG_SERVICE], env={"BOTPRESS_LANG_OFFLINE": "false"})
    compose(["exec", "-T", "--user", "0", LANG_SERVICE, "sh", "-lc", f"mkdir -p {lang_dir} && chown -R botpress:botpress {lang_dir}"])
    compose_exec(LANG_SERVICE, f"wget -qO {lang_dir}/index.json {metadata_url}")
    compose(["restart", LANG_SERVICE])
    time.sleep(5)

    requested = False
    for _ in range(60):
        result = compose_exec(
            LANG_SERVICE,
            f"wget -qO- --post-data='' http://localhost:{lang_port}/languages/{lang} >/dev/null 2>&1",
            check=False,
        )
        if result.returncode == 0:
            requested = True
            break
        time.sleep(2)

    if not requested:
        print(f"The local language server did not accept the '{lang}' download request in time.", file=sys.stderr)
        print("Check: docker logs botpress-v12-lang", file=sys.stderr)
        return 1

    print(flush=True)
    print(f"Requested language download for '{lang}'.", flush=True)
    print("Use `python3 manage.py inspect` and `docker compose logs botpress-lang` to monitor progress.", flush=True)
    return 0


def prepare_offline(args: argparse.Namespace) -> int:
    lang = args.language or env_value("BOTPRESS_BOOTSTRAP_LANGUAGE", "en")
    print("Starting the local Botpress language server so assets can be downloaded...", flush=True)
    compose(["up", "-d", LANG_SERVICE], env={"BOTPRESS_LANG_OFFLINE": "false"})
    time.sleep(5)

    if download_language(argparse.Namespace(language=lang)) != 0:
        return 1

    print(flush=True)
    print("Restarting the full stack in offline mode...", flush=True)
    compose(["up", "-d"], env={"BOTPRESS_LANG_OFFLINE": "true"})
    print(flush=True)
    print("Offline-ready Botpress starter should now be running.", flush=True)
    print(f"Open: {env_value('BOTPRESS_EXTERNAL_URL', local_http_url())}", flush=True)
    print("Use `python3 manage.py inspect` to verify the live configuration.", flush=True)
    return 0


def inspect_runtime(_: argparse.Namespace) -> int:
    print("== Container Status ==", flush=True)
    compose(["ps"])

    print(flush=True)
    print("== HTTP Check ==", flush=True)
    local_url = local_http_url()
    if wait_for_http_ready(local_url, timeout_seconds=10):
        try:
            request = urllib.request.Request(local_url, method="HEAD")
            with urllib.request.urlopen(request, timeout=3) as response:
                print(f"HTTP {response.status} {response.reason}")
                for key, value in response.headers.items():
                    print(f"{key}: {value}")
        except (urllib.error.URLError, TimeoutError, ConnectionResetError, OSError, http.client.HTTPException) as exc:
            print(f"Botpress responded during startup checks but the final HTTP probe still failed: {exc}")
    else:
        print("Botpress did not answer HTTP HEAD within the expected window.")
    print(f"Configured external URL: {env_value('BOTPRESS_EXTERNAL_URL', local_url)}")

    print(flush=True)
    print("== Botpress Runtime Env ==", flush=True)
    env_lines = docker(
        ["inspect", compose(["ps", "-q", BOT_SERVICE], capture=True).stdout.strip(), "--format", "{{range .Config.Env}}{{println .}}{{end}}"],
        capture=True,
    ).stdout.splitlines()
    for line in env_lines:
        if line.startswith("BP_MODULE_NLU_"):
            print(line)

    print(flush=True)
    print("== Botpress Config ==", flush=True)
    compose_exec(
        BOT_SERVICE,
        "sed -n '/\"superAdmins\": \\[/,/\\],/p' /botpress/data/global/botpress.config.json && "
        "sed -n '/\"sendUsageStats\":/p;/\"eventCollector\": {/,/  },/p;/\"authStrategies\": {/,/  },/p' "
        "/botpress/data/global/botpress.config.json",
    )

    print(flush=True)
    print("== NLU Config ==", flush=True)
    compose_exec(
        BOT_SERVICE,
        "sed -n '/\"nluServer\": {/,/  },/p;/\"ducklingURL\":/p;/\"ducklingEnabled\":/p;/\"languageSources\": \\[/,/\\]/p' "
        "/botpress/data/global/config/nlu.json",
    )
    print("Note: the persisted nlu.json may still show the legacy remote language source, but the live BP_MODULE_NLU_* environment overrides above are what the running NLU server actually uses.")

    print(flush=True)
    print("== Lang Server Recent Logs ==", flush=True)
    compose_logs(LANG_SERVICE)

    print(flush=True)
    print("== Botpress Recent Logs ==", flush=True)
    compose_logs(BOT_SERVICE)
    return 0


def harden_runtime(args: argparse.Namespace) -> int:
    language_source_url = args.language_source_url or os.environ.get("BOTPRESS_LANGUAGE_SOURCE_URL", "")
    compose_exec(
        BOT_SERVICE,
        "set -e\n"
        "cp /botpress/data/global/botpress.config.json /botpress/data/global/botpress.config.json.bak\n"
        "cp /botpress/data/global/config/nlu.json /botpress/data/global/config/nlu.json.bak\n"
        "perl -0pi -e 's/\"sendUsageStats\": true/\"sendUsageStats\": false/g' /botpress/data/global/botpress.config.json\n"
        "perl -0pi -e 's#\"ducklingURL\": \"https://duckling\\.botpress\\.io\"#\"ducklingURL\": \"http://localhost:8000\"#g' /botpress/data/global/config/nlu.json\n",
    )

    if language_source_url:
        compose_exec(
            BOT_SERVICE,
            "perl -0pi -e 's#\"languageSources\": \\[\\s*\\{\\s*\"endpoint\": \"[^\"]+\"\\s*\\}\\s*\\]#"
            f"\"languageSources\": [\\n    {{\\n      \"endpoint\": \"{language_source_url}\"\\n    }}\\n  ]#s' "
            "/botpress/data/global/config/nlu.json",
        )

    compose(["restart", BOT_SERVICE])
    print(flush=True)
    print("Runtime config patched and container restarted.", flush=True)
    print("Use `python3 manage.py inspect` to confirm the live settings.", flush=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Botpress v12 work-prep starter control script")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "start": start,
        "stop": stop,
        "start-onprem-check": start_onprem_check,
        "inspect": inspect_runtime,
        "prepare-offline": prepare_offline,
        "download-language": download_language,
        "harden-runtime": harden_runtime,
    }

    for name, func in commands.items():
        sub = subparsers.add_parser(name)
        sub.set_defaults(func=func)

    subparsers.choices["prepare-offline"].add_argument("language", nargs="?")
    subparsers.choices["download-language"].add_argument("language", nargs="?")
    subparsers.choices["harden-runtime"].add_argument("--language-source-url")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
