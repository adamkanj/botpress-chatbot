# Botpress Mental Model

This note is meant to help future-you understand the basics of how Botpress works before you touch the real project at work.

It is intentionally practical, not academic.

## The Simple Picture

Think of Botpress as a chatbot application server with an admin UI on top.

At a high level:

1. users talk to a chat interface
2. the chat interface sends messages to Botpress
3. Botpress decides what the bot should do next
4. Botpress returns a response to the chat interface

So the core job of Botpress is:

- receive a message
- figure out the intent or route
- follow a flow or rule
- send back the next response

## The Main Pieces

### 1. Runtime

This is the running Botpress server.

It handles:

- incoming messages
- bot execution
- state/session handling
- admin/studio access
- channels like web chat

In this learning repo, Docker is just the easiest way to run that runtime locally.

### 2. Studio / Admin UI

This is where you configure the bot.

This is the part you use to:

- create a bot
- edit flows
- add responses
- manage FAQ-style content
- preview behavior

You can think of this as the control panel for the runtime.

### 3. Bot

A bot is the actual chatbot project inside Botpress.

A bot usually contains:

- flows
- content
- intents or training examples
- configuration
- fallback behavior

For learning, it helps to think of one bot as one self-contained conversation app.

### 4. Flows

Flows are the conversation paths.

A flow is basically:

- when the user says or does X
- go to this step
- send this response
- maybe ask another question
- then route to the next step

Flows are the “logic map” of the chatbot.

### 5. Content / FAQ

This is the actual information the bot says.

Examples:

- hours
- contact info
- return policy

The most important beginner idea is:

- flows define what path the bot follows
- content defines what the bot says

### 6. Fallback

Fallback is what happens when the bot does not know what to do.

This matters a lot in real projects, because many chatbot failures are not crashes. They are confusing answers, wrong routing, or weak fallback behavior.

### 7. Webchat / Embed

This is how the chatbot appears on a website.

For your work mental model, do not think:

- “we build inside their website repo”

Think:

- “we provide a chatbot service or integration point”
- “their team embeds or connects to it”

That boundary is important.

## How Messages Usually Flow

Here is the simplest way to picture it:

1. A user types a message in a web chat widget.
2. The widget sends the message to the Botpress server.
3. Botpress checks the current conversation state.
4. Botpress tries to determine what the message means.
5. Botpress routes the conversation into the right flow or reply path.
6. Botpress sends back the next message.
7. The chat widget displays that response to the user.

That is the basic loop.

## What You Are Really Learning In This Sandbox

You are not trying to master all of Botpress.

You are trying to understand:

- what the runtime is
- what the UI is
- what a bot contains
- how flows differ from plain answers
- how fallback works
- how a website would probably talk to the chatbot later

If you can explain those five things clearly, the sandbox is already doing its job.

## How To Think About The Work Version

At work, the real system will probably look more like this:

- your team owns the chatbot runtime and bot logic
- another team owns the website
- the website team integrates the chatbot into their frontend
- users interact through the website, but the chatbot behavior comes from your side
- internal editors use the private Botpress admin side on your side

So mentally separate:

- chatbot service ownership
- website ownership

That helps avoid confusion later.

## What To Expect When You Start At Work

The real work will probably involve questions like:

- Where will the chatbot be hosted?
- How does the website talk to it?
- What content will feed it?
- Who updates the bot?
- Who owns failures and monitoring?
- How much customization does the website team need?

Those questions are normal. You do not need to solve them all right now.

## Practical Beginner Approach

When you are learning Botpress, work in this order:

1. Run it locally.
2. Create one tiny bot.
3. Add a welcome message.
4. Add a few FAQ answers.
5. Add one short guided flow.
6. Test one unknown question.
7. Observe what changed and where you changed it.

That order teaches the most important ideas fast.

## What To Watch Out For

Because this is legacy Botpress v12, remember:

- some parts may feel dated
- setup may be awkward
- default Botpress relies on external Botpress language infrastructure unless you replace it
- local testing is useful even if the real deployment later changes

So do not judge the whole idea only by polish. Focus on understanding the architecture and workflow.

## One-Paragraph Summary

Botpress is a chatbot server with an admin UI where you build bots made of flows, content, and fallback logic. Users talk through a chat interface, the interface sends messages to Botpress, Botpress decides what should happen next, and then sends back a response. In a real company setup, your team would likely own the chatbot service and conversation logic while another team embeds that chatbot into the website.
