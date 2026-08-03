#!/usr/bin/env bash
# One-shot entry point for a fresh machine: global rules + every skill.
#
#   git clone https://github.com/ShinKiHun/claude-skills.git ~/claude-skills
#   ~/claude-skills/setup.sh
#
# Re-run after `git pull` to refresh. Extra options are forwarded to
# install.sh, so `./setup.sh --target claude` narrows the target the same way.
#
# This is a thin wrapper: install.sh installs every skill by default, and
# --global-rules adds the always-on rules in ~/.claude/CLAUDE.md that plain
# install.sh deliberately leaves alone.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL="$REPO_DIR/install.sh"

if [ ! -f "$INSTALL" ]; then
  echo "install.sh not found next to setup.sh: $INSTALL" >&2
  exit 1
fi

echo "==> installing global rules (~/.claude/CLAUDE.md, loaded every session) + all skills"
bash "$INSTALL" --global-rules "$@"

echo
echo "Done. Refresh later with:"
echo "  cd \"$REPO_DIR\" && git pull && ./setup.sh"
