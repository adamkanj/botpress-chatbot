# Integration Observations

This file is here so you can turn local testing into a cleaner service boundary for work later.

## Working Assumption

The most likely work shape is:

- the website/application team owns their own repo and page release process
- your team owns the chatbot runtime and behavior
- their pages connect to your chatbot service instead of sharing code with your repo

## What To Observe Locally

While testing Botpress locally, keep notes on:

- how the webchat or public chat path is exposed
- what URL or config another team would need from you
- whether the public chat side can stay separate from the internal admin side
- whether the integration feels widget-based, endpoint-based, or both

## Work Questions To Answer Later

- What exact integration method should the website team use?
- Does Botpress require a public base URL for that method?
- What proxy, domain, and CORS rules are needed?
- Can the client-facing application pass user or session context safely?
- How much visual customization would the website/application team need?
- Should your team expose raw Botpress webchat, or place a thinner integration layer in front of it?

## What Counts As Success Here

Success in this repo is not fully solving integration.

Success is being able to say:

- what your team would host
- what the website team would consume
- what internal URLs stay private
- what public/chat-facing path would be exposed
