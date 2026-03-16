# Agent Instructions

This file provides instructions for AI agents working on this project across multiple sessions.

## Project Overview

[Update this section with your project description]

## Agent Types

| Agent | Role | When Invoked |
|-------|------|--------------|
| **Sprint** | Feature planning | New sprint or requirement iteration |
| **Coding** | Feature implementation | Each development session |

## Workflow

```
┌─────────────────┐
│   Sprint Agent  │  <──  User provides requirements
└────────┬────────┘
         │         Generates feature list
         v
┌─────────────────┐
│  Coding Agent   │  <──  Implements one feature per session
└────────┬────────┘
         │
         │         Loop until sprint complete
         v
┌─────────────────┐
│   Sprint Agent  │  <──  Next iteration
└─────────────────┘
```

## Commands

```bash
# Framework Scripts
python3 [path-to-skill]/scripts/init_project.py <name> -d "[description]"
python3 [path-to-skill]/scripts/status.py
python3 [path-to-skill]/scripts/validate_structure.py
python3 [path-to-skill]/scripts/archive_sprint.py --list     # List completed sprints
python3 [path-to-skill]/scripts/archive_sprint.py            # Archive completed sprints

# Project Commands (customize for your project)
npm run dev       # Start development server
npm run build     # Production build
npm run lint      # Run linter
npm run test      # Run tests

# Git Workflow
git log --oneline -10     # Review recent commits
git status                # Check working tree
```

## Tech Stack

[Update this section with your actual tech stack]

- Framework: [Your framework]
- Language: [Your language]
- Styling: [Your styling solution]
- Testing: [Your testing framework]

## Code Style Guidelines

[Update this section with your project's code style]

### Naming Conventions
- Components: [Your convention]
- Utilities: [Your convention]
- Files: [Your convention]

### Code Patterns
- [Pattern 1]
- [Pattern 2]

## Git Commit Format

```
<type>(<scope>): <description>

[optional body]

Feature: <feature-id>
```

**Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`

## Status Values

| Feature Status | Description | Sprint Status | Description |
|----------------|-------------|---------------|-------------|
| `pending` | Not started | `planning` | Being defined by Sprint Agent |
| `in_progress` | Currently being worked on | `in_progress` | Features being implemented |
| `completed` | Fully implemented and tested | `completed` | All features done |
| `blocked` | Cannot proceed due to dependency | `on_hold` | Paused for some reason |

## Core Files

| File | Purpose | Who Updates |
|------|---------|-------------|
| `features.json` | Sprints and feature list with status | Sprint creates, Coding updates status |
| `progress.md` | Session-by-session progress log | Every agent at end of session |
| `AGENTS.md` | This file - agent instructions | Rarely modified |

## Session Protocol

### Start of Session
1. `pwd` to confirm directory
2. Read `progress.md` for recent work
3. `git log --oneline -10` for commit history
4. Run lint/build to verify state

### During Work
- Pick **ONE** pending feature
- Make frequent, logical commits
- Test thoroughly before marking complete

### End of Session
- Update `progress.md` with summary
- Update `features.json` if feature complete
- Ensure no lint/build errors

## Critical Rules

1. **One Feature Per Session** - Don't implement multiple features
2. **Always Leave Working Code** - Never end with broken tests or build
3. **Test End-to-End** - Verify as a user would experience
4. **Commit Frequently** - Small commits enable rollback
5. **Document Decisions** - Future agents need context
6. **Don't Delete Features** - Only change status in `features.json`
