# Chatbot Modes

This note is here to make the main architecture choice feel simple.

There are three realistic versions of this project:

1. `NLU chatbot`
2. `Hybrid Botpress + LLM chatbot`
3. `LLM-first chatbot`

## 1. NLU Chatbot

This is what the repo is currently set up to run.

How it works:

- a user sends a message
- Botpress receives it
- Botpress NLU tries to understand the intent
- Botpress routes the user into a flow, response, or fallback
- the reply comes from configured logic and content

What powers it:

- Botpress server
- Botpress standalone NLU
- Botpress language server
- local language assets such as `bp.en.100.bin`
- Duckling for structured extraction like dates and numbers

What it feels like:

- more controlled
- more predictable
- better for business-managed flows
- better for guided support journeys
- less “smart” in open-ended conversations

What your coworkers can do in the UI:

- add flows
- change routing
- manage fallback behavior
- update business-owned chatbot responses

GPU needed:

- no

Best fit when:

- the chatbot is mainly guided
- the team wants high control
- the company wants internal users to manage flows later

## 2. Hybrid Botpress + LLM Chatbot

This is usually the most practical long-term design if you want both flows and AI.

How it works:

- Botpress still owns the conversation flow and orchestration
- internal users still build and manage flows in Botpress
- certain steps, fallbacks, or actions call a local LLM when needed

Example:

- FAQs and guided steps stay in flows
- open-ended explanation or summarization goes to a local `vLLM` model
- Botpress decides when to call the model

What powers it:

- everything from the NLU chatbot
- plus a local model service such as `vLLM`

What it feels like:

- still structured where you want control
- smarter where you want more natural answers
- best balance between internal business control and AI capability

What your coworkers can do in the UI:

- still add flows
- still manage business logic
- still decide where the model is or is not used

GPU needed:

- only for the LLM part

Best fit when:

- the company still wants flows
- but also wants better answers for open-ended prompts
- and you want to preserve internal editor control

## 3. LLM-First Chatbot

This is the “model answers almost everything” version.

How it works:

- a user sends a message
- the message goes mainly to a model
- the model generates the answer directly
- flows are minimal or secondary

What powers it:

- local `vLLM` or another model-serving stack
- a real instruct/chat model

What it feels like:

- more natural and flexible
- more open-ended
- less predictable
- harder for non-technical users to control precisely

What your coworkers can do in the UI:

- much less, unless you build a custom layer around it
- flows become less central
- Botpress becomes less valuable if almost everything is delegated to the model

GPU needed:

- yes, usually

Best fit when:

- the main value is open-ended AI conversation
- not business-managed flow editing

## What We Have Right Now

Right now, the repo is in the first category:

- `NLU chatbot`

It is not yet:

- `Hybrid Botpress + LLM`
- `LLM-first`

## Best Default Recommendation

Based on your requirements so far, the most likely good path is:

1. start with the `NLU chatbot`
2. confirm flows and internal editor ownership work well
3. only then decide whether to add a local LLM

If a local LLM is added later, the best target is probably:

- `Hybrid Botpress + LLM`

not:

- `LLM-first`

because your company still wants flows and internal users managing those flows later.
