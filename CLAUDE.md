# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Harness is a Claude skill for managing long-running AI projects across multiple context windows. Two agent roles collaborate: Sprint Agent plans features, Coding Agent implements them (single feature or parallel via `--parallel` flag).

Command definitions and slash commands are defined in SKILL.md.

## Commands

```bash
# Framework scripts (all support --project-dir/-p flag)
python3 scripts/resolve_project_dir.py [-s dir]               # Find project dir by walking up for features.json/progress.md
python3 scripts/init_project.py <name> [-d "description"]     # Initialize tracking files
python3 scripts/status.py                                     # Show project status
python3 scripts/validate_structure.py                         # Validate features.json
python3 scripts/archive_sprint.py [--list|--dry-run|--force]  # Archive sprints

# Release/packaging (supports semver: v1.0.0, 0.4.0-beta.2)
python3 scripts/release.py <version> [--dry-run]              # Package into dist/agent-harness.skill, create git tag + GitHub Release

# Python linting
python3 -m py_compile scripts/*.py                            # Syntax check all scripts
```

## Architecture

### Core Files
- `features.json` - Sprint and feature tracking (Sprint Agent creates, Coding Agent updates status)
- `progress.md` - Session log (prepend new entries)
- `SKILL.md` - Skill definition with subcommand routing and slash commands
- `references/sprint-agent.md` - Sprint Agent workflow
- `references/coding-agent.md` - Coding Agent session protocol (includes Parallel Mode)

### Agent Cycle
1. **Sprint Agent** - Analyzes requirements, breaks into atomic features with acceptance criteria, orders by dependencies
2. **Coding Agent** - Implements features (single or parallel with `--parallel`), tests, updates tracking files, commits
3. **Loop** until sprint complete, then archive and plan next

### Templates and Packaging
- `assets/` - Templates for `features.json`, `progress.md`, `AGENTS.md` used by `init_project.py`
- `.skillignore` - Exclude patterns for skill packaging (like `.gitignore` for `.skill` zip)
- `release.py` packages into `dist/agent-harness.skill` respecting `.skillignore`, creates git tag + GitHub Release

### Loading Architecture
The skill uses three-level progressive loading to minimize context usage:
1. **Metadata** - Always loaded (~100 words)
2. **SKILL.md** - Loaded when skill is triggered (~150 lines)
3. **References** - Loaded per agent role (`sprint-agent.md`, `coding-agent.md`, `examples.md`)

### Project Directory Resolution
`resolve_project_dir.py` walks up from cwd to find the directory containing `features.json` or `progress.md`, skipping `.agent-harness`, `node_modules`, `.git`, `__pycache__`. Every agent workflow calls this first to ensure files are written to the correct location.

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
7. **Windows encoding** - Prefix script commands with `$env:PYTHONIOENCODING="utf-8";` for GBK compatibility
