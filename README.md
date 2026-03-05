# Agent Harness

Framework for long-running AI agents that work across multiple context windows. Enables Claude to execute complex, multi-session projects through Sprint-Coding agent cycles.

## Overview

Agent Harness solves the challenge of managing large projects that span multiple context windows by using two specialized agents:

- **Sprint Agent**: Plans features and breaks down requirements
- **Coding Agent**: Implements features one at a time per session

The framework maintains context through structured files, ensuring continuity across sessions.

## Key Features

- **Progress Tracking**: Maintains session logs and feature status
- **Quality Gates**: Ensures working code at each session end
- **Dependency Management**: Handles feature dependencies automatically
- **Context Preservation**: Never lose progress across context resets
- **Sprint Planning**: Structured approach to breaking down requirements

## Installation

This is a skill that integrates with Claude. To use it:

1. Clone or download this skill to your local machine
2. Ensure the skill is accessible to your Claude instance
3. The skill will be automatically available when needed

## Quick Start

### 1. Initialize a New Project

```bash
python3 scripts/init_project.py "My Project" -d "A description of my project"
```

This creates:
- `features.json` - Feature tracking file
- `progress.md` - Session log file

### 2. Start Sprint Planning

When you need to plan features for a new project or sprint, Claude will automatically invoke the Sprint Agent skill. Just describe your requirements:

```
I need to build a user authentication system with:
- Email/password login
- Social login (Google, GitHub)
- Password reset
- Session management
```

The Sprint Agent will:
- Break down requirements into atomic features
- Define acceptance criteria for each feature
- Order features by dependencies
- Create a sprint in `features.json`

### 3. Implement Features

Claude will invoke the Coding Agent for each development session. It will:
- Select the next pending feature
- Implement following acceptance criteria
- Test thoroughly
- Update progress tracking files
- Commit changes

### 4. Check Status

Monitor your project progress:

```bash
python3 scripts/status.py
```

Shows:
- Current sprint status
- Feature completion status
- Recent sessions
- Next steps

### 5. Validate Structure

Ensure your feature tracking is correct:

```bash
python3 scripts/validate_structure.py
```

## Core Concepts

### Sprint Agent

**When invoked:**
- New project initialization
- New sprint iteration
- Requirement updates

**Responsibilities:**
- Analyze user requirements
- Break into atomic features
- Define acceptance criteria
- Order by dependencies
- Document in `features.json`

### Coding Agent

**When invoked:**
- Each development session

**Session Protocol:**

**Start:**
1. Confirm working directory
2. Review recent work in `progress.md`
3. Check commit history
4. Verify project state (lint/build)

**Work:**
1. Select ONE feature
2. Understand acceptance criteria
3. Implement incrementally
4. Test thoroughly

**End:**
1. Update `progress.md`
2. Update feature status in `features.json`
3. Ensure no errors
4. Commit changes

## Workflow

```
User Requirements
      ↓
┌─────────────────┐
│  Sprint Agent   │ ← Plans features
└────────┬────────┘
         │
         ↓
   features.json
         │
         ↓
┌─────────────────┐
│  Coding Agent   │ ← Implements one feature
└────────┬────────┘
         │
         ↓
  Working Code
         │
         ├─→ Update progress.md
         ├─→ Update features.json
         └─→ Commit changes
         
    (Loop until sprint complete)
```

## File Structure

### Core Tracking Files

| File | Purpose | Who Updates |
|------|---------|-------------|
| `features.json` | Sprints and feature definitions | Sprint creates, Coding updates status |
| `progress.md` | Session-by-session log | Every agent |
| `AGENTS.md` | Project-specific instructions | User |

### Feature Definition

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

### Status Values

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

## Scripts

### init_project.py

Initialize tracking files for a new project:

```bash
python3 scripts/init_project.py <name> [-d description] [-o output-dir]
```

### status.py

Display current project status:

```bash
python3 scripts/status.py
```

### validate_structure.py

Validate `features.json` schema:

```bash
python3 scripts/validate_structure.py
```

## Critical Rules

1. **One Feature Per Session** - Coding Agent implements only one feature
2. **Always Leave Working Code** - Never break the build
3. **Test End-to-End** - Verify as user would experience
4. **Commit Frequently** - Small commits enable rollback
5. **Document Decisions** - Future agents need context
6. **Never Delete Features** - Only change status
7. **Use Progress Log** - Record every session

## Common Patterns

### Starting New Sprint

1. User provides requirements
2. Sprint Agent analyzes and breaks down
3. Creates features in `features.json`
4. Logs planning session in `progress.md`
5. Returns feature summary

### Implementing Feature

1. Coding Agent reads `progress.md` and `features.json`
2. Selects next pending feature
3. Implements following acceptance criteria
4. Tests thoroughly
5. Updates tracking files
6. Commits changes

### Handling Blockers

1. Mark feature as `blocked` in `features.json`
2. Document blocker in `progress.md`
3. Move to next independent feature
4. Return to blocked feature when resolved

## Templates

Templates are available in `assets/`:
- `features.json` - Feature tracking template
- `progress.md` - Session log template
- `AGENTS.md` - Project instructions template

## References

Detailed workflow documentation:

- [Sprint Workflow](references/sprint-workflow.md) - Sprint Agent detailed process
- [Coding Workflow](references/coding-workflow.md) - Coding Agent session protocol
- [File Structure](references/file-structure.md) - Complete file schemas

## Best Practices

### Sprint Agent
- Break large features into atomic pieces
- Define clear acceptance criteria
- Consider dependencies carefully
- Balance sprint complexity mix

### Coding Agent
- Follow session protocol strictly
- Test before marking complete
- Commit frequently with clear messages
- Stay focused on one feature

## Troubleshooting

### Build is broken
1. Check recent commits
2. Review `progress.md` for changes
3. Fix errors
4. Verify with lint/build

### Feature too large
1. Sprint Agent splits into smaller features
2. Each becomes independent feature
3. Mark dependencies if needed

### Context lost
1. Read `progress.md` - Recent sessions
2. Read `features.json` - Current state
3. Read `AGENTS.md` - Project conventions
4. Check git log - Recent changes

## License

This skill is provided as-is for use with Claude AI assistants.

## Contributing

Feel free to adapt the scripts and templates to fit your project's specific needs. The framework is designed to be flexible and extensible.
