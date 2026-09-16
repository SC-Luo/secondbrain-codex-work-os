#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${HOME}/.agents/skills"
MODE="link"
DRY_RUN=false
GLOBAL_AGENTS_TARGET=""
SKILLS=(work-os-project-init work-os-start work-os-shutdown work-os-update)

usage() {
  cat <<'EOF'
Usage: bash scripts/install-macos-linux.sh [options]

Options:
  --target <directory>          Skills directory (default: ~/.agents/skills)
  --mode <link|copy>            Installation mode (default: link)
  --global-agents-target <file> Create the portable global AGENTS file only if absent
  --dry-run                     Show intended actions without changing files
  --help                        Show this help

Existing files and directories are never replaced.
EOF
}

run() {
  if "$DRY_RUN"; then
    printf 'DRY RUN: '; printf '%q ' "$@"; printf '\n'
  else
    "$@"
  fi
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target) TARGET_DIR="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --global-agents-target) GLOBAL_AGENTS_TARGET="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ "$MODE" != "link" ] && [ "$MODE" != "copy" ]; then
  printf '%s\n' '--mode must be link or copy' >&2
  exit 2
fi

run mkdir -p "$TARGET_DIR"
for skill in "${SKILLS[@]}"; do
  source_dir="$REPO_ROOT/skills/$skill"
  destination="$TARGET_DIR/$skill"
  [ -f "$source_dir/SKILL.md" ] || { printf 'Missing source skill: %s\n' "$source_dir" >&2; exit 1; }
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    if [ -L "$destination" ] && [ "$(readlink "$destination")" = "$source_dir" ]; then
      printf 'Already linked: %s\n' "$destination"
      continue
    fi
    printf 'Skipped existing destination: %s\n' "$destination" >&2
    continue
  fi
  if [ "$MODE" = "link" ]; then
    run ln -s "$source_dir" "$destination"
  else
    run cp -R "$source_dir" "$destination"
  fi
done

if [ -n "$GLOBAL_AGENTS_TARGET" ]; then
  if [ -e "$GLOBAL_AGENTS_TARGET" ] || [ -L "$GLOBAL_AGENTS_TARGET" ]; then
    printf 'Skipped existing global AGENTS target: %s\n' "$GLOBAL_AGENTS_TARGET" >&2
  else
    run mkdir -p "$(dirname "$GLOBAL_AGENTS_TARGET")"
    run cp "$REPO_ROOT/agents/GLOBAL_AGENTS.md" "$GLOBAL_AGENTS_TARGET"
  fi
fi

printf 'Work OS %s installation completed.\n' "$(tr -d '\n' < "$REPO_ROOT/VERSION")"
