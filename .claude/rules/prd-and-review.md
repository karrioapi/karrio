# PRD-First Workflow & Review Gates

## Mandatory PRD Rule

Every non-trivial feature MUST have a PRD before implementation begins. PRDs live in `PRDs/` at the repo root.

### When Required

- New features or modules
- Architectural changes (model splits, schema changes)
- Changes affecting multiple modules
- Database migrations with data transformation
- Breaking API changes

### When NOT Required

- Bug fixes with obvious root cause
- Dependency updates
- Typo/doc fixes
- Test-only changes

## PRD Template

Use `PRDs/TEMPLATE.md`. Key requirements:
- ASCII architecture diagrams (MANDATORY — no mermaid/images)
- Existing Code Analysis section (what was studied, what to reuse)
- Tables over prose for structured data
- Implementation plan with specific file paths
- Testing strategy following unittest/karrio test patterns

## Fresh-Context Review Gate

After implementation, a fresh-context agent should review against:

1. **PRD Compliance** — all requirements met, no scope creep
2. **Test Coverage** — every mutation/query/model has tests
3. **Code Quality** — karrio.lib usage, functional style, no anti-patterns
4. **Migration Safety** — correct ordering, data preservation
5. **Security** — tenant isolation, no hardcoded secrets

## AI Development Workflow

```
1. PRD Phase → Write PRD with ASCII diagrams, study existing code
2. Implementation → Follow conventions, write tests alongside code
3. Review Phase → Fresh-context agent reviews against PRD + checklist
4. PR Phase → Clean commits, all tests passing, PRD referenced
```
