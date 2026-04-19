# Setup Guide

## Goal

Run a local Botpress v12 instance with the fewest moving parts possible so you can learn the product, not wrestle with infrastructure.

## Prerequisites

- Docker Desktop or Docker Engine with Compose
- A browser
- Enough free disk space for the Botpress image and local runtime data

## Files Used

- `docker-compose.yml`
- `.env.example`
- Docker named volume `botpress_data` created automatically on first start

## Start The Runtime

From this repo:

```bash
docker compose up -d
```

Then open:

```text
http://localhost:3000
```

## Stop The Runtime

```bash
docker compose down
```

This keeps the local Botpress data in the Docker named volume `botpress_data`.

## Reset The Runtime

If you want to start over completely, stop the containers and remove the Docker volume.

Do that only when you are okay losing local Botpress state.

## First-Time Learning Tasks

Once the UI loads:

1. Look around the main admin/studio interface.
2. Create one learning bot.
3. Name it something obvious like `learning-lab-bot`.
4. Build only the small bot described in `sample-bot/bot-brief.md`.
5. Test one known-answer path and one fallback path.

## What To Pay Attention To

- Where bot settings live
- How flows are created and edited
- How content/Q&A is entered
- How fallback behavior is configured
- How the webchat preview behaves
- What would be hard to explain to a teammate later

## Troubleshooting Notes

If the image pull fails:

- confirm Docker can reach GitHub Container Registry
- try `docker compose pull`
- confirm the image tag in `.env.example` still exists

If the UI loads slowly on first start:

- give the container another minute before assuming it failed
- inspect logs with `docker compose logs botpress`

If you need a clean restart:

- `docker compose down`
- `docker compose up -d`
