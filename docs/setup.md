# Setup Guide

## Goal

Run a local Botpress v12 instance in a way that stays simple but is closer to a real on-prem architecture you could discuss at work.

## Prerequisites

- Docker Desktop or Docker Engine with Compose
- A browser
- Enough free disk space for the Botpress image and local runtime data

## Files Used

- `manage.py`
- `docker-compose.yml`
- `ops/compose.onprem-check.yml`
- `.env.example`
- Docker named volume `botpress_data` created automatically on first start
- Docker named volume `botpress_lang_data` created automatically on first start

## Start The Runtime

From this repo:

```bash
python3 manage.py start
```

This starts two containers:

- `botpress-v12-lab`
- `botpress-v12-lang`

By default, the Botpress browser port is bound to `127.0.0.1` only. That is intentional so the starter does not expose the admin UI broadly on a Linux server unless you explicitly change it.

Then open:

```text
http://localhost:3000
```

## Download The Local Language Assets

The self-hosted language server needs its model files available locally.

For English, run:

```bash
python3 manage.py download-language en
```

This downloads:

- the metadata index used by the local language server
- the English tokenization/vectorization assets into the `botpress_lang_data` Docker volume

This step needs internet access once.
After the assets are downloaded, you can restart in stricter offline mode.

If you want to handle the online bootstrap plus offline restart in one step, use:

```bash
python3 manage.py prepare-offline
```

## Start In Offline Mode

After downloading the assets once, you can start the stack in offline mode:

```bash
python3 manage.py prepare-offline
```

If you want the stricter test that also blocks the known Botpress-hosted runtime domains inside the containers:

```bash
python3 manage.py start-onprem-check
```

That is the most useful local proof for the requirement that Botpress should keep working without relying on those hosted Botpress runtime endpoints.

## Stop The Runtime

```bash
python3 manage.py stop
```

This keeps the local Botpress data in the Docker named volume `botpress_data`.
The self-hosted language server keeps its model assets in the Docker named volume `botpress_lang_data`.

## Reset The Runtime

If you want to start over completely, stop the containers and remove the Docker volumes.

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
- Whether the self-hosted language server behaves cleanly enough for a strictly internal deployment
- Whether the preloaded offline language assets are enough for the languages you care about
- What parts of the final work project are clearly “runtime hosting” vs “flow/content management”

## Troubleshooting Notes

If the image pull fails:

- confirm Docker can reach GitHub Container Registry
- try `docker compose pull`
- confirm the image tag in `.env.example` still exists

If the UI loads slowly on first start:

- give the container another minute before assuming it failed
- inspect logs with `docker compose logs botpress`

If you need a clean restart:

- `python3 manage.py stop`
- `python3 manage.py start`

If you want to inspect the runtime:

- `python3 manage.py inspect`

If the language download looks stuck:

- inspect `docker logs botpress-v12-lang`
- confirm the language volume is writable
- retry `python3 manage.py download-language en`
