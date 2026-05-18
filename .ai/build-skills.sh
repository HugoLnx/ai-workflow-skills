#!/usr/bin/env bash
# build-skills.sh — Build all harness SKILL.md files from .ai/skills/ source of truth.
# Idempotent: safe to run multiple times.
# Writes only to: .claude/skills/ .agents/skills/ .cursor/skills/ .github/skills/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

HARNESSES=(claude codex cursor copilot)
declare -A HARNESS_DIRS=(
  [claude]=".claude/skills"
  [codex]=".agents/skills"
  [cursor]=".cursor/skills"
  [copilot]=".github/skills"
)

skills_processed=0
skill_mds_written=0
symlinks_created=0
symlinks_verified=0
errors=0

create_or_verify_symlink() {
  local link="$1"
  local target="$2"

  if [ -L "$link" ]; then
    local current_target
    current_target="$(readlink "$link")"
    if [ "$current_target" = "$target" ]; then
      symlinks_verified=$((symlinks_verified + 1))
    else
      ln -sf "$target" "$link"
      symlinks_created=$((symlinks_created + 1))
    fi
  elif [ -e "$link" ]; then
    echo "ERROR: $link exists but is not a symlink — skipping" >&2
    errors=$((errors + 1))
  else
    ln -s "$target" "$link"
    symlinks_created=$((symlinks_created + 1))
  fi
}

write_if_changed() {
  local path="$1"
  local content="$2"

  if [ -f "$path" ] && [ "$(cat "$path")" = "$content" ]; then
    return 0
  fi
  printf '%s' "$content" > "$path"
  skill_mds_written=$((skill_mds_written + 1))
}

if [ ! -d "$SKILLS_SRC" ]; then
  echo "ERROR: $SKILLS_SRC does not exist. Nothing to build." >&2
  exit 1
fi

for skill_dir in "$SKILLS_SRC"/*/; do
  [ -d "$skill_dir" ] || continue

  skill_name="$(basename "$skill_dir")"
  content_src="$skill_dir/content.md"

  if [ ! -f "$content_src" ]; then
    echo "ERROR: $skill_dir/content.md missing — skipping skill '$skill_name'" >&2
    errors=$((errors + 1))
    continue
  fi

  for harness in "${HARNESSES[@]}"; do
    yaml_src="$skill_dir/${harness}.yaml"

    if [ ! -f "$yaml_src" ]; then
      echo "ERROR: $yaml_src missing — skipping harness '$harness' for skill '$skill_name'" >&2
      errors=$((errors + 1))
      continue
    fi

    target_base="$REPO_ROOT/${HARNESS_DIRS[$harness]}/$skill_name"
    mkdir -p "$target_base"

    # Symlink content.md using relative path
    rel_content="$(realpath --relative-to="$target_base" "$content_src")"
    create_or_verify_symlink "$target_base/content.md" "$rel_content"

    # Symlink any other files/dirs (excluding .yaml files)
    for item in "$skill_dir"/*; do
      item_name="$(basename "$item")"
      # Skip .yaml files and content.md (already handled)
      case "$item_name" in
        *.yaml|content.md) continue ;;
      esac
      rel_item="$(realpath --relative-to="$target_base" "$item")"
      create_or_verify_symlink "$target_base/$item_name" "$rel_item"
    done

    # Build SKILL.md content: frontmatter + blank line + @content.md
    frontmatter="$(cat "$yaml_src")"
    skill_md_content="---
${frontmatter}---

@content.md
"

    write_if_changed "$target_base/SKILL.md" "$skill_md_content"
  done

  skills_processed=$((skills_processed + 1))
done

echo ""
echo "build-skills complete"
echo "  Skills processed : $skills_processed"
echo "  SKILL.md written : $skill_mds_written"
echo "  Symlinks created : $symlinks_created"
echo "  Symlinks verified: $symlinks_verified"
if [ "$errors" -gt 0 ]; then
  echo "  Errors           : $errors (see above)"
  exit 1
fi
