---
name: work-os-update
description: Update or diagnose an installed Secondbrain Codex Work OS package when the user asks to refresh shared skills, check an installation, or compare installed content with the package release.
---

# Work OS Update

Treat the checked-out Work OS repository as the release source and local skill locations as installed views.

1. Identify the package checkout and the requested target skills directory.
2. Run the package diagnosis helper before making changes when a target already exists.
3. Check for a clean package working tree before a Git update. Do not discard local package changes.
4. Use the package update helper only when the user authorized a network update.
5. Re-run installation only to add missing destinations; do not overwrite existing skills or global `AGENTS.md` files.

Report the release version, linked or copied skills, skipped paths, and any manual action required. Do not update consuming project rules, secrets, or runtime configuration.
