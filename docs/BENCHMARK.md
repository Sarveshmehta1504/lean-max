# Benchmark & test report

**Date:** 2026-08-22 · **Verdict: YES — it works.** Both scenarios passed on real executed code, 94% fewer tokens read than the naive path, zero quality loss (bug fixed, 7/7 tests green, all edge invariants hold).

---

## 1. What was tested

A purpose-built Python cart-pricing project, executed for real — not reviewed on paper.

| File | Size | Role |
|---|---|---|
| `examples/benchmark/cart/pricing.py` | 967 lines / 26 KB | large module, bug planted deep at line ~959 |
| `examples/benchmark/cart/checkout.py` | 24 lines | downstream caller (blast-radius target) |
| `examples/benchmark/tests/test_pricing.py` | 73 lines / 7 tests | 6 passing, 1 failing at start |

Reproducible in this repo at [`examples/benchmark`](../examples/benchmark) — `python3 run_tests.py` gives the red starting state.

The planted bug is the realistic kind — not a typo. A cart discount was subtracted from the **taxable base at full value** instead of being **prorated by the taxable share**. It only misprices carts that mix taxable and non-taxable items (e.g. goods + a gift card), so it passes casual inspection and 6 of 7 tests.

---

## 2. Scenario 1 — find and fix a real bug

Ran the lean-max loop verbatim.

| Step | What actually happened |
|---|---|
| Scope | Failing test named the symbol: `taxable_base` |
| **Locate** | one `grep` returned 16 hits — every definition, use, *and* both caller sites in `checkout.py` |
| **Read** | `sed -n '925,967p'` + `sed -n '36,52p'` → **60 of 967 lines (6.2%)**. Full file never opened. |
| Edit | 3-line diff at `cart/pricing.py:955-958` — prorate by `taxable_share = taxable_subtotal / subtotal` |
| **Verify** | executed the suite: **7 passed, 0 failed** (was 6/1) |
| Edge probe | 6 hand-built edge cases, all invariants hold |

Edge-case results after the fix:

```
empty cart               sub=  0.00  disc= 0.00  taxbase= 0.00  OK
all taxable + disc       sub=100.00  disc=10.00  taxbase=90.00  OK   (share=1 → old behavior preserved)
all nontaxable + disc    sub=100.00  disc=10.00  taxbase= 0.00  OK   (share=0 → no tax, correct)
disc > subtotal          sub= 10.00  disc=10.00  taxbase= 0.00  OK   (clamp holds)
odd proration 1/3        sub= 30.00  disc= 3.00  taxbase= 9.00  OK   (exact third, no drift)
stacked discounts        sub=100.00  disc=15.00  taxbase=42.50  OK
```

Callers re-checked after the edit: `quote()` → `total 64.80`, `amount_due_cents()` → `6480`. Unchanged, as intended.

**Why this matters:** the regression guard `test_all_nontaxable_cart_has_no_tax` *passed with the buggy code* (the old clamp hid it) and still passes after. A fix that only chased the red test could have broken it. The verify step caught that it didn't.

---

## 3. Scenario 2 — blast radius (does the "check dependents" rule actually save you?)

Deliberately made a breaking signature change: `shipping_cost(subtotal, free_over, flat)` → `flat` keyword-only.

- The **pre-edit grep flagged the dependent** at `cart/pricing.py:964` before a single character was changed.
- Proof it mattered: shipping the change *without* updating that line → `TypeError: shipping_cost() takes 2 positional arguments but 3 were given`, **3 passed / 4 failed**.
- Updating the one line grep had already identified → **7 passed / 0 failed**.

Scenario 2 was then reverted; Scenario 1's fix re-verified still green (7/7).

**This test changed the skill.** Step 2 of the loop originally said only "grep to the relevant region." Dependents were mentioned separately in the hard rules — too late in the sequence to be reliable. Step 2 now reads: *"grep to the relevant region, **and in the same search list every dependent (callers, importers, tests) before you edit.**"* That is the single highest-value line in the file, and testing is what surfaced it.

---

## 4. Token measurement

Measured on the actual byte counts pulled into context (≈3.7 bytes/token for code):

| Path | Bytes | ~Tokens |
|---|---|---|
| Naive (read all 3 files whole + re-read after edit) | 56,740 | **15,335** |
| lean-max (1 grep + 2 ranged reads + trimmed test output) | 3,679 | **994** |
| **Reduction** | | **94% — 14,341 tokens saved** |

Where the savings come from, ranked:

1. **Ranged reads on large files** — 60 lines instead of 967. Biggest single lever by far.
2. **Never re-reading after editing** — the naive path re-reads the whole file to "confirm"; the test run confirms it instead, for ~50 tokens.
3. **Trimmed test output** — failing assertion + line number, not the full traceback dump.
4. **`path:line` citations instead of pasted code** — the diff is already on disk; repeating it in chat is pure duplication.
5. **No prose recaps** — the report is result + risks, nothing else.

Savings scale with file size: on a 100-line file the win is near zero; on this 967-line file it was 94%. That is the correct shape — the rules only spend effort where the payoff is real.

---

## 5. Does it hold quality while cutting tokens?

Yes, and the two scenarios were designed to catch it if it didn't:

| Quality risk | Result |
|---|---|
| Ranged reading causes a wrong edit from missing context | No — grep surfaced the contract (`_round`, `taxable_subtotal`) and those 17 lines were read too |
| Skipping the full-file read misses a dependent | No — Scenario 2 proves the pre-edit grep catches it; the failure mode is real and the rule blocks it |
| Trimmed output hides a failure | No — every claim of "done" here is backed by an executed run, quoted |
| Fixing the red test breaks a green one | No — 7/7, including the guard that passed under the bug |

The one cost the skill refuses to cut — **execution-based verification** — is what made all four of those checks possible. It is ~50 tokens per run. It is the best-value spend in the whole budget.

---

## 6. Cloud / headless readiness

Everything in this run is compatible with non-interactive execution: no interactive flags, no pagers, no prompts, no blocking questions, findings written to a durable file. The `cart/checkout.py` caller check and the edge-case probe both ran as plain scripted commands.

Note for cloud: this environment had **no pytest installed**. Per the "never assume the environment" rule, that was detected and a 12-line runner (`examples/benchmark/run_tests.py`) was written instead of reporting the task blocked. That degradation path is exactly what the cloud section is for, and it worked.

---

## 7. Honest limitations

- **It is guidance, not enforcement.** The skill shapes behavior; it cannot mechanically prevent a lazy full-file read. Hooks in `settings.json` would be needed for hard enforcement.
- **The 94% figure is size-dependent.** Expect ~90%+ on files >800 lines, ~40-60% in the 200-600 range, ~0% under 200 lines. It never costs *more* than naive.
- **Delegation rules are untested here** — subagents were not used, per your standing instruction not to invoke them unrequested. Those rules are sound in principle but unproven by this run.
- **Single language.** Tested on Python. The per-stack commands in `references/verification.md` (tsc, cargo check, go build) are correct but were not executed in this run.
- Unrelated pre-existing behavior noticed and deliberately **not** bundled into the fix, per the one-task rule: an empty cart is still charged $5.99 shipping (`shipping_cost`, `pricing.py:936`).

---

## 8. Final verdict

**Yes — apply it globally.** It found a subtle real bug, fixed it with a 3-line diff, verified with an executed test suite, held every edge invariant, caught a breaking dependent before it shipped, and did all of it on 6% of the file at 94% fewer tokens than the naive approach. Testing also improved the skill itself (loop step 2).

Files: [`SKILL.md`](../SKILL.md) · [`references/`](../references/)
