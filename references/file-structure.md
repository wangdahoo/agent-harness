# File Structure and Schema

## Table of Contents
1. [Core Files](#core-files)
2. [features.json Schema](#featuresjson-schema)
3. [progress.md Structure](#progressmd-structure)
4. [File Locations](#file-locations)

## Core Files

| File | Purpose | Created By |
|------|---------|-----------|
| `features.json` | Sprint and feature tracking | Sprint Agent |
| `progress.md` | Session-by-session log | All Agents |
| `AGENTS.md` | Agent instructions | User/Initialization |

## features.json Schema

### Complete Schema

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
      "features": [
        {
          "id": "string (required, unique)",
          "category": "core | ui | api | auth | data | infra",
          "priority": "high | medium | low",
          "title": "string (required)",
          "description": "string (required)",
          "acceptance_criteria": ["string"],
          "technical_notes": "string",
          "status": "pending | in_progress | completed | blocked",
          "dependencies": ["feature-id"],
          "estimated_complexity": "small | medium | large",
          "files_affected": ["path/to/file"]
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "last_updated": "YYYY-MM-DD"
  }
}
```

### Field Descriptions

#### Project Section

- `name`: Project identifier
- `description`: Brief project description
- `tech_stack`: Array of technologies
- `created_at`: ISO date string

#### Sprint Section

- `id`: Unique sprint identifier (e.g., "sprint-001")
- `name`: Human-readable sprint name
- `goal`: Clear sprint objective
- `status`: Current sprint state
  - `planning`: Being defined
  - `in_progress`: Features being implemented
  - `completed`: All features done
  - `on_hold`: Temporarily paused
- `created_at`: Sprint start date

#### Feature Section

- `id`: Unique feature identifier (e.g., "s1-feat-001")
- `category`: Feature type
  - `core`: Business logic
  - `ui`: User interface
  - `api`: API endpoints
  - `auth`: Authentication/authorization
  - `data`: Database/models
  - `infra`: Infrastructure/config
- `priority`: Feature importance
  - `high`: Blocker or essential
  - `medium`: Important but not blocking
  - `low`: Nice to have
- `title`: Short feature name
- `description`: Detailed feature description
- `acceptance_criteria`: Array of testable criteria
- `technical_notes`: Implementation hints
- `status`: Current feature state
  - `pending`: Not started
  - `in_progress`: Currently being worked on
  - `completed`: Fully implemented and tested
  - `blocked`: Cannot proceed
- `dependencies`: Array of feature IDs this depends on
- `estimated_complexity`: Size estimate
  - `small`: < 2 hours
  - `medium`: 2-4 hours
  - `large`: 4+ hours
- `files_affected`: Files that will be modified

## progress.md Structure

### Template

```markdown
# Project Progress Log

This file tracks the progress of all agent sessions.

---

## Session Template

```markdown
## Session N - YYYY-MM-DD
**Agent**: Sprint | Coding
**Sprint**: [Sprint ID if applicable]
**Feature**: [Feature ID if applicable]

### Work Completed
- [What was implemented or done]

### Tests Performed
- [How changes were verified]

### Issues Encountered
- [Any blockers, bugs, or challenges]

### Decisions Made
- [Architectural or design choices]

### Next Steps
- [Recommended next actions]
```

---

## Sessions

<!-- New sessions added above this line -->
```

### Entry Types

**Sprint Planning Entry:**
```markdown
## Sprint Planning - YYYY-MM-DD
**Agent**: Sprint Agent
**Sprint**: sprint-001 - Authentication Sprint

### Requirements Received
- User authentication with email/password
- Social login with Google and GitHub
- Password reset functionality

### Features Planned
- Total: 8 features
- High priority: 5
- Medium priority: 2
- Low priority: 1

### Sprint Goal
Implement complete user authentication flow including social login

### Implementation Order
1. s1-feat-001 - Setup auth provider (infra)
2. s1-feat-002 - Create login UI (ui)
3. s1-feat-003 - Implement login logic (core)
...
```

**Coding Session Entry:**
```markdown
## Session 3 - 2024-01-15
**Agent**: Coding Agent
**Sprint**: sprint-001
**Feature**: s1-feat-003 - Implement login logic

### Implementation
- Added login API route at /api/auth/login
- Implemented JWT token generation
- Added password validation with bcrypt

### Files Changed
- src/app/api/auth/login/route.ts - New login endpoint
- src/lib/auth.ts - Token generation utilities
- src/lib/validators.ts - Password validation

### Tests Performed
- Tested login with valid credentials ✓
- Tested login with invalid password ✓
- Tested login with non-existent user ✓
- Verified token expiration ✓

### Issues Encountered
- Initial bcrypt import error, resolved by using bcryptjs

### Acceptance Criteria Status
- [x] Login endpoint returns JWT on success
- [x] Invalid credentials return 401
- [x] Token includes user ID and expiration

### Next Steps
- Ready for s1-feat-004: Session management
```

## File Locations

### Standard Location

All tracking files should be in the **project root**:

```
project-root/
├── features.json
├── progress.md
├── AGENTS.md
├── .agent-harness/
│   └── archived/           # Archived completed sprints
│       └── sprint-001_*/
│           ├── features.json
│           └── progress.md
├── src/
├── public/
└── package.json
```

### Archived Sprints

Completed sprints are archived to `.agent-harness/archived/` to keep `features.json` clean.

**Archive command:**
```bash
python3 scripts/archive_sprint.py
```

**Archive folder naming:** `{sprint-id}_{sprint-name}_{timestamp}`

**Archived files:**
- `features.json` - Sprint data with metadata
- `progress.md` - Sessions related to that sprint

### Initialization

Use the init script to create files:

```bash
python3 scripts/init_project.py "My Project" -d "Description"
```

This creates:
- `features.json` - From template
- `progress.md` - From template

### Validation

Validate structure:

```bash
python3 scripts/validate_structure.py
```

Checks:
- Required fields present
- Valid status values
- Correct JSON structure
- Feature ID uniqueness

## Best Practices

### features.json

1. **Never delete features** - Only change status
2. **Use descriptive IDs** - `s1-feat-001` not `feat1`
3. **Keep descriptions clear** - Avoid ambiguity
4. **Update last_updated** - On every change
5. **Include all fields** - Even if optional

### progress.md

1. **Add entries at top** - Most recent first
2. **Be specific** - Not vague summaries
3. **Include failures** - Not just successes
4. **Document decisions** - Why choices were made
5. **Link to features** - Reference feature IDs

### AGENTS.md

1. **Project-specific** - Not generic instructions
2. **Include tech stack** - Actual technologies used
3. **Define conventions** - Code style, naming
4. **Keep updated** - Reflect current practices
5. **Be concise** - Agents read this every session
