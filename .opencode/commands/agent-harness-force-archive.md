---
description: Force archive ALL sprints including incomplete
agent: build
---

Force archive ALL sprints, including incomplete ones.

**Warning:** This will archive all sprints regardless of status.

IMPORTANT: Scripts are located in the skill directory, not the project directory.
Use `find ~ -path "*/agent-harness/scripts/archive_sprint.py" -not -path "*/archived/*" 2>/dev/null | head -1` to locate the script.

Steps:
1. Run `python3 <SCRIPT_PATH> --list --force --project-dir "$(pwd)"` to show all sprints
2. Show warning that ALL sprints will be archived
3. Ask user for explicit confirmation
4. If confirmed, run `python3 <SCRIPT_PATH> --force --project-dir "$(pwd)"`
5. Commit changes: `git add -A && git commit -m "chore: force archive all sprints"`
6. Confirm successful archive
