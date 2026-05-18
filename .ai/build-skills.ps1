# build-skills.ps1 — Build all harness SKILL.md files from .ai/skills/ source of truth.
# Idempotent: safe to run multiple times.
# Writes only to: .claude/skills\ .agents/skills\ .cursor/skills\ .github/skills\
#
# Requirements: Developer Mode OR Administrator privileges for symlink creation.
# Enable Developer Mode: Settings -> System -> Developer Mode

#Requires -Version 5.1

$ErrorActionPreference = 'Stop'

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot   = Split-Path -Parent $scriptDir
$skillsSrc  = Join-Path $scriptDir 'skills'

$harnessDirs = @{
    claude  = '.claude\skills'
    codex   = '.agents\skills'
    cursor  = '.cursor\skills'
    copilot = '.github\skills'
}

$skillsProcessed  = 0
$skillMdsWritten  = 0
$symlinksCreated  = 0
$symlinksVerified = 0
$errors           = 0

function Get-RelativePath([string]$from, [string]$to) {
    $fromUri = [System.Uri]::new($from.TrimEnd('\') + '\')
    $toUri   = [System.Uri]::new($to)
    $rel     = $fromUri.MakeRelativeUri($toUri).ToString()
    return $rel -replace '/', '\'
}

function Create-OrVerify-Symlink([string]$link, [string]$target) {
    if (Test-Path $link -PathType Any) {
        $item = Get-Item $link -Force
        if ($item.LinkType -eq 'SymbolicLink') {
            if ($item.Target -eq $target) {
                $script:symlinksVerified++
                return
            }
            Remove-Item $link -Force
        } else {
            Write-Host "ERROR: $link exists but is not a symlink — skipping" -ForegroundColor Red
            $script:errors++
            return
        }
    }

    $parentDir = Split-Path $link -Parent
    if (-not (Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }

    try {
        New-Item -ItemType SymbolicLink -Path $link -Target $target -Force | Out-Null
        $script:symlinksCreated++
    } catch {
        if ($_.Exception.Message -match 'privilege|access|denied') {
            Write-Host "ERROR: Symlinks require Developer Mode (Settings -> System -> Developer Mode) or Administrator privileges on Windows." -ForegroundColor Red
            Write-Host "       Failed to create symlink: $link -> $target" -ForegroundColor Red
        } else {
            Write-Host "ERROR: Could not create symlink $link -> $target : $($_.Exception.Message)" -ForegroundColor Red
        }
        $script:errors++
    }
}

function Write-IfChanged([string]$path, [string]$content) {
    if (Test-Path $path) {
        $existing = [System.IO.File]::ReadAllText($path)
        if ($existing -eq $content) { return }
    }
    $parentDir = Split-Path $path -Parent
    if (-not (Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }
    [System.IO.File]::WriteAllText($path, $content, [System.Text.UTF8Encoding]::new($false))
    $script:skillMdsWritten++
}

if (-not (Test-Path $skillsSrc -PathType Container)) {
    Write-Host "ERROR: $skillsSrc does not exist. Nothing to build." -ForegroundColor Red
    exit 1
}

foreach ($skillDir in Get-ChildItem -Path $skillsSrc -Directory) {
    $skillName  = $skillDir.Name
    $contentSrc = Join-Path $skillDir.FullName 'content.md'

    if (-not (Test-Path $contentSrc)) {
        Write-Host "ERROR: $contentSrc missing — skipping skill '$skillName'" -ForegroundColor Red
        $errors++
        continue
    }

    foreach ($harness in $harnessDirs.Keys) {
        $yamlSrc = Join-Path $skillDir.FullName "$harness.yaml"

        if (-not (Test-Path $yamlSrc)) {
            Write-Host "ERROR: $yamlSrc missing — skipping harness '$harness' for skill '$skillName'" -ForegroundColor Red
            $errors++
            continue
        }

        $targetBase = Join-Path $repoRoot (Join-Path $harnessDirs[$harness] $skillName)
        New-Item -ItemType Directory -Path $targetBase -Force | Out-Null

        # Symlink content.md using relative path
        $contentLink = Join-Path $targetBase 'content.md'
        $relContent  = Get-RelativePath -from $targetBase -to $contentSrc
        Create-OrVerify-Symlink -link $contentLink -target $relContent

        # Symlink any other files/dirs (excluding .yaml files and content.md)
        foreach ($item in Get-ChildItem -Path $skillDir.FullName) {
            if ($item.Name -match '\.yaml$' -or $item.Name -eq 'content.md') { continue }
            $itemLink = Join-Path $targetBase $item.Name
            $relItem  = Get-RelativePath -from $targetBase -to $item.FullName
            Create-OrVerify-Symlink -link $itemLink -target $relItem
        }

        # Build SKILL.md: frontmatter from <harness>.yaml + blank line + @content.md
        $frontmatter   = [System.IO.File]::ReadAllText($yamlSrc)
        $skillMdContent = "---`n${frontmatter}---`n`n@content.md`n"

        $skillMdPath = Join-Path $targetBase 'SKILL.md'
        Write-IfChanged -path $skillMdPath -content $skillMdContent
    }

    $skillsProcessed++
}

Write-Host ""
Write-Host "build-skills complete"
Write-Host "  Skills processed : $skillsProcessed"
Write-Host "  SKILL.md written : $skillMdsWritten"
Write-Host "  Symlinks created : $symlinksCreated"
Write-Host "  Symlinks verified: $symlinksVerified"
if ($errors -gt 0) {
    Write-Host "  Errors           : $errors (see above)" -ForegroundColor Red
    exit 1
}
