# Manager Alignment Note

These are the simplest points to align on before the real work starts.

## Recommended Direction

The best default approach is:

- self-host Botpress as a service
- configure and secure it for your environment
- avoid forking Botpress source unless a hard blocker forces that decision

## Current Manager Direction

The current direction is now clearer:

- `phase 1`
  - use Botpress as a self-hosted service
  - learn from real usage first
- `phase 2 later if needed`
  - fork and modify Botpress source only after you know what the service model cannot handle

That means the team is not choosing between the two paths immediately.
It is choosing the service path first, and keeping the source-fork path as a later fallback.

## Why That Direction Fits Better

- it matches the service model where your team hosts chatbot capability and another team consumes it
- it keeps the internal admin surface separate from the client-facing website
- it is faster to prove and easier to hand off to business-owned flow editors
- it avoids taking ownership of a legacy Botpress code fork unless absolutely necessary

## Best Clarifying Questions

Ask these first:

1. Do you expect us to deploy and configure self-hosted Botpress, or do you expect us to fork and modify Botpress source code itself?
2. Is “no chatbot or NLU data leaves our network” a hard requirement?
3. Do you want the first version to be a flow-based NLU chatbot, an LLM chatbot, or a hybrid where flows stay in Botpress and only certain steps call a local model?
4. Will AD FS protect only the internal admin side, or do end users also need authenticated chat access?
5. If we later add a local model service, what GPU budget can we actually reserve on the shared server?
6. Are internal users mainly expected to maintain flows and routing, or do you also expect them to control model-backed answer behavior?

## Short Explanation Of The Options

- `NLU chatbot`
  - Botpress handles flows, routing, and responses with its own NLU stack
  - best when internal users mainly manage guided flows
- `Hybrid Botpress + LLM chatbot`
  - Botpress still handles flows, but some steps call a local model
  - best when you want both internal flow ownership and smarter AI behavior
- `LLM-first chatbot`
  - a model generates most answers directly
  - best when open-ended AI is the priority, but it reduces business-user control

## Practical Technical Position

The current repo result supports this position:

- self-hosting Botpress as a service looks viable
- strict local processing looks much more viable when Botpress uses a self-hosted Botpress language server
- a local `vLLM` service is optional and should only be added if the chatbot needs model-powered behavior beyond native Botpress flows and NLU
- a future source fork should be justified by real gaps discovered after phase 1, not by guesswork up front
