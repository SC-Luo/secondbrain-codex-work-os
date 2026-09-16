#!/usr/bin/env python3
"""Install the web-design-selector runtime link and global Codex trigger."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


SKILL_NAME = "web-design-selector"
DESIGN_LIBRARY_REPOSITORY = "https://github.com/VoltAgent/awesome-design-md.git"
START_MARKER = "<!-- web-design-selector:start -->"
END_MARKER = "<!-- web-design-selector:end -->"
GLOBAL_RULE = f"""{START_MARKER}
Before creating a new webpage, website, landing page, dashboard, portal, web app UI, or materially redesigning one, invoke `$web-design-selector` and follow its selection workflow. Reuse an established project `DESIGN.md` for routine edits. Explicit user instructions and project-owned brand or design systems take precedence.
{END_MARKER}"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the web-design-selector skill for the current user."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        help="Override the Codex home directory for validation or testing.",
    )
    parser.add_argument(
        "--design-library",
        type=Path,
        help="Use this existing design-library checkout, or create it here with --download-library.",
    )
    parser.add_argument(
        "--download-library",
        action="store_true",
        help="Clone VoltAgent/awesome-design-md when no complete design library is available.",
    )
    return parser.parse_args()


def find_vault_library(skill_source: Path) -> Path | None:
    for candidate in (skill_source, *skill_source.parents):
        library = candidate / "10-專案" / "awesome-design-md"
        if (library / "README.md").is_file() and (library / "design-md").is_dir():
            return library
    return None


def is_complete_library(library: Path) -> bool:
    return (
        (library / "README.md").is_file()
        and (library / "design-md").is_dir()
        and (library / ".git").exists()
    )


def clone_library(library: Path) -> Path:
    if library.exists():
        raise RuntimeError(f"Design library path already exists but is incomplete: {library}")
    library.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", DESIGN_LIBRARY_REPOSITORY, str(library)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Unable to clone the design library: {detail}")
    return library


def resolve_library(args: argparse.Namespace, skill_source: Path, codex_home: Path) -> Path:
    library = (
        args.design_library.expanduser().resolve()
        if args.design_library
        else find_vault_library(skill_source)
    )
    if library and is_complete_library(library):
        return library
    if args.download_library:
        target = library or (codex_home / SKILL_NAME / "awesome-design-md")
        return clone_library(target)
    if library:
        raise RuntimeError(f"Design library is incomplete: {library}")
    raise RuntimeError(
        "Cannot locate a design library. Re-run with --download-library, "
        "or provide --design-library <path>."
    )


def patch_global_agents(path: Path) -> str:
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    has_start = START_MARKER in content
    has_end = END_MARKER in content
    if has_start != has_end:
        raise RuntimeError(
            f"Refusing to edit {path}: only one web-design-selector marker exists."
        )
    if has_start:
        before, remainder = content.split(START_MARKER, 1)
        _, after = remainder.split(END_MARKER, 1)
        updated = before.rstrip() + "\n\n" + GLOBAL_RULE + after
        action = "updated"
    else:
        prefix = content.rstrip()
        updated = (prefix + "\n\n" if prefix else "") + GLOBAL_RULE + "\n"
        action = "added"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(updated, encoding="utf-8")
    return action


def paths_are_same(left: Path, right: Path) -> bool:
    try:
        return os.path.samefile(left, right)
    except (FileNotFoundError, OSError):
        return left.resolve(strict=False) == right.resolve(strict=False)


def install_runtime(skill_source: Path, target: Path) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if paths_are_same(target, skill_source):
            return "already linked"
        marker = target / ".web-design-selector-runtime-copy"
        if target.is_dir() and marker.is_file():
            recorded_source = marker.read_text(encoding="utf-8").strip()
            if Path(recorded_source).resolve(strict=False) != skill_source.resolve():
                raise RuntimeError(f"Runtime copy at {target} belongs to another source.")
            shutil.copytree(skill_source, target, dirs_exist_ok=True)
            marker.write_text(str(skill_source) + "\n", encoding="utf-8")
            return "refreshed fallback copy"
        raise RuntimeError(
            f"Refusing to replace existing skill path {target}. Move it manually and rerun."
        )

    if os.name == "nt":
        junction = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(skill_source)],
            text=True,
            capture_output=True,
            check=False,
        )
        if junction.returncode == 0:
            return "created junction"
        shutil.copytree(skill_source, target)
        (target / ".web-design-selector-runtime-copy").write_text(
            str(skill_source) + "\n", encoding="utf-8"
        )
        return "created fallback copy"

    target.symlink_to(skill_source, target_is_directory=True)
    return "created symlink"


def configure_line_endings(library: Path) -> None:
    if os.name != "nt":
        return
    result = subprocess.run(
        ["git", "-C", str(library), "config", "--local", "core.autocrlf", "true"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Unable to configure Git line endings: {detail}")


def main() -> int:
    args = parse_args()
    skill_source = Path(__file__).resolve().parent.parent
    codex_home = (
        args.codex_home.expanduser().resolve()
        if args.codex_home
        else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    )
    library = resolve_library(args, skill_source, codex_home)
    design_count = sum(1 for _ in (library / "design-md").glob("*/DESIGN.md"))
    if design_count == 0:
        raise RuntimeError(f"Design library is incomplete: {library}")
    runtime_target = codex_home / "skills" / SKILL_NAME
    pointer = codex_home / SKILL_NAME / "library-path.txt"

    install_action = install_runtime(skill_source, runtime_target)
    pointer.parent.mkdir(parents=True, exist_ok=True)
    pointer.write_text(str(library.resolve()) + "\n", encoding="utf-8")
    agents_action = patch_global_agents(codex_home / "AGENTS.md")
    configure_line_endings(library)

    print(f"skill: {install_action}: {runtime_target}")
    print(f"library: {library} ({design_count} DESIGN.md files)")
    print(f"pointer: {pointer}")
    print(f"global AGENTS rule: {agents_action}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"bootstrap failed: {error}", file=sys.stderr)
        raise SystemExit(1)
