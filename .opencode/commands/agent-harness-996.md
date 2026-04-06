---
description: Execute parallel coding tasks with subagent orchestration (996 mode)
agent: build
---

Execute the 996 parallel coding workflow for the current project.

This command enables parallel task orchestration - the main agent dispatches multiple
subagents to implement features in parallel, verifies results, and updates tracking files.

**Arguments**: $ARGUMENTS (optional: --max-parallel=N, default 5)

Follow the 996 Agent workflow:
1. First load the agent-harness skill to get detailed instructions from references/996-agent.md
2. Pre-flight checks:
   - Run `pwd` to confirm current project directory
   - Read features.json to check for uncompleted sprint (status: in_progress or planning)
   - Read progress.md for recent context
   - Run `git status` to ensure clean working tree
3. If no uncompleted sprint exists, exit with message to run /agent-harness-sprint first
4. Analyze remaining features:
   - Build dependency graph to identify ready features
   - Detect file conflicts using files_affected field
   - Create execution batches respecting max parallelism
5. Dispatch subagents for parallel execution:
   - Each subagent MUST receive the CONTEXT RESET header in its prompt
   - Ensure subagents start with clean context, no assumptions from prior work
   - See references/996-agent.md for full prompt template with context isolation
6. Verify results and handle failures (mark blocked, continue others)
7. Update features.json with all feature status changes
8. Write progress.md entry summarizing orchestration results
9. Commit changes: `chore: 996 orchestration complete - N features`

CRITICAL: Always operate on files in the current project directory (pwd), NOT in the skill directory.
