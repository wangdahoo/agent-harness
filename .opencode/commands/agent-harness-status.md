---
description: Show current project status
agent: build
---

Show the current agent-harness project status.

IMPORTANT: Scripts are located in the skill directory, not the project directory.
Use `find ~ -path "*/agent-harness/scripts/status.py" -not -path "*/archived/*" 2>/dev/null | head -1` to locate the script.

Run `python3 <SCRIPT_PATH> --project-dir "$(pwd)"` and display:
- Current sprint and goal
- Feature completion statistics
- Next recommended feature
- Any blocked features
