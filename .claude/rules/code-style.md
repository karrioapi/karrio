# Code Style & Naming Conventions

## General Principles

- Write code as if the same person authored the entire codebase — consistency is paramount.
- Favor functional, declarative style: list comprehensions, `map` / `filter` / `reduce`.
- `list(dict.fromkeys(items))` for order-preserving deduplication.
- Concise but readable — no unnecessary verbosity, no cryptic one-liners.
- Never reinvent the wheel — always search for existing utilities before writing new code.

## Python

- PEP 8, 4-space indentation, format with `ruff format` (previously `black`), type-check with `mypy`.
- `snake_case` for modules/functions, `PascalCase` for classes.
- Import order: stdlib → third-party → karrio core → local/relative.
- **Always use `import karrio.lib as lib`** — NEVER the legacy `DP`, `SF`, `NF`, `DF`, `XP` utilities, and NEVER create new utility functions that duplicate `lib.*`.
- Use specific exceptions; never bare `except:` or `except Exception:`.
- No mutable default arguments — use `functools.partial` or sentinel pattern.

### Localization (i18n)

- **All user-facing strings** must use `django.utils.translation.gettext` (or `gettext_lazy`) — never hardcode messages.
- This includes: error messages, validation messages, notification text, and any string returned in API responses that users see.
- Import as `from django.utils.translation import gettext as _` and wrap strings: `_("Shipment created successfully")`.
- Internal log messages and developer-facing strings (e.g., exception names, debug logs) do NOT need `gettext`.

## TypeScript / React

- 2-space indentation, format with Prettier.
- `PascalCase` for components, `camelCase` for functions/variables.
- Functional components only — no class components; use hooks.
- Import order: React/Next → third-party → `@karrio/*` packages → local.
- Always import types from `@karrio/types` — never define inline.
- Use existing hooks from `@karrio/hooks/*` — never raw fetch/axios.
- Use existing UI components from `@karrio/ui` — never duplicate patterns.
- Never use `any` — use proper types, or `unknown` with type guards.
- Use regenerate scripts (`./bin/run-generate-on`, Next codegen) for type generation — never manually edit generated files.

## Django Models

- Tenant-scoped models inherit from `OwnedEntity` and are filtered via `Model.access_by(request)` (or `Model.objects.filter(org=request.user.org)` at the ORM level).
- System models: plain `models.Model` (no tenant scoping).
- Register with `@core.register_model` decorator when applicable.
- Use `functools.partial(core.uuid, prefix="xxx_")` for ID generation.
- JSONField defaults: `functools.partial(karrio.server.core.models._identity, value=[])` (never bare `[]`).

## Serializers

- Use mixin classes for shared logic between Account and System serializers.
- `@owned_model_serializer` for tenant-scoped serializers (handles `created_by` + `link_org()`).
- Plain serializers for system-scoped models (manual `created_by` in `create()`).
- Always use `Serializer.map()` pattern for validation + save.

## Anti-Patterns (NEVER DO)

- `pytest` — always `unittest` for SDK, `karrio test` for Django server.
- Raw SQL in migrations — use Django migration operations (`AddField`, `RemoveField`, `RenameField`, `AlterField`, `RunPython`) only.
- `RunSQL` — must work across SQLite, PostgreSQL, MySQL.
- New utility functions duplicating `karrio.lib` — check `lib.*` reference first.
- Bare exceptions, mutable defaults, `any` types.
- Class components in React — use function components + hooks.
- Manual CSS files — use Tailwind classes.
- Features not explicitly requested.
