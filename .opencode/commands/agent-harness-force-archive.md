---
description: Force archive ALL sprints including incomplete
agent: build
---

Force archive ALL sprints, including incomplete ones.

**Warning:** This will archive all sprints regardless of status.

Steps:
1. Run `python3 scripts/archive_sprint.py --list` to show all sprints
2. Show warning that ALL sprints will be archived
3. Ask user for explicit confirmation
4. If confirmed, run `python3 scripts/archive_sprint.py --force`
5. Confirm successful archive
