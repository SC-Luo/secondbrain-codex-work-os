---
name: work-os-shutdown
description: Safely close or hand off an active work session by updating verified project state and identifying any explicit next action or requested Git follow-up.
---

# Work OS Shutdown

Leave the project ready for a later session or another agent without creating competing state.

- Update `PROJECT_STATE.md` with verified outcome, remaining task, blockers, next best action, and verification evidence when the project uses it.
- Create or update `HANDOFF.md` only for a real temporary transfer; record only the session delta and link back to canonical state.
- Keep durable decisions in `DECISIONS.md`, not in a handoff.
- Inspect the working tree and clearly distinguish this session's changes from pre-existing changes.

Never stage, commit, push, deploy, or alter external services unless the user explicitly asked for that action. Report the available Git follow-up rather than assuming authorization.
