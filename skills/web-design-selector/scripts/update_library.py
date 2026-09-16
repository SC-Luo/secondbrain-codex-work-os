#!/usr/bin/env python3
"""Safely fast-forward the local awesome-design-md mirror on explicit request."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


EXPECTED_HTTPS = "https://github.com/voltagent/awesome-design-md"
EXPECTED_SSH = "git@github.com:voltagent/awesome-design-md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fast-forward the design reference library.")
    parser.add_argument("--library", type=Path, help="Override the design library path.")
    parser.add_argument("--codex-home", type=Path, help="Override the Codex home directory.")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate path, origin, cleanliness, and design count without fetching.",
    )
    return parser.parse_args()


def run_git(library: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(library), "-c", "core.autocrlf=true", *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result


def normalize_remote(value: str) -> str:
    return value.strip().lower().removesuffix(".git").rstrip("/")


def resolve_library(args: argparse.Namespace) -> Path:
    if args.library:
        return args.library.expanduser().resolve()
    codex_home = (
        args.codex_home.expanduser().resolve()
        if args.codex_home
        else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    )
    pointer = codex_home / "web-design-selector" / "library-path.txt"
    if not pointer.is_file():
        raise RuntimeError(f"Library pointer is missing: {pointer}. Rerun bootstrap.py.")
    return Path(pointer.read_text(encoding="utf-8").strip()).expanduser().resolve()


def main() -> int:
    args = parse_args()
    library = resolve_library(args)
    if not (library / ".git").exists() or not (library / "design-md").is_dir():
        raise RuntimeError(f"Not a complete awesome-design-md mirror: {library}")

    remote = normalize_remote(run_git(library, "remote", "get-url", "origin").stdout)
    if remote not in {EXPECTED_HTTPS, EXPECTED_SSH}:
        raise RuntimeError(f"Unexpected origin remote; refusing to fetch: {remote}")

    status = run_git(library, "status", "--porcelain", "--untracked-files=normal").stdout
    if status.strip():
        raise RuntimeError(
            "The design library has tracked or untracked changes. Refusing to update."
        )

    before = run_git(library, "rev-parse", "HEAD").stdout.strip()
    design_count = sum(1 for _ in (library / "design-md").glob("*/DESIGN.md"))
    if design_count == 0:
        raise RuntimeError("No DESIGN.md files were found.")
    if args.check_only:
        print("library: ready for fast-forward update")
        print(f"commit: {before}")
        print(f"design files: {design_count}")
        return 0

    run_git(library, "fetch", "origin", "main")
    remote_head = run_git(library, "rev-parse", "origin/main").stdout.strip()
    if before != remote_head:
        ancestry = run_git(
            library, "merge-base", "--is-ancestor", before, remote_head, check=False
        )
        if ancestry.returncode != 0:
            raise RuntimeError("Remote main is not a fast-forward of local HEAD.")
        run_git(library, "merge", "--ff-only", "origin/main")

    after = run_git(library, "rev-parse", "HEAD").stdout.strip()
    design_count = sum(1 for _ in (library / "design-md").glob("*/DESIGN.md"))
    if design_count == 0:
        raise RuntimeError("Update completed but no DESIGN.md files were found.")

    state = "already current" if before == after else "updated"
    print(f"library: {state}")
    print(f"commit: {after}")
    print(f"design files: {design_count}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"update failed: {error}", file=sys.stderr)
        raise SystemExit(1)
