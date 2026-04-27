# Coding Agent Reference

## Table of Contents
1. [Session Protocol](#session-protocol)
2. [Implementation Process](#implementation-process)
3. [File Schemas](#file-schemas)
4. [Testing Requirements](#testing-requirements)
5. [Examples](#examples)

## Session Protocol

### Start of Session

**Always perform in order:**

1. **Confirm Location**
   ```bash
   pwd
   ```

2. **Review Recent Work**
   ```bash
   git log --oneline -10
   ```
   Read `progress.md` to understand previous sessions. This step is mandatory — it provides the context from prior sessions that enables continuity across context windows.

3. **Review Feature Status**
   Read `features.json` to see:
   - Current sprint status
   - Completed features
   - In-progress features
   - Pending features
   - Dependencies

4. **Verify Project State**
   Run lint and build commands (see project's AGENTS.md).

   **⚠️ If broken, fix existing issues before starting new work.**

### End of Session

**Always perform:**

1. Update `progress.md` with session summary
2. Update `features.json` if feature complete
3. Ensure no lint/build errors
4. Commit all changes — this is critical for maintaining project state across sessions:
   ```bash
   git add features.json progress.md [implementation files]
   git commit -m "feat(<scope>): <description>"
   ```
   Never skip the commit step. Each session must end with a clean commit so the next session can start fresh.

## Implementation Process

### Step 1: Select Feature

Choose **ONE** feature per session. Prioritize:

1. Features from current in-progress sprint
2. High-priority pending features with completed dependencies
3. Features that build on recent work

### Step 2: Understand Feature

Before coding:

1. Read acceptance criteria carefully
2. Review technical notes
3. Verify dependencies are satisfied
4. Identify affected files
5. Plan implementation approach

### Step 3: Plan Implementation

Write a brief plan covering:
- Which files will be modified
- What patterns to follow
- What tests to write
- Potential challenges

### Step 4: Implement Incrementally

**Key principles:**

1. **Small Commits** - Frequent, logical commits
2. **Test Continuously** - Verify each change
3. **Stay Focused** - Don't scope-creep
4. **Follow Conventions** - Match existing code style

**Commit message format:**
```
<type>(<scope>): <description>

[optional body]

Feature: <feature-id>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`

### Step 5: Verify Implementation

Check all acceptance criteria:
- [ ] Each criterion can be demonstrated
- [ ] Happy path works
- [ ] Error scenarios handled
- [ ] Edge cases considered

## File Schemas

### progress.md Structure

Add entry at **top** of sessions section:

```markdown
## Session N - YYYY-MM-DD
**Agent**: Coding Agent
**Sprint**: [Sprint ID]
**Feature**: [Feature ID and title]

### Implementation
- [What was implemented]
- [Key decisions made]

### Files Changed
- path/to/file.ts - [brief description]
- path/to/another.ts - [brief description]

### Tests Performed
- [How the feature was verified]
- [What scenarios were tested]

### Issues Encountered
- [Any blockers or bugs found]
- [How they were resolved]

### Acceptance Criteria Status
- [x] Criterion 1
- [x] Criterion 2
- [ ] Criterion 3 (if incomplete, explain why)

### Next Steps
- [Recommended next feature or follow-up]
```

### features.json Updates

Only update feature status field:

```json
{
  "id": "s1-feat-001",
  "status": "completed"  // or "in_progress"
}
```

### Feature Status Values

| Status | When to Use |
|--------|-------------|
| `pending` | Not started |
| `in_progress` | Currently being worked on |
| `completed` | Fully implemented and tested |
| `blocked` | Cannot proceed due to blocker |

## Testing Requirements

### Pre-Completion Testing

Before marking feature complete:

1. **Functional Testing**
   - Test as a user would interact
   - Verify all acceptance criteria
   - Check happy path and errors

2. **Cross-Platform Testing**
   - Test relevant platforms for the project
   - See project's AGENTS.md for requirements

3. **Technical Testing**
   - Lint passes (see AGENTS.md for command)
   - Build succeeds (see AGENTS.md for command)
   - Application starts without errors
   - No console errors

### Testing Checklist

```
☐ Happy path works
☐ Error handling works
☐ Responsive on all devices (if applicable)
☐ Theme compatibility (if applicable)
☐ Internationalization (if applicable)
☐ No console errors
☐ No lint errors
☐ Build passes
```

## Examples

See [examples.md](examples.md) for complete examples.

## Quality Checklist

### Before Marking Feature Complete

```
☐ All acceptance criteria met
☐ Lint passes
☐ Build succeeds
☐ Manual testing completed
☐ Code committed with descriptive message
☐ progress.md updated
☐ features.json status updated
☐ No TODO comments left
☐ No debug code remaining
```

### End of Session Checklist

```
☐ Feature complete (or clearly documented why not)
☐ No lint or build errors
☐ Code committed
☐ progress.md updated
☐ features.json updated (if feature complete)
☐ Application in working state
```

## Critical Rules

1. **One Feature Per Session** - Don't try to do too much
2. **Always Leave Working Code** - Never leave codebase broken
3. **Follow Acceptance Criteria** - Implement exactly what's specified
4. **Follow Project Conventions** - See project's AGENTS.md for code style
5. **Don't Modify features.json Lightly** - Only change feature status
6. **Commit Frequently** - Enable rollback

## Red Flags - Stop and Fix

**Stop immediately if you encounter:**

- Build errors
- Lint errors
- Failing tests
- Application won't start
- Previously working feature broken
- Uncommitted changes from previous session

**Fix these before proceeding with new work.**
