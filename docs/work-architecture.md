# Work Architecture Note

This note is the simplest practical mental model for the work version of this project.

## The Core Split

Think about the system as three separate layers:

1. `client-facing website`
   - owned by the website/application team
   - renders the chat entry point in their page
   - sends chat requests to your chatbot service

2. `Botpress service`
   - owned by your team
   - hosts Botpress Studio/admin for internal users
   - hosts the runtime that executes flows and bot logic
   - stores bot config and chatbot state internally

3. `local NLP and optional local LLM services`
   - also owned by your team
   - provide the language-processing layer Botpress needs
   - optionally provide generative/model-based features later

## What Botpress Needs By Itself

For native Botpress v12 flows and NLU, the minimum internal stack is:

- `botpress-v12-lab`
- `botpress-v12-lang`
  - local Duckling
  - local Botpress language server

That stack is what satisfies the basic Botpress flow/intents path.

For the work version, the clean access model is:

- internal Botpress Studio/admin stays private
- internal editors authenticate through your work auth layer such as AD FS in front of Botpress
- public or client-facing pages only talk to the chatbot-facing service layer
- the public/chat side should not expose the internal editing surface

## Where vLLM Or Ollama Fit

`vLLM` and `Ollama` do **not** replace the Botpress language server.

They only become useful if you want to add a second capability such as:

- generative answers
- summarization
- retrieval-augmented responses
- custom actions that call a local model endpoint

So the clean architecture is:

- first, get Botpress working fully internal with its own local language server
- second, decide whether you actually need an LLM sidecar

## When To Prefer vLLM

Prefer `vLLM` if:

- the work server already has it running
- you want an OpenAI-compatible local inference endpoint
- you expect GPU-backed inference at higher throughput
- your team is comfortable operating a model-serving container

This is the better fit for a more serious internal model service.
It also means your existing `vLLM 0.18.1` container at work may already be enough if you later add model-powered features.

## When To Prefer Ollama

Prefer `Ollama` if:

- you want simpler local experimentation
- you want easy model pulls and lightweight testing
- you are still validating model behavior rather than designing a more formal inference service

This is the better fit for fast local experimentation.

## Practical Recommendation

For this Botpress project, the order should be:

1. prove Botpress can run fully internally with the local language-server setup
2. prove internal flow editors can log in and manage flows safely
3. prove the website team can consume the chatbot as a separate service
4. only then decide whether a local `vLLM` or `Ollama` sidecar is needed

This also matches the current phased direction:

1. `phase 1 now`
   - run Botpress as a hosted service
   - learn its strengths and limits in actual usage
2. `phase 2 only if needed later`
   - fork and modify Botpress source if real product gaps justify that cost

If the real chatbot behavior is mostly:

- guided flows
- FAQs
- fallback routing
- business-owned flow editing

then you may not need a local LLM at all for the first version.

If later you want:

- more open-ended answers
- retrieval over internal documents
- model-based summarization or rewriting

then a local `vLLM` sidecar is probably the best production-style fit, especially since you already have GPU-backed `vLLM 0.18.1` at work.

For your shared-GPU environment, the safer starting posture is:

- do not require an LLM for version one unless the flows clearly need it
- if you add `vLLM`, start with one GPU, not both
- cap GPU usage conservatively instead of using the default aggressive memory behavior
- prefer a smaller instruct model before trying to stretch into heavier models
- treat any move to a larger model or multi-GPU setup as a separate team decision

## Suggested Work Shape

Keep the work system mentally separated like this:

- website team embeds chat entry point
- your team hosts Botpress
- your team hosts the local Botpress language server
- your team protects the internal Botpress admin side with work auth and role restrictions
- optional local `vLLM` service is used only by Botpress actions or custom integrations, not as the base Botpress NLU replacement
- a Botpress source fork is reserved for later only if the hosted-service path proves insufficient
