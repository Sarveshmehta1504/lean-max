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
