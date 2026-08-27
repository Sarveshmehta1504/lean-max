# Setup audit — token drains that have nothing to do with how you code

Before optimizing how files are read, check what every request pays *before it starts*.
Run `./audit.sh` from the repo, or check these by hand.

## 1. Installed skills are a per-request tax

Claude must be told every installed skill's name and description so it knows one exists.
That index sits in the system prompt of **every request**, used or not.

Measured on a real setup: **1,990 installed skills = ~103,000 tokens on every request.**
The user had ever invoked 5 of them. At ~500 requests/day that is ~51M tokens/day —
more than every file read, every output, and every session combined.

Install skills when you need them, not speculatively. Archive (don't delete) the rest.

## 2. A 1M context window multiplies cache-read cost

`"model": "opus[1m]"` lets a session grow to ~1,000,000 tokens before it is forced to
compact — and **every turn re-reads the whole cached prefix**. Standard context caps at
200k, cutting per-turn cache read by up to 5×.

Use 1M only when a single task genuinely needs it. It is not free headroom; it is a
larger bill on every turn.

## 3. Oversized sessions lose context *and* cost the most

A 224 MB transcript is ~63M tokens of history against a 200k window. It cannot be held,
so it auto-compacts repeatedly, replacing detail with summary. You pay maximum price for
context that is already degraded.

See `context.md` — persist to `STATE.md` and clear.

## 4. Routing and credentials

- **`ANTHROPIC_BASE_URL` in settings.json** routes every prompt, file, and secret Claude
  sees through a third-party host. Sometimes deliberate (cost routers); make sure it is.
- **`ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` stored inline** is plaintext on disk,
  readable by anything running as your user, and it leaks into session transcripts the
  moment anything prints that file. Rotate and move to the keychain.

Neither costs tokens directly. Both belong in the same audit because they are the other
half of "is my setup actually configured the way I think it is."

## Ranked impact

| Fix | Typical saving |
|---|---|
| Prune unused skills | up to ~100k tokens **per request** |
| Standard instead of 1M context | up to 5× less cache read per turn |
| STATE.md + `/clear` instead of endless sessions | ~75% of remaining cache read |
| lean-max's read/output rules | ~14k tokens per large file read |

The first three are configuration. Only the fourth is about how you work — and it is the
smallest of the four. Fix the setup first.
