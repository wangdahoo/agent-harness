# 996 Agent Reference

Parallel task orchestration mode for executing multiple coding tasks concurrently.

## Table of Contents
1. [Overview](#overview)
2. [Pre-flight Checks](#pre-flight-checks)
3. [Analysis Phase](#analysis-phase)
4. [Dispatch Phase](#dispatch-phase)
5. [Verification Phase](#verification-phase)
6. [State Update Phase](#state-update-phase)
7. [Error Handling](#error-handling)
8. [Examples](#examples)

## Overview

The 996 mode enables parallel execution of coding tasks by:
- Analyzing dependencies and file conflicts
- Dispatching multiple subagents to implement features concurrently
- Verifying results and updating tracking files
- Continuing execution even when individual tasks fail

**Key Constraints:**
- Maximum 3-5 concurrent subagents (configurable via --max-parallel)
- Features with file conflicts run sequentially
- Failed features marked as `blocked`, others continue

## Pre-flight Checks

Perform these checks in order before starting orchestration:

### 1. Confirm Location
```bash
python3 scripts/resolve_project_dir.py
```
Store the output as the absolute project directory. Use it for all reads/writes of `features.json` and `progress.md`.

### 2. Check for Uncompleted Sprint
Read `features.json` and look for:
- Sprint with status `in_progress` or `planning`
- Features with status `pending` or `blocked`

If no uncompleted sprint exists, exit with:
```
No uncompleted sprint found. Run /agent-harness-sprint first to plan a sprint.
```

### 3. Review Recent Context
Read `progress.md` to understand:
- Recent work completed
- Any blockers or issues
- Current project state

### 4. Verify Clean Working Tree
```bash
git status
```
If there are uncommitted changes, exit with:
```
Working tree has uncommitted changes. Please commit or stash before running 996 mode.
```

## Analysis Phase

### Step 1: Build Dependency Graph

For each pending/blocked feature, check if all dependencies are satisfied:

```python
def get_ready_features(features):
    """Get features whose dependencies are all completed."""
    completed_ids = {f["id"] for f in features if f["status"] == "completed"}

    ready = []
    for f in features:
        if f["status"] in ("pending", "blocked"):
            deps = set(f.get("dependencies", []))
            if deps.issubset(completed_ids):
                ready.append(f)

    return ready
```

### Step 2: Detect File Conflicts

Group features by file overlap. Features modifying the same files cannot run in parallel:

```python
def build_parallel_batches(features, max_parallel=5):
    """
    Group features into batches respecting file conflicts.

    Features in the same batch can run in parallel (no file overlap).
    Batches run sequentially.
    """
    batches = []
    remaining = features.copy()

    while remaining:
        batch = []
        files_in_use = set()

        for f in remaining:
            if len(batch) >= max_parallel:
                break

            # Check file conflict
            f_files = set(f.get("files_affected", []))
            if not f_files & files_in_use:  # No overlap
                batch.append(f)
                files_in_use |= f_files

        if not batch:
            # Force add one to avoid deadlock (circular file conflicts)
            batch = [remaining[0]]
            files_in_use = set(remaining[0].get("files_affected", []))

        batches.append(batch)
        for f in batch:
            remaining.remove(f)

    return batches
```

### Step 3: Output Execution Plan

Display the execution plan to the user:

```
996 Execution Plan
==================
Total ready features: 8
Max parallelism: 5

Batch 1 (parallel):
  - s1-feat-002: Add login page (files: src/auth/login.ts)
  - s1-feat-003: Add signup page (files: src/auth/signup.ts)
  - s1-feat-004: Add API client (files: src/api/client.ts)

Batch 2 (parallel):
  - s1-feat-005: Connect login to API (files: src/auth/login.ts, src/api/client.ts)
  - s1-feat-006: Add dashboard (files: src/pages/dashboard.tsx)

Batch 3 (parallel):
  - s1-feat-007: Dashboard auth check (files: src/pages/dashboard.tsx, src/auth/)
```

## Dispatch Phase

### Subagent Prompt Template

For each feature, spawn a subagent with this prompt structure:

```
Implement ONE feature for this project.

## CONTEXT RESET - READ THIS FIRST
This is an isolated task. You MUST:
1. DISREGARD any context from previous conversations or tasks
2. NOT assume any prior knowledge about the project state
3. Read all necessary files fresh to understand current state
4. Start with a clean mental state - this is your ONLY task

## Feature Details
- **ID**: <feature_id>
- **Title**: <title>
- **Description**: <description>
- **Acceptance Criteria**:
  <criteria_list>
- **Technical Notes**: <technical_notes>
- **Files to Modify**: <files_affected>

## Your Task
1. Read features.json and progress.md to understand project context
2. Implement the feature following the coding-agent.md guidelines
3. Test all acceptance criteria
4. Run lint/build to verify no breakage
5. Commit your changes with message: feat(<scope>): <brief description> (Feature: <feature_id>)

## Critical Rules
- Do NOT modify features.json or progress.md - the orchestrator will update these
- Focus ONLY on this feature - do not modify unrelated code
- Ensure the codebase remains in a working state
- Signal completion by stating "FEATURE COMPLETE: <feature_id>" at the end
- If you cannot complete the feature, state "FEATURE BLOCKED: <feature_id> - <reason>"
```

### Spawning Subagents

Use the Agent tool to spawn subagents:

```json
{
  "subagent_type": "general-purpose",
  "description": "Implement feature <id>",
  "prompt": "<full prompt from template above>",
  "run_in_background": true
}
```

### Monitoring Execution

For each batch:
1. Spawn all subagents in the batch as background tasks
2. Wait for all subagents to complete using TaskOutput
3. Collect results (success/failure) for each feature
4. Proceed to verification phase

## Verification Phase

For each completed subagent:

### 1. Check Completion Signal
- Look for "FEATURE COMPLETE: <id>" in subagent output
- If "FEATURE BLOCKED: <id>" found, mark as blocked with reason

### 2. Verify Code Quality
```bash
# Run project-specific lint command
<lint_command>

# Run project-specific build command
<build_command>
```

### 3. Verify Acceptance Criteria
Review the implementation against each acceptance criterion:
- [ ] Criterion 1: <status>
- [ ] Criterion 2: <status>
- ...

### 4. Record Result
```python
results = {
    "feature_id": {
        "status": "completed" | "blocked",
        "reason": None | "<failure_reason>",
        "files_changed": ["list", "of", "files"]
    }
}
```

## State Update Phase

### 1. Update features.json

For each feature result:
- If completed: Set `status: "completed"`
- If blocked: Set `status: "blocked"` and add `blocked_reason` field

```json
{
  "id": "s1-feat-003",
  "status": "completed"
}
```

```json
{
  "id": "s1-feat-004",
  "status": "blocked",
  "blocked_reason": "Lint errors in implementation"
}
```

### 2. Write progress.md Entry

Add entry at the **top** of the sessions section:

```markdown
## 996 Orchestration - YYYY-MM-DD
**Agent**: 996 Orchestrator
**Sprint**: [Sprint ID]
**Max Parallelism**: [N]

### Execution Summary
| Feature | Status | Result |
|---------|--------|--------|
| s1-feat-002 | completed | success |
| s1-feat-003 | completed | success |
| s1-feat-004 | blocked | lint errors in src/api/client.ts |

### Statistics
- Total features: 8
- Completed: 6
- Blocked: 2
- Success rate: 75%

### Blocked Features Detail
- **s1-feat-004**: Lint errors in src/api/client.ts - needs manual review
- **s1-feat-007**: Dependency on s1-feat-004 not satisfied

### Files Changed
- src/auth/login.ts - Added login form component
- src/auth/signup.ts - Added signup form component
- src/api/client.ts - API client implementation (has lint errors)
- src/pages/dashboard.tsx - Dashboard page with auth check

### Next Steps
- Review and fix blocked features manually
- Run /agent-harness code to address remaining issues
```

### 3. Final Commit
```bash
git add features.json progress.md
git commit -m "chore: 996 orchestration complete - 6/8 features completed"
```

## Error Handling

### Subagent Failure

When a subagent fails or signals blocked:

1. **Record the failure**:
   ```python
   results[feature_id] = {
       "status": "blocked",
       "reason": "<reason from subagent or verification>"
   }
   ```

2. **Continue execution**: Do not stop other subagents or batches

3. **Document in progress.md**: Include failure reason in the summary

### Merge Conflicts

If two features somehow conflict despite file coordination:

1. **Detect**: Build/lint failures after multiple features
2. **Isolate**: Check recent commits to identify conflicting features
3. **Revert one**: `git revert <commit_hash>`
4. **Mark blocked**: Update feature status and reason

### Catastrophic Failure

If multiple features fail and codebase is in bad state:

1. **Stop orchestration**: Do not dispatch more subagents
2. **Assess damage**: Run full test suite and build
3. **Rollback if needed**:
   ```bash
   git reset --hard HEAD~N  # Rollback N commits
   ```
4. **Document**: Update progress.md with failure analysis
5. **Recommend**: Suggest manual intervention or single-feature mode

## Examples

### Example 1: Simple Parallel Execution

**features.json state:**
```json
{
  "sprints": [{
    "id": "s1",
    "status": "in_progress",
    "features": [
      {"id": "s1-feat-001", "status": "completed"},
      {"id": "s1-feat-002", "status": "pending", "dependencies": [], "files_affected": ["src/a.ts"]},
      {"id": "s1-feat-003", "status": "pending", "dependencies": [], "files_affected": ["src/b.ts"]},
      {"id": "s1-feat-004", "status": "pending", "dependencies": [], "files_affected": ["src/c.ts"]}
    ]
  }]
}
```

**Execution:**
- All 3 features have no dependencies
- No file conflicts (different files)
- All run in parallel in Batch 1

### Example 2: Dependency Chain

**features.json state:**
```json
{
  "features": [
    {"id": "f1", "status": "completed"},
    {"id": "f2", "status": "pending", "dependencies": ["f1"]},
    {"id": "f3", "status": "pending", "dependencies": ["f1"]},
    {"id": "f4", "status": "pending", "dependencies": ["f2", "f3"]}
  ]
}
```

**Execution:**
- Batch 1: f2, f3 (both depend only on completed f1)
- Batch 2: f4 (depends on f2, f3 from Batch 1)

### Example 3: File Conflict

**features.json state:**
```json
{
  "features": [
    {"id": "f1", "status": "pending", "dependencies": [], "files_affected": ["src/auth.ts", "src/api.ts"]},
    {"id": "f2", "status": "pending", "dependencies": [], "files_affected": ["src/api.ts", "src/utils.ts"]},
    {"id": "f3", "status": "pending", "dependencies": [], "files_affected": ["src/pages.ts"]}
  ]
}
```

**Execution:**
- f1 and f2 both modify src/api.ts → conflict
- Batch 1: f1, f3 (no conflict between them)
- Batch 2: f2 (waits for f1 to finish)

## Quality Checklist

### Before Starting Orchestration
- [ ] Confirmed project directory with pwd
- [ ] Found uncompleted sprint in features.json
- [ ] Clean working tree (no uncommitted changes)
- [ ] Read progress.md for context

### After Each Batch
- [ ] All subagents completed (or timed out)
- [ ] Collected results for each feature
- [ ] Verified lint/build passes

### After Orchestration Complete
- [ ] Updated features.json with all status changes
- [ ] Written comprehensive progress.md entry
- [ ] Committed all tracking file changes
- [ ] Codebase in working state (lint/build pass)

## Critical Rules

1. **Continue on Failure** - Blocked features don't stop other features
2. **Respect File Conflicts** - Features modifying same files run sequentially
3. **Max Parallelism** - Never exceed 5 concurrent subagents
4. **Orchestrator Updates State** - Subagents don't modify features.json or progress.md
5. **Clean State Required** - Only run 996 on clean working tree
6. **Verify Each Feature** - Run lint/build after each batch
7. **Context Isolation** - Every subagent MUST receive CONTEXT RESET header to ensure clean mental state
