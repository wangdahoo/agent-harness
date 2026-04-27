---
description: Start coding session for next feature
agent: build
---

Start a coding session to implement the next pending feature.

Follow the Coding Agent workflow:
1. First load the agent-harness skill to get detailed instructions from references/coding-agent.md
2. Resolve project directory: run `python3 scripts/resolve_project_dir.py`, store output as PROJECT_DIR. Use this absolute path for all file operations.
3. Read progress.md and features.json from PROJECT_DIR
4. Select next pending feature (respect dependencies)
5. Implement the feature
6. Test the implementation
7. Update progress.md and features.json in PROJECT_DIR
8. Commit: `git add -A && git commit -m "feat(<scope>): <description>"`

CRITICAL: Run `python3 scripts/resolve_project_dir.py` to get the correct project directory. Never use bare relative paths for features.json or progress.md.
