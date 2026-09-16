---
name: work-os-project-init
description: Initialize or migrate a project into the portable Work OS model when the user asks to set up a project, repair legacy agent guidance, or establish a Codex-friendly project entry.
---

# Work OS Project Init

Create the smallest project contract that makes the requested work safe to continue. Inspect the target root and its existing entry files before proposing changes.

- For an active complex project, use `README.md` for durable context and `PROJECT_STATE.md` as the only current operational truth.
- Create `DECISIONS.md`, `HANDOFF.md`, project memory, or extra directories only when their actual trigger exists.
- Keep `AGENTS.md` limited to project-specific mandatory rules: verification, safety, runtime, permission, and domain constraints.
- For a legacy project, migrate on touch. Do not bulk rename, archive, or replace unclear existing artifacts.
- If two files compete for the same authority, report the conflict before creating another file.

Before changing files, state the target root, scope, existing authorities, acceptance criteria, and anything needing an owner decision. Verify that all created artifacts have distinct responsibilities.
