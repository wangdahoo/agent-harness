# Sprint Agent Reference

## Table of Contents
1. [Workflow](#workflow)
2. [Feature Breakdown](#feature-breakdown)
3. [File Schemas](#file-schemas)
4. [Examples](#examples)

## Workflow

### When Invoked

1. **New Project**: After initialization
2. **New Sprint**: User requests new iteration
3. **Requirement Update**: User wants to modify planned features

### Archive Completed Sprints First

Before creating a new sprint, archive completed sprints:

```bash
python3 scripts/archive_sprint.py --list      # List completed sprints
python3 scripts/archive_sprint.py --dry-run   # Preview archive
python3 scripts/archive_sprint.py             # Archive
```

Archived sprints move to `.agent-harness/archived/`.

### Planning Process

#### Step 1: Analyze Requirements

Break down requirements into categories:

- **Core Features** - Essential for MVP/sprint goal
- **Supporting Features** - Enhance core functionality
- **Technical Enablers** - Infrastructure, refactoring

Context sources:
- User's high-level requirements
- Existing `features.json`
- Previous sprint learnings from `progress.md`

#### Step 2: Create Atomic Features

Each feature must be:

- **Atomic**: Completable in one session (2-4 hours)
- **Independent**: Minimal dependencies
- **Testable**: Clear acceptance criteria
- **Valuable**: Delivers user value

#### Step 3: Categorize and Prioritize

Categories: `core`, `ui`, `api`, `auth`, `data`, `infra`

Priorities:
- `high`: Sprint blockers, core functionality
- `medium`: Important but not blocking
- `low`: Nice to have, can be deferred

#### Step 4: Define Acceptance Criteria

Format: `Given [context], when [action], then [outcome]`

Example: `Given a user is logged in, when they click "Add to Cart", then the item should appear in their cart with correct quantity.`

#### Step 5: Order by Dependencies

Rules:
1. Infrastructure first, then features
2. Core before supporting features
3. UI after backend support
4. Features with dependencies must wait

## Feature Breakdown

### Feature Definition

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

Mark dependencies with feature IDs:

```json
"dependencies": ["s1-feat-001", "s1-feat-002"]
```

## File Schemas

### features.json Structure

```json
{
  "project": {
    "name": "string (required)",
    "description": "string (required)",
    "tech_stack": ["string"],
    "created_at": "YYYY-MM-DD (required)"
  },
  "sprints": [
    {
      "id": "string (required, unique)",
      "name": "string (required)",
      "goal": "string",
      "status": "planning | in_progress | completed | on_hold",
      "created_at": "YYYY-MM-DD",
      "features": [ /* feature objects */ ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "last_updated": "YYYY-MM-DD"
  }
}
```

### Sprint Status Values

| Status | Description |
|--------|-------------|
| `planning` | Being defined |
| `in_progress` | Features being implemented |
| `completed` | All features done |
| `on_hold` | Temporarily paused |

### Feature Status Values

| Status | Description |
|--------|-------------|
| `pending` | Not started |
| `in_progress` | Currently being worked on |
| `completed` | Fully implemented and tested |
| `blocked` | Cannot proceed |

### Category Definitions

| Category | Description |
|----------|-------------|
| `core` | Business logic, main features |
| `ui` | User interface, components |
| `api` | API routes, data fetching |
| `auth` | Authentication, authorization |
| `data` | Database, models, migrations |
| `infra` | Configuration, deployment, tooling |

## Examples

See [examples.md](examples.md) for complete examples.

## Output Requirements

### Update features.json

Add new sprint with structured features following schema above.

### Update progress.md

Add planning session entry at top:

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

```markdown
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
