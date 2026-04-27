---
description: Create or update sprint with feature breakdown
agent: build
---

Create or update sprint for the current agent-harness project.

Requirements: $ARGUMENTS

Follow the Sprint Agent workflow:
1. First load the agent-harness skill to get detailed instructions from references/sprint-agent.md
2. Resolve project directory: run `python3 <SCRIPT_PATH>/resolve_project_dir.py`, store output as PROJECT_DIR. All reads/writes of features.json and progress.md MUST use this absolute path.
3. Read features.json and progress.md from PROJECT_DIR
4. If requirements provided, analyze and break into atomic features
5. Define acceptance criteria for each feature
6. Order by dependencies
7. Write features.json and progress.md to PROJECT_DIR

CRITICAL: Before any file operation, run `python3 scripts/resolve_project_dir.py` to get the correct project directory. Never guess or use bare relative paths.
CRITICAL: Always run `python3 scripts/validate_structure.py --project-dir "$PROJECT_DIR"` after updating features.json.
Use `find ~ -path "*/agent-harness/scripts/resolve_project_dir.py" -not -path "*/archived/*" 2>/dev/null | head -1` to locate the script.
CRITICAL: After all changes, commit with: `git add features.json progress.md && git commit -m "sprint: plan sprint features"`
