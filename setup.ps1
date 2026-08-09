#Requires -Version 5.1
<#
.SYNOPSIS
One-shot entry point for a fresh machine: global rules + every skill.

.DESCRIPTION
Thin wrapper over install.ps1. install.ps1 installs every skill by default;
-GlobalRules adds the always-on rules in ~/.claude/CLAUDE.md that a plain
install deliberately leaves alone.

    git clone https://github.com/ShinKiHun/claude-skills.git $HOME\claude-skills
    & $HOME\claude-skills\setup.ps1

Re-run after `git pull` to refresh. Extra arguments are forwarded to
install.ps1, so `.\setup.ps1 -Target Claude` narrows the target the same way.
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments)]
    [string[]]$Forward
)

$ErrorActionPreference = 'Stop'

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Install = Join-Path $RepoDir 'install.ps1'

if (-not (Test-Path -LiteralPath $Install)) {
    throw "install.ps1 not found next to setup.ps1: $Install"
}

Write-Host '==> installing global rules (~/.claude/CLAUDE.md, loaded every session) + all skills'
& $Install -GlobalRules @Forward
if ($LASTEXITCODE) { exit $LASTEXITCODE }

# Continuity hooks are merged into settings.json, never written over it — other
# tools' hooks live in the same file. Skipped (not fatal) when python is absent.
Write-Host ''
Write-Host '==> installing continuity hooks (SessionStart / Stop)'
# Get-Command alone is not enough on Windows: the Microsoft Store App Execution
# Alias resolves but only prints "Python" and exits non-zero. Probe it actually runs.
$Py = $null
foreach ($cand in 'python', 'python3') {
    $cmd = Get-Command $cand -ErrorAction SilentlyContinue
    if (-not $cmd) { continue }
    & $cmd.Source -c 'import sys' 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $Py = $cmd.Source; break }
}
if ($Py) {
    & $Py (Join-Path $RepoDir 'hooks/install_hooks.py') $RepoDir
    if ($LASTEXITCODE) {
        Write-Host '  (hook install failed - skills and rules are still installed)'
    }
} else {
    Write-Host '  (python not found - skipping hooks; skills and rules are still installed)'
}

Write-Host ''
Write-Host 'Done. Refresh later with:'
Write-Host "  cd `"$RepoDir`"; git pull; .\setup.ps1"
