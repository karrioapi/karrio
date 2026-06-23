# Skill: Django GraphQL Development

Add queries, mutations, types, and inputs to karrio's Strawberry GraphQL schema.

## When to Use

- Adding new GraphQL queries or mutations
- Creating new Strawberry types for existing Django models
- Extending the base (tenant) or admin (system) graph
- Adding GraphQL endpoints from an extension module (e.g. `orders`, `pricing`, `documents`)

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    GraphQL Request                           │
│                                                              │
│  Client ──POST /graphql──> schema.py ──> Query/Mutation      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  schema.py:                                            │  │
│  │    pkgutil.iter_modules(schemas.__path__)              │  │
│  │    → collects Query, Mutation, extra_types per module  │  │
│  │    → class Query(*QUERIES):  pass                      │  │
│  │    → class Mutation(*MUTATIONS):  pass                 │  │
│  └────────────────────────┬───────────────────────────────┘  │
│                           │                                   │
│       ┌───────────────────┼───────────────────┐              │
│       ▼                   ▼                   ▼               │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────┐      │
│  │schemas/  │     │<ext>/    │     │admin/schemas/    │      │
│  │base/     │     │schemas/  │     │base/             │      │
│  │  __init__│     │  <ext>/  │     │  __init__        │      │
│  │  types   │     │          │     │  types           │      │
│  │  inputs  │     │          │     │  inputs          │      │
│  │  mutations│     │          │     │  mutations       │      │
│  └────┬─────┘     └──────────┘     └──────────────────┘      │
│       │                                                       │
│       ▼                                                       │
│  Model.access_by(request)  ──>  DRF Serializer  ──>  save()  │
└──────────────────────────────────────────────────────────────┘
```

Relevant files:

- `modules/graph/karrio/server/graph/schema.py` — auto-discovery via `pkgutil.iter_modules`
- `modules/graph/karrio/server/graph/schemas/base/` — canonical tenant schema (users, shipments, trackers, carriers, rate sheets, metafields, …)
- `modules/admin/karrio/server/admin/schemas/base/` — canonical system-admin schema
- `modules/graph/karrio/server/graph/utils.py` — `BaseInput`, `BaseMutation`, `Paginated`, `Connection[T]`, `paginated_connection`, `is_unset`, `authentication_required`, `password_required`, `error_wrapper`
- `modules/admin/karrio/server/admin/utils.py` — `staff_required`, `superuser_required`

## Two Schema Domains

| Aspect           | Base graph (tenant)                 | Admin graph (system)                |
| ---------------- | ----------------------------------- | ----------------------------------- |
| URL              | `/graphql`                          | `/admin/graphql`                    |
| Scope            | Tenant (per-org)                    | System-wide (staff / superuser)     |
| Auth decorator   | `@utils.authentication_required`    | + `@admin.staff_required` on top    |
| Model queries    | `Model.access_by(info.context.request)` | `Model.objects.all()`            |
| Schema location  | `modules/graph/karrio/server/graph/schemas/`       | `modules/admin/karrio/server/admin/schemas/` |
| Extension location | `modules/<name>/karrio/server/graph/schemas/<name>/` | `modules/<name>/karrio/server/admin/schemas/<name>/` |

## File Layout (4-file pattern)

Every schema module (base, admin, or extension) follows the same thin-interface layout. See `.claude/rules/extension-patterns.md` for the dependency rules between these files — circular imports cause silent schema registration failures.

```
schemas/<name>/
├── __init__.py    # Query + Mutation classes + extra_types (thin interface, REQUIRED)
├── types.py       # @strawberry.type definitions with resolve/resolve_list
├── inputs.py      # @strawberry.input Filter + Mutation inputs
└── mutations.py   # @strawberry.type mutation classes with mutate()
```

## Step-by-Step: Add a New Feature

### Step 1 — Define inputs (`inputs.py`)

```python
import typing
import strawberry

import karrio.server.graph.utils as utils


# Filter input — extends Paginated (gives offset + first)
@strawberry.input
class WidgetFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    status: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[utils.JSON] = strawberry.UNSET


# Mutation input — extends BaseInput (gives to_dict() + pagination())
@strawberry.input
class CreateWidgetMutationInput(utils.BaseInput):
    name: str
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateWidgetMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
```

Karrio conventions:

- Optional fields default to `strawberry.UNSET`, never `None`.
- Filters extend `utils.Paginated` (see `modules/graph/karrio/server/graph/utils.py`).
- Mutation inputs extend `utils.BaseInput`; the `.to_dict()` method strips `UNSET` values.
- Use typed enums from `karrio.server.graph.utils` (e.g. `utils.ShipmentStatusEnum`, `utils.CarrierNameEnum`) over raw strings whenever the value is enumerable.

### Step 2 — Define types (`types.py`)

```python
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.core.filters as filters
import karrio.server.graph.schemas.base.inputs as inputs
import karrio.server.manager.models as manager  # or your extension module's models


@strawberry.type
class WidgetType:
    id: str
    name: str
    description: typing.Optional[str] = None
    metadata: typing.Optional[utils.JSON] = None
    created_at: typing.Optional[str] = None

    # Computed field — resolved per instance, `self` is the model
    @strawberry.field
    def display_name(self: manager.Widget) -> str:
        return f"{self.name} ({self.id})"

    # Single-item resolver
    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["WidgetType"]:
        return (
            manager.Widget.access_by(info.context.request)
            .filter(id=id)
            .first()
        )

    # List resolver with pagination + filtering
    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: typing.Optional[inputs.WidgetFilter] = strawberry.UNSET,
    ) -> utils.Connection["WidgetType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.WidgetFilter()
        queryset = filters.WidgetFilter(
            _filter.to_dict(),
            manager.Widget.access_by(info.context.request),
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
```

Karrio conventions:

- Single-item resolver returns `Optional[Type]`; list resolver returns `utils.Connection[Type]` (karrio's paginated wrapper, not Relay's).
- Always use `Model.access_by(info.context.request)` in the base graph — this enforces tenant isolation. Never use `Model.objects.all()` here.
- Use `utils.is_unset(filter)` to check the sentinel — `None`/truthiness checks do not work.
- Factory methods that construct the type from a dict/record belong on the type itself as `@staticmethod parse(...)` — never in `utils.py` (that would create a circular import; see `.claude/rules/extension-patterns.md`).

### Step 3 — Define mutations (`mutations.py`)

```python
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.serializers as serializers
import karrio.server.graph.schemas.base.types as types
import karrio.server.graph.schemas.base.inputs as inputs
import karrio.server.manager.models as manager
from karrio.server.serializers import process_dictionaries_mutations


@strawberry.type
class CreateWidgetMutation(utils.BaseMutation):
    widget: typing.Optional[types.WidgetType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.CreateWidgetMutationInput
    ) -> "CreateWidgetMutation":
        serializer = serializers.WidgetModelSerializer(
            data=input,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        return CreateWidgetMutation(widget=serializer.save())  # type: ignore


@strawberry.type
class UpdateWidgetMutation(utils.BaseMutation):
    widget: typing.Optional[types.WidgetType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateWidgetMutationInput
    ) -> "UpdateWidgetMutation":
        instance = manager.Widget.access_by(info.context.request).get(id=input["id"])
        serializer = serializers.WidgetModelSerializer(
            instance,
            partial=True,
            data=process_dictionaries_mutations(["metadata"], input, instance),
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        return UpdateWidgetMutation(widget=serializer.save())  # type: ignore
```

Karrio conventions:

- Inherit from `utils.BaseMutation` to get the `errors` field for free.
- Mutations that require a password use `@utils.password_required` in addition to `@utils.authentication_required` (see `CreateAPIKeyMutation` in `mutations.py` for a reference).
- For JSON fields (`metadata`, `options`, `config`), route the payload through `process_dictionaries_mutations([...], input, instance)` — this merges partial dict updates instead of replacing them.
- Delegate validation + save to DRF serializers in `karrio.server.graph.serializers` (or a `karrio.server.<module>.serializers` for extension modules). Mutation bodies stay short.
- For generic delete mutations, reuse `mutations.DeleteMutation.mutate(info, model=..., validator=...)` as in the base graph's `delete_parcel` / `delete_metafield`.

### Step 4 — Wire up schema (`__init__.py`)

Keep `__init__.py` as a **thin interface** — Query fields use `strawberry.field(resolver=...)`, Mutation methods are one-liners that delegate to `mutations.X.mutate(info, **input.to_dict())`. No business logic here.

```python
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.types as types
import karrio.server.graph.schemas.base.inputs as inputs
import karrio.server.graph.schemas.base.mutations as mutations

extra_types: list = []  # REQUIRED even if empty


@strawberry.type
class Query:
    widget: typing.Optional[types.WidgetType] = strawberry.field(
        resolver=types.WidgetType.resolve
    )
    widgets: utils.Connection[types.WidgetType] = strawberry.field(
        resolver=types.WidgetType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_widget(
        self, info: Info, input: inputs.CreateWidgetMutationInput
    ) -> mutations.CreateWidgetMutation:
        return mutations.CreateWidgetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_widget(
        self, info: Info, input: inputs.UpdateWidgetMutationInput
    ) -> mutations.UpdateWidgetMutation:
        return mutations.UpdateWidgetMutation.mutate(info, **input.to_dict())
```

Auto-discovery: `modules/graph/karrio/server/graph/schema.py` iterates `schemas/` via `pkgutil.iter_modules()` and collects `Query`, `Mutation`, and `extra_types` from every sub-package. No manual registration — but the module must be installed (`-e ./modules/<name>` in `requirements.build.txt`) and opt in via `modules/<name>/karrio/server/settings/<name>.py`.

### Step 5 — Add the Django filter

```python
# modules/<module>/karrio/server/<module>/filters.py
import karrio.server.filters as filters  # NOT django_filters directly
import karrio.server.manager.models as manager


class WidgetFilter(filters.FilterSet):
    keyword = filters.CharFilter(method="keyword_filter")
    status = filters.CharInFilter(field_name="status", lookup_expr="in")
    metadata_key = filters.CharInFilter(
        field_name="metadata", method="metadata_key_filter"
    )
    order_by = filters.OrderingFilter(fields={"created_at": "created_at"})

    class Meta:
        model = manager.Widget
        fields: list = []

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)
```

`karrio.server.filters` re-exports `django_filters` plus karrio-specific filters (`CharInFilter`, …) — see `modules/core/karrio/server/filters/abstract.py`.

### Step 6 — Add the serializer

Serializers live in `modules/<module>/karrio/server/<module>/serializers/` (or a single `serializers.py`). For tenant-scoped models, wrap with `@owned_model_serializer` — it links the instance to `request.user.org` automatically.

```python
from rest_framework import serializers
from karrio.server.serializers import owned_model_serializer
import karrio.server.manager.models as manager


@owned_model_serializer
class WidgetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = manager.Widget
        exclude = ["created_at", "updated_at", "created_by"]
```

For system-scoped (admin) serializers, don't wrap; set `created_by` manually in `.create()`:

```python
class SystemWidgetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = manager.SystemWidget
        exclude = ["created_at", "updated_at", "created_by"]

    def create(self, validated_data, **kwargs):
        validated_data["created_by"] = self.context.user
        return super().create(validated_data)
```

### Step 7 — Add tests

Tests use `karrio.server.graph.tests.GraphTestCase` (see `modules/graph/karrio/server/graph/tests/base.py`) — it creates class-level user, token, and carrier fixtures via `setUpTestData`.

```python
from unittest import mock
from karrio.server.graph.tests import GraphTestCase


class TestWidgetSchema(GraphTestCase):

    def test_create_widget(self):
        response = self.query(
            """
            mutation create_widget($data: CreateWidgetMutationInput!) {
              create_widget(input: $data) {
                widget { id name }
                errors { field messages }
              }
            }
            """,
            operation_name="create_widget",
            variables=CREATE_DATA,
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, CREATE_RESPONSE)

    def test_list_widgets(self):
        response = self.query(
            """
            query widgets { widgets { edges { node { id name } } } }
            """,
            operation_name="widgets",
        )
        self.assertResponseNoErrors(response)


CREATE_DATA = {"data": {"name": "Test widget"}}
CREATE_RESPONSE = {
    "data": {
        "create_widget": {
            "widget": {"id": mock.ANY, "name": "Test widget"},
            "errors": None,
        }
    }
}
```

Run tests:

```bash
karrio test --failfast karrio.server.<module>.tests
```

Debug tip: add `print(response.data)` before `self.assertDictEqual(...)` when diagnosing failures, then remove it. `lib.to_dict()` strips `None` and empty strings — expected fixtures should not include them.

## Admin Graph Differences

Admin schemas live under `modules/admin/karrio/server/admin/schemas/` and in extension modules under `modules/<name>/karrio/server/admin/schemas/<name>/`.

```python
# types.py in an admin schema — no access_by(), add staff_required
import karrio.server.admin.utils as admin
import karrio.server.graph.utils as utils


@strawberry.type
class SystemWidgetType:
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info, id: str) -> typing.Optional["SystemWidgetType"]:
        return manager.SystemWidget.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: typing.Optional[inputs.SystemWidgetFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemWidgetType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemWidgetFilter()
        queryset = filters.SystemWidgetFilter(
            _filter.to_dict(),
            manager.SystemWidget.objects.all(),  # no access_by
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
```

Use `admin.superuser_required` for mutations that must be restricted to superusers only.

## N+1 Prevention

Always push `select_related` / `prefetch_related` into the model manager so that both REST and GraphQL benefit automatically.

```python
class WidgetManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("created_by")
            .prefetch_related("tags", "services")
        )
```

Inside a resolver that touches the same related field twice (e.g. returning computed fields that reuse `self.created_by`), call `.select_related` explicitly on the queryset produced by `access_by`.

## Extension Module GraphQL

To contribute GraphQL from `modules/<name>/`:

1. Create `modules/<name>/karrio/server/graph/schemas/<name>/` with the 4-file layout above.
2. **Do not** create `__init__.py` anywhere above the leaf `<name>/` directory — shared paths (`karrio/server/graph/`, `karrio/server/graph/schemas/`) must remain implicit namespace packages, otherwise they shadow the core modules. See `.claude/rules/extension-patterns.md`.
3. Add `-e ./modules/<name>` to `requirements.build.txt` (Docker / prod) **and** `requirements.server.dev.txt` (dev). Without both, schema discovery silently skips your module.
4. Add `karrio.server.<name>.tests` to `bin/run-server-tests` so CI picks it up.
5. Create `modules/<name>/karrio/server/settings/<name>.py` with `INSTALLED_APPS += ["karrio.server.<name>"]` so settings auto-discovery picks up the module (see `apps/api/karrio/server/settings/__init__.py`).

For admin-scoped extensions, use `modules/<name>/karrio/server/admin/schemas/<name>/` instead of `graph/schemas/<name>/`.

## Karrio Conventions Recap

- `import karrio.lib as lib` — never legacy `DP`/`SF`/`NF`/`DF`/`XP`.
- User-facing strings wrap in `gettext_lazy` as `_("...")`.
- `self.maxDiff = None` in `setUp()` (already done in `GraphTestCase`).
- Use `unittest` / `karrio test`, never `pytest`.
- Don't hand-build the final `schema.Schema(...)` — `modules/graph/karrio/server/graph/schema.py` owns that; just export `Query`, `Mutation`, and `extra_types` from your module.
