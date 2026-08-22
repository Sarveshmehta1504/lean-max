# What counts as verified

Per-stack commands live in `stacks.md`. This file is the standard.

## Tiers — use the highest available, and name which one you used

1. **Executed** — ran the code/test/build and read the output. The only tier that lets you say "works."
2. **Typechecked** — compiler/type checker/linter passed on the changed files. Say "compiles, not executed."
3. **Traced** — walked every branch of the changed path by hand, including error paths and each caller grep found. Acceptable only when execution is genuinely impossible. Say so explicitly.
4. **Unverified** — you edited and stopped. Must be stated in those words.

Reporting tier 2 or 3 as if it were tier 1 is the single most damaging failure available here. It converts an honest partial result into a false one.

## Rules

- **The test must actually exercise your change.** A green suite that never touches the new path is not evidence. Confirm the test hits the line — break it deliberately if unsure and watch it go red.
- **Baseline before, compare after.** Record what was failing *before* your edit. Otherwise you cannot tell a fix from a coincidence.
- **Every previously-green test must stay green.** A suite that goes green by weakening a guard is a regression wearing a success costume.
- **Quote failures trimmed** — the failing assertion plus 2 lines. Never a full traceback dump; never a silent summary.
- **Failed verification means fix and re-verify** — never report the fix as done with a footnote that tests fail.
- **Edge probe on anything with branches:** empty, zero, negative, max, null/None, and the boundary on each condition you touched. Six cases costs ~200 tokens and catches what the happy-path test won't.
- **Irreversible actions verify twice** — migrations, deletes, deploys, money, auth. Dry-run, read the plan, then act.

## When you cannot verify

Say it in this shape, not vaguely:

> Unverified: no test runner in this environment. Traced all 3 callers by hand (`a.py:40`, `b.py:112`, `c.py:9`); logic holds. Needs `pytest tests/test_x.py` before merge.

That is a usable result. "Should be fine" is not.
