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

Write-Host ''
Write-Host 'Done. Refresh later with:'
Write-Host "  cd `"$RepoDir`"; git pull; .\setup.ps1"
