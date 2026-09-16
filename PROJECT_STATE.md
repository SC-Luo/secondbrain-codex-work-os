---
title: Secondbrain Codex Work OS State
status: active
updated: 2026-09-16
---

# Project State

## Project Goal

Provide a versioned portable Work OS that can be safely installed on multiple computers and used by independent projects.

## Current Outcome

Local 0.2.0 package adds portable web-design selection and is ready for a release-location decision.

## Current Phase

Ready for release-location decision.

## Current Task

Complete GitHub sign-in, create the approved private remote, and push the initial release.

## Confirmed

- The package will use the Codex-compatible `~/.agents/skills` user scope.
- Existing global `AGENTS.md` files must never be overwritten.
- Consuming projects remain independent repositories.
- The macOS/Linux installer creates links in a temporary target and skips existing destinations.
- This Mac has the four release skills linked in its user-level skills directory.
- The existing web-design-selector source is now owned by this package; its prior Secondbrain path is a compatibility link.
- A fresh computer can bootstrap the selector with either an existing design library or an explicit library download.
- The initial commit contains only the 27 Work OS package files.

## Inferred

- A private Git remote will be the appropriate later distribution channel.

## Unknown

- The final GitHub repository URL, pending account sign-in and creation.

## Blockers

- None for local package creation.

## Human Decisions

- Create and publish a private GitHub repository named `secondbrain-codex-work-os`.

## Next Best Action

After GitHub sign-in, create the private remote, add `origin`, push `main`, and record the resulting URL.

## Verification

- Shell syntax passed for all macOS/Linux scripts.
- Temporary-target dry-run, link installation, global-agent creation, doctor, and no-overwrite checks passed.
- Real user-level link installation and doctor check passed without creating a global `AGENTS.md`.
- All four skills passed frontmatter and placeholder checks.
- The bundled Skill Creator validator could not run because this environment lacks the `yaml` Python module.
- Windows PowerShell scripts were not executed because PowerShell is unavailable on this host.
- The selector passed isolated bootstrap, pointer, global-rule, source-resolution, Python syntax, and design-library health checks.
- Initial Git commit passed `git diff --cached --check` before commit.

## Canonical References

- `policy/PORTABLE_OPERATING_POLICY.md`
- `AGENTS.md`
- `VERSION`
