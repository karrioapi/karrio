# Extension Patterns — "Extend, Don't Modify Core"

## The Golden Rule

Karrio is modular by design: `modules/core`, `modules/graph`, `modules/admin` form the server core; `modules/connectors/*` are plugins; everything else (`modules/orders`, `modules/data`, `modules/documents`, `modules/events`, `modules/pricing`, `modules/manager`, ...) is an auto-discovered extension module.

**Prefer adding a new extension module over modifying an existing one.** Modify a core module only when the feature is genuinely generic and benefits all karrio deployments.

## Decision Tree

```
Is this feature specific to one domain (orders, documents, pricing, …)?
  YES -> Extend or create the relevant modules/<name>/ package
  NO  -> Is it a bug fix in an existing module?
    YES -> Fix in that module, isolate to a clean commit
    NO  -> Is it a new generic capability the server always needs?
      YES -> Add to modules/core or modules/graph
      NO  -> Create a new extension module in modules/<name>/
```

## The Extension Module Pattern

### Architecture

```
                    ┌────────────────────────────────────────┐
                    │               karrio/                  │
                    │                                        │
                    │  modules/                              │
                    │  ├── core/      (OSS core)             │
                    │  ├── graph/     (OSS graph)            │
                    │  ├── admin/     (OSS admin)            │
                    │  ├── manager/                          │
                    │  ├── orders/                           │
                    │  ├── data/                             │
                    │  ├── documents/                        │
                    │  ├── events/                           │
                    │  ├── pricing/                          │
                    │  ├── connectors/*/  (carrier plugins)  │
                    │  └── <your-module>/                    │
                    │         │                              │
                    │         │ hooks via                     │
                    │         │ AppConfig.ready()             │
                    │         ▼                              │
                    │  ┌────────────────────┐                │
                    │  │  core hook points  │                │
                    │  │  @pre_processing    │                │
                    │  │  pkgutil discover  │                │
                    │  │  INSTALLED_APPS    │                │
                    │  └────────────────────┘                │
                    └────────────────────────────────────────┘
```

### Canonical Examples

Study these before creating new extensions:

- `modules/orders/karrio/server/orders/` — domain module with REST + GraphQL + signals
- `modules/events/karrio/server/events/` — webhook/event delivery module with Huey task registration
- `modules/documents/karrio/server/documents/` — module that registers its own auto-discovered URLs
- `modules/graph/karrio/server/graph/schemas/base/` — reference GraphQL module layout (base schemas for the whole server)

### Module File Organization

Keep `__init__.py` as a **thin interface definition** — just `Query` field declarations and `Mutation` one-liner delegations. All resolver logic belongs in `types.py` and `mutations.py`.

**Canonical reference:** `modules/graph/karrio/server/graph/schemas/base/__init__.py`

- **`__init__.py`** — Interface only. `Query` uses `strawberry.field(resolver=types.XType.resolve)`. `Mutation` methods are one-liners that delegate to `mutations.XMutation.mutate()`. No business logic, no imports of domain modules.
- **`types.py`** — Strawberry types with `resolve` / `resolve_list` static methods containing query logic.
- **`inputs.py`** — Strawberry input types and filters.
- **`mutations.py`** — Mutation classes with `mutate()` static methods containing mutation logic.
- **`datatypes.py`** — `@attr.s(auto_attribs=True)` dataclasses for structured data flowing through the module. Prefer typed attributes over raw dicts.
- **`utils.py`** — Reusable helper functions (payload builders, transformers, formatters, availability decorators). **Must not import from `types.py` or `mutations.py`** — see dependency rule below.

```
modules/<name>/karrio/server/graph/schemas/<name>/
├── __init__.py      # Thin interface: Query fields + Mutation delegators
├── types.py         # Strawberry types + resolve/resolve_list methods
├── inputs.py        # Strawberry input types and filters
├── mutations.py     # Mutation classes + mutate() methods
├── datatypes.py     # @attr.s dataclasses for typed data
└── utils.py         # Business logic, payload builders, decorators
```

### Dependency Direction (one-way only)

Imports between schema files must flow in one direction. Circular imports between these files cause silent schema registration failures (`schema.py` catches the error and skips the module).

```
__init__.py ──→ types.py ──→ utils.py
            ──→ mutations.py ──→ utils.py
            ──→ inputs.py
```

- **`utils.py`** must never import `types.py` or `mutations.py`.
- **`types.py`** must never import `mutations.py` (or vice versa).
- Factory methods that construct a GraphQL type belong as **static methods on the type itself** (e.g., `ShipmentType.parse(...)`), not in `utils.py`.

```python
# ✅ Good — type knows how to construct itself
@strawberry.type
class ItemType:
    id: int
    name: str

    @staticmethod
    def parse(raw: dict) -> "ItemType":
        return ItemType(id=raw["id"], name=raw.get("name", ""))

# ❌ Bad — utils.py imports types.py, creating circular dependency
# utils.py
import karrio.server.graph.schemas.items.types as types
def enrich_item(raw: dict) -> types.ItemType:  # circular!
    return types.ItemType(...)
```

```python
# ✅ Good __init__.py — thin interface
@strawberry.type
class Query:
    items: typing.List[types.ItemType] = strawberry.field(
        resolver=types.ItemType.resolve_list
    )
    item: typing.Optional[types.ItemType] = strawberry.field(
        resolver=types.ItemType.resolve
    )

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_item(self, info: Info, input: inputs.CreateItemInput) -> mutations.CreateItemMutation:
        return mutations.CreateItemMutation.mutate(info, **input.__dict__)

# ❌ Bad __init__.py — inline resolver logic
@strawberry.type
class Query:
    @strawberry.field
    @staticmethod
    def items(info: Info) -> typing.List[types.ItemType]:
        # 50 lines of business logic...
```

### Hook Registration Pattern

```python
# apps.py
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    name = "karrio.server.orders"

    def ready(self):
        from karrio.server.orders import signals  # noqa: registers signal handlers
        # Append validation hooks to a core serializer's pre_process_functions:
        # from karrio.server.manager.serializers import ShipmentSerializer
        # ShipmentSerializer.pre_process_functions.append(validators.validate_order_link)
```

### Settings Auto-Discovery

```python
# modules/<name>/karrio/server/settings/<name>.py
from karrio.server.settings.base import *  # noqa

INSTALLED_APPS += ["karrio.server.<name>"]
KARRIO_URLS += ["karrio.server.<name>.urls"]  # if module has REST endpoints
```

Karrio discovers settings modules via `importlib.util.find_spec()` at startup. Your settings file runs only if the module is installed via `-e ./modules/<name>` in `requirements.build.txt`.

### GraphQL Extension (Auto-Discovery)

```python
# modules/<name>/karrio/server/graph/schemas/<name>/__init__.py
import strawberry
import typing
from strawberry.types import Info

@strawberry.type
class Query:
    # Fields auto-merged into root Query via pkgutil.iter_modules()
    ...

@strawberry.type
class Mutation:
    # Fields auto-merged into root Mutation
    ...

extra_types: typing.List = []  # required even if empty
```

### Namespace Packages — NEVER Add `__init__.py` to Shared Paths

Karrio uses **implicit namespace packages** (`pkgutil.extend_path`) so that multiple installed packages can contribute to the same Python namespace (e.g., `karrio.server.graph.schemas`). The core packages (`modules/graph/`, `modules/admin/`, etc.) already define the namespace roots.

**NEVER add `__init__.py` files to namespace paths that are owned by another package.** Doing so converts the implicit namespace package into a regular package, which shadows the core package and breaks `pkgutil.iter_modules()` discovery.

```
# ❌ WRONG — adding __init__.py to a namespace owned by core graph
modules/<yourmod>/karrio/server/graph/__init__.py            # breaks karrio.server.graph
modules/<yourmod>/karrio/server/graph/schemas/__init__.py    # breaks schema discovery

# ✅ CORRECT — only add __init__.py inside your module's own leaf directory
modules/<yourmod>/karrio/server/graph/schemas/<yourmod>/__init__.py  # leaf: your schema module
modules/<yourmod>/karrio/server/<yourmod>/__init__.py                # leaf: your module root
```

**Rule of thumb:** if a directory path already exists in another installed module (e.g., `modules/graph/karrio/server/graph/`), do NOT create an `__init__.py` at that same path in your extension module. Only the **leaf directory** unique to your module gets `__init__.py`.

### Core Hook Points

| Hook | Location | Purpose |
|------|----------|---------|
| `@pre_processing` | `karrio.server.core.utils` | Append validators to serializer pipelines |
| `AppConfig.ready()` | Django app startup | Register hooks, signal handlers |
| `pkgutil.iter_modules()` | `graph/schema.py`, `admin/schema.py` | Auto-discover GraphQL schemas |
| `importlib.util.find_spec()` | `settings/base.py` | Auto-discover settings modules |
| `KARRIO_URLS` | `settings/base.py` | Register REST URL patterns |
| `huey` task registry | `karrio.server.events.task_definitions` | Auto-discovered background tasks |

## Creating a New Extension Module

1. Create directory: `modules/<name>/karrio/server/<name>/`.
2. Add `apps.py` with `AppConfig` and optional `ready()` hook.
3. Add `karrio/server/settings/<name>.py` for auto-discovery.
4. Add GraphQL schemas under `karrio/server/graph/schemas/<name>/` or `karrio/server/admin/schemas/<name>/` (admin is OSS-side; NOT `ee/insiders/modules/admin`).
5. **Do NOT add `__init__.py` to shared namespace paths** (e.g., `karrio/server/graph/`, `karrio/server/admin/`) — only the leaf directory unique to your module gets `__init__.py` (see "Namespace Packages" above).
6. Add tests under `modules/<name>/karrio/server/<name>/tests/`.
7. **Add `karrio.server.<name>.tests` to `bin/run-server-tests`** — without this, tests pass locally but never run in CI.
8. **Add `-e ./modules/<name>` to `requirements.build.txt`** — without this the module is not installed in Docker images and schema discovery silently skips it.
9. Use the `create-extension-module` skill for scaffolding.

## Connectors vs Extension Modules

Carrier connectors under `modules/connectors/*/` follow a separate structure documented in [`carrier-integration.md`](./carrier-integration.md) — use `./bin/cli sdk add-extension` to scaffold. Do NOT use the extension-module pattern for carriers.
