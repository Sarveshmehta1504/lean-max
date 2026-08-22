# Token triage

## Reading budget by file size

| File size | Approach |
|---|---|
| <200 lines | Read whole. Grep discipline here costs more than it saves. |
| 200–600 | Grep the symbol; read ±60 lines around each hit, plus imports and type definitions at the top. |
| 600–2000 | Grep first, always. Read only matched ranges. Whole-file only if restructuring it. |
| >2000 | Grep, then read ranges one at a time as needed. Consider delegating to a subagent. |

Measured on a 967-line file: grep + 60 ranged lines cost ~994 tokens vs ~15,335 to read naively — 94% less, same fix, same verification.

## Search discipline
- One targeted regex beats three vague ones. Search the *symbol*, not a keyword.
- `rg -l` first — size the blast radius before reading a single line.
- `rg -n -B3 -A8` gives enough context to judge without opening the file.
- Exclude noise early: `--type-not test`, `-g '!dist'`, `-g '!*.lock'`, `-g '!node_modules'`.

## When context is already long — keep, in priority order
1. The file(s) currently being edited.
2. Type/interface definitions and calling contracts.
3. The failing test or error output.
4. The user's stated constraints and decisions.

Droppable: earlier exploration, superseded drafts, full logs, files you read but didn't touch. Compact rather than continuing to accrete — a compacted session outperforms a bloated one on the same task.

## Delegation math
Delegate when `(files to read × avg size)` exceeds what the answer is worth **and** the answer compresses to a paragraph.

Qualifies: "where is X used across the repo", migrations, audits, multi-package sweeps, unfamiliar-codebase orientation.
Does not: a single known file, anything you'll need the full contents of anyway.

## Output budget
| Reply type | Target |
|---|---|
| Bug fix | 1–3 lines + `path:line` |
| Feature | paths, one usage example if non-obvious, risks |
| Investigation | answer first, evidence second, ≤5 lines |
| Review | findings ranked by severity, each with a concrete failure scenario |
| Refactor | what moved where + "no behavior change" |

Never restate in prose what the diff already says.

## Where the savings actually come from — ranked
1. Ranged reads on large files (dominant lever).
2. Not re-reading a file after editing it — the test run confirms it, for ~50 tokens.
3. Trimmed test/log output.
4. `path:line` citations instead of pasted code.
5. No recaps or preamble.

Note the shape: savings scale with file size and approach zero on small files. That is correct — the rules only spend effort where the payoff is real, and never cost more than the naive path.
