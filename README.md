# Botpress v12 Work-Prep Starter

This repo is a personal work-prep starter for legacy self-hosted Botpress v12.

It is meant to help you:

- how to run Botpress v12 locally
- prove whether Botpress can stay fully internal for its native NLU path
- understand how the Studio/admin side and the client-facing chat side would be separated
- prepare cleaner questions, architecture notes, and deployment instincts for the real work project

The default stack in this repo now follows the more realistic on-prem Botpress v12 pattern:

- `botpress-v12-lab`: Botpress server and Studio/admin UI
- `botpress-v12-lang`: self-hosted Botpress language server plus Duckling

This is still not a production-ready chatbot service, but it is now set up to validate a much stricter on-prem path than the upstream defaults.

## What Is In This Repo

- `manage.py`: Python control script for starting, inspecting, and validating the local Botpress stack
- `docker-compose.yml`: the primary local Botpress v12 runtime with a self-hosted language server
- `ops/compose.onprem-check.yml`: optional validation override that blocks known Botpress-hosted runtime endpoints
- `.env.example`: example runtime overrides
- `docs/setup.md`: step-by-step local setup
- `docs/learning-path.md`: a focused 2-week learning plan
- `docs/work-notes.md`: notes template for what you learn
- `docs/integration-observations.md`: how to think about the likely service boundary at work
- `docs/botpress-onprem-validation.md`: what is and is not local by default, and how to validate it yourself
- `docs/chatbot-modes.md`: the plain-English difference between NLU, hybrid, and LLM-first chatbot designs
- `docs/work-architecture.md`: where Botpress ends and where an optional local `vLLM` or `Ollama` sidecar would fit
- `docs/work-readiness-checklist.md`: what is already proven vs what still needs work-environment validation
- `docs/manager-alignment.md`: the simplest talking points and clarification questions for your manager
- `sample-bot/`: a tiny bot brief and sample content to recreate inside Botpress

## Quick Start

1. Install Docker Desktop or Docker Engine with Compose support.
2. Copy `.env.example` to `.env` if you want to override defaults.
3. Start Botpress:

```bash
python3 manage.py start
```

If you want to bootstrap the stricter offline-ready path in one step:

```bash
python3 manage.py prepare-offline
```

If you want to pre-download the English language assets for the local language server manually:

```bash
python3 manage.py download-language en
```

If you want to test the stricter local-only path after the assets are present:

```bash
python3 manage.py start-onprem-check
```

4. Open `http://localhost:3000`.
5. Follow [docs/setup.md](docs/setup.md).

Botpress data is stored in a Docker named volume in this setup, which avoids Windows/WSL path issues during local learning.
Language-server assets are stored in a separate Docker named volume.
The main Botpress port binds to `127.0.0.1` by default for a safer local/server posture. If you later need a different bind host, override `BOTPRESS_BIND_HOST` in `.env`.

## What We Proved

We verified three important things in this repo:

1. Default Botpress v12 is not fully local.
   It tries to use Botpress-hosted language infrastructure by default.
2. Botpress v12 supports a self-hosted replacement path.
   We rewired the runtime to a local Botpress language server plus local Duckling.
3. The stricter local-only design can keep working offline.
   After preloading the English language assets, we started Botpress with the known Botpress-hosted runtime domains blocked and the stack still came up cleanly.

That means this repo is now best thought of as:

- a work-prep starter
- a validation artifact for “can Botpress stay internal?”
- not the final work deployment repo itself

## Current Project Direction

Based on manager guidance, the intended path is:

1. `Phase 1`
   - deploy and learn the self-hosted Botpress service model
   - validate what works and what does not in real usage
2. `Phase 2`
   - only if needed later, fork the Botpress source and change platform internals
   - do this only after real usage reveals gaps that configuration and supported extensions cannot solve

So this repo is intentionally optimized for phase 1, not for maintaining a Botpress source fork.

## Local Architecture

The key architectural point is that Botpress v12's "language server" is not a modern LLM endpoint. It serves tokenization and vectorization assets used by Botpress NLU.

That means:

- `vLLM` is not the direct replacement for Botpress's external language dependency
- `Ollama` is not the direct replacement for Botpress's external language dependency
- the correct first replacement is the Botpress `lang-server` itself

If you later want generative responses, summaries, or retrieval-style answers, that can still be added as a second layer with a local `vLLM` or `Ollama` sidecar.

If your work server already has a usable `vLLM` service, that is the better serious candidate for later model-powered features.

## Recommended Working Order

1. Get Botpress running locally.
2. Read [docs/setup.md](docs/setup.md).
3. Recreate the sample bot described in [sample-bot/bot-brief.md](sample-bot/bot-brief.md).
4. Capture notes in [docs/work-notes.md](docs/work-notes.md).
5. Review [docs/botpress-onprem-validation.md](docs/botpress-onprem-validation.md) to understand what was actually proven.
6. Review [docs/chatbot-modes.md](docs/chatbot-modes.md) and [docs/work-architecture.md](docs/work-architecture.md) to understand the difference between the current NLU setup and future hybrid/LLM options.
7. Review [docs/work-readiness-checklist.md](docs/work-readiness-checklist.md) to map this into the work environment.
8. Use [docs/manager-alignment.md](docs/manager-alignment.md) if you need to clarify scope with your manager.

## On-Prem Validation

This repo now includes a stricter validation path for the requirement "nothing leaves the premises."

- `python3 manage.py inspect`
  - shows the live Botpress config, NLU config, logs, and HTTP status
- `python3 manage.py harden-runtime`
  - turns off usage stats and rewrites Duckling to local runtime config
- `python3 manage.py start-onprem-check`
  - starts Botpress with the optional validation override from `ops/compose.onprem-check.yml`
- `python3 manage.py download-language en`
  - downloads the metadata index and the English language assets into the local language-server volume
- `python3 manage.py prepare-offline en`
  - preloads the language assets and restarts the stack in offline mode

Important:

- The default upstream Botpress v12 runtime is **not** fully local by default.
- This repo now overrides that design by wiring Botpress to a self-hosted Botpress language server with `BP_MODULE_NLU_LANGUAGESOURCES`.
- We already validated that the local architecture can still start when the known Botpress-hosted runtime domains are blocked, as long as the language assets were downloaded beforehand.

## What Is Satisfied Now

Within the limits of a home work-prep repo, the following are satisfied:

- Botpress runs self-hosted in Docker on Linux
- the native Botpress NLU path can be kept local after preloading language assets
- the stricter local-only validation path is repeatable through `manage.py`
- the repo is Python-driven at the control layer instead of shell-script driven
- the design keeps Botpress separate from any optional future local LLM service

## What Is Still Deferred To Work

These items belong to the real work environment, not this home starter:

- AD FS integration and internal editor access control
- reverse proxy, TLS, DNS, and public/internal route separation
- backup, monitoring, alerting, and log retention
- final decision on whether a local `vLLM` sidecar is needed at all
- shared GPU policy if model-backed features are added later

## What This Repo Is Not

This repo is not:

- a fork of the Botpress platform source
- a final production deployment
- proof that AD FS, role restrictions, or website integration are already solved
- a Python application that imports Botpress as a library

Botpress is being used here as a self-hosted platform runtime. The Python in this repo is an orchestration layer for local bring-up, validation, and work-prep operations.

## Important Legacy Context

Botpress v12 is legacy software. This repo is only for learning and preparation.

- Treat it as a local sandbox, not as a production deployment.
- If installation is awkward or outdated, that is still useful learning.
- Prefer noting friction down rather than trying to over-engineer around it here.
