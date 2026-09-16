#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${HOME}/.agents/skills"

if [ "${1:-}" = "--target" ] && [ -n "${2:-}" ]; then
  TARGET_DIR="$2"
elif [ "${1:-}" = "--help" ]; then
  printf 'Usage: bash scripts/update-macos-linux.sh [--target <directory>]\n'
  exit 0
elif [ "$#" -gt 0 ]; then
  printf 'Usage: bash scripts/update-macos-linux.sh [--target <directory>]\n' >&2
  exit 2
fi

if [ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]; then
  printf '%s\n' 'Refusing to update: the package checkout has uncommitted changes.' >&2
  exit 1
fi
if ! git -C "$REPO_ROOT" remote get-url origin >/dev/null 2>&1; then
  printf '%s\n' 'Refusing to update: no origin remote is configured for this package.' >&2
  exit 1
fi
git -C "$REPO_ROOT" pull --ff-only
bash "$SCRIPT_DIR/install-macos-linux.sh" --target "$TARGET_DIR"
