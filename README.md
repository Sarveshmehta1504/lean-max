# lean-max

**A Claude Code skill that cuts token usage on coding tasks by up to 94% — without cutting quality.**

Most token waste in AI coding isn't the thinking. It's reading a 967-line file to change 3 lines, pasting code back into chat that's already on disk, and narrating what you just did. lean-max removes that, and spends the savings where it actually matters: **verifying the change actually works.**

[![validate](https://github.com/Sarveshmehta1504/lean-max/actions/workflows/validate.yml/badge.svg)](https://github.com/Sarveshmehta1504/lean-max/actions/workflows/validate.yml)
[![token reduction](https://img.shields.io/badge/tokens-94%25%20reduction-brightgreen)](docs/BENCHMARK.md)
[![benchmark](https://img.shields.io/badge/benchmark-reproducible-success)](examples/benchmark)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-D97757)](https://docs.claude.com/en/docs/claude-code/skills)
[![resident cost](https://img.shields.io/badge/resident%20cost-~1.8k%20tokens-informational)](#structure)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![stars](https://img.shields.io/github/stars/Sarveshmehta1504/lean-max?style=flat&color=yellow)](https://github.com/Sarveshmehta1504/lean-max/stargazers)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](docs/CONTRIBUTING.md)

---

## The measured result

Real benchmark, real executed code — reproducible in this repo ([`examples/benchmark`](examples/benchmark)):

A 967-line Python module with a subtle pricing bug (a discount subtracted from the taxable base at full value instead of prorated — only misprices carts mixing taxable and non-taxable items, so it passes 6 of 7 tests and survives casual review).

| Approach | Tokens | Outcome |
|---|---|---|
| Naive — read the files whole | **15,335** | bug fixed |
| lean-max — grep, then read 60 of 967 lines | **994** | bug fixed, **+ 6 edge cases verified** |
| | **↓ 94%** | |

The lean run read **6.2% of the file** and still produced the better result, because the tokens it saved on narration went into an executed test run and an edge-case probe.

**Savings scale with file size:** ~90%+ above 800 lines, ~40–60% at 200–600, ~0% under 200 lines. It never costs more than the naive approach — the skill explicitly tells the model to stop optimizing on small files.

---

## Install

**One repo:**
```bash
git clone https://github.com/Sarveshmehta1504/lean-max.git
cd lean-max && ./install.sh /path/to/your/repo
```

**Everywhere on your machine** (available in every project):
```bash
git clone https://github.com/Sarveshmehta1504/lean-max.git
mkdir -p ~/.claude/skills/lean-max
cp -r lean-max/SKILL.md lean-max/references ~/.claude/skills/lean-max/
```

Then use it:
```
/lean-max
```

**Always on, no invocation** — append the core rules to `~/.claude/CLAUDE.md`. See [docs/ALWAYS-ON.md](docs/ALWAYS-ON.md) for the compact version and its tradeoff.

**Web chat, desktop app, and cloud sessions** — those never read local files. Paste [docs/account-preferences.md](docs/account-preferences.md) into your claude.ai account preferences to cover them.

---

## What it actually does

**Calibrates before it optimizes.** A 40-line file gets read whole — running grep discipline on it costs more than it saves. Only files above 200 lines get the ranged-read treatment. Anything touching auth, money, migrations, or deletes gets an adversarial pass on top.

**Greps dependents *before* editing, not after tests break.** This single rule is the highest-value line in the skill. In benchmark scenario 2, a signature change shipped without it produced `TypeError` and 4 failing tests. The pre-edit grep had already listed the exact line that needed updating.

**Refuses to fake verification.** Four tiers — executed / typechecked / traced / unverified — and the model must name which one it used. "Should work" is not an allowed output. A test suite that goes green because a guard was weakened is treated as a regression, not a success.

**Kills output waste.** No recaps, no "I've successfully…", no restating your request, no pasting back code that's already on disk. Citations are `path:line`.

**Persists context instead of hoarding it.** The biggest cost in long-running work isn't file reads — it's the conversation being re-read every turn. A 224 MB session measured in testing had auto-compacted 204 times: already losing detail, still paying full price. lean-max writes what matters to a `STATE.md` and clears, which is both cheaper and *more* faithful than a session that summarizes itself behind your back.

**Treats installed skills as a per-request tax.** Every skill's name and description rides in the system prompt whether you use it or not. On one real setup, 1,990 installed skills cost ~103,000 tokens on *every request* — more than every file read combined. Install what you use.

**Knows when to spend more.** Irreversible changes, unfamiliar code, verification that failed twice — the skill tells the model to escalate deliberately and say why. Cutting tokens is not the goal; not wasting them is.

---

## Check your setup first

Before optimizing how you work, check what every request pays before it starts:

```bash
./audit.sh
```

It flags the drains that have nothing to do with coding style — a bloated skill index
(measured at ~103,000 tokens *per request* on one real setup), a 1M context window
multiplying cache reads, oversized sessions that auto-compact and lose detail anyway,
plus third-party API routing and plaintext credentials. Read-only; it changes nothing.

Full detail: [references/setup-audit.md](references/setup-audit.md).

## Structure

Progressive disclosure — **66% of the skill never enters context unless the task needs it.**

```
SKILL.md              99 lines   ~1,850 tok   always loaded
references/
├── playbooks.md      73 lines   \
├── budget.md         52 lines    |
├── enforcement.md    48 lines    |  ~3,600 tok — loaded on demand only
├── stacks.md         34 lines    |
└── verification.md   30 lines   /
```

The ~1,850-token resident cost is recovered the first time you avoid reading one large file whole.

| File | What's in it |
|---|---|
| [`SKILL.md`](SKILL.md) | The operating rules — calibration, the loop, hard rules, token rules, cloud/headless mode |
| [`references/playbooks.md`](references/playbooks.md) | 7 task types: bug fix, feature, refactor, review, investigation, migration, stuck-debugging |
| [`references/verification.md`](references/verification.md) | The four tiers and what disqualifies a check |
| [`references/stacks.md`](references/stacks.md) | Locate + verify commands for 14 stacks, plus per-stack traps |
| [`references/budget.md`](references/budget.md) | Reading budgets by file size, search discipline, delegation math |
| [`references/enforcement.md`](references/enforcement.md) | Hooks that make the rules mechanical instead of advisory |

---

## Reproduce the benchmark

```bash
cd examples/benchmark
python3 run_tests.py        # 6 passed, 1 failed — the planted bug
```

Then hand the failing test to Claude with and without the skill and compare what each reads. Full methodology, edge-case table, and the blast-radius scenario: [docs/BENCHMARK.md](docs/BENCHMARK.md).

---

## Honest limitations

- **Advisory by default.** It shapes behavior; it can't force it. [`references/enforcement.md`](references/enforcement.md) shows how to make verification mechanical via hooks.
- **Savings are size-dependent.** Near zero on small files. That's by design.
- **Benchmarked on Python.** The other 13 stacks' commands are standard and correct but weren't executed in the benchmark run.
- **Delegation rules are unproven** — subagent fan-out is sound in principle, untested here.

---

## Works with

Claude Code (CLI, desktop, web, IDE extensions), cloud/headless sessions, and CI. Section 4 of `SKILL.md` covers non-interactive runs specifically: no blocking questions, no interactive flags, no assumptions about installed tooling, durable output trail.

## Contributing

Improvements welcome — especially benchmark runs on other languages. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). The bar: **a change to the rules should come with evidence it changed an outcome.** That's how the pre-edit-grep rule got in.

## License

MIT — see [LICENSE](LICENSE).
