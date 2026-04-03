# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Harness is a Claude skill for managing long-running AI projects across multiple context windows. It uses a Sprint-Coding agent cycle: Sprint Agent plans features, Coding Agent implements them one at a time.

## Commands

```bash
# Framework scripts (all support --project-dir/-p flag)
python3 scripts/init_project.py <name> [-d "description"]   # Initialize tracking files
python3 scripts/status.py                                   # Show project status
python3 scripts/validate_structure.py                       # Validate features.json
python3 scripts/archive_sprint.py [--list|--dry-run|--force]  # Archive sprints

# Python linting
python3 -m py_compile scripts/*.py                          # Syntax check all scripts
```

## Architecture

### Core Files
- `features.json` - Sprint and feature tracking (Sprint Agent creates, Coding Agent updates status)
- `progress.md` - Session log (prepend new entries)
- `SKILL.md` - Skill definition with slash commands
- `references/sprint-agent.md` - Sprint Agent workflow
- `references/coding-agent.md` - Coding Agent session protocol

### Slash Commands (.opencode/commands/)
Commands like `/agent-harness-init`, `/agent-harness-sprint`, `/agent-harness-code` are defined here. They trigger agent workflows defined in SKILL.md and references/.

### Sprint-Coding Cycle
1. **Sprint Agent** - Analyzes requirements, breaks into atomic features with acceptance criteria, orders by dependencies
2. **Coding Agent** - Implements ONE feature per session, tests, updates tracking files, commits
3. **Loop** until sprint complete, then archive and plan next

## Status Values

| Feature | Sprint |
|---------|--------|
| `pending`, `in_progress`, `completed`, `blocked` | `planning`, `in_progress`, `completed`, `on_hold` |

## Code Style

- **Python 3.8+**, standard library only (no external dependencies)
- **Formatting**: PEP 8, 2-space indent for JSON
- **Type hints**: Use for function parameters and return types
- **Error handling**: Return error message lists, use try/except for file operations
- **Exit codes**: 0 for success, non-zero for failure

## Git Commits

```
<type>(<scope>): <description>
```
Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`

## Critical Rules

1. **No external dependencies** - Scripts must use only Python standard library
2. **Backward compatibility** - Changes must not break existing features.json files
3. **One feature per session** - Coding Agent implements only one feature
4. **Always leave working code** - Never break the build
5. **Never delete features** - Only change status
6. **Validate before write** - Run validate_structure.py after modifying features.json
