---
name: agent-harness
description: "Framework for long-running AI agents that work across multiple context windows. Use when Claude needs to execute complex, multi-session projects that require: (1) Breaking down large requirements into manageable features, (2) Tracking progress across multiple sessions, (3) Maintaining context between context window resets, (4) Coordinating Sprint (planning) and Coding (implementation) agents, (5) Managing feature dependencies and prioritization, (6) Ensuring code quality and working state at each session end. Commands: /agent-harness, /agent-harness-init, /agent-harness-sprint, /agent-harness-code, /agent-harness-status, /agent-harness-archive, /agent-harness-force-archive. Based on Anthropic's research on effective harnesses for long-running agents."
---

# Agent Harness

Framework for executing complex, multi-session projects using Sprint-Coding agent cycles.

## Overview

Agent Harness enables Claude to manage long-running projects by:

- **Sprint Agent**: Plans features and breaks down requirements
- **Coding Agent**: Implements features one at a time
- **Progress Tracking**: Maintains context across sessions
- **Quality Gates**: Ensures working code at each step

## Commands

Agent Harness provides slash commands with tab completion. Type `/agent-harness` to see all commands.

### `/agent-harness`

Show available commands and usage.

**Output:**
```
Agent Harness Commands:
  /agent-harness-init <name>   - Initialize new project tracking files
  /agent-harness-sprint [req]  - Create or update sprint with feature breakdown
  /agent-harness-code          - Start coding session for next feature
  /agent-harness-status        - Show current project status
  /agent-harness-archive       - Archive completed sprints
  /agent-harness-force-archive - Force archive ALL sprints (including incomplete)
```

### `/agent-harness-init <name>`

Initialize new project tracking files.

**Example:** `/agent-harness-init My App`

**Actions:**
- Create `features.json` and `progress.md`
- Run `python3 scripts/init_project.py "My App"`

### `/agent-harness-sprint [requirements]`

Create or update sprint with feature breakdown.

**Examples:**
- `/agent-harness-sprint` - Review current sprint and plan next
- `/agent-harness-sprint Add user authentication with email and social login`
- `/agent-harness-sprint Build dashboard with charts and filters`

**Actions:**
1. Archive completed sprints (if any)
2. Analyze requirements
3. Break into atomic features with acceptance criteria
4. Update `features.json` and `progress.md`
5. Read [sprint-agent.md](references/sprint-agent.md) for detailed workflow

### `/agent-harness-code`

Start coding session for next feature.

**Actions:**
1. Review `progress.md` and `features.json`
2. Select next pending feature
3. Implement following session protocol
4. Read [coding-agent.md](references/coding-agent.md) for protocol

### `/agent-harness-status`

Show current project status.

**Output:**
- Current sprint and goal
- Feature completion statistics
- Next recommended feature
- Run `python3 scripts/status.py`

### `/agent-harness-archive`

Archive completed sprints.

**Actions:**
- List completed sprints
- Move to `.agent-harness/archived/`
- Run `python3 scripts/archive_sprint.py`

### `/agent-harness-force-archive`

Force archive ALL sprints (including incomplete ones).

**Warning:** This will archive all sprints regardless of their status.

**Actions:**
- List all sprints to be archived
- Confirm with user
- Move all to `.agent-harness/archived/`
- Run `python3 scripts/archive_sprint.py --force`

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

**→ Read [references/sprint-agent.md](references/sprint-agent.md) for workflow, schemas, and examples**

### 2. Feature Implementation (Coding Agent)

**When:** Each development session

**Session Protocol:**

| Phase | Actions |
|-------|---------|
| **Start** | `pwd` → read `progress.md` → `git log` → run lint/build |
| **Work** | Select ONE feature → implement → test |
| **End** | Update `progress.md` → update `features.json` → commit |

**→ Read [references/coding-agent.md](references/coding-agent.md) for protocol, testing, and schemas**

### 3. Iterate

Loop: Sprint Agent → Coding Agent → Coding Agent → ... → Sprint Agent

## Core Files

| File | Purpose |
|------|---------|
| `features.json` | Sprint and feature tracking |
| `progress.md` | Session log - add entries at top |
| `AGENTS.md` | Project-specific instructions |

**→ See [references/sprint-agent.md](references/sprint-agent.md) or [references/coding-agent.md](references/coding-agent.md) for schemas**

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

**By Agent Role:**
- **[sprint-agent.md](references/sprint-agent.md)** - Sprint Agent: workflow, feature breakdown, schemas
- **[coding-agent.md](references/coding-agent.md)** - Coding Agent: session protocol, testing, schemas

**Complete Examples:**
- **[examples.md](references/examples.md)** - Realistic examples of features.json, progress.md, and workflows
