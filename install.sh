#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$REPO_DIR/skills"
TARGET="all"
SKILL="*"
LIST_ONLY=0
GLOBAL_RULES=0

usage() {
  echo "Usage: ./install.sh [--target claude|codex|all] [--skill NAME|*] [--list] [--global-rules]"
  echo "  --global-rules   Link global/user-CLAUDE.md to ~/.claude/CLAUDE.md (opt-in; backs up an existing file)"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="$2"
      shift 2
      ;;
    --skill)
      SKILL="$2"
      shift 2
      ;;
    --list)
      LIST_ONLY=1
      shift
      ;;
    --global-rules)
      GLOBAL_RULES=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

list_skills() {
  local dir description
  for dir in "$SOURCE_ROOT"/*; do
    [ -f "$dir/SKILL.md" ] || continue
    description="$(awk '/^description:/{sub(/^description:[[:space:]]*/, ""); print; exit}' "$dir/SKILL.md")"
    printf '%-24s %s\n' "$(basename "$dir")" "$description"
  done
}

if [ "$LIST_ONLY" -eq 1 ]; then
  list_skills
  exit 0
fi

case "$TARGET" in
  claude|codex|all) ;;
  *)
    echo "Invalid target: $TARGET" >&2
    usage >&2
    exit 2
    ;;
esac

CLAUDE_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
if [ -n "${CODEX_SKILLS_DIR:-}" ]; then
  CODEX_DIR="$CODEX_SKILLS_DIR"
elif [ -n "${CODEX_HOME:-}" ]; then
  CODEX_DIR="$CODEX_HOME/skills"
else
  CODEX_DIR="$HOME/.agents/skills"
fi

sources=()
if [ "$SKILL" = "*" ]; then
  for dir in "$SOURCE_ROOT"/*; do
    [ -f "$dir/SKILL.md" ] && sources+=("$dir")
  done
else
  source_dir="$SOURCE_ROOT/$SKILL"
  if [ ! -f "$source_dir/SKILL.md" ]; then
    echo "Unknown skill: $SKILL" >&2
    echo "Available skills:" >&2
    list_skills >&2
    exit 1
  fi
  sources+=("$source_dir")
fi

if [ "${#sources[@]}" -eq 0 ]; then
  echo "No skills found under $SOURCE_ROOT" >&2
  exit 1
fi

install_link() {
  local source_dir="$1"
  local target_root="$2"
  local name destination
  name="$(basename "$source_dir")"
  destination="$target_root/$name"

  mkdir -p "$target_root"

  if [ -L "$destination" ]; then
    ln -sfn "$source_dir" "$destination"
  elif [ -e "$destination" ]; then
    echo "Refusing to replace existing non-link path: $destination" >&2
    echo "Inspect or back it up, then run the installer again." >&2
    return 1
  else
    ln -s "$source_dir" "$destination"
  fi

  if [ ! -f "$destination/SKILL.md" ]; then
    echo "Verification failed: $destination/SKILL.md is not readable" >&2
    return 1
  fi

  echo "installed: $destination -> $source_dir"
}

for source_dir in "${sources[@]}"; do
  if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
    install_link "$source_dir" "$CLAUDE_DIR"
  fi
  if [ "$TARGET" = "codex" ] || [ "$TARGET" = "all" ]; then
    install_link "$source_dir" "$CODEX_DIR"
  fi
done

# Opt-in only: this replaces the user-level CLAUDE.md that every session in every
# folder loads, so it must never happen as a side effect of installing a skill.
if [ "$GLOBAL_RULES" -eq 1 ]; then
  rules_source="$REPO_DIR/global/user-CLAUDE.md"
  if [ ! -f "$rules_source" ]; then
    echo "Global rules not found: $rules_source" >&2
    exit 1
  fi
  claude_md="${CLAUDE_GLOBAL_RULES:-$HOME/.claude/CLAUDE.md}"
  mkdir -p "$(dirname "$claude_md")"
  # Skip the backup when the file is already our rules: on Windows/MSYS `ln -s` falls back
  # to a copy, so an unguarded rerun would pile up identical .bak files.
  if [ -e "$claude_md" ] && [ ! -L "$claude_md" ] && ! cmp -s "$claude_md" "$rules_source"; then
    backup="$claude_md.bak.$(date +%Y%m%d%H%M%S)"
    cp "$claude_md" "$backup"
    echo "backed up existing global rules: $backup"
  fi
  ln -sfn "$rules_source" "$claude_md"
  if [ ! -f "$claude_md" ]; then
    echo "Verification failed: $claude_md is not readable" >&2
    exit 1
  fi
  echo "installed global rules: $claude_md -> $rules_source"
fi

echo "Installation verified. Start a new agent session if the Skill is not discovered immediately."
