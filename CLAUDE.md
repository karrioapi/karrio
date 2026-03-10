# Claude Code Instructions

## Architecture

Karrio is a **universal shipping API** monorepo:
- **Backend**: Django API (`apps/api/`), carrier connectors (`modules/connectors/`), core modules (`modules/`)
- **Frontend**: Next.js dashboard (`apps/dashboard/`), shared packages (`packages/`)
- **Scripts**: `bin/` — setup, testing, release, schema generation
- **Submodules**: `ee/insiders`, `ee/platform`, `community`

## Essential Conventions

- **Always use `import karrio.lib as lib`** — never legacy utilities (`DP`, `SF`, `NF`)
- **Functional style**: `map`, `filter`, comprehensions over imperative loops
- **No pytest** — use `unittest` (SDK) and `karrio test` (Django)
- **Never edit generated files** — `mapper.py`, `karrio/schemas/<carrier>/*.py` are auto-generated
- **Schema generation**: edit `schemas/*.json`, run `./bin/run-generate-on modules/connectors/<carrier>`
- **Multi-tenancy**: always filter by org context (`Shipment.objects.filter(org=request.user.org)`)
- **N+1 prevention**: `select_related()`, `prefetch_related()`, `bulk_update()`

## Key Commands

```bash
source bin/activate-env                                          # Activate Python env
./bin/run-sdk-tests                                              # All SDK + connector tests
python -m unittest discover -v -f modules/connectors/<c>/tests   # Single carrier tests
./bin/run-server-tests                                           # All Django tests
karrio test --failfast karrio.server.<module>.tests              # Single Django module
./bin/start                                                      # API (5002) + Worker
npm run build                                                    # Turbo build all
```

## Debugging

- Add `print(response.data)` before assertions in failing Django tests — remove when passing
- `lib.to_dict()` strips `None` and empty strings — expected fixtures shouldn't include them
- `lib.failsafe()` swallows exceptions — remove temporarily to see actual errors
- `str(None)` returns `"None"` — guard with truthy check first

## Commit Rules

- Format: `type(scope): summary` — never commit without user permission
- Never add `Co-Authored-By` lines
- Run tests before pushing

## Detailed Rules

Scoped rules are in `.claude/rules/`:
- `code-style.md` — naming, imports, formatting
- `testing.md` — test commands, patterns, fixtures
- `git-workflow.md` — commits, submodules, changelog
- `django-patterns.md` — multi-tenancy, N+1, migrations, Huey jobs
- `carrier-integration.md` — connector structure, definition of done

## Skills

Skills in `.claude/skills/` provide step-by-step guides:
- `carrier-integration/` — Full carrier connector implementation (5 phases)
- `release/` — Version bumping, package sync, frozen requirements, changelog
- `debugging/` — Request lifecycle, debugging commands, common pitfalls
- `project-setup/` — Environment setup, running servers, schema generation

## Full Reference

- [AGENTS.md](./AGENTS.md) — Comprehensive conventions, utilities reference, domain context
- [CARRIER_INTEGRATION_GUIDE.md](./CARRIER_INTEGRATION_GUIDE.md) — Carrier-specific integration guide
