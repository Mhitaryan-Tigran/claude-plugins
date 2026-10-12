# brief

A layer between you and Claude Code. It reads every prompt before Claude does.

- **Every prompt, no delay.** Claude gets a short instruction: if the prompt is vague, settle what it can from the conversation, memory, code and git first, then ask only the real decisions through the question form with concrete options, and know what "done" means before starting.
- **`??` before a prompt, about ten seconds.** A second model (Sonnet by default) reads the recent conversation and writes a full brief: the intent, the prompt rewritten as a complete task, a done bar, memory notes to read, open questions with ready options, and flags for plan-first and outward actions. You see the brief above the answer; Claude treats its questions as candidates and asks only what it cannot settle itself.
- **`,` before a prompt** skips the plugin for that message. Short replies such as "yes", "go on" or an answer to Claude's own question are skipped too.

Prompts like "update the app" or "make a site" turn into a task with scope and a finish line instead of a guess.

## Install

```
/plugin marketplace add Mhitaryan-Tigran/claude-plugins
/plugin install brief@tigran-macintosh
```

Restart Claude Code, then run `/brief-setup` to pick the model, the language and your profile.

It calls `claude -p` for the `??` brief, so it works with whatever Claude Code is signed in with, a subscription or an API key. Python 3 is the only requirement.

## Settings

`~/.claude/brief.json`, overridden per project by `.claude/brief.json`. Every key is optional.

| Key | Default | Meaning |
|---|---|---|
| `model` | `sonnet` | Model that writes the `??` brief |
| `language` | `English` | Language of the parts shown to you |
| `light` | `true` | The short clarify-first instruction on every prompt |
| `show_brief` | `true` | Show the full `??` brief above the answer |
| `deep_prefix` | `??` | Prefix for a full brief |
| `bypass_prefix` | `,` | Prefix that skips the plugin |
| `replies` | yes, ok, go… | Short replies that never trigger it |
| `timeout` | `25` | Seconds the brief may take before the prompt goes through untouched |
| `profile` | empty | A sentence about you, or a path to a markdown file |
| `memory_index` | empty | Markdown index of your notes, links as `[Title](name.md)`, so the brief can point Claude at the right ones |
| `context_command` | empty | Shell command whose output joins every brief, such as a calendar or `git status` |
| `log` | `~/.claude/brief/log.jsonl` | Every prompt with its brief or skip reason; empty string turns it off |

## How it fails

Any error or timeout lets the prompt through unchanged and writes one line to the log. The second model runs with no tools, no settings and no MCP servers, so it can read but never act, and it cannot trigger the hook again.

## Why

Coding agents solve far fewer tasks when the instruction is ambiguous than when it is clarified, and the clarifying questions that help are the ones asked after looking at the code, not before. Claude Code hooks cannot rewrite a prompt or open a form, so the plugin adds context and leaves the asking to Claude.

## License

MIT
