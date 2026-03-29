---
description: Archive completed sprints
agent: build
---

Archive completed sprints to .agent-harness/archived/

Steps:
1. Run `python3 scripts/archive_sprint.py --list` to show completed sprints
2. Ask user for confirmation
3. Run `python3 scripts/archive_sprint.py` to archive
4. Confirm successful archive
