# lean-max setup audit (Windows / PowerShell)
# Finds token drains and risky config in a Claude Code setup. Read-only.
#   .\audit.ps1
$C = Join-Path $env:USERPROFILE ".claude"
$S = Join-Path $C "settings.json"
function Issue($m){ Write-Host "  ISSUE   " -ForegroundColor Red   -NoNewline; Write-Host $m }
function Warn($m) { Write-Host "  CHECK   " -ForegroundColor Yellow -NoNewline; Write-Host $m }
function Ok($m)   { Write-Host "  OK      " -ForegroundColor Green  -NoNewline; Write-Host $m }
Write-Host "`nlean-max setup audit`n"

# 1. Installed skills - a per-request tax
$skillDir = Join-Path $C "skills"
if (Test-Path $skillDir) {
  $skills = @(Get-ChildItem $skillDir -Directory -ErrorAction SilentlyContinue)
  $chars = 0
  foreach ($s in $skills) {
    $f = Join-Path $s.FullName "SKILL.md"
    if (Test-Path $f) {
      $head = (Get-Content $f -TotalCount 20 -ErrorAction SilentlyContinue) -join "`n"
      foreach ($line in ($head -split "`n")) {
        if ($line -match '^(name|description):\s*(.+)$') { $chars += $matches[2].Length + 6 }
      }
    }
  }
  $tok = [math]::Round($chars / 3.7)
  if ($tok -gt 20000) {
    Issue "$($skills.Count) skills installed = ~$tok tokens in EVERY request's system prompt."
    Write-Host "          Every skill's name+description is sent whether you use it or not."
    Write-Host "          Archive what you don't use - often the single largest drain."
  } elseif ($tok -gt 5000) { Warn "$($skills.Count) skills = ~$tok tokens per request. Worth trimming." }
  else { Ok "$($skills.Count) skills = ~$tok tokens per request." }
}

# 2. Context window
if (Test-Path $S) {
  try {
    $cfg = Get-Content $S -Raw | ConvertFrom-Json
    $model = $cfg.model
    if ($model -like "*[1m]*") {
      Issue "model is '$model' - a 1M context window."
      Write-Host "          Every turn re-reads the whole cached prefix, so sessions grow 5x"
      Write-Host "          larger before compacting. Use standard context unless you need 1M."
    } elseif ([string]::IsNullOrEmpty($model)) { Ok "model not pinned (using default)." }
    else { Ok "model: $model" }
  } catch { Warn "settings.json is not valid JSON - fix before trusting other checks." }

  # 3. Routing and credentials
  $raw = Get-Content $S -Raw
  if ($raw -match 'ANTHROPIC_BASE_URL') {
    Issue "ANTHROPIC_BASE_URL is set - traffic routed through a non-Anthropic host."
    Write-Host "          Every prompt, file, and secret Claude sees transits that host."
  } else { Ok "no base-URL override - talking to Anthropic directly." }
  if ($raw -match '"(ANTHROPIC_AUTH_TOKEN|ANTHROPIC_API_KEY)"\s*:\s*"[^"]+"') {
    Issue "a credential is stored in plaintext in settings.json."
    Write-Host "          Readable by anything running as your user. Rotate it."
  } else { Ok "no plaintext credentials in settings.json." }
}

# 4. Oversized sessions
$proj = Join-Path $C "projects"
if (Test-Path $proj) {
  $big = @(Get-ChildItem $proj -Recurse -Filter *.jsonl -ErrorAction SilentlyContinue |
           Where-Object { $_.Length -gt 20MB } | Sort-Object Length -Descending)
  if ($big.Count -gt 0) {
    Issue "$($big.Count) session transcript(s) over 20 MB."
    foreach ($f in $big | Select-Object -First 3) {
      Write-Host ("          {0,6:N0} MB  {1}" -f ($f.Length/1MB), $f.Name)
    }
    Write-Host "          Those sessions already lost detail to compaction at full price."
    Write-Host "          Persist context to STATE.md and /clear - see references/context.md"
  } else { Ok "no oversized session transcripts." }

  # 5. Context persistence in use?
  $states = @(Get-ChildItem $proj -Recurse -Filter STATE.md -ErrorAction SilentlyContinue)
  if ($states.Count -gt 0) { Ok "$($states.Count) project(s) using STATE.md." }
  else { Warn "no STATE.md found - long projects re-carry context every session." }
}
Write-Host ""
