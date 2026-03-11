# Skill: Create PRD

Write a Product Requirements Document before implementing any non-trivial feature.

## When to Use

- Before any new feature implementation
- Before architectural changes or model refactors
- Before changes affecting multiple modules
- Before database migrations with data transformations

## PRD Location

All PRDs go in `PRDs/` at the repo root. Use the template at `PRDs/TEMPLATE.md`.

## Process

### 1. Research Phase

Before writing the PRD:

```
a) Study existing code that will be affected
   - Read relevant models, serializers, types, mutations
   - Understand current data flow and architecture
   - Document what exists in "Existing Code Analysis" section

b) Study similar implementations in the codebase
   - Find analogous patterns (e.g., how SystemConnection parallels what you need)
   - Note reusable components, mixins, utilities from karrio.lib

c) Check if this can be an extension module (for downstream repos)
   - Can @pre_processing or AppConfig.ready() support this?
   - Would a hook pattern avoid modifying core?
```

### 2. Draft Phase

Create `PRDs/<FEATURE_NAME>.md` using the template. Key requirements:

- **ASCII diagrams are MANDATORY** — no mermaid, no image links, no external tools
- **Existing Code Analysis** section must show what code was studied
- **Tables over prose** for comparisons, field references, risk assessments
- **Implementation plan** must list specific file paths and phases
- **Testing strategy** must follow unittest/karrio test patterns (NEVER pytest)

### 3. Architecture Diagram Guidelines

Always use ASCII box-drawing characters:

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Box 1   │─>│ Box 2   │─>│ Box 3   │
└─────────┘  └────┬────┘  └─────────┘
                  │
                  ▼
             ┌─────────┐
             │ Box 4   │
             └─────────┘
```

Characters to use: `┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼ ► ▼ ◄ ▲ ──> <──`

### 4. Review & Iterate

- Identify gaps and open questions
- Ask clarifying questions before implementation
- Get approval on the PRD before writing code

## Template Sections (Quick Reference)

1. **Metadata** — project, version, date, status, owner, type
2. **Executive Summary** — 2-3 sentences + key decisions + scope
3. **Open Questions** — pending decisions, edge cases
4. **Problem Statement** — current state (code), desired state (code)
5. **Goals & Success Criteria** — goals, metrics table, launch criteria
6. **Alternatives Considered** — table with pros/cons/decision
7. **Technical Design** — ASCII diagrams, models, API changes
8. **Edge Cases & Failure Modes** — table format
9. **Implementation Plan** — phased with files and effort
10. **Testing Strategy** — unittest patterns, test cases with code
11. **Risk Assessment** — impact/probability/mitigation table
12. **Migration & Rollback** — backward compatibility, data safety

## Naming Convention

Use `SCREAMING_SNAKE_CASE` for PRD filenames: `PRDs/FEATURE_NAME.md`
