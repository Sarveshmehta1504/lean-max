# Setup prompt

Paste this into Claude Code on a fresh machine. It is self-contained — the assistant needs
no prior context. It audits first, reports, and only then changes anything.

---

```
Set up this machine to use far fewer tokens with Claude Code, without losing output
quality or any of my existing data.

Reference repo: https://github.com/Sarveshmehta1504/lean-max
Read its README.md and docs/WINDOWS.md first — they contain the full method.

Work in this order and DO NOT skip the reporting step:

PHASE 1 — AUDIT ONLY. Change nothing yet.
1. Clone the repo to a temp folder and run its audit (audit.ps1 on Windows,
   audit.sh on macOS/Linux). It is read-only.
2. Independently verify these four things and show me the actual numbers:
   a) How many skills are installed in %USERPROFILE%\.claude\skills (or ~/.claude/skills),
      and roughly how many tokens their name+description index costs per request
      (~3.7 bytes per token). Also tell me which of them I have ACTUALLY invoked —
      search my session transcripts under .claude\projects for skill invocations.
   b) Whether settings.json pins a 1M context window ("model": "opus[1m]").
   c) Whether settings.json contains an ANTHROPIC_BASE_URL override or an inline
      ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEY.
   d) The size of my largest session transcripts, and how many times each has been
      auto-compacted.
3. STOP and report all findings in a short table, ranked by how many tokens each is
   costing me. Tell me which are worth fixing and which are not. Wait for my go-ahead.

PHASE 2 — APPLY, only after I approve.
4. Skills: MOVE unused ones to a skills-archive folder — never delete. Write a manifest
   of every skill name + description FIRST so nothing becomes unfindable, and give me a
   command to search and restore any of them by name. Keep the ones I actually use.
   Verify afterwards that archived + kept = the original total, with none unaccounted for.
5. settings.json: back it up with a timestamp first. If it pins a 1M context window,
   change it to standard. If there is a third-party base-URL override or a plaintext
   credential, remove it and tell me to rotate that key. Preserve every other key exactly
   — show me the before/after key list to prove nothing was lost.
6. Install the lean-max skill itself into .claude/skills/lean-max (SKILL.md + references/).
7. Optionally append the compact always-on core from docs/always-on-core.md to my global
   CLAUDE.md, and tell me the per-session token cost of doing so.

PHASE 3 — VERIFY AND EXPLAIN.
8. Re-run the audit and show me before/after numbers for each fix.
9. Tell me plainly what is now automatic versus what depends on my habits.
10. Confirm nothing was lost: my memory files, session transcripts, settings keys,
    plugins, and MCP config must all be intact. Show me the evidence, not a claim.

Rules for you throughout:
- Never delete anything. Move and back up, always reversibly.
- Show measured numbers, not estimates, wherever you can measure.
- If a step fails or you are unsure, stop and tell me rather than guessing.
- Do not modify any of my project repositories. This is a Claude-level setup only.
```

---

## Why it is shaped this way

**Audit before change.** The assistant reports what is actually costing tokens on *that*
machine before touching it. The numbers differ per machine; the fix should follow the
evidence, not this document.

**Archive, never delete.** Skill pruning is the biggest lever and the easiest to regret.
Manifest first, move second, verify the totals reconcile.

**Prove, don't claim.** Every phase ends with evidence — before/after counts, key lists,
reconciliation. "Nothing was lost" is a claim; a matching total is proof.

**Stay out of the repos.** Every one of these fixes is machine configuration. A setup task
has no business editing project code.
