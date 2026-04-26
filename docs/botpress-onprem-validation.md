# Botpress v12 On-Prem Validation

This note captures what we verified ourselves about legacy self-hosted Botpress v12 and what changed in this repo.

## Short Verdict

Botpress v12 is **not fully local by default**, but Botpress's own v12 docs support a self-hosted language-server architecture.

This repo now follows that architecture:

- `botpress-v12-lab`
  - Botpress server and Studio/admin UI
- `botpress-v12-lang`
  - local Duckling
  - local Botpress language server

That changes the core question from:

- "Does default Botpress call external services?"

to:

- "Does the self-hosted language-server architecture remove the outbound dependency cleanly enough for our needs?"

Based on our latest validation in this repo, the answer looks like:

- `yes for the native Botpress NLU path`, if you self-host `lang-server`, preload the required language assets, and run the language server in offline mode afterward

## What We Verified

### 1. Default Botpress v12 is not fully local

Before the compose update, the live runtime and source code both showed:

- local Botpress server on port `3000`
- local Studio/admin UI
- local Duckling process on `http://localhost:8000`
- local standalone NLU process on `http://localhost:3200`
- default external language source at `https://lang-01.botpress.io`

The generated runtime config also showed:

- `sendUsageStats: true`
- `ducklingURL: "https://duckling.botpress.io"`
- `languageSources[0].endpoint: "https://lang-01.botpress.io"`

### 2. Blocking the default external language source breaks NLU

We validated this directly.

When we blocked the known Botpress-hosted runtime domains inside the container, the NLU service failed during startup and entered a restart loop. The logs showed:

- timeout / refused connection when contacting `https://lang-01.botpress.io`
- `Could not load Language Provider`
- `There was an error while initializing Engine tools`
- repeated NLU restarts until the maximum reboot count was exceeded

That proved the default setup does **not** satisfy a strict "nothing leaves the network" requirement.

### 3. Botpress documents a self-hosted replacement path

Botpress's own v12 Docker documentation explicitly supports:

- a separate self-hosted language server
- `BP_MODULE_NLU_LANGUAGESOURCES` pointing Botpress to that local service
- `BP_MODULE_NLU_DUCKLINGURL` pointing Botpress to a local Duckling service

That is the architecture now used by `docker-compose.yml` in this repo.

### 4. The self-hosted language-server path worked in offline mode

After switching the repo to a two-container architecture, we:

1. downloaded the language metadata index locally
2. downloaded the English language assets into the language-server volume
3. restarted the stack with the language server in offline mode
4. blocked the known Botpress-hosted runtime domains inside both containers

The result:

- the local language server still loaded the pre-downloaded English assets
- Botpress still pointed at the local language server and local Duckling
- the Botpress stack started cleanly

That is the strongest proof we have so far that Botpress v12 can be pushed into a much more fully internal deployment model for its native NLU path.

## What The Botpress Language Server Actually Is

The Botpress language server is **not** a general LLM.

It hosts domain-agnostic NLP assets used by Botpress NLU, including:

- SentencePiece tokenization models
- FastText vectorization models

That means:

- `vLLM` is not the direct replacement for this dependency
- `Ollama` is not the direct replacement for this dependency
- the correct first replacement is the Botpress `lang-server` itself

If you later want generative responses or retrieval-augmented answers, you can still add a local LLM sidecar, but that is a second architectural layer, not the first fix for Botpress v12 NLU.

Examples of that second layer:

- local `vLLM` if you already have GPU-backed OpenAI-compatible inference available
- local `Ollama` if you want a simpler local model runtime for experimentation

## What To Validate Next

Use the Python control script in the repo root to validate the stricter requirement against the new architecture.

### Inspect the live runtime

```bash
python3 manage.py inspect
```

This shows:

- both containers
- the Botpress NLU environment overrides
- the persisted Botpress config
- recent logs from Botpress and the self-hosted language server

### Apply safer local defaults

```bash
python3 manage.py harden-runtime
```

This turns off usage stats and rewrites the persisted Duckling URL to the local service.

### Start in strict on-prem check mode

```bash
python3 manage.py start-onprem-check
```

This maps known Botpress-hosted runtime domains to localhost inside both containers:

- `lang-01.botpress.io`
- `duckling.botpress.io`
- `license.botpress.io`

If the updated local architecture still works in this mode, that is the strongest local proof that Botpress can be run without relying on those hosted runtime endpoints.

### Start in explicit offline mode

```bash
python3 manage.py prepare-offline
```

This sets `BOTPRESS_LANG_OFFLINE=true` for the self-hosted language server.

Before using it, make sure the required language assets were downloaded:

```bash
python3 manage.py download-language en
```

## Best-Practice Guidance For This Project

- keep the admin/studio UI internal only
- put Botpress behind a reverse proxy with TLS
- keep the public website integration limited to the chatbot endpoint/webchat layer
- do not expose the standalone NLU server directly
- do not expose the self-hosted language server directly outside your trusted network
- disable usage stats in any serious validation environment
- preload only the language assets you actually need
- treat the self-hosted language-server startup and offline behavior as the main go/no-go checkpoint
- treat any local LLM as an optional sidecar, not as the replacement for Botpress native NLU

## Practical Conclusion

Botpress v12 can still be used for:

- learning
- proof of concept
- evaluating internal editor workflows

Botpress v12 becomes a real fit for a strict on-prem deployment only if the self-hosted language-server architecture works reliably enough for your team to own.

Our current repo result is encouraging:

- default upstream Botpress v12 is not good enough
- Botpress v12 plus self-hosted `lang-server` plus preloaded offline assets looks much closer to the requirement
