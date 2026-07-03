#!/bin/bash
# claude-skills 설치: repo 안의 각 스킬 폴더를 ~/.claude/skills/ 에 symlink
set -e
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"
for d in "$REPO_DIR"/*/; do
    name=$(basename "$d")
    [ -f "$d/SKILL.md" ] || continue
    ln -sfn "$d" "$SKILLS_DIR/${name%/}"
    echo "linked: $SKILLS_DIR/${name%/} -> $d"
done
echo "완료. Claude Code 새 세션부터 사용 가능."
