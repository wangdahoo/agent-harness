---
description: Archive completed sprints
agent: build
---

Archive completed sprints to .agent-harness/archived/

IMPORTANT: Scripts are located in the skill directory, not the project directory.
Use `find ~ -path "*/agent-harness/scripts/archive_sprint.py" -not -path "*/archived/*" 2>/dev/null | head -1` to locate the script.

Steps:
1. Run `python3 <SCRIPT_PATH> --list --project-dir "$(pwd)"` to show completed sprints
2. Ask user for confirmation
3. Run `python3 <SCRIPT_PATH> --project-dir "$(pwd)"` to archive
4. Confirm successful archive
