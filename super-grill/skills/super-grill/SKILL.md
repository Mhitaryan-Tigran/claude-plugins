---
name: super-grill
description: Interview the user about a task before building it, one question at a time, until the plan is shared. Use when the user runs /super-grill or /grill, says "grill me", "interview me", "ask me questions first" or "let's pin this down before you start", or hands over a large or vague task they want questioned before any code is written.
---

# Super-grill

The user wants to be questioned about the task before anything is built. Turn a loose idea into a plan both of you agree on, then stop and ask whether to start.

## Before the first question

Read what is already knowable: the conversation, the code and the files it touches, git history, project docs, any memory or notes the session has. Whatever these settle is not asked. Keep a short private list of the decisions that are still open, ordered so that each answer narrows the next question: goal and audience first, then scope, then behaviour and edge cases, then how it will be checked.

## The interview

- Ask one question at a time with the AskUserQuestion tool. Never batch several open decisions into one call.
- Give two to four concrete options, the one you would choose first with "(Recommended)" after it, each with one line on what it means in practice. The user can always type their own answer.
- Ask only what changes what gets built. Skip anything with an obvious default and say which default you took when you sum up.
- After each answer, check whether it settles other open points or opens new ones, and update the list. Look things up between questions when an answer points somewhere new in the code.
- If an answer contradicts an earlier one or the code, say so plainly and ask which one stands.
- Stop when the remaining open points are ones the user would happily leave to you. Most tasks need three to eight questions; past twelve, sum up what is known and ask whether to keep going.
- Write no code and change no files during the interview.

## The summary

When the interview ends, give a short spec in the user's language:

- Goal: one or two lines.
- Decisions: each answer as a settled fact, plus the defaults you took.
- Out of scope: what will not be done.
- Done when: the concrete check that proves it works.

Then ask once whether to start, or to change something first. Start only on a clear yes.
