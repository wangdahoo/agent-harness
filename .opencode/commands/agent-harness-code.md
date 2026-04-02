---
description: Start coding session for next feature
agent: build
---

Start a coding session to implement the next pending feature.

Follow the Coding Agent workflow:
1. First load the agent-harness skill to get detailed instructions from references/coding-agent.md
2. Run `pwd` to confirm current project directory
3. Read progress.md for recent work
4. Read features.json for current state
5. Select next pending feature (respect dependencies)
6. Implement the feature
7. Test the implementation
8. Update progress.md and features.json in the current project directory
9. Commit changes

CRITICAL: Always operate on files in the current project directory (pwd), NOT in the skill directory.
