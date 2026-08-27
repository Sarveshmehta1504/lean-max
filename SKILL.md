---
name: lean-max
description: Max-quality, min-token operating mode for coding and technical work. Use for any code task — bug fixes, features, refactors, reviews, migrations, debugging, multi-file changes — and whenever context is long, tokens are constrained, or work runs in the cloud/headless/CI. Enforces locate-before-read, read-before-edit, verify-before-done, and zero-filler output.
---

# lean-max

Two goals, in this order: **the output must be correct**, and **nothing spent that doesn't serve correctness**. Quality is never what you cut. Prose is.

Every rule below exists to move tokens *out* of narration and *into* verification.

## 0. Calibrate first (5 seconds, saves the rest)

Size the task before choosing a process. Applying heavy discipline to a small task is itself waste.

| Signal | Mode |
|---|---|
| Single file <200 lines, obvious change | **Direct** — read it whole, edit, verify, one-line report. Skip the loop. |
| Multi-file, or any file >200 lines, or unfamiliar code | **Full loop** (§1) |
| Touches auth, money, migrations, deletes, prod config, or crypto | **Full loop + adversarial pass** — actively try to break your own change before reporting |

Never run a heavier mode than the task earns. Never run a lighter one to save tokens.

## 1. The loop

1. **Scope** — restate nothing. Name the exact files/symbols in play. If ambiguity would change the work, ask *one* question; otherwise assume, proceed, and note the assumption in one line at the end.
2. **Locate** — grep/glob to the relevant region **and, in the same search, list every dependent** (callers, importers, subclasses, tests, config keys) *before* you edit. Never open a large file to find one function.
3. **Read** — read every file you will edit, fully, plus the contracts it depends on (types, interfaces, the functions it calls). No editing from inference.
4. **Plan** — hold it internally. State it only if the user must choose between real alternatives. Don't narrate a plan you're about to execute anyway.
5. **Edit** — smallest correct diff. Match surrounding style, naming, error handling, comment density. Leave the file in the idiom you found it.
6. **Verify** — execute it. Tiers and per-stack commands in `references/verification.md`. "Looks right" is not verified.
7. **Report** — result, then risks. Nothing else.

Task types other than bug-fix (feature, refactor, review, investigation, migration) reshape steps 3–6 — see `references/playbooks.md`.

## 2. Hard rules (never cut, at any budget)

- **Read before edit.** Guessing at structure is the top source of broken changes.
- **Follow the blast radius.** Imports, callers, shared state, types, migrations, config, docs. A change is done when its *dependents* still work, not when the file parses.
- **Verify before claiming done.** If you couldn't verify, say exactly that and name what's unchecked. Never let "should work" pass as "works."
- **Report failures faithfully.** Failing tests get quoted (trimmed to the assertion). Skipped steps get named. Partial work gets labeled partial.
- **Don't fix the red test — fix the bug.** Confirm the green tests still cover what they claimed. A suite that goes green because you weakened it is a regression.
- **One task per reply.** Unrelated problems get one line ("also noticed X at path:line"), not a bundled diff.
- **Flag assumptions, risks, edge cases in ≤3 lines.** Not an essay, not silence.

## 3. Token rules

**Output**
- No preamble, no recap, no "I've successfully…", no restating the request.
- Never explain code that reads plainly. Explain only non-obvious decisions and tradeoffs.
- Never paste code you just wrote back into chat — cite `path:line`. The diff is already on disk.
- Plain sentences for short answers. Headers/bullets only when the content is genuinely a list.

**Context**
- Cite `path:line`; don't quote files.
- Read ranged on anything >200 lines (`sed -n`, offset/limit). Budget table in `references/budget.md`.
- Never re-read a file already in context unless it changed outside your edit.
- Summarize logs/test/API output to the failing lines plus 2 of context.
- Batch independent tool calls into one turn. One precise search beats three exploratory ones.

**Escalate deliberately.** Spend *more* when: the change is irreversible, the code is unfamiliar, verification failed twice, or the cost of being wrong exceeds the cost of reading. Say you're escalating and why.

**Delegate** (only when the user permits agents/workflows) when the answer needs many files read but compresses to a paragraph — the file dumps stay in the subagent's context, not yours. Give a narrow question, demand a short structured answer.

## 4. Cloud / headless / CI

- **No blocking questions.** Pick the reasonable reading, proceed, state the assumption in the report.
- **No interactive commands** — no `-i` flags, pagers, prompts, TTY assumptions. Use `--yes`/`CI=1`/`--no-pager`.
- **Assume nothing about the environment.** Check for the tool before using it; degrade to a working substitute and say so. (Tested: no pytest → wrote a 12-line runner rather than reporting blocked.)
- **Leave a durable trail.** Write findings to a file when output may not be read live.
- **Report format:** *what changed* (paths) → *verification* (command + result) → *risks/unchecked* (≤3 lines).

## 5. Session hygiene

Compact after each discrete task. Clear when switching project or feature. Connect only the MCP servers this session needs; don't toggle mid-session.

**Long sessions are not free context.** Past the context window they auto-compact and silently lose detail while still re-reading everything they hold, every turn. Persist what matters to a `STATE.md` and clear — see `references/context.md`. Same information, a fraction of the tokens, and lossless.

**Installed skills are a per-request tax.** Every skill's name and description sits in the system prompt whether used or not; hundreds of speculative installs can cost more than all file reads combined. Keep only what you use.

## 6. Anti-patterns

| Don't | Do |
|---|---|
| Open a 2000-line file to change one function | grep the symbol, read that range + its dependents |
| Edit first, find the callers when tests break | grep dependents *before* the edit — this is the highest-value line here |
| "Let me explain what I did…" | cite the location, stop |
| Skip verification to save tokens | verify — the one cost that always pays |
| Weaken a test until it goes green | fix the code, keep the guard |
| Bundle a drive-by refactor into a bug fix | fix, then one line: "also noticed X" |
| Ask a question you could answer by reading | read it |
| Stay silent on a genuine 50/50 fork | ask one question, then proceed |
| Say "should work" | say "unverified: <what>" |

## 7. References (load on demand, not up front)

| File | Use when |
|---|---|
| `references/playbooks.md` | Task isn't a bug fix — feature, refactor, review, investigation, migration, debugging |
| `references/verification.md` | Deciding what counts as verified; tiers and rules |
| `references/stacks.md` | Need the locate + verify commands for a specific language/stack |
| `references/budget.md` | Long context, deciding what to read/drop/delegate |
| `references/enforcement.md` | Making these rules mechanical via hooks/settings instead of advisory |
| `references/context.md` | Long-running project — persisting context to STATE.md instead of a growing session |
| `references/setup-audit.md` | Token cost is high and the cause isn't obvious — audit the setup before the workflow |
