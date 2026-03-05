---
name: agent-harness
description: Framework for long-running AI agents that work across multiple context windows. Use when Claude needs to execute complex, multi-session projects that require: (1) Breaking down large requirements into manageable features, (2) Tracking progress across multiple sessions, (3) Maintaining context between context window resets, (4) Coordinating Sprint (planning) and Coding (implementation) agents, (5) Managing feature dependencies and prioritization, (6) Ensuring code quality and working state at each session end. Based on Anthropic's research on effective harnesses for long-running agents.
---

# Agent Harness

Framework for executing complex, multi-session projects using Sprint-Coding agent cycles.

## Overview

Agent Harness enables Claude to manage long-running projects by:

- **Sprint Agent**: Plans features and breaks down requirements
- **Coding Agent**: Implements features one at a time
- **Progress Tracking**: Maintains context across sessions
- **Quality Gates**: Ensures working code at each step

## Quick Start

### Initialize Project

```bash
python3 scripts/init_project.py "Project Name" -d "Description"
```

Creates:
- `features.json` - Feature tracking
- `progress.md` - Session log

### Check Status

```bash
python3 scripts/status.py
```

Shows current sprint, feature status, and recent sessions.

### Validate Structure

```bash
python3 scripts/validate_structure.py
```

Validates `features.json` schema and structure.

## Workflow

### 1. Sprint Planning

**When:** New project or iteration  
**Agent:** Sprint Agent

**Actions:**
1. Analyze user requirements
2. Break into atomic features
3. Define acceptance criteria
4. Order by dependencies
5. Update `features.json`
6. Log in `progress.md`

**See:** [references/sprint-workflow.md](references/sprint-workflow.md)

### 2. Feature Implementation

**When:** Each development session  
**Agent:** Coding Agent

**Session Protocol:**

**Start:**
1. `pwd` - Confirm directory
2. Read `progress.md` - Recent work
3. `git log --oneline -10` - Commit history
4. Run lint/build - Verify state

**Work:**
1. Select ONE feature
2. Understand acceptance criteria
3. Implement incrementally
4. Test thoroughly

**End:**
1. Update `progress.md`
2. Update `features.json` status
3. Ensure no errors
4. Commit changes

**See:** [references/coding-workflow.md](references/coding-workflow.md)

### 3. Iterate

Loop until sprint complete:
- Sprint Agent → Feature list
- Coding Agent → Implement feature 1
- Coding Agent → Implement feature 2
- ...repeat...
- Sprint Agent → Next iteration

## Core Files

| File | Purpose | Who Updates |
|------|---------|-------------|
| `features.json` | Sprints and features | Sprint creates, Coding updates status |
| `progress.md` | Session log | Every agent |
| `AGENTS.md` | Project instructions | User |

**See:** [references/file-structure.md](references/file-structure.md) for schemas

## Feature Definition

Each feature in `features.json`:

```json
{
  "id": "s1-feat-001",
  "category": "core | ui | api | auth | data | infra",
  "priority": "high | medium | low",
  "title": "Feature title",
  "description": "Detailed description",
  "acceptance_criteria": ["Given X, when Y, then Z"],
  "technical_notes": "Implementation hints",
  "status": "pending | in_progress | completed | blocked",
  "dependencies": ["feature-id"],
  "estimated_complexity": "small | medium | large",
  "files_affected": ["path/to/file"]
}
```

## Status Values

**Feature Status:**
- `pending` - Not started
- `in_progress` - Being worked on
- `completed` - Fully implemented and tested
- `blocked` - Cannot proceed

**Sprint Status:**
- `planning` - Being defined
- `in_progress` - Features being implemented
- `completed` - All features done
- `on_hold` - Temporarily paused

## Critical Rules

1. **One Feature Per Session** - Don't implement multiple
2. **Always Leave Working Code** - Never break the build
3. **Test End-to-End** - Verify as user would experience
4. **Commit Frequently** - Small commits enable rollback
5. **Document Decisions** - Future agents need context
6. **Never Delete Features** - Only change status
7. **Use Progress Log** - Record every session

## Scripts Reference

### init_project.py

```bash
python3 scripts/init_project.py <name> [-d description] [-o output-dir]
```

Initialize tracking files in project.

### status.py

```bash
python3 scripts/status.py
```

Display project status, features, and recent sessions.

### validate_structure.py

```bash
python3 scripts/validate_structure.py
```

Validate `features.json` structure and schema.

## Templates

Templates are in `assets/`:

- `features.json` - Feature tracking template
- `progress.md` - Session log template
- `AGENTS.md` - Project instructions template

## Common Patterns

### Starting New Sprint

1. User provides requirements
2. Invoke Sprint Agent
3. Sprint Agent reads existing `features.json`
4. Creates new sprint with features
5. Logs planning session in `progress.md`
6. Returns feature summary

### Implementing Feature

1. Invoke Coding Agent
2. Agent reads `progress.md` and `features.json`
3. Selects next pending feature
4. Implements following acceptance criteria
5. Tests thoroughly
6. Updates `progress.md` and `features.json`
7. Commits changes

### Handling Blockers

1. Mark feature as `blocked` in `features.json`
2. Document blocker in `progress.md`
3. Move to next feature
4. Return to blocked feature when resolved

## Best Practices

### Sprint Agent

- Break large features into atomic pieces
- Define clear acceptance criteria
- Consider dependencies carefully
- Balance sprint complexity mix
- Document rationale for decisions

### Coding Agent

- Follow session protocol strictly
- Test before marking complete
- Commit frequently with clear messages
- Stay focused on one feature
- Leave code in working state

## Troubleshooting

### Build is broken

**Fix before starting new work:**
1. Check recent commits
2. Review `progress.md` for changes
3. Fix errors
4. Verify with lint/build

### Feature too large

**Break down further:**
1. Sprint Agent splits into smaller features
2. Each becomes independent feature
3. Mark dependencies if needed

### Context lost

**Recover from files:**
1. Read `progress.md` - Recent sessions
2. Read `features.json` - Current state
3. Read `AGENTS.md` - Project conventions
4. Check git log - Recent changes

## Integration with Projects

### Customizing AGENTS.md

Add project-specific information:
- Tech stack details
- Code style conventions
- Testing requirements
- Deployment process

### Adapting Scripts

Scripts can be customized for:
- Different package managers (npm/yarn/pnpm)
- Different lint commands
- Different build commands
- Different test frameworks

## References

- **Sprint Workflow**: [references/sprint-workflow.md](references/sprint-workflow.md)
- **Coding Workflow**: [references/coding-workflow.md](references/coding-workflow.md)
- **File Structure**: [references/file-structure.md](references/file-structure.md)
