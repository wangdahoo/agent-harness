---
name: agent-harness
description: "Framework for long-running AI agents that work across multiple context windows. Use when Claude needs to execute complex, multi-session projects that require: (1) Breaking down large requirements into manageable features, (2) Tracking progress across multiple sessions, (3) Maintaining context between context window resets, (4) Coordinating Sprint (planning) and Coding (implementation) agents, (5) Managing feature dependencies and prioritization, (6) Ensuring code quality and working state at each session end. Based on Anthropic's research on effective harnesses for long-running agents."
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

```bash
python3 scripts/init_project.py "Project Name" -d "Description"
python3 scripts/status.py
python3 scripts/validate_structure.py
```

## Workflow

### 1. Sprint Planning (Sprint Agent)

**When:** New project or iteration

1. Analyze user requirements
2. Break into atomic features with acceptance criteria
3. Order by dependencies
4. Update `features.json` and `progress.md`

**→ Read [references/sprint-workflow.md](references/sprint-workflow.md) for detailed process**

### 2. Feature Implementation (Coding Agent)

**When:** Each development session

**Session Protocol:**

| Phase | Actions |
|-------|---------|
| **Start** | `pwd` → read `progress.md` → `git log` → run lint/build |
| **Work** | Select ONE feature → implement → test |
| **End** | Update `progress.md` → update `features.json` → commit |

**→ Read [references/coding-workflow.md](references/coding-workflow.md) for detailed protocol**

### 3. Iterate

Loop: Sprint Agent → Coding Agent → Coding Agent → ... → Sprint Agent

## Core Files

| File | Purpose |
|------|---------|
| `features.json` | Sprint and feature tracking (schema: see file-structure.md) |
| `progress.md` | Session log - add entries at top |
| `AGENTS.md` | Project-specific instructions |

**→ Read [references/file-structure.md](references/file-structure.md) for complete schemas**

## Scripts

```bash
python3 scripts/init_project.py <name> [-d desc] [-o dir]  # Initialize tracking
python3 scripts/status.py                                  # Show status
python3 scripts/validate_structure.py                      # Validate features.json
python3 scripts/archive_sprint.py [--list|--dry-run]       # Archive completed sprints
```

## Critical Rules

1. **One Feature Per Session** - Don't implement multiple
2. **Always Leave Working Code** - Never break the build
3. **Test End-to-End** - Verify as user would experience
4. **Commit Frequently** - Small commits enable rollback
5. **Never Delete Features** - Only change status
6. **Use Progress Log** - Record every session

## References

- **[sprint-workflow.md](references/sprint-workflow.md)** - Sprint Agent process, feature breakdown, dependency management
- **[coding-workflow.md](references/coding-workflow.md)** - Session protocol, testing requirements, quality checklist
- **[file-structure.md](references/file-structure.md)** - Complete schemas for features.json and progress.md
