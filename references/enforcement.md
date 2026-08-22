# Enforcement — making the rules mechanical

The skill is advisory: it shapes behavior but cannot prevent a shortcut. These make parts of it structural. All are opt-in; nothing here is required for the skill to work.

## Hooks (`~/.claude/settings.json`)

Hooks run in the harness, not in the model, so they hold even when the model is under context pressure — exactly when discipline degrades.

**Auto-verify after edits** — makes the "verify before done" rule impossible to skip silently:
```json
{ "hooks": { "PostToolUse": [ {
  "matcher": "Edit|Write",
  "hooks": [ { "type": "command",
    "command": "cd \"$CLAUDE_PROJECT_DIR\" 2>/dev/null && [ -f package.json ] && npx tsc --noEmit 2>&1 | head -20 || true" } ]
} ] } }
```

**Block edits to fragile paths** — pair with the CLAUDE.md "known-fragile files" list:
```json
{ "hooks": { "PreToolUse": [ {
  "matcher": "Edit|Write",
  "hooks": [ { "type": "command",
    "command": "case \"$CLAUDE_TOOL_INPUT_FILE_PATH\" in *migrations/*|*.env*) echo 'fragile path — confirm with user first' >&2; exit 2;; esac" } ]
} ] } }
```
Exit code 2 blocks the call and returns the message to the model.

Ask before adding hooks — they run on every matching call and a slow hook taxes every edit. Use the `update-config` skill to install them correctly rather than hand-editing settings.

## Repo-level pairing

Put in each repo's `CLAUDE.md`:
```
Stack:
Test command:
Known-fragile files (edit surgically, single-file only):
Never touch without asking:
```
This is the single highest-value addition — it removes an entire discovery round-trip per session, paying for itself immediately.

## Measuring whether it's working

Track across sessions:
- **Verification rate** — % of "done" claims backed by an executed command. Target 100%.
- **Rework rate** — % of changes needing a follow-up fix. Should trend down.
- **Read ratio** — lines read ÷ lines in touched files. Should sit well under 0.3 on large files.

If rework rises while read ratio falls, the budget is being cut too aggressively — escalate per §3.
