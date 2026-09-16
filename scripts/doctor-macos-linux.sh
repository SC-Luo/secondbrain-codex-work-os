#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${HOME}/.agents/skills"
SKILLS=(work-os-project-init work-os-start work-os-shutdown work-os-update)

if [ "${1:-}" = "--target" ] && [ -n "${2:-}" ]; then
  TARGET_DIR="$2"
elif [ "${1:-}" = "--help" ]; then
  printf 'Usage: bash scripts/doctor-macos-linux.sh [--target <directory>]\n'
  exit 0
elif [ "$#" -gt 0 ]; then
  printf 'Usage: bash scripts/doctor-macos-linux.sh [--target <directory>]\n' >&2
  exit 2
fi

status=0
printf 'Secondbrain Codex Work OS %s\n' "$(tr -d '\n' < "$REPO_ROOT/VERSION")"
for skill in "${SKILLS[@]}"; do
  destination="$TARGET_DIR/$skill"
  if [ -L "$destination" ]; then
    printf 'LINKED  %s -> %s\n' "$skill" "$(readlink "$destination")"
  elif [ -f "$destination/SKILL.md" ]; then
    printf 'COPIED  %s\n' "$skill"
  else
    printf 'MISSING %s\n' "$skill" >&2
    status=1
  fi
done
exit "$status"
