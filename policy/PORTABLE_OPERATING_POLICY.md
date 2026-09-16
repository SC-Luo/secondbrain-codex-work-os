---
title: Portable Work OS Policy
scope: cross-project
status: active
version: 0.1.0
---

# Portable Work OS Policy

This policy governs reusable behavior distributed by this repository. A consuming repository's explicit rules, security boundaries, and owner instructions take precedence.

## Canonical responsibilities

Use one owner for each kind of information:

- `AGENTS.md`: durable mandatory behavior for the repository or directory.
- `PROJECT_STATE.md`: current operational truth for an active complex project.
- `DECISIONS.md`: durable human, business, or architecture decisions.
- `HANDOFF.md`: a temporary transfer delta, never a second project-state file.
- `SKILL.md`: a verified repeatable executable procedure.

Do not put session history, changing task progress, or one-off workarounds into `AGENTS.md`.

## Context and execution

Load context progressively: applicable instructions, project state, only the references needed for the task, then raw history only if an evidence gap remains. For a small, reversible task, execute directly. Plan first for architecture, migration, multi-system, irreversible, or externally consequential work.

Before modifying existing files, preserve unrelated work, confirm the exact target, and verify the current content is still the content you assessed. Do not stage, commit, push, deploy, or modify external systems unless the owner asked for that action.

## Learning boundary

Promote a lesson only after its cause, correction, verification, and reusability are understood. A recurring mandatory behavior belongs in `AGENTS.md`; a verified repeatable procedure belongs in a skill. A single workaround is neither by default.

## Package boundary

This package provides a portable baseline. It must not become a second source of truth for a project's state, secrets, product decisions, or runtime configuration.
