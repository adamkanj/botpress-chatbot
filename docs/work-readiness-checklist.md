# Work Readiness Checklist

Use this file to separate what is already proven in this repo from what still needs validation in the real work environment.

## Already Proven In This Repo

- Botpress v12 can run self-hosted in Docker
- Botpress Studio/admin can stay on your side as a private service
- the default external Botpress language dependency can be replaced with a self-hosted Botpress language server
- the local language server can preload English assets and then run in offline mode
- Botpress can start while the known Botpress-hosted runtime domains are blocked, as long as the required assets were downloaded first

## Still Needs Work-Environment Validation

### Internal Editor Access

- decide where AD FS sits in front of the internal Botpress admin URL
- define who gets editor/admin access
- confirm whether Botpress-side roles are enough or whether access should be enforced mostly at the proxy/auth layer
- decide how the first local bootstrap admin account will be retired or limited once work auth is in place

### Public Or Client-Facing Chat Access

- decide whether the website team uses a widget, custom frontend, or a narrow integration layer
- keep the public/chat-facing endpoint separate from the internal admin surface
- define any session or user context that needs to be passed from the client-facing application

### Hosting And Networking

- set the real `BOTPRESS_EXTERNAL_URL`
- place Botpress behind TLS and a reverse proxy
- keep the local language server private to the trusted network
- keep the standalone NLU service private
- enforce egress rules if “nothing leaves the network” is a hard requirement
- decide whether metadata and image pulls should come directly from the internet or from an internal mirror

### Data And Storage

- decide where persistent Docker volumes live at work
- define backup and restore expectations
- define log retention expectations
- confirm which data is allowed to be stored in conversation logs
- decide whether chat logs need masking, redaction, or stricter retention controls

### Bot Ownership Model

- decide who creates the first set of flows
- define how managers or department leads will update flows later
- define a promotion/change process before business-owned flow changes go live

### Optional Local LLM Layer

- decide whether the first version needs an LLM at all
- if yes, prefer the existing work `vLLM` service before adding another inference runtime
- keep the local LLM as an optional sidecar, not as the replacement for Botpress native NLU
- keep to one GPU first if the service is shared with teammates
- avoid the default high GPU reservation behavior when running on shared cards
- prefer a smaller or quantized instruct model first and add larger models only if the use case really needs them
- decide an explicit GPU-memory budget with the team before enabling any production-facing model service

### Monitoring And Operations

- define container restart and health-check expectations in the work environment
- define where Docker/container logs will be collected
- define who gets alerted when Botpress or the language server fails
- decide who owns patching the legacy Botpress runtime and how often that review happens

## Recommended First Work Milestone

The first practical milestone should be:

1. self-hosted Botpress runtime
2. self-hosted Botpress language server
3. one private internal editor path
4. one client-facing chat path
5. one sample bot that proves the end-to-end service boundary

That is enough to validate the architecture before spending time on heavier customization.
