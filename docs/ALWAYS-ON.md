# Always-on mode

`/lean-max` loads the skill only when invoked. To apply it to **every** Claude Code session without typing anything, put a compact core into `~/.claude/CLAUDE.md`.

## The tradeoff

| | Skill (`/lean-max`) | Always-on (`CLAUDE.md`) |
|---|---|---|
| Resident cost | 0 until invoked, then ~1,850 tok | paid every session, coding or not |
| Coverage | only when you remember to invoke | automatic, never forgotten |
| Full detail | all 5 references available | core rules only; references still load on demand |

Use the **compact core** below rather than pasting all of `SKILL.md`. It's ~450 tokens instead of ~1,850, keeps every rule that changes outcomes, and points at the skill for the rest.

## The compact core

Append to `~/.claude/CLAUDE.md`:

```markdown
# Operating rules (lean-max)

## Quality — never cut
- Read every file you'll edit, fully, before editing. No guessing at structure.
- Grep dependents (callers, importers, tests, config) BEFORE editing, not after tests break.
- Verify by executing. Name the tier: executed / typechecked / traced / unverified.
  "Should work" is not an allowed answer.
- Fix the bug, not the red test. A suite that greens by weakening a guard is a regression.
- Flag assumptions, risks, edge cases in <=3 lines.

## Tokens — cut these
- No recaps, preamble, or restating the request. No "I've successfully...".
- Never paste back code that's already on disk — cite path:line.
- Files >200 lines: grep the symbol, read ranged. <200 lines: read whole.
- Never re-read a file already in context. Summarize logs to the failing lines + 2.
- Batch independent tool calls. One precise search beats three vague ones.

## Calibrate
Small + obvious -> just do it. Multi-file or unfamiliar -> full loop.
Auth/money/migrations/deletes -> full loop + try to break your own change first.
Escalate deliberately (and say so) when a change is irreversible or verification failed twice.

## Headless/CI
No blocking questions, no interactive flags, assume no tooling is installed (check first).
Report: what changed (paths) -> verification (command + result) -> risks/unchecked.

Full detail: /lean-max
```

## Install it

```bash
curl -fsSL https://raw.githubusercontent.com/Sarveshmehta1504/lean-max/main/docs/always-on-core.md >> ~/.claude/CLAUDE.md
```

Or copy the block above manually.

## Removing it

Delete the `# Operating rules (lean-max)` section from `~/.claude/CLAUDE.md`. The skill keeps working via `/lean-max`.
