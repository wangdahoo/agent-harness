# Sprint Agent Workflow

## Table of Contents
1. [Overview](#overview)
2. [When Invoked](#when-invoked)
3. [Input Analysis](#input-analysis)
4. [Feature Breakdown Process](#feature-breakdown-process)
5. [Feature Definition Guidelines](#feature-definition-guidelines)
6. [Dependency Management](#dependency-management)
7. [Output Requirements](#output-requirements)

## Overview

The Sprint Agent is a product planning specialist responsible for translating user requirements into structured, actionable feature lists.

## When Invoked

1. **New Project**: After initialization
2. **New Sprint**: User requests new iteration
3. **Requirement Update**: User wants to modify planned features

## Before Creating New Sprint

### Archive Completed Sprints

Before creating a new sprint, archive any completed sprints to keep `features.json` clean:

```bash
# List completed sprints
python3 scripts/archive_sprint.py --list

# Dry run to see what would be archived
python3 scripts/archive_sprint.py --dry-run

# Archive completed sprints
python3 scripts/archive_sprint.py
```

Archived sprints are moved to `.agent-harness/archived/` with:
- `features.json` - Sprint and feature data
- `progress.md` - Related session logs

### Archive Directory Structure

```
.agent-harness/
└── archived/
    └── sprint-001_authentication_20240115_143000/
        ├── features.json    # Archived sprint data
        └── progress.md      # Related sessions
```

## Input Analysis

### Requirements Breakdown

Break down user requirements into three categories:

1. **Core Features** - Essential for MVP/sprint goal
2. **Supporting Features** - Enhance core functionality
3. **Technical Enablers** - Infrastructure, refactoring

### Context Sources

- User's high-level requirements description
- Project context from existing `features.json`
- Previous sprint learnings from `progress.md`

## Feature Breakdown Process

### Step 1: Identify Core Capabilities

List the main capabilities needed:
- What user problems are being solved?
- What key functionality is required?
- What are the non-negotiable deliverables?

### Step 2: Break into Atomic Features

Each feature must be:
- **Atomic**: Completable in one session (2-4 hours)
- **Independent**: Minimal dependencies
- **Testable**: Clear acceptance criteria
- **Valuable**: Delivers user value

### Step 3: Categorize and Prioritize

Use these categories:
- `core`: Business logic, main features
- `ui`: Components, pages, styling
- `api`: API routes, data fetching
- `auth`: Authentication, authorization
- `data`: Database, models, migrations
- `infra`: Configuration, deployment, tooling

Priority levels:
- `high`: Sprint blockers, core functionality
- `medium`: Important but not blocking
- `low`: Nice to have, can be deferred

### Step 4: Define Acceptance Criteria

Each criterion should follow:
```
Given [context], when [action], then [outcome]
```

Example:
```
Given a user is logged in, when they click "Add to Cart", 
then the item should appear in their cart with correct quantity.
```

## Feature Definition Guidelines

### Required Fields

```json
{
  "id": "s1-feat-001",
  "category": "core | ui | api | auth | data | infra",
  "priority": "high | medium | low",
  "title": "Short feature title",
  "description": "Detailed description",
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "technical_notes": "Implementation hints",
  "status": "pending",
  "dependencies": [],
  "estimated_complexity": "small | medium | large",
  "files_affected": ["path/to/file.ts"]
}
```

### Complexity Estimation

- **small**: < 2 hours, simple changes
- **medium**: 2-4 hours, moderate complexity
- **large**: 4+ hours, break into smaller features

### Dependencies

Mark dependencies clearly:
```json
"dependencies": ["s1-feat-001", "s1-feat-002"]
```

## Dependency Management

### Ordering Rules

1. Order features by dependencies
2. Infrastructure first, then features
3. Core before supporting features
4. UI after backend support

### Blocking Identification

- Features with dependencies must wait
- Parallel features have no mutual dependencies
- Critical path: longest dependency chain

### Suggested Implementation Order

```
1. [infra-001] Setup authentication provider
2. [auth-001] Configure auth middleware
3. [ui-001] Create login page
4. [core-001] Implement login logic
5. [ui-002] Create dashboard
6. [core-002] Implement dashboard data fetching
```

## Output Requirements

### Update features.json

Add new sprint with structured features. See `references/file-structure.md` for schema.

### Update progress.md

Add planning session entry:

```markdown
## Sprint Planning - YYYY-MM-DD
**Agent**: Sprint Agent
**Sprint**: [Sprint ID and Name]

### Requirements Received
- [User's requirement summary]

### Features Planned
- Total: N features
- High priority: N
- Medium priority: N
- Low priority: N

### Sprint Goal
[Clear goal statement]

### Implementation Order
1. [feature-id] - [title]
2. [feature-id] - [title]

### Notes
[Any context or decisions]
```

### Summary Output Format

```
## Sprint Planning Complete

### Sprint: [Name]
**Goal**: [Sprint goal]

### Feature Summary
- Total features: N
- High priority: N (list IDs)
- Medium priority: N
- Low priority: N

### Recommended Implementation Order
1. [id] [title] - [complexity]
2. [id] [title] - [complexity]

### Dependencies
- [id] depends on [id]
- No blockers for: [ids]

### Ready for Development
Run the Coding Agent with the first pending feature: [first-feature-id]
```

## Critical Rules

1. **Never Remove Features** - Only add or change status
2. **Unique IDs** - Each feature must have a unique ID
3. **Respect Tech Stack** - Features must be achievable
4. **Balance Sprint** - Mix of complexity levels
5. **Document Decisions** - Explain prioritization rationale
