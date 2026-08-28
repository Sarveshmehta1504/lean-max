# Windows setup — the whole thing, in order

The skill is only 2 of the 5 levers. **Three of them are machine configuration**, and
cloning this repo does not apply them. Do all five or you keep the token bill.

| Lever | Type | Typical saving |
|---|---|---|
| 1. Prune unused skills | config | up to ~100k tokens **per request** |
| 2. Standard context, not 1M | config | up to 5× less cache read per turn |
| 3. No proxy / no plaintext key | config | security, not tokens |
| 4. STATE.md checkpointing | skill | measured 63M → ~641 tokens |
| 5. Read/output discipline | skill | ~14k per large file read |

Everything lives under `%USERPROFILE%\.claude\` — same layout as macOS.

---

## Step 0 — see where you actually stand

```powershell
git clone https://github.com/Sarveshmehta1504/lean-max.git
cd lean-max
powershell -ExecutionPolicy Bypass -File .\audit.ps1
```

Read-only. It changes nothing and tells you which of the five apply to you.

## Step 1 — prune skills (usually the biggest win by far)

Every installed skill's name and description sits in the system prompt of **every
request**, used or not. On one real machine, 1,990 installed skills cost **~103,000
tokens per request** — the user had ever invoked 5.

```powershell
.\skillctl.ps1 count
.\skillctl.ps1 prune lean-max,jq
```

Nothing is deleted — skills move to `%USERPROFILE%\.claude\skills-archive\` and a
manifest records every name and description.

```powershell
.\skillctl.ps1 search postgres
.\skillctl.ps1 restore <name>
```

## Step 2 — stop using a 1M context window

Open `%USERPROFILE%\.claude\settings.json`. If you see:

```json
"model": "opus[1m]"
```

change it to `"model": "opus"`. A 1M window doesn't give you more memory; it lets a
session grow 5× larger before compacting, and **every turn re-reads the whole prefix**.

Only safe once Step 4 is in place — a smaller window compacts sooner, and STATE.md is
what stops compaction from eating your context.

## Step 3 — check routing and credentials

In the same file, if there is an `env` block containing `ANTHROPIC_BASE_URL`, every
prompt, file, and secret Claude sees is being routed through that host. If
`ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY` is stored inline, it is plaintext on disk
and it leaks into session transcripts the moment anything prints that file.

Remove the block unless you put it there deliberately, and rotate the key if you did.

## Step 4 — install the skill

```powershell
mkdir "$env:USERPROFILE\.claude\skills\lean-max" -Force
Copy-Item .\SKILL.md "$env:USERPROFILE\.claude\skills\lean-max\"
Copy-Item .\references "$env:USERPROFILE\.claude\skills\lean-max\" -Recurse -Force
```

Use it with `/lean-max`. Steps 0 and 8 of its loop resume from and checkpoint to
`STATE.md` automatically — you don't run a separate command.

## Step 5 — always-on core (optional but recommended)

Append the compact core to `%USERPROFILE%\.claude\CLAUDE.md` so the rules apply without
invoking anything:

```powershell
Get-Content .\docs\always-on-core.md | Add-Content "$env:USERPROFILE\.claude\CLAUDE.md"
```

~371 tokens per session, recovered the first time one large file isn't read whole.

## Step 6 — account preferences (covers every device at once)

`~/.claude/CLAUDE.md` is a **local file**; it does not sync. Web chat, desktop, and cloud
sessions never see it. Paste [account-preferences.md](account-preferences.md) into
**claude.ai → Settings → Profile → Personal preferences**.

Do this once and it applies on Windows, macOS, phone — every surface tied to your account.

---

## Then verify

```powershell
.\audit.ps1
```

All config checks should read OK. If skills still show a large token count, Step 1 didn't
take — check you ran it against the right `%USERPROFILE%`.

## The habit that keeps it fixed

Work → let the skill checkpoint `STATE.md` → `/clear` → resume. One endless session per
project is what recreates the bill, on any OS.

## Note

`audit.ps1` and `skillctl.ps1` were written for PowerShell 5.1+ but authored on macOS and
have not been executed on Windows. They are read-only except `prune`/`restore`, which only
move directories. Review before running, and prefer `count` before `prune`. Bug reports
welcome — see CONTRIBUTING.
