# Agent Instructions for agent-harness

## Project Overview

Agent Harness is a Python-based framework for long-running AI agents that work across multiple context windows. Three agent roles collaborate: Sprint Agent plans features, Coding Agent implements them one at a time, 996 Agent runs multiple features in parallel via subagents. No external dependencies — standard library only.

## Build/Lint/Test Commands

```bash
# Syntax check all scripts
python3 -m py_compile scripts/*.py

# Syntax check a single script
python3 -m py_compile scripts/init_project.py

# Validate features.json schema
python3 scripts/validate_structure.py -p .

# Show project status
python3 scripts/status.py -p .

# Initialize tracking files
python3 scripts/init_project.py <name> -d "description" -p .

# Archive completed sprints
python3 scripts/archive_sprint.py --list
python3 scripts/archive_sprint.py --dry-run
python3 scripts/archive_sprint.py

# Package and release (supports semver: v1.0.0, 0.4.0-beta.2)
python3 scripts/release.py <version> --dry-run
python3 scripts/release.py <version>

# Git workflow
git log --oneline -10
git status
```

All scripts support `--project-dir` / `-p` to specify the project directory.

## Project Structure

```
agent-harness/
├── scripts/
│   ├── init_project.py        # Initialize tracking files from templates
│   ├── status.py              # Display project status from features.json
│   ├── validate_structure.py  # Validate features.json schema
│   ├── archive_sprint.py      # Archive completed sprints
│   └── release.py             # Package .skill zip and publish GitHub Release
├── assets/
│   ├── features.json          # Template for feature tracking
│   └── progress.md            # Template for session logs
├── references/
│   ├── sprint-agent.md        # Sprint Agent workflow
│   ├── coding-agent.md        # Coding Agent session protocol
│   ├── 996-agent.md           # 996 parallel orchestration protocol
│   └── examples.md            # Realistic usage examples
├── .skillignore               # Exclude patterns for skill packaging
├── SKILL.md                   # Skill definition with subcommand routing
├── CLAUDE.md                  # Claude Code guidance
└── AGENTS.md                  # This file
```

## Code Style Guidelines

### Python (3.8+, standard library only)

**Shebang and module docstring** — every script starts with:

```python
#!/usr/bin/env python3
"""One-line description of the script."""
```

**Imports** — standard library only, alphabetical order, group `from` imports after `import`:

```python
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
```

**Naming conventions:**

- Functions and variables: `snake_case`
- Module-level constants: `UPPER_SNAKE_CASE` (e.g., `ARCHIVED_DIR`, `SKILL_NAME`)
- Type hints on all function parameters and return types

**Docstrings** — Google style with `Args:` and `Returns:`:

```python
def validate_feature(feature: Dict, feature_idx: int) -> List[str]:
    """Validate a single feature.

    Args:
        feature: Feature dictionary to validate.
        feature_idx: Index for error reporting.

    Returns:
        List of error messages (empty if valid).
    """
```

**Error handling** — return error message lists for validation functions; use `try/except` for file I/O:

```python
if not filepath.exists():
    return [f"File not found: {filepath}"]

try:
    with open(filepath, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    return [f"Invalid JSON: {e}"]
```

**Entry point pattern** — use `argparse`, return exit codes, call `sys.exit(main())`:

```python
def main():
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("required_arg", help="...")
    parser.add_argument("--project-dir", "-p", default=".", help="...")
    args = parser.parse_args()

    try:
        # implementation
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Exit codes:** 0 = success, non-zero = failure.

### JSON (features.json)

- 2-space indentation
- `snake_case` keys
- Status values: lowercase with underscores

### Markdown

- ATX-style headers (`#`, `##`, `###`)
- Blank lines before and after headers
- Fenced code blocks with language tags
- Lines under 80 characters where practical

## Status Values

| Feature Status | Description | Sprint Status | Description |
|----------------|-------------|---------------|-------------|
| `pending` | Not started | `planning` | Being defined |
| `in_progress` | Active work | `in_progress` | Implementing |
| `completed` | Done | `completed` | All done |
| `blocked` | Cannot proceed | `on_hold` | Paused |

Feature categories: `core`, `ui`, `api`, `auth`, `data`, `infra`
Feature priorities: `high`, `medium`, `low`

## Git Commit Format

```
<type>(<scope>): <description>

Feature: <feature-id>    # optional footer
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`

## Session Protocol

### Start of Session

1. `pwd` to confirm directory
2. Read `progress.md` for recent work
3. `git log --oneline -10` for commit history
4. Run `python3 scripts/validate_structure.py` to verify state
5. If broken, fix existing issues before starting new work

### End of Session

1. Update `progress.md` with session summary (prepend at top)
2. Update `features.json` if feature complete
3. Run `python3 -m py_compile scripts/*.py` to verify
4. Run `python3 scripts/validate_structure.py` to verify
5. Commit all changes

## Core Tracking Files

| File | Purpose | Who Updates |
|------|---------|-------------|
| `features.json` | Sprints and feature list | Sprint Agent creates, Coding Agent updates status |
| `progress.md` | Session log (prepend new entries) | Every agent at end of session |

## Critical Rules

1. **No external dependencies** — scripts must use only Python standard library
2. **Backward compatibility** — changes must not break existing features.json files
3. **One feature per session** — Coding Agent implements only one feature
4. **Never delete features** — only change status
5. **Always leave working code** — never break the build
6. **Validate before write** — run `validate_structure.py` after modifying features.json
7. **Clear error messages** — all errors should be actionable and specific
8. **Exit codes** — return 0 for success, non-zero for failure
