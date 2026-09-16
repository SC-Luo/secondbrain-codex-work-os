# Secondbrain Codex Work OS

## Scope

- This repository is the versioned distribution source for portable Work OS policy, templates, and skills.
- It does not own any consuming project's current state, decisions, secrets, runtime configuration, or deployment rules.

## Mandatory constraints

- Keep one canonical source for each portable policy, template, and skill. Do not duplicate a skill under a second name merely for compatibility.
- Install and update scripts must be opt-in, must not overwrite an existing destination, and must never transmit or store credentials.
- Test installers only against a temporary target, never a real user skills or Codex configuration directory.
- Do not publish, create a remote, stage, commit, or push without explicit owner instruction.
