#!/usr/bin/env bash
# lean-max setup audit — finds token drains and risky config in a Claude Code setup.
# Read-only: reports, never changes anything.
#   ./audit.sh
C=~/.claude; S=$C/settings.json
red()  { printf "\033[31m  ISSUE   \033[0m%s\n" "$1"; }
warn() { printf "\033[33m  CHECK   \033[0m%s\n" "$1"; }
ok()   { printf "\033[32m  OK      \033[0m%s\n" "$1"; }
echo; echo "lean-max setup audit"; echo

# 1. Installed skills — a per-request tax
n=$(ls -d "$C"/skills/*/ 2>/dev/null | wc -l | tr -d ' ')
if [ "${n:-0}" -gt 0 ]; then
  tok=$(python3 - <<'PY' 2>/dev/null
import glob,re,os
t=0
for f in glob.glob(os.path.expanduser('~/.claude/skills/*/SKILL.md')):
    try:
        s=open(f,errors='ignore').read(2000)
        m=re.search(r'^description:\s*(.+)$',s,re.M); nm=re.search(r'^name:\s*(.+)$',s,re.M)
        if m: t+=len(m.group(1))+len(nm.group(1) if nm else '')+6
    except: pass
print(round(t/3.7))
PY
)
  if [ "${tok:-0}" -gt 20000 ]; then
    red "$n skills installed = ~${tok} tokens in EVERY request's system prompt."
    echo "          Every skill's name+description is sent whether you use it or not."
    echo "          Archive what you don't use; this is often the largest single drain."
  elif [ "${tok:-0}" -gt 5000 ]; then
    warn "$n skills = ~${tok} tokens per request. Worth trimming."
  else
    ok "$n skills = ~${tok} tokens per request."
  fi
fi

# 2. Context window — multiplies cache-read cost per turn
if [ -f "$S" ]; then
  model=$(python3 -c "import json;print(json.load(open('$S')).get('model',''))" 2>/dev/null)
  case "$model" in
    *"[1m]"*) red "model is '$model' — a 1M context window."
              echo "          Every turn re-reads the whole cached prefix, so sessions can grow"
              echo "          5x larger before compacting. Use standard context unless you need 1M." ;;
    "")       ok "model not pinned (using default)." ;;
    *)        ok "model: $model" ;;
  esac
fi

# 3. Third-party routing / credentials in plaintext
if [ -f "$S" ]; then
  if grep -q 'ANTHROPIC_BASE_URL' "$S" 2>/dev/null; then
    red "ANTHROPIC_BASE_URL is set — traffic is routed through a non-Anthropic host."
    echo "          Every prompt, file, and secret Claude sees transits that host."
  else ok "no base-URL override — talking to Anthropic directly."; fi
  if grep -qE '"(ANTHROPIC_AUTH_TOKEN|ANTHROPIC_API_KEY)"\s*:\s*"[^"]+"' "$S" 2>/dev/null; then
    red "a credential is stored in plaintext in settings.json."
    echo "          Readable by anything running as your user. Rotate it and use the keychain."
  else ok "no plaintext credentials in settings.json."; fi
fi

# 4. Session size — the other big cache-read driver
big=$(find "$C/projects" -name '*.jsonl' -size +20M 2>/dev/null | wc -l | tr -d ' ')
if [ "${big:-0}" -gt 0 ]; then
  red "$big session transcript(s) over 20 MB."
  find "$C/projects" -name '*.jsonl' -size +20M 2>/dev/null | head -3 | while read f; do
    c=$(grep -c 'isCompactSummary\|"summary"' "$f" 2>/dev/null || echo 0)
    printf "          %6.0f MB, auto-compacted ~%s times\n" "$(ls -l "$f" | awk '{print $5/1048576}')" "$c"
  done
  echo "          Those sessions already lost detail to compaction while paying full price."
  echo "          Persist context to STATE.md and /clear — see references/context.md"
else ok "no oversized session transcripts."; fi

# 5. Context persistence in use?
if find "$C/projects" -name 'STATE.md' 2>/dev/null | grep -q .; then
  ok "$(find "$C/projects" -name 'STATE.md' 2>/dev/null | wc -l | tr -d ' ') project(s) using STATE.md."
else warn "no STATE.md found — long-running projects re-carry context every session."; fi

echo
