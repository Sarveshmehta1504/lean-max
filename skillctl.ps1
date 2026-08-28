# skillctl (Windows) - archive, search, and restore Claude skills.
#   .\skillctl.ps1 count
#   .\skillctl.ps1 prune  lean-max,jq          # archive everything EXCEPT these
#   .\skillctl.ps1 search postgres
#   .\skillctl.ps1 restore <name>
param([Parameter(Position=0)][string]$Cmd = "help",
      [Parameter(Position=1)][string]$Arg = "")
$C = Join-Path $env:USERPROFILE ".claude"
$S = Join-Path $C "skills"; $A = Join-Path $C "skills-archive"
New-Item -ItemType Directory -Force -Path $A | Out-Null
$MAN = Join-Path $A "MANIFEST.txt"

switch ($Cmd) {
  "count" {
    $a = @(Get-ChildItem $S -Directory -ErrorAction SilentlyContinue).Count
    $b = @(Get-ChildItem $A -Directory -ErrorAction SilentlyContinue).Count
    Write-Host "  active:   $a"; Write-Host "  archived: $b"
  }
  "prune" {
    if (-not $Arg) { Write-Host "usage: .\skillctl.ps1 prune name1,name2"; break }
    $keep = $Arg -split ',' | ForEach-Object { $_.Trim() }
    # write the manifest FIRST so nothing becomes unfindable
    Get-ChildItem $S -Directory | ForEach-Object {
      $f = Join-Path $_.FullName "SKILL.md"; $d = ""
      if (Test-Path $f) {
        foreach ($line in (Get-Content $f -TotalCount 20)) {
          if ($line -match '^description:\s*(.+)$') { $d = $matches[1]; break }
        }
      }
      "$($_.Name)`t$d"
    } | Set-Content $MAN
    $n = 0
    Get-ChildItem $S -Directory | Where-Object { $keep -notcontains $_.Name } | ForEach-Object {
      Move-Item $_.FullName (Join-Path $A $_.Name) -Force; $n++
    }
    Write-Host "  archived $n skills; kept: $($keep -join ', ')"
    Write-Host "  manifest written to $MAN - nothing is lost, restore any by name."
  }
  "search" {
    if (-not (Test-Path $MAN)) { Write-Host "no manifest - run prune first"; break }
    Select-String -Path $MAN -Pattern $Arg -SimpleMatch | Select-Object -First 40 |
      ForEach-Object { Write-Host ("  " + $_.Line) }
  }
  "restore" {
    $src = Join-Path $A $Arg
    if (-not (Test-Path $src)) { Write-Host "not in archive: $Arg"; break }
    Move-Item $src (Join-Path $S $Arg) -Force
    Write-Host "restored: $Arg  (active in your next Claude session)"
  }
  default {
    Write-Host "  .\skillctl.ps1 count"
    Write-Host "  .\skillctl.ps1 prune lean-max,jq   # archive all EXCEPT these"
    Write-Host "  .\skillctl.ps1 search <term>"
    Write-Host "  .\skillctl.ps1 restore <name>"
  }
}
