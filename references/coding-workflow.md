# Coding Agent Workflow

## Table of Contents
1. [Overview](#overview)
2. [Session Protocol](#session-protocol)
3. [Feature Implementation Process](#feature-implementation-process)
4. [Testing Requirements](#testing-requirements)
5. [Progress Documentation](#progress-documentation)
6. [Quality Checklist](#quality-checklist)

## Overview

The Coding Agent implements features defined by the Sprint Agent in discrete sessions, maintaining a clean, working codebase.

## Session Protocol

### Start of Session

**Always perform these steps in order:**

1. **Confirm Location**
   ```bash
   pwd
   ```

2. **Review Recent Work**
   ```bash
   git log --oneline -10
   ```
   Read `progress.md` to understand previous sessions.

3. **Review Feature Status**
   Read `features.json` to see:
   - Current sprint status
   - Completed features
   - In-progress features
   - Pending features
   - Dependencies

4. **Verify Project State**
   ```bash
   pnpm lint      # Check code quality
   pnpm build     # Ensure build passes
   ```
   
   **⚠️ If broken, fix existing issues before starting new work.**

### End of Session

**Always perform these steps:**

1. Update `progress.md` with session summary
2. Update `features.json` if feature complete
3. Ensure no lint/build errors
4. Commit all changes

## Feature Implementation Process

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

Check all acceptance criteria are met:
- [ ] Each criterion can be demonstrated
- [ ] Happy path works
- [ ] Error scenarios handled
- [ ] Edge cases considered

## Testing Requirements

### Pre-Completion Testing

Before marking feature complete:

1. **Functional Testing**
   - Test as a user would interact
   - Verify all acceptance criteria
   - Check happy path and errors

2. **Cross-Platform Testing**
   - Responsive design (mobile/tablet/desktop)
   - Dark/light theme compatibility
   - Different locales (if i18n enabled)

3. **Technical Testing**
   - `pnpm lint` passes
   - `pnpm build` succeeds
   - Application starts without errors
   - No console errors

### Testing Checklist

```
☐ Happy path works
☐ Error handling works
☐ Responsive on all devices
☐ Dark mode works
☐ Light mode works
☐ i18n keys used (no hardcoded text)
☐ No console errors
☐ No lint errors
☐ Build passes
```

## Progress Documentation

### Update progress.md

Add entry at the **top** of the sessions section:

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

### Update features.json

Only update the feature status:

```json
{
  "id": "s1-feat-001",
  "status": "completed"  // or "in_progress"
}
```

## Quality Checklist

### Before Marking Feature Complete

```
☐ All acceptance criteria met
☐ pnpm lint passes
☐ pnpm build succeeds
☐ Manual testing completed
☐ Responsive design verified
☐ Theme compatibility checked
☐ i18n keys used for all text
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
4. **Use Translations** - No hardcoded user-facing strings
5. **Theme Aware** - Test in both dark and light modes
6. **Don't Modify features.json Lightly** - Only change feature status
7. **Commit Frequently** - Enable rollback

## Red Flags - Stop and Fix

**Stop immediately if you encounter:**

- Build errors
- Lint errors
- Failing tests
- Application won't start
- Previously working feature broken
- Uncommitted changes from previous session

**Fix these before proceeding with new work.**

## Best Practices

### Code Style

- Follow existing patterns
- Use shadcn/ui components
- Tailwind CSS for styling
- Strict TypeScript
- Named imports for React

### Commits

- Small, logical commits
- Conventional commit messages
- Include feature ID in footer
- Clear, descriptive messages

### Testing

- Test as a user would
- Check both success and failure cases
- Verify responsive design
- Test themes and locales
- No manual testing shortcuts
