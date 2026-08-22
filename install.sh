#!/usr/bin/env bash
# lean-max installer — copies the skill into a repo's .claude/skills/ so it
# travels with the code (works in cloud sessions, CI, and on other machines).
#
#   ./install.sh              install into the current repo
#   ./install.sh /path/repo   install into a specific repo
#   ./install.sh --uninstall [path]
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE=install
[ "${1:-}" = "--uninstall" ] && { MODE=uninstall; shift; }
TARGET="${1:-$PWD}"
DEST="$TARGET/.claude/skills/lean-max"

if [ "$MODE" = uninstall ]; then
  [ -d "$DEST" ] && rm -rf "$DEST" && echo "removed $DEST" || echo "not installed at $TARGET"
  exit 0
fi

[ -d "$TARGET" ] || { echo "no such directory: $TARGET" >&2; exit 1; }
mkdir -p "$DEST/references"
cp "$SRC/SKILL.md" "$DEST/SKILL.md"
cp "$SRC/references/"*.md "$DEST/references/"
echo "installed lean-max -> $DEST"

# Only SKILL.md + references are needed at runtime; docs stay in the source copy.
if [ -d "$TARGET/.git" ] && ! grep -qs 'lean-max' "$TARGET/.gitignore" 2>/dev/null; then
  echo "note: $TARGET is a git repo — the skill will show as untracked."
  echo "      commit it to share with the team, or add '.claude/skills/lean-max/' to .gitignore to keep it local."
fi
