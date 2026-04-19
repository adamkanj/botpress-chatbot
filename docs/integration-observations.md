# Integration Observations

This file is here so you can turn local testing into better instincts for the real project later.

## What To Observe During Learning

While testing local Botpress v12, note:

- how webchat is exposed locally
- whether it looks like a hosted widget, script include, or something else
- what configuration would likely need to be shared with another team
- whether the chatbot seems easy or awkward to embed into an existing website

## Likely Real-World Boundary

Based on your current understanding, the website team would probably:

- keep ownership of their frontend repo
- add the chatbot integration on their side
- control when website changes are released

Your team would probably:

- host the chatbot runtime
- configure bot behavior and content
- own chatbot-side updates
- document how the website team should connect to it

## Questions To Answer Later

- What exact webchat embed method does Botpress v12 support?
- Does embedding require a public base URL?
- What domain or CORS settings are needed?
- Can user/session context be passed safely into the chatbot?
- How much UI customization would the website team want?

## What Counts As Success Here

Success in this sandbox is not solving integration. It is understanding enough of Botpress to ask better questions when the real work begins.

