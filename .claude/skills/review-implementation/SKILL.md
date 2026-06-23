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

- [ ] Every new mutation/query/endpoint has a corresponding test
- [ ] Every model change has a migration test
- [ ] Tests use `assertResponseNoErrors` + `assertDictEqual` pattern
- [ ] No `pytest` usage anywhere in new code
- [ ] `mock.ANY` used for dynamic fields (id, timestamps)
- [ ] Carrier tests follow the 4-method pattern (if carrier work)
- [ ] Imports at top of test file — never inside a test method

### 4. Extension Pattern Check

- [ ] New domain logic lives in `modules/<name>/`, not sprinkled across `modules/core` / `modules/graph` / `modules/manager`
- [ ] Hooks used where applicable (`@pre_processing`, `AppConfig.ready()`)
- [ ] New modules follow the pattern in `.claude/rules/extension-patterns.md`
- [ ] Module registered in `requirements.build.txt` (`-e ./modules/<name>`) AND in `bin/run-server-tests`

### 5. Code Quality Check

Review each changed file for:

- [ ] Uses `import karrio.lib as lib` — no legacy `DP`/`SF`/`NF`/`DF`/`XP`
- [ ] Functional style (list comprehensions, `map`/`filter`) rather than imperative loops
- [ ] No bare `except:` / `except Exception:` — specific exceptions only
- [ ] No mutable default arguments
- [ ] No `any` types in TypeScript
- [ ] Django: `OwnedEntity` for tenant-scoped models, plain `Model` for system models
- [ ] GraphQL: `utils.Connection[T]` for lists, `@authentication_required` on resolvers
- [ ] No manually edited auto-generated files (`mapper.py`, `karrio/schemas/<carrier>/*`, `packages/karriojs/api/generated/*`)
- [ ] User-facing strings wrapped in `gettext`

### 6. N+1 Query Prevention Check

**CRITICAL**: N+1 queries are the #1 performance killer. Check every changed model, serializer, and view. Full patterns in `.claude/rules/django-patterns.md`.

**New models:**
- [ ] Custom manager with `get_queryset()` that applies `select_related` / `prefetch_related`
- [ ] ForeignKey fields have `select_related` in the manager
- [ ] Reverse FK / M2M fields have `prefetch_related` in the manager

**Serializers / GraphQL types:**
- [ ] No FK access (e.g., `obj.carrier.name`) without corresponding `select_related` in the queryset
- [ ] No reverse FK iteration (e.g., `obj.items.all()`) without `prefetch_related`
- [ ] Computed `@strawberry.field` methods don't trigger per-row queries

**Views / Resolvers:**
- [ ] List views use optimized querysets (via manager or explicit `.select_related()`)
- [ ] No `Model.objects.get(pk=pk)` inside loops — batch with `filter(pk__in=pks)`

**Bulk operations:**
- [ ] No `for x in data: Model.objects.create()` — use `bulk_create()`
- [ ] No `for x in qs: x.save()` — use `bulk_update()`

**Red flags to grep for:**

```bash
git diff main...HEAD -U0 | grep -E '\.(save|create)\(' | head -20
git diff main...HEAD -U0 | grep -E '\.objects\.(get|filter)' | head -20
git diff main...HEAD -U0 | grep -E '\.all\(\)' | head -20
```

### 7. Migration Safety Check (if migrations exist)

- [ ] Operations ordered correctly (create table before data migration before column removal)
- [ ] Data migrations preserve existing data
- [ ] Dependencies include all prerequisite migrations
- [ ] No `RunSQL` — uses Django operations only
- [ ] Works across SQLite, PostgreSQL, MySQL
- [ ] Rolling-deploy safe (no removals that crash running pods on older code)

### 8. Security Check

- [ ] No hardcoded secrets or credentials
- [ ] Tenant isolation: all queries filtered by `org=request.user.org`
- [ ] No raw SQL injection vectors
- [ ] Input validation at system boundaries (serializers, GraphQL inputs)
- [ ] Sensitive fields not logged / tracked in request recordings

## Output Format

Report findings as:

```
## Review Summary

### Status: PASS / NEEDS CHANGES

### Findings
1. [PASS] PRD compliance — all requirements met
2. [FAIL] Missing test for `delete_rate_sheet` mutation
3. [WARN] Consider using mixin pattern for shared serializer logic
4. [FAIL] `obj.carrier.name` accessed in serializer without `select_related`

### Required Actions
- Add test for delete mutation in `modules/<module>/karrio/server/<module>/tests/`
- Add `select_related("carrier")` to the serializer's base queryset
```
