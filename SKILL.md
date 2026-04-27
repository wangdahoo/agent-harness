---
name: agent-harness
description: "Framework for long-running AI agents across multiple context windows. USE WHEN user types /agent-harness or mentions sprint planning, feature breakdown, multi-session projects. Subcommands: init, sprint, code, 996, status, archive, force-archive."
argument-hint: init|sprint|code|996|status|archive|force-archive [args...]
user-invocable: true
---

# Agent Harness

## Subcommand Routing

When invoked as `/agent-harness <subcommand>`, route to the appropriate workflow:

| Subcommand | Action |
|------------|--------|
| `init <name>` | Run `python3 scripts/init_project.py "<name>" --project-dir "$(pwd)"` |
| `sprint [req]` | Execute Sprint Agent workflow (see references/sprint-agent.md) |
| `code` | Execute Coding Agent workflow (see references/coding-agent.md) |
| `996` | Execute 996 parallel orchestration (see references/996-agent.md) |
| `status` | Run `python3 scripts/status.py --project-dir "$(pwd)"` |
| `archive` | Run archive workflow |
| `force-archive` | Run force archive workflow |
| `help` or empty | Show available commands |

**Usage examples:**
- `/agent-harness init "My Project"` - Initialize new project
- `/agent-harness sprint "Add authentication"` - Plan sprint
- `/agent-harness code` - Start coding session
- `/agent-harness 996` - Execute parallel coding with subagent orchestration
- `/agent-harness status` - Show status

CRITICAL: Always operate on files in the current project directory, NOT in the skill directory. At the start of every workflow, run `python3 scripts/resolve_project_dir.py` to get the correct absolute path. Use this path for ALL reads/writes of `features.json` and `progress.md`.

Framework for executing complex, multi-session projects using Sprint-Coding agent cycles.

## Overview

Agent Harness enables Claude to manage long-running projects by:

- **Sprint Agent**: Plans features and breaks down requirements
- **Coding Agent**: Implements features one at a time
- **996 Agent**: Orchestrates parallel feature implementation with subagents
- **Progress Tracking**: Maintains context across sessions
- **Quality Gates**: Ensures working code at each step

## Commands

Agent Harness provides slash commands with tab completion. Type `/agent-harness` to see all commands.

### `/agent-harness`

Show available commands and usage.

**Output:**
```
Agent Harness Commands:
  /agent-harness init <name>           - Initialize new project tracking files
  /agent-harness sprint [req]          - Create or update sprint with feature breakdown
  /agent-harness code                  - Start coding session for next feature
  /agent-harness 996                   - Execute parallel coding with subagent orchestration
  /agent-harness status                - Show current project status
  /agent-harness archive               - Archive completed sprints
  /agent-harness force-archive         - Force archive ALL sprints (including incomplete)
```

### `/agent-harness init <name>`

Initialize new project tracking files.

**Example:** `/agent-harness init My App`

**Actions:**
- Create `features.json` and `progress.md`
- Run `python3 scripts/init_project.py "My App"`
- Commit the initialized files: `git add features.json progress.md && git commit -m "chore: initialize project tracking"`

### `/agent-harness sprint [requirements]`

Create or update sprint with feature breakdown.

**Examples:**
- `/agent-harness sprint` - Review current sprint and plan next
- `/agent-harness sprint Add user authentication with email and social login`
- `/agent-harness sprint Build dashboard with charts and filters`

**Actions:**
1. Archive completed sprints (if any)
2. Analyze requirements
3. Break into atomic features with acceptance criteria
4. Update **only** `features.json` and `progress.md` — do NOT create extra files like summary documents
5. Display sprint planning summary in terminal
6. Ask user to confirm the sprint plan before committing
7. After user confirms, commit: `git add features.json progress.md && git commit -m "chore: sprint planning - <sprint-name>"`
8. Read [sprint-agent.md](references/sprint-agent.md) for detailed workflow

### `/agent-harness code`

Start coding session for next feature.

**Actions:**
1. Review `progress.md` and `features.json`
2. Select next pending feature
3. Implement following session protocol
4. Commit code after implementation: `git add -A && git commit -m "feat(<scope>): <description>"`
5. Read [coding-agent.md](references/coding-agent.md) for protocol

### `/agent-harness 996`

Execute parallel coding tasks with subagent orchestration.

**Examples:**
- `/agent-harness 996` - Run parallel orchestration with default settings
- `/agent-harness 996 --max-parallel=3` - Limit to 3 concurrent subagents

**Actions:**
1. Check for uncompleted sprint
2. Analyze dependencies and file conflicts
3. Dispatch subagents for parallel execution
4. Verify results and update tracking files
5. Commit: `git add -A && git commit -m "chore: 996 orchestration complete - N features"`
6. Read [996-agent.md](references/996-agent.md) for protocol

**Use when:** You want to accelerate sprint completion by running multiple coding tasks in parallel.

### `/agent-harness status`

Show current project status.

**Output:**
- Current sprint and goal
- Feature completion statistics
- Next recommended feature
- Run `python3 scripts/status.py`

### `/agent-harness archive`

Archive completed sprints.

**Actions:**
- List completed sprints
- Move to `.agent-harness/archived/`
- Run `python3 scripts/archive_sprint.py`
- Commit: `git add -A && git commit -m "chore: archive completed sprint"`

### `/agent-harness force-archive`

Force archive ALL sprints (including incomplete ones).

**Warning:** This will archive all sprints regardless of their status.

**Actions:**
- List all sprints to be archived
- Confirm with user
- Move all to `.agent-harness/archived/`
- Run `python3 scripts/archive_sprint.py --force`
- Commit: `git add -A && git commit -m "chore: force archive all sprints"`

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

All scripts support `--project-dir` / `-p` to specify the project directory. When using slash commands, `--project-dir "$(pwd)"` is passed automatically.

```bash
python3 scripts/resolve_project_dir.py [-s dir]                # Resolve project directory
python3 scripts/init_project.py <name> [-d desc] [-p dir]     # Initialize tracking
python3 scripts/status.py [-p dir]                             # Show status
python3 scripts/validate_structure.py [-p dir]                 # Validate features.json
python3 scripts/archive_sprint.py [-p dir] [--list|--dry-run]  # Archive completed sprints
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
- **[996-agent.md](references/996-agent.md)** - 996 Agent: parallel orchestration, subagent dispatch, conflict detection

**Complete Examples:**
- **[examples.md](references/examples.md)** - Realistic examples of features.json, progress.md, and workflows
