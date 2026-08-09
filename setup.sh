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

# Continuity hooks are merged into settings.json, never written over it — other
# tools' hooks live in the same file. Skipped (not fatal) when python is absent.
echo
echo "==> installing continuity hooks (SessionStart / Stop)"
# `command -v python3` is not enough on Windows: the Microsoft Store ships an
# App Execution Alias at WindowsApps/python3 that resolves but only prints
# "Python" and exits non-zero. Probe that the interpreter actually runs.
PY=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import sys" >/dev/null 2>&1; then
    PY="$cand"
    break
  fi
done
if [ -n "$PY" ]; then
  "$PY" "$REPO_DIR/hooks/install_hooks.py" "$REPO_DIR" || \
    echo "  (hook install failed — skills and rules are still installed)"
else
  echo "  (python not found — skipping hooks; skills and rules are still installed)"
fi

echo
echo "Done. Refresh later with:"
echo "  cd \"$REPO_DIR\" && git pull && ./setup.sh"
