# Playbooks — the loop reshaped per task type

The core loop (locate → read → edit → verify) is bug-fix shaped. Other work reshapes steps 3–6. Pick one; don't run a generic process over a specific task.

---

## Bug fix
1. Reproduce first. A bug you can't trigger is a bug you can't confirm fixed.
2. Grep the symbol in the error/stack trace. Read that range + its dependents.
3. Find the **cause**, not the symptom. Ask "why did this value get here?" until the answer is a line of code.
4. Write or identify the test that fails for the right reason *before* fixing.
5. Fix minimally. Re-run: the target test goes green, every other test stays green.
6. Report: root cause in one sentence, fix location, what else was in the blast radius.

**Trap:** the red test going green proves nothing if a green test was silently weakened. Confirm coverage still holds.

---

## New feature / greenfield
1. Find the nearest existing analogue in the codebase and read it fully. Match its structure — consistency beats your preferences.
2. Locate the integration points: routes, exports, DI registration, config, migrations, types.
3. Write the smallest end-to-end slice first (one path working) before breadth.
4. Verify by *executing the feature*, not just compiling it.
5. Report: entry point, how to invoke it, what's stubbed vs complete.

**Trap:** building breadth before one path works. You end up with six half-features and no verification.

---

## Refactor
1. **Establish the safety net first.** Existing tests green *before* you touch anything — record the baseline. No tests? Write a characterization test that pins current behavior, even if that behavior is odd.
2. Grep every call site. A refactor's blast radius is its entire point of risk.
3. Change in mechanical steps, each independently green. Never rename + restructure + retype in one diff.
4. Verify: same tests, same results. Behavior identical or the change is not a refactor.
5. Report: what moved where, and explicitly — "no behavior change" or the exact intended change.

**Trap:** a refactor that "also fixes" something. Split it: refactor green, then fix separately.

---

## Code review
1. Read the diff, then read enough surrounding code to judge it. A diff alone hides what it breaks.
2. Check in priority order: **correctness → security → blast radius → tests → performance → style.** Stop reporting when value drops below noise.
3. Every finding needs a concrete failure scenario: inputs → wrong output. "This looks fragile" is not a finding.
4. Verify claims before reporting them — a wrong review finding costs more than a missed one.
5. Report ranked by severity. No style nits above a real bug.

---

## Investigation / "why does X happen"
1. State the hypothesis before searching, so evidence can falsify it.
2. Cheapest discriminating evidence first — logs and greps before deep reads.
3. Follow data flow backward from the symptom, not forward from the entry point.
4. Answer first, evidence second, ≤5 lines unless asked to expand.

**Trap:** reading forward from `main`. Always walk backward from the observed wrong value.

---

## Migration / sweep (upgrade, rename, API change)
1. `rg -l` first to size the blast radius. Count sites before touching one.
2. Categorize sites into mechanical vs judgment-required. Handle mechanical ones with one scripted pass.
3. Verify per batch, not at the end. A 200-site change verified once is unverifiable.
4. Report the count: sites found, sites changed, sites deliberately skipped and why. Never let a silent cap read as full coverage.

---

## Debugging when stuck (two failed attempts)
Stop editing. The next edit is a guess and guesses compound.
1. State what you *know* is true vs what you *assumed*. Test the assumptions — that is where the bug is.
2. Bisect: remove half the system. Does it still fail?
3. Add one instrumentation point that discriminates between the top two hypotheses.
4. Escalate the token budget deliberately and say so. This is the case where reading more is cheaper than guessing more.
