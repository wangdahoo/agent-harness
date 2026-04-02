---
description: Initialize new agent-harness project
agent: build
---

Initialize a new agent-harness project with name: $ARGUMENTS

IMPORTANT: Scripts are located in the skill directory, not the project directory.
Use `find ~ -path "*/agent-harness/scripts/init_project.py" -not -path "*/archived/*" 2>/dev/null | head -1` to locate the script.

Steps:
1. Find the script path, then run: `python3 <SCRIPT_PATH> "$ARGUMENTS" --project-dir "$(pwd)"`
2. Confirm files were created successfully in the current project directory
3. Suggest next step: run `/agent-harness-sprint` to plan features
