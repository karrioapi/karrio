# Skill: Review Implementation

Perform a fresh-context review of completed work against PRD, tests, and conventions.

## When to Use

- After implementation is complete, before creating a PR
- As a quality gate before merging
- When reviewing someone else's changes

## Process

### 1. Gather Context

```bash
# See all changes
git diff main...HEAD --stat
git log main...HEAD --oneline

# Read the PRD (if one exists)
ls PRDs/
```

### 2. PRD Compliance Check

- [ ] All requirements from PRD are implemented
- [ ] No scope creep — nothing beyond PRD spec
- [ ] Architecture matches PRD diagrams
- [ ] All phases from implementation plan are complete

### 3. Test Coverage Check

```bash
# Run relevant tests
./bin/run-server-tests
./bin/run-sdk-tests

# Verify test files were added/updated
git diff main...HEAD --name-only | grep -i test
```

- [ ] Every new mutation/query has a corresponding test
- [ ] Every model change has a migration test
- [ ] Tests use `assertResponseNoErrors` + `assertDictEqual` pattern
- [ ] No `pytest` usage anywhere in new code
- [ ] `mock.ANY` used for dynamic fields (id, timestamps)
- [ ] Carrier tests follow 4-method pattern (if carrier work)

### 4. Code Quality Check

Review each changed file for:

- [ ] Uses `import karrio.lib as lib` (not legacy utilities)
- [ ] Functional style (list comprehensions, map/filter)
- [ ] No bare exceptions, mutable defaults, `any` types
- [ ] Django: `OwnedEntity` for tenant-scoped, N+1 prevention
- [ ] GraphQL: `utils.Connection[T]` for lists, proper decorators
- [ ] No manually edited auto-generated files

### 5. Migration Safety Check (if applicable)

- [ ] Operations ordered correctly
- [ ] Data migrations preserve existing data
- [ ] No `RunSQL` — Django operations only
- [ ] Works across SQLite, PostgreSQL, MySQL

### 6. Security Check

- [ ] No hardcoded secrets
- [ ] Tenant isolation (queries filtered by org)
- [ ] Input validation at boundaries

## Output Format

```
## Review Summary

### Status: PASS / NEEDS CHANGES

### Findings
1. [PASS] PRD compliance — all requirements met
2. [FAIL] Missing test for delete mutation
3. [WARN] Consider using mixin for shared logic

### Required Actions
- Add test for delete mutation
```
