# Botpress v12 Learning Sandbox

This repo is a personal learning sandbox for legacy self-hosted Botpress v12.

It is intentionally small. The point is to help you learn:

- how to run Botpress v12 locally
- how the Studio/admin UI feels
- how to create a bot, flows, FAQs, and fallback behavior
- how webchat/embed likely works at a high level
- what questions to carry into the real work project later

This is not a production-ready chatbot service.

## What Is In This Repo

- `docker-compose.yml`: local Botpress v12 runtime
- `.env.example`: optional runtime overrides
- `scripts/start.ps1`: start helper for Windows PowerShell
- `scripts/stop.ps1`: stop helper for Windows PowerShell
- `docs/setup.md`: step-by-step local setup
- `docs/learning-path.md`: a focused 2-week learning plan
- `docs/work-notes.md`: notes template for what you learn
- `docs/integration-observations.md`: how to think about the likely service boundary at work
- `sample-bot/`: a tiny bot brief and sample content to recreate inside Botpress

## Quick Start

1. Install Docker Desktop or Docker Engine with Compose support.
2. Copy `.env.example` to `.env` if you want to override defaults.
3. Start Botpress:

```bash
docker compose up -d
```

Or from PowerShell:

```powershell
./scripts/start.ps1
```

4. Open `http://localhost:3000`.
5. Follow [docs/setup.md](docs/setup.md).

Botpress data is stored in a Docker named volume in this setup, which avoids Windows/WSL path issues during local learning.

## Recommended Learning Order

1. Get Botpress running locally.
2. Read [docs/setup.md](docs/setup.md).
3. Recreate the sample bot described in [sample-bot/bot-brief.md](sample-bot/bot-brief.md).
4. Capture notes in [docs/work-notes.md](docs/work-notes.md).
5. Review [docs/integration-observations.md](docs/integration-observations.md) once you have tested webchat locally.

## Important Legacy Context

Botpress v12 is legacy software. This repo is only for learning and preparation.

- Treat it as a local sandbox, not as a production deployment.
- If installation is awkward or outdated, that is still useful learning.
- Prefer noting friction down rather than trying to over-engineer around it here.
