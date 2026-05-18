# Symlink Strategy

Consult this file when creating or debugging symlinks during `generate` or `build-skill` mode.

All symlinks use **relative paths** so the repository remains portable across machines and operating systems.

---

## macOS / Linux

```sh
# Symlink content.md
ln -s ../../../.ai/skills/<name>/content.md .claude/skills/<name>/content.md

# Symlink a directory (e.g. references/)
ln -s ../../../.ai/skills/<name>/references  .claude/skills/<name>/references
```

Repeat for each harness, adjusting the target base path:

| Harness | Target base |
|---|---|
| Claude Code | `.claude/skills/<name>/` |
| Codex CLI | `.agents/skills/<name>/` |
| Cursor | `.cursor/skills/<name>/` |
| Copilot | `.github/skills/<name>/` |

---

## Windows

Requires **Developer Mode** (Settings → System → Developer Mode) **or** Administrator privileges.

```powershell
# File symlink
New-Item -ItemType SymbolicLink `
  -Path ".claude\skills\<name>\content.md" `
  -Target "..\..\..\.ai\skills\<name>\content.md"

# Directory symlink
New-Item -ItemType SymbolicLink `
  -Path ".claude\skills\<name>\references" `
  -Target "..\..\..\.ai\skills\<name>\references"
```

### Computing the relative path in PowerShell

```powershell
function Get-RelativePath([string]$from, [string]$to) {
    $fromUri = [System.Uri]::new($from.TrimEnd('\') + '\')
    $toUri   = [System.Uri]::new($to)
    $rel     = $fromUri.MakeRelativeUri($toUri).ToString()
    return $rel -replace '/', '\'
}
```

### Error handling

If symlink creation fails due to permissions:

```
Symlinks require Developer Mode (Settings → System → Developer Mode) or Administrator privileges on Windows.
```

Offer to copy the file instead, but warn the user:
> Copies break the single-source guarantee — any edit to `.ai/skills/<name>/content.md` will not propagate to copied files until the build script is re-run.

---

## Verifying existing symlinks

### macOS / Linux
```sh
# Check target of an existing symlink
readlink .claude/skills/<name>/content.md

# List all symlinks in a harness skill folder
find .claude/skills/<name> -type l
```

### Windows (PowerShell)
```powershell
# Check symlink target
(Get-Item ".claude\skills\<name>\content.md" -Force).Target

# List all symlinks in a harness skill folder
Get-ChildItem ".claude\skills\<name>" -Force | Where-Object { $_.LinkType -eq 'SymbolicLink' }
```
