# Agent Instructions for agent-harness

This file provides instructions for AI agents working on this project.

## Project Overview

Agent Harness is a Python-based framework for long-running AI agents that work across multiple context windows. It enables Claude to execute complex, multi-session projects through Sprint-Coding agent cycles.

## Tech Stack

- **Language**: Python 3.8+ (standard library only, no external dependencies)
- **File Formats**: JSON for data, Markdown for documentation
- **Target Environment**: Claude AI assistant skill

## Build/Lint/Test Commands

```bash
# Framework Scripts
python3 scripts/init_project.py <name> -d "[description]"   # Initialize tracking files
python3 scripts/status.py                                   # Show project status
python3 scripts/validate_structure.py                       # Validate features.json

# Python Linting
python3 -m py_compile scripts/*.py                          # Syntax check all scripts

# Git Workflow
git log --oneline -10                                       # Review recent commits
git status                                                  # Check working tree
```

## Code Style Guidelines

### Python Style

- **Python Version**: Compatible with Python 3.8+
- **No External Dependencies**: Use only standard library modules
- **Formatting**: Follow PEP 8 conventions

#### Imports

```python
# Standard library imports first, alphabetically
import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
```

#### Naming Conventions

- **Functions**: `snake_case` (e.g., `create_features_json`, `validate_sprint`)
- **Variables**: `snake_case` (e.g., `features_path`, `sprint_idx`)
- **Constants**: `UPPER_SNAKE_CASE` for module-level constants
- **Type hints**: Use for function parameters and return types

#### Function Structure

```python
def validate_feature(feature: Dict, feature_idx: int) -> List[str]:
    """Validate a single feature.
    
    Args:
        feature: Feature dictionary to validate
        feature_idx: Index for error reporting
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    return errors
```

#### Error Handling

```python
# Use explicit error returns with messages
if not filepath.exists():
    return [f"File not found: {filepath}"]

# Use try/except for file operations
try:
    with open(filepath, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    return [f"Invalid JSON: {e}"]
```

#### Main Function Pattern

```python
def main():
    """Entry point for the script."""
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("required_arg", help="Required argument")
    parser.add_argument("--optional", "-o", default="value", help="Optional")
    args = parser.parse_args()
    
    try:
        # Implementation
        return 0  # Success
    except Exception as e:
        print(f"Error: {e}")
        return 1  # Failure

if __name__ == "__main__":
    sys.exit(main())
```

### JSON Style (features.json)

- **Indentation**: 2 spaces
- **Keys**: snake_case
- **Status values**: lowercase with underscores

### Markdown Style

- Use ATX-style headers (`#`, `##`, `###`)
- Include blank lines before and after headers
- Use fenced code blocks with language tags
- Keep lines under 80 characters where practical

## Status Values

| Feature Status | Description | Sprint Status | Description |
|----------------|-------------|---------------|-------------|
| `pending` | Not started | `planning` | Being defined |
| `in_progress` | Active work | `in_progress` | Implementing |
| `completed` | Done | `completed` | All done |
| `blocked` | Cannot proceed | `on_hold` | Paused |

## Git Commit Format

```
<type>(<scope>): <description>
```

**Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`

## Session Protocol

### Start of Session
1. `pwd` to confirm directory
2. Read `progress.md` for recent work
3. `git log --oneline -10` for commit history
4. Run `python3 scripts/validate_structure.py` to verify state

### End of Session
- Update `progress.md` with summary
- Update `features.json` if feature complete
- Run `python3 scripts/validate_structure.py` to verify
- Commit changes

## Core Files

| File | Purpose | Who Updates |
|------|---------|-------------|
| `features.json` | Sprints and feature list | Sprint creates, Coding updates status |
| `progress.md` | Session log | Every agent at end of session |
| `AGENTS.md` | Agent instructions | Rarely modified |

## Project Structure

```
agent-harness/
├── scripts/
│   ├── init_project.py      # Initialize tracking files
│   ├── status.py            # Display project status
│   └── validate_structure.py # Validate features.json
├── assets/
│   ├── features.json        # Template for feature tracking
│   ├── progress.md          # Template for session logs
│   └── AGENTS.md            # Template for project AGENTS.md
├── references/
│   ├── sprint-workflow.md   # Sprint Agent process
│   ├── coding-workflow.md   # Coding Agent session protocol
│   └── file-structure.md    # Complete file schemas
├── SKILL.md                 # Skill definition for Claude
├── README.md                # Project documentation
└── AGENTS.md                # This file
```

## Critical Rules

1. **No External Dependencies** - Scripts must use only Python standard library
2. **Backward Compatibility** - Changes must not break existing features.json files
3. **Clear Error Messages** - All errors should be actionable and specific
4. **Exit Codes** - Return 0 for success, non-zero for failure
5. **Validate Before Write** - Always validate JSON before writing
