# Context persistence

The largest token cost in long-running work is not file reads — it is the conversation
being re-read on every turn. Measured on a real setup: a 224 MB session had auto-compacted
19 times, meaning it was already discarding detail while still charging full price for
what remained. Its whole useful state fits in ~640 tokens.

**Conversation context costs `size × turns`. File context costs `size`, once.**

| | Transcript | STATE.md |
|---|---|---|
| Touch of Gold (measured) | 224 MB / ~63.5M tok | ~641 tok |
| Web Wizard (measured) | 42 MB / ~12M tok | ~585 tok |

## Where STATE.md lives

`~/.claude/projects/<encoded-project-path>/STATE.md` by default — it is *your* working
memory, not the repo's. Put it in `<project>/.claude/STATE.md` only if the user wants it
shared with the team, and never commit it unless they ask.

## Resume — step 0 of the loop

1. Read `STATE.md`. That is the context; don't rebuild it by re-reading the codebase.
2. Say in one line what you're picking up: *"Resuming <project>: <current task>."*
3. Read only the code the current task actually touches.

No STATE.md? Say so and offer to create one.

## Checkpoint — step 8 of the loop

**Rewrite** it, never append — a growing file re-creates the problem it solves. Keep it
under ~400 lines. Do it at the end of each discrete task, unprompted.

Record only what cannot be re-derived from the code:

- **Decisions and their reasons.** "Chose X over Y because Z." The *why* is what
  compaction destroys first and grep can never recover.
- **Current task** and the exact next step.
- **Gotchas** — what broke, what's fragile, what not to touch, as `path:line`.
- **Standing constraints** the user has repeated ("must not lag", "never touch X").
- **Open questions** awaiting the user.

Do NOT record: file contents, code that's on disk, directory listings, anything `grep`
answers in seconds, or a narrative of what happened. Re-derivable is not worth carrying.

**Don't duplicate existing project docs.** If the repo already has `CLAUDE.md`,
`DECISION_LOG.md`, ADRs, or a README that covers architecture, point at them by path and
record only what they don't: what is in flight right now.

## Template

```markdown
# <project> — STATE
Updated: <date>

## What this is
<2-3 lines: purpose, stack, entry point. Point at CLAUDE.md/ADRs rather than repeating them.>

## Current task
<what's in flight, and the exact next step>

## Gotchas
- <fragile thing> at `path:line`

## Standing constraints
- <things the user has said more than once>

## Done recently
- <one line per completed chunk>

## Open questions
- <awaiting user>
```

## Why this is not "losing context"

Auto-compaction is lossy, automatic, and invisible — you cannot see what it dropped.
STATE.md is lossless, deliberate, and inspectable: the user can read exactly what carries
forward and correct it. It is strictly more faithful than a long session, at a fraction
of the tokens.

A session kept under ~50k tokens never auto-compacts at all, so nothing is ever lost to
summarization in the first place.

## Long autonomous runs

For agents running many hours, context is guaranteed to reset — no window is large enough.
Checkpoint after every bounded chunk, not at the end, and keep a task queue alongside
STATE.md so a crash costs one chunk instead of the whole run.
