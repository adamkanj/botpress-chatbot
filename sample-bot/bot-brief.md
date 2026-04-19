# Sample Bot Brief

Create this bot manually in the Botpress UI as your learning exercise.

## Bot Name

`learning-lab-bot`

## Bot Goal

A tiny support-style bot that can:

- greet the user
- answer a few simple FAQs
- guide the user to one next step
- fail gracefully when it does not know the answer

## Minimum Features

### Welcome

Start with a simple greeting such as:

> Hi, I'm your learning bot. I can answer a few simple questions about hours, contact info, and returns.

### FAQ Topics

Use the sample content in `sample-bot/faq-content.md` for:

- business hours
- contact email
- return policy

### Guided Flow

Add one short flow for:

- “How do I contact support?”

Example steps:

1. ask whether the user wants email or phone support
2. reply with the right contact option
3. end with a friendly prompt to ask something else

### Fallback

Use a fallback message like:

> I’m still a small learning bot, so I may not know that yet. Try asking about hours, contact, or returns.

## What To Learn From This Bot

- how to create/edit a bot
- how responses are organized
- how a simple guided flow differs from direct FAQ answers
- how fallback behavior is configured
- how your changes appear in webchat

