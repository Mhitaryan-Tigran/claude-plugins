---
description: "Configure prompt-boost: model, language, prefixes, profile and context sources"
---

# prompt-boost setup

Set up `~/.claude/prompt-boost.json` for the user (or `.claude/prompt-boost.json` in the current project if they ask for a project-only setup).

1. Read the existing config if there is one, and `${CLAUDE_PLUGIN_ROOT}/boost.py` for the defaults in `DEFAULTS`.
2. Ask in one AskUserQuestion call:
   - Model for `??` briefs: sonnet (recommended), opus, haiku.
   - Language for the parts shown to the user: the language they write in, or English.
   - Light mode on every prompt (a short instruction to clarify vague prompts, no delay): on (recommended) or off.
   - Show the full `??` brief above the answer: yes (recommended) or no.
3. Ask in plain text for a short profile: who they are, what they work on, how they write. Save it as `profile` (a sentence or two inline, or a path to a markdown file).
4. Offer optional context sources: `memory_index`, a path to a markdown index of notes whose links look like `[Title](name.md)`; `context_command`, a shell command whose output is added to every brief (for example a calendar or `git status`).
5. Write only the keys that differ from the defaults, as JSON, and show the result.
6. Tell the user: end a prompt with `??` for a full brief, with `,` to skip the plugin for that message; the log is at `~/.claude/prompt-boost/log.jsonl`.
