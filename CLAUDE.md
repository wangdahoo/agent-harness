# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Harness is a Claude skill for managing long-running AI projects across multiple context windows. Three agent roles collaborate: Sprint Agent plans features, Coding Agent implements them one at a time, 996 Agent runs multiple features in parallel via subagents.

Supports two CLI formats: **OpenCode** (`/agent-harness-init`) and **Claude Code** (`/agent-harness init`). Command definitions live in `.opencode/commands/`.

## Commands

```bash
# Framework scripts (all support --project-dir/-p flag)
python3 scripts/init_project.py <name> [-d "description"]   # Initialize tracking files
python3 scripts/status.py                                   # Show project status
python3 scripts/validate_structure.py                       # Validate features.json
python3 scripts/archive_sprint.py [--list|--dry-run|--force]  # Archive sprints

# Release/packaging (supports semver: v1.0.0, 0.4.0-beta.2)
python3 scripts/release.py <version> [--dry-run]            # Package & publish to GitHub Releases

# Python linting
python3 -m py_compile scripts/*.py                          # Syntax check all scripts
```

## Architecture

### Core Files
- `features.json` - Sprint and feature tracking (Sprint Agent creates, Coding Agent updates status)
- `progress.md` - Session log (prepend new entries)
- `SKILL.md` - Skill definition with subcommand routing and slash commands
- `references/sprint-agent.md` - Sprint Agent workflow
- `references/coding-agent.md` - Coding Agent session protocol
- `references/996-agent.md` - 996 Agent parallel orchestration protocol

### Agent Cycle
1. **Sprint Agent** - Analyzes requirements, breaks into atomic features with acceptance criteria, orders by dependencies
2. **Coding Agent** - Implements ONE feature per session, tests, updates tracking files, commits
3. **996 Agent** - Analyzes dependency graph and file conflicts, dispatches subagents in parallel batches (max 5), verifies results
4. **Loop** until sprint complete, then archive and plan next

### Templates and Packaging
- `assets/` - Templates for `features.json`, `progress.md`, `AGENTS.md` used by `init_project.py`
- `.skillignore` - Exclude patterns for skill packaging (like `.gitignore` for `.skill` zip)
- `release.py` packages into `dist/agent-harness.skill` respecting `.skillignore`, creates git tag + GitHub Release

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
