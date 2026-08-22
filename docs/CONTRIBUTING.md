# Contributing

## The bar

**A change to the rules should come with evidence it changed an outcome.**

That standard is why the highest-value rule in the skill exists. "Grep dependents before editing" wasn't written from intuition — a benchmark scenario shipped a signature change without it, produced `TypeError` and 4 failing tests, and the rule was added to the loop as a result.

Opinions about what *ought* to help are cheap. A before/after on real executed code is not.

## What's most useful

1. **Benchmark runs on other stacks.** The 94% figure is measured on Python. TypeScript, Go, and Rust numbers would materially strengthen the claim — or correct it.
2. **Counter-evidence.** A case where following the skill produced a *worse* result is more valuable than another case where it worked. Open an issue.
3. **Playbooks for task types not covered** — see `references/playbooks.md` for the shape.
4. **Stack rows** in `references/stacks.md` — locate command, fast check, real verify, and the trap specific to that stack.

## What to avoid

- Growing `SKILL.md`. It's the resident cost, paid on every load. New detail belongs in `references/`, behind a one-line pointer. A PR that adds 40 lines to `SKILL.md` needs to justify the tokens.
- Style rules with no measurable effect on correctness or cost.
- Advice that can't be checked.

## Running the benchmark

```bash
cd examples/benchmark
python3 run_tests.py     # expect: 6 passed, 1 failed
```

The failing test is intentional — the planted bug is in `cart/pricing.py` in `price_cart()`. To measure: give the failure to Claude with and without the skill, and compare bytes read and whether the fix survives the edge cases in `docs/BENCHMARK.md`.

## PRs

Keep them scoped to one change. Include the evidence in the description.
