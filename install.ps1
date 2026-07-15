[CmdletBinding()]
param(
    [ValidateSet('All', 'Claude', 'Codex')]
    [string]$Target = 'All',

    [string]$Skill = '*',

    [ValidateSet('Junction', 'Copy')]
    [string]$Mode = 'Junction',

    [switch]$List,

    # Opt-in: link global/user-CLAUDE.md to ~/.claude/CLAUDE.md (backs up an existing file).
    [switch]$GlobalRules
)

$ErrorActionPreference = 'Stop'
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceRoot = Join-Path $RepoDir 'skills'

function Get-AvailableSkills {
    Get-ChildItem -LiteralPath $SourceRoot -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') } |
        Sort-Object Name
}

function Get-SkillDescription {
    param([Parameter(Mandatory)][string]$SkillFile)

    $line = Select-String -LiteralPath $SkillFile -Pattern '^description:\s*(.+)$' |
        Select-Object -First 1
    if ($null -eq $line) {
        return ''
    }
    return $line.Matches[0].Groups[1].Value
}

$AvailableSkills = @(Get-AvailableSkills)

if ($List) {
    foreach ($item in $AvailableSkills) {
        $description = Get-SkillDescription -SkillFile (Join-Path $item.FullName 'SKILL.md')
        [PSCustomObject]@{
            Name = $item.Name
            Description = $description
        }
    }
    return
}

if ($Skill -eq '*') {
    $SelectedSkills = $AvailableSkills
} else {
    $SelectedSkills = @($AvailableSkills | Where-Object Name -EQ $Skill)
    if ($SelectedSkills.Count -eq 0) {
        $names = ($AvailableSkills.Name -join ', ')
        throw "Unknown skill '$Skill'. Available skills: $names"
    }
}

if ($SelectedSkills.Count -eq 0) {
    throw "No skills found under $SourceRoot"
}

$ClaudeDir = if ($env:CLAUDE_SKILLS_DIR) {
    $env:CLAUDE_SKILLS_DIR
} else {
    Join-Path $HOME '.claude\skills'
}

$CodexDir = if ($env:CODEX_SKILLS_DIR) {
    $env:CODEX_SKILLS_DIR
} elseif ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME 'skills'
} else {
    Join-Path $HOME '.agents\skills'
}

function Install-Skill {
    param(
        [Parameter(Mandatory)][System.IO.DirectoryInfo]$Source,
        [Parameter(Mandatory)][string]$TargetRoot
    )

    New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
    $destination = Join-Path $TargetRoot $Source.Name

    if (Test-Path -LiteralPath $destination) {
        $existing = Get-Item -LiteralPath $destination -Force
        if (($existing.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            $existingTarget = [string]$existing.Target
            if ($existingTarget -and
                ([IO.Path]::GetFullPath($existingTarget) -eq [IO.Path]::GetFullPath($Source.FullName))) {
                Write-Host "already installed: $destination"
            } else {
                throw "Refusing to replace link with a different target: $destination"
            }
        } else {
            throw "Refusing to replace existing non-link path: $destination"
        }
    } elseif ($Mode -eq 'Copy') {
        Copy-Item -LiteralPath $Source.FullName -Destination $destination -Recurse
        Write-Host "copied: $destination"
    } else {
        try {
            New-Item -ItemType Junction -Path $destination -Target $Source.FullName | Out-Null
            Write-Host "linked: $destination -> $($Source.FullName)"
        } catch {
            Write-Warning "Junction creation failed; falling back to a copy. Rerun after git pull to update it."
            Copy-Item -LiteralPath $Source.FullName -Destination $destination -Recurse
            Write-Host "copied: $destination"
        }
    }

    $installedSkill = Join-Path $destination 'SKILL.md'
    if (-not (Test-Path -LiteralPath $installedSkill)) {
        throw "Verification failed: $installedSkill is not readable"
    }
}

foreach ($source in $SelectedSkills) {
    if ($Target -in @('Claude', 'All')) {
        Install-Skill -Source $source -TargetRoot $ClaudeDir
    }
    if ($Target -in @('Codex', 'All')) {
        Install-Skill -Source $source -TargetRoot $CodexDir
    }
}

# Opt-in only: this replaces the user-level CLAUDE.md that every session in every
# folder loads, so it must never happen as a side effect of installing a skill.
if ($GlobalRules) {
    $rulesSource = Join-Path $RepoDir 'global\user-CLAUDE.md'
    if (-not (Test-Path -LiteralPath $rulesSource)) {
        throw "Global rules not found: $rulesSource"
    }

    $claudeMd = if ($env:CLAUDE_GLOBAL_RULES) {
        $env:CLAUDE_GLOBAL_RULES
    } else {
        Join-Path $HOME '.claude\CLAUDE.md'
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $claudeMd) -Force | Out-Null

    if (Test-Path -LiteralPath $claudeMd) {
        $existing = Get-Item -LiteralPath $claudeMd -Force
        if (($existing.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) {
            # Skip the backup when the file is already our rules: if symlink creation fell back
            # to a copy, an unguarded rerun would pile up identical .bak files.
            $sameContent = (Get-FileHash -LiteralPath $claudeMd).Hash -eq
                (Get-FileHash -LiteralPath $rulesSource).Hash
            if (-not $sameContent) {
                $backup = "$claudeMd.bak." + (Get-Date -Format 'yyyyMMddHHmmss')
                Copy-Item -LiteralPath $claudeMd -Destination $backup
                Write-Host "backed up existing global rules: $backup"
            }
        }
        Remove-Item -LiteralPath $claudeMd -Force
    }

    try {
        New-Item -ItemType SymbolicLink -Path $claudeMd -Target $rulesSource | Out-Null
        Write-Host "installed global rules: $claudeMd -> $rulesSource"
    } catch {
        Write-Warning 'Symlink creation failed; falling back to a copy. Rerun after git pull to update it.'
        Copy-Item -LiteralPath $rulesSource -Destination $claudeMd
        Write-Host "copied global rules: $claudeMd"
    }

    if (-not (Test-Path -LiteralPath $claudeMd)) {
        throw "Verification failed: $claudeMd is not readable"
    }
}

Write-Host 'Installation verified. Start a new agent session if the Skill is not discovered immediately.'
