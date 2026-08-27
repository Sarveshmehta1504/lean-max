# Context persistence

The largest token cost in a long-running project is not file reads — it is the
conversation itself being re-read on every turn. Measured on a real setup:
a 224 MB session had auto-compacted **204 times**, meaning it was already
discarding detail while still charging maximum price for what remained.

**Conversation context costs `size × turns`. File context costs `size`, once.**


A long session does not preserve context — it auto-compacts and discards detail, while re-reading everything it still holds on every turn. A file preserves context exactly, and is read only when needed.

**Conversation context costs `size × turns`. File context costs `size`, once.**

## STATE.md location

`<project>/.claude/STATE.md`, or `~/.claude/projects/<encoded-path>/STATE.md` when the project shouldn't carry the file. Never commit it unless the user asks.

## Resume (start of session)

1. Read `STATE.md`. That is your context — do not re-derive it by reading the codebase.
2. Confirm in one line what you're picking up: *"Resuming <project>: <current task>."*
3. Only read code the current task actually touches.

If no STATE.md exists, say so and offer to create one.

## Save (before /clear, /compact, or ending)

Rewrite `STATE.md` — don't append; a growing file re-creates the problem. Keep it under ~400 lines.

Record only what cannot be re-derived from the code:

- **Decisions and their reasons.** "Chose X over Y because Z." The why is what's lost in compaction.
- **Current task** and the exact next step.
- **Gotchas** — what broke, what's fragile, what not to touch.
- **Key paths** as `path:line` anchors.
- **Open questions** awaiting the user.

Do NOT record: file contents, code that's on disk, directory listings, anything `grep` answers in seconds, or narrative of what happened. Those are re-derivable; the reasoning is not.

## Template

```markdown
# <project> — STATE
Updated: <date>

## What this is
<2-3 lines: purpose, stack, entry point>

## Architecture decisions
- <decision> — because <reason>

## Current task
<what's in flight, and the exact next step>

## Gotchas
- <fragile thing> at `path:line`

## Done recently
- <one line per completed chunk>

## Open questions
- <awaiting user>
```

## Rhythm

Work → `/state save` → `/clear` → next task resumes from STATE.md.

Save at the end of each discrete task, not each message. A session that stays under ~50k tokens never auto-compacts, so nothing is ever lost to summarization.

## Why this is not "losing context"

Auto-compaction is lossy, automatic, and invisible. STATE.md is lossless, deliberate, and inspectable — you can read exactly what carries forward and correct it. It is strictly more reliable than a long session, at a fraction of the tokens.
