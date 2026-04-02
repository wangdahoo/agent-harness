---
description: Create or update sprint with feature breakdown
agent: build
---

Create or update sprint for the current agent-harness project.

Requirements: $ARGUMENTS

Follow the Sprint Agent workflow:
1. First load the agent-harness skill to get detailed instructions from references/sprint-agent.md
2. Read features.json and progress.md from the current project directory (use `pwd` to confirm)
3. If requirements provided, analyze and break into atomic features
4. Define acceptance criteria for each feature
5. Order by dependencies
6. Update features.json and progress.md in the current project directory

CRITICAL: Always operate on files in the current project directory (pwd), NOT in the skill directory.
CRITICAL: Always run `python3 scripts/validate_structure.py --project-dir "$(pwd)"` after updating features.json.
Use `find ~ -path "*/agent-harness/scripts/validate_structure.py" -not -path "*/archived/*" 2>/dev/null | head -1` to locate the script.
