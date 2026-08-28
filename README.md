# lean-max

**A Claude Code skill that cuts token usage on coding work — without cutting quality.**

Most token waste in AI coding isn't the thinking. It's reading a 967-line file to change
three lines, pasting code back into chat that's already on disk, narrating work the diff
already shows, and dragging a 200 MB conversation behind you all day. lean-max removes
that and spends the savings where it counts: **actually verifying the change works.**

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

Reproducible in this repo ([`examples/benchmark`](examples/benchmark)) — a 967-line Python
module with a subtle pricing bug that passes 6 of 7 tests and survives casual review.

| Approach | Tokens | Outcome |
|---|---|---|
| Naive — read the files whole | **15,335** | bug fixed |
| lean-max — grep, then read 60 of 967 lines | **994** | bug fixed, **+ 6 edge cases verified** |
| | **↓ 94%** | |

The lean run read **6.2% of the file** and produced the *better* result, because the
tokens saved on narration went into an executed test run.

Savings scale with file size: ~90%+ above 800 lines, ~40–60% at 200–600, ~0% under 200.
It never costs more than the naive path — the skill tells the model to stop optimizing on
small files.

---

## Read this before installing

**The skill is only 2 of the 5 things that drive your token bill.** Three are machine
configuration, and installing this repo does not change them. On one real setup the
config levers were **200× larger** than the skill's file-reading rules.

| Lever | Type | Typical saving |
|---|---|---|
| 1. Prune unused skills | **config** | up to ~100k tokens **per request** |
| 2. Standard context, not 1M | **config** | up to 5× less cache read per turn |
| 3. No proxy / no plaintext key | **config** | security, not tokens |
| 4. STATE.md checkpointing | skill | measured 63M → ~641 tokens |
| 5. Read/output discipline | skill | ~14k per large file read |

Lever 1 is usually the shock. Every installed skill's name and description sits in the
system prompt of **every request**, used or not. One machine had 1,990 skills installed —
**~103,000 tokens on every single request** — and had ever invoked 5 of them.

So start with the audit, not the install.

---

## Setup

### Step 0 — audit (do this first, on either OS)

Read-only. Changes nothing. Tells you which of the five levers apply to you.

**macOS / Linux**
```bash
git clone https://github.com/Sarveshmehta1504/lean-max.git
cd lean-max && ./audit.sh
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/Sarveshmehta1504/lean-max.git
cd lean-max
powershell -ExecutionPolicy Bypass -File .\audit.ps1
```

### Step 1 — prune skills (usually the biggest win)

Nothing is deleted; skills move to `skills-archive/` and a manifest keeps every one
searchable and restorable by name.

**macOS / Linux** — the audit prints your count; archive with a `mv`, or use the helper
in `~/.claude/skills-archive/skillctl` after your first prune.

**Windows**
```powershell
.\skillctl.ps1 count
.\skillctl.ps1 prune lean-max,jq
.\skillctl.ps1 search postgres     # find anything you archived
.\skillctl.ps1 restore <name>
```

### Step 2 — stop using a 1M context window

In `settings.json` (`~/.claude/` on macOS, `%USERPROFILE%\.claude\` on Windows), change:

```json
"model": "opus[1m]"   →   "model": "opus"
```

A 1M window is not extra memory. It lets a session grow 5× larger before compacting,
and **every turn re-reads the whole cached prefix**. Do this *after* Step 4 — a smaller
window compacts sooner, and STATE.md is what keeps compaction from eating your context.

### Step 3 — check routing and credentials

In the same file: an `env` block with `ANTHROPIC_BASE_URL` routes every prompt, file, and
secret Claude sees through a third-party host. An inline `ANTHROPIC_AUTH_TOKEN` or
`ANTHROPIC_API_KEY` is plaintext on disk and leaks into transcripts the moment anything
prints that file. Remove unless deliberate; rotate the key if it was.

### Step 4 — install the skill

**macOS / Linux**
```bash
./install.sh /path/to/your/repo          # one project
```
```bash
mkdir -p ~/.claude/skills/lean-max && cp -r SKILL.md references ~/.claude/skills/lean-max/
```

**Windows**
```powershell
mkdir "$env:USERPROFILE\.claude\skills\lean-max" -Force
Copy-Item .\SKILL.md "$env:USERPROFILE\.claude\skills\lean-max\"
Copy-Item .\references "$env:USERPROFILE\.claude\skills\lean-max\" -Recurse -Force
```

Then use it with `/lean-max`.

### Step 5 — always on, no invocation (optional)

Append the compact ~371-token core to your global `CLAUDE.md`:

**macOS / Linux**
```bash
cat docs/always-on-core.md >> ~/.claude/CLAUDE.md
```
**Windows**
```powershell
Get-Content .\docs\always-on-core.md | Add-Content "$env:USERPROFILE\.claude\CLAUDE.md"
```

See [docs/ALWAYS-ON.md](docs/ALWAYS-ON.md) for the tradeoff.

### Step 6 — cover web, desktop, and cloud (one step, every device)

`CLAUDE.md` is a **local file** — it does not sync. Web chat, the desktop app, and cloud
sessions never see it. Paste [docs/account-preferences.md](docs/account-preferences.md)
into **claude.ai → Settings → Profile → Personal preferences**. Once, and it applies on
every device tied to your account.

### Then verify

Re-run the audit. All config checks should read OK.

Full Windows walkthrough: **[docs/WINDOWS.md](docs/WINDOWS.md)**.

---

## What it actually does

**Calibrates before it optimizes.** A 40-line file gets read whole — grep discipline there
costs more than it saves. Only files above 200 lines get ranged reads. Anything touching
auth, money, migrations, or deletes gets an adversarial pass on top.

**Greps dependents *before* editing, not after tests break.** The highest-value line in the
skill, and it came from testing rather than intuition: a benchmark scenario that skipped it
shipped a `TypeError` and 4 failing tests, while the pre-edit grep had already named the
exact line to fix.

**Refuses to fake verification.** Four tiers — executed / typechecked / traced / unverified
— and the model must say which it used. "Should work" is not an allowed output. A suite
that goes green because a guard was weakened is treated as a regression.

**Resumes and checkpoints automatically.** Step 0 of the loop reads `STATE.md` if the
project has one; step 8 rewrites it when a task finishes — unprompted, as part of
finishing. Invoke the skill and the cycle runs itself: resume → work → checkpoint → clear.

**Persists context instead of hoarding it.** A 224 MB session measured in testing had
auto-compacted ~19 times: already losing detail, still paying full price for what remained.
Its entire useful state fit in ~641 tokens of `STATE.md` — cheaper *and* more faithful than
a session that summarizes itself behind your back.

**Kills output waste.** No recaps, no "I've successfully…", no restating your request, no
pasting back code that's on disk. Citations are `path:line`.

**Knows when to spend more.** Irreversible changes, unfamiliar code, verification that
failed twice — escalate deliberately and say why. Cutting tokens isn't the goal; not
wasting them is.

---

## Structure

Progressive disclosure — **66% of the skill never enters context unless the task needs it.**

```
SKILL.md              107 lines  ~1,850 tok   always loaded
references/
├── context.md         89 lines  \
├── playbooks.md       73 lines   |
├── budget.md          52 lines   |  ~4,500 tok — on demand only
├── setup-audit.md     55 lines   |
├── enforcement.md     48 lines   |
├── stacks.md          34 lines   |
└── verification.md    30 lines  /
```

| File | What's in it |
|---|---|
| [`SKILL.md`](SKILL.md) | The loop, hard rules, token rules, cloud/headless mode |
| [`references/playbooks.md`](references/playbooks.md) | 7 task types: bug fix, feature, refactor, review, investigation, migration, stuck-debugging |
| [`references/context.md`](references/context.md) | STATE.md — what to record, what never to, long autonomous runs |
| [`references/verification.md`](references/verification.md) | The four tiers and what disqualifies a check |
| [`references/stacks.md`](references/stacks.md) | Locate + verify commands for 14 stacks, and their traps |
| [`references/budget.md`](references/budget.md) | Reading budgets by file size, search discipline, delegation math |
| [`references/setup-audit.md`](references/setup-audit.md) | The config-level drains, in detail |
| [`references/enforcement.md`](references/enforcement.md) | Hooks that make the rules mechanical, not advisory |

CI fails the build if `SKILL.md` exceeds 130 lines — low resident cost is the whole point,
so growth is treated as a regression.

---

## Reproduce the benchmark

```bash
cd examples/benchmark && python3 run_tests.py    # 6 passed, 1 failed — the planted bug
```

Then hand the failing test to Claude with and without the skill and compare what each
reads. Methodology, edge-case table, and the blast-radius scenario:
[docs/BENCHMARK.md](docs/BENCHMARK.md).

---

## Honest limitations

- **Advisory by default.** It shapes behavior; it can't force it. `references/enforcement.md`
  shows how to make verification mechanical with hooks.
- **Savings are size-dependent.** Near zero on small files. By design.
- **Benchmarked on Python.** The other 13 stacks' commands are standard but weren't executed
  in the benchmark run.
- **The PowerShell scripts were authored on macOS and not executed on Windows.** Read-only
  except `prune`/`restore`, which only move directories. Run `count` before `prune`.
- **Delegation rules are unproven** — subagent fan-out is sound in principle, untested here.

---

## Works with

Claude Code on macOS, Linux, and Windows (CLI, desktop, web, IDE extensions), plus
cloud/headless sessions and CI. Section 4 of `SKILL.md` covers non-interactive runs: no
blocking questions, no interactive flags, no assumptions about installed tooling.

## Contributing

Especially benchmark runs on other languages, and Windows testing of the PowerShell
scripts. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). The bar: **a change to the rules
should come with evidence it changed an outcome.**

## License

MIT — see [LICENSE](LICENSE).
