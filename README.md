# Secondbrain Codex Work OS

A versioned, installable portable layer for the Secondbrain v2 working model. It lets one person use the same workflow skills and baseline rules across independent repositories and computers without making those projects part of the Secondbrain vault.

## What this owns

- `policy/PORTABLE_OPERATING_POLICY.md`: portable baseline and artifact responsibilities.
- `skills/`: reusable workflows for project initialization, startup, shutdown, and Work OS maintenance.
- `skills/web-design-selector/`: an optional web-design selection workflow and its installer.
- `templates/`: starting points for a consuming project's `AGENTS.md` and `PROJECT_STATE.md`.
- `scripts/`: opt-in local installation, update, and diagnosis helpers.

It does not replace a consuming project's `AGENTS.md`, nor does it store project state, secrets, deployment configuration, or a project's domain rules.

## Install on a computer

Clone this repository wherever you keep local tooling, then run the installer from its root.

```sh
bash scripts/install-macos-linux.sh
```

The default installs symbolic links for the four skills into `~/.agents/skills`. Existing destinations are never replaced. Use `--dry-run` to inspect work first, `--mode copy` when symlinks are unavailable, or `--target <directory>` to choose another location.

On Windows, run:

```powershell
.\scripts\install-windows.ps1
```

Use `--global-agents-target <path>` (macOS/Linux) or `-GlobalAgentsTarget <path>` (Windows) only on a fresh device where you want to create a new global `AGENTS.md`; the installer refuses to overwrite one that already exists.

## Update

After this repository has an `origin` remote, update it with:

```sh
bash scripts/update-macos-linux.sh
```

Linked skills immediately read the updated source. Run the installer again to link newly added skills. Restart Codex if a newly added skill is not listed yet.

## Add web design selection on another computer

The selector has one explicit external dependency: a local clone of VoltAgent's `awesome-design-md` library. From a fresh clone of this Work OS repository, run:

```sh
python3 skills/web-design-selector/scripts/bootstrap.py --download-library
```

This explicitly clones the design library, links `web-design-selector` into that computer's Codex skills directory, writes its library pointer, and adds or updates only the marked `web-design-selector` block in that computer's global `AGENTS.md`. It refuses to replace another skill at the same path. On Windows, run the equivalent:

```powershell
.\skills\web-design-selector\scripts\install-windows.ps1 --download-library
```

To use an existing local library instead of downloading it, pass `--design-library <path>`. After installation, start a new Codex session and ask for a new website or material UI redesign; Codex can select the skill automatically, or you can explicitly say `$web-design-selector`.

## Use with a project

Keep a project such as a course-management system in its own Git repository. Put only that project's mandatory rules in its root `AGENTS.md`, current operational truth in `PROJECT_STATE.md` when the project is active and complex, and only project-specific workflows in `.agents/skills/`.

Start with [templates/project-AGENTS.md](templates/project-AGENTS.md) and [templates/PROJECT_STATE.md](templates/PROJECT_STATE.md), adapting them rather than copying old project progress into `AGENTS.md`.

## Release discipline

Edit portable content here, validate the affected skill with the bundled Skill Creator validator, record a concise `CHANGELOG.md` entry, then tag a release after owner review. Keep package changes separate from changes to consuming projects.
