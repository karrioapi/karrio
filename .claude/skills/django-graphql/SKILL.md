# Skill: Django GraphQL Development

Add queries, mutations, types, and inputs to the Strawberry GraphQL schema.

## When to Use

- Adding new GraphQL queries or mutations
- Creating new types for existing models
- Extending base (tenant) or admin (system) graph
- Adding GraphQL to an extension module

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GraphQL Request                       │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐   │
│  │  Client   │──>│ Strawberry│──>│ Schema Discovery  │   │
│  │  Query/   │   │  Router   │   │ pkgutil.iter_     │   │
│  │  Mutation │   │          │   │ modules(schemas/) │   │
│  └──────────┘    └──────────┘    └────────┬─────────┘   │
│                                           │              │
│                  ┌────────────────────────┐│              │
│                  │  Multiple Inheritance  ││              │
│                  │  Query(*QUERIES)       ││              │
│                  │  Mutation(*MUTATIONS)  │◄              │
│                  └────────┬───────────────┘               │
│                           │                              │
│           ┌───────────────┼───────────────┐              │
│           ▼               ▼               ▼              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │schemas/base/ │ │schemas/docs/ │ │schemas/<ext>/│     │
│  │ __init__.py  │ │ __init__.py  │ │ __init__.py  │     │
│  │ types.py     │ │ types.py     │ │ types.py     │     │
│  │ mutations.py │ │ mutations.py │ │ mutations.py │     │
│  │ inputs.py    │ │ inputs.py    │ │ inputs.py    │     │
│  └──────┬───────┘ └──────────────┘ └──────────────┘     │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐    ┌──────────────┐                    │
│  │  Serializer  │──>│  Django Model │                    │
│  │  (DRF)       │   │  (ORM)       │                    │
│  └──────────────┘    └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## Two Schema Domains

| Aspect | Base Graph | Admin Graph |
|--------|-----------|-------------|
| URL | `/graphql` | `/admin/graphql` |
| Scope | Tenant (per-org) | System-wide (staff only) |
| Auth decorator | `@utils.authentication_required` | `@admin.staff_required` |
| Model queries | `Model.access_by(request)` | `Model.objects.all()` |
| Schemas location | `karrio/server/graph/schemas/` | `karrio/server/admin/schemas/` |

## File Structure (4-file pattern)

Every schema module follows the same structure:

```
schemas/<name>/
├── __init__.py    # Query & Mutation classes (required)
├── types.py       # @strawberry.type definitions
├── mutations.py   # Mutation implementations
└── inputs.py      # Filter & mutation inputs
```

## Step-by-Step: Add a New Feature

### Step 1: Define the Input (`inputs.py`)

```python
import strawberry
import typing
from strawberry.types import Info

import karrio.server.graph.utils as utils

# Filter input (for queries) — extends Paginated for offset/limit
@strawberry.input
class MyItemFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    status: typing.Optional[str] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET

# Mutation input — extends BaseInput
@strawberry.input
class CreateMyItemInput(utils.BaseInput):
    name: str
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET

@strawberry.input
class UpdateMyItemInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
```

**Key patterns:**
- Optional fields default to `strawberry.UNSET` (not `None`)
- Filters extend `utils.Paginated` (gives `offset`, `first`, `after`, `before`)
- Mutation inputs extend `utils.BaseInput` (gives `to_dict()`, `pagination()`)

### Step 2: Define the Type (`types.py`)

```python
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.core.filters as filters
import karrio.server.mymodule.models as models
import karrio.server.graph.schemas.<name>.inputs as inputs

@strawberry.type
class MyItemType:
    id: str
    name: str
    description: typing.Optional[str] = None
    metadata: typing.Optional[utils.JSON] = None
    created_at: typing.Optional[str] = None

    # Computed field (resolved per-instance)
    @strawberry.field
    def display_name(self: models.MyItem) -> str:
        return f"{self.name} ({self.id})"

    # Single-item resolver
    @staticmethod
    @utils.authentication_required
    def resolve(
        info: Info, id: str
    ) -> typing.Optional["MyItemType"]:
        return (
            models.MyItem.access_by(info.context.request)
            .filter(id=id)
            .first()
        )

    # List resolver with pagination + filtering
    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: typing.Optional[inputs.MyItemFilter] = strawberry.UNSET,
    ) -> utils.Connection["MyItemType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.MyItemFilter()
        queryset = filters.MyItemFilter(
            _filter.to_dict(),
            models.MyItem.access_by(info.context.request),
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
```

**Key patterns:**
- `resolve()` returns `Optional[Type]` — single item or None
- `resolve_list()` returns `utils.Connection[Type]` — paginated list
- Always use `Model.access_by(request)` for tenant scoping
- Use `utils.is_unset(filter)` to check for strawberry.UNSET

### Step 3: Define Mutations (`mutations.py`)

```python
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.<name>.types as types
import karrio.server.graph.schemas.<name>.inputs as inputs
import karrio.server.graph.serializers as serializers

@strawberry.type
class CreateMyItemMutation(utils.BaseMutation):
    my_item: typing.Optional[types.MyItemType] = None

    @staticmethod
    @utils.authentication_required
    @utils.error_wrapper
    def mutate(
        info: Info, **input: inputs.CreateMyItemInput
    ) -> "CreateMyItemMutation":
        serializer = serializers.MyItemModelSerializer(
            data=input,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        return CreateMyItemMutation(my_item=serializer.save())

@strawberry.type
class UpdateMyItemMutation(utils.BaseMutation):
    my_item: typing.Optional[types.MyItemType] = None

    @staticmethod
    @utils.authentication_required
    @utils.error_wrapper
    def mutate(
        info: Info, **input: inputs.UpdateMyItemInput
    ) -> "UpdateMyItemMutation":
        id = input.get("id")
        instance = models.MyItem.access_by(info.context.request).get(id=id)
        serializer = serializers.MyItemModelSerializer(
            instance,
            data=input,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        return UpdateMyItemMutation(my_item=serializer.save())
```

**Key patterns:**
- Inherit from `utils.BaseMutation` (gives `errors` field)
- `@utils.error_wrapper` catches exceptions and returns them as errors
- Use `**input` to accept keyword args from the input class
- Use serializer for validation and saving

### Step 4: Wire Up Schema (`__init__.py`)

```python
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.schemas.<name>.types as types
import karrio.server.graph.schemas.<name>.inputs as inputs
import karrio.server.graph.schemas.<name>.mutations as mutations

extra_types: list = []  # REQUIRED even if empty

@strawberry.type
class Query:
    my_item: typing.Optional[types.MyItemType] = strawberry.field(
        resolver=types.MyItemType.resolve
    )
    my_items: utils.Connection[types.MyItemType] = strawberry.field(
        resolver=types.MyItemType.resolve_list
    )

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_my_item(
        self, info: Info, input: inputs.CreateMyItemInput
    ) -> mutations.CreateMyItemMutation:
        return mutations.CreateMyItemMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_my_item(
        self, info: Info, input: inputs.UpdateMyItemInput
    ) -> mutations.UpdateMyItemMutation:
        return mutations.UpdateMyItemMutation.mutate(info, **input.to_dict())
```

**Auto-discovery**: This module is automatically found by `pkgutil.iter_modules()` in `schema.py` — no manual registration needed.

### Step 5: Add Django Filter

```python
# core/filters.py
import django_filters as filters
import karrio.server.mymodule.models as models

class MyItemFilter(filters.FilterSet):
    keyword = filters.CharFilter(method="keyword_filter")
    status = filters.CharFilter(field_name="status")
    metadata_key = filters.CharFilter(
        field_name="metadata", method="metadata_key_filter"
    )
    order_by = filters.OrderingFilter(fields={"created_at": "created_at"})

    class Meta:
        model = models.MyItem
        fields: list = []

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)
```

### Step 6: Add Serializer

```python
# For tenant-scoped models (with org linking):
@owned_model_serializer
class MyItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyItem
        exclude = ["created_at", "updated_at", "created_by"]

# For system-scoped models (admin only):
class SystemMyItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SystemMyItem
        exclude = ["created_at", "updated_at", "created_by"]

    def create(self, validated_data, **kwargs):
        validated_data["created_by"] = self.context.user
        return super().create(validated_data)
```

### Step 7: Add Tests

```python
from karrio.server.graph.tests import GraphTestCase
import karrio.server.mymodule.models as models

class TestMyItem(GraphTestCase):
    fixtures = ["fixtures"]

    def test_create_my_item(self):
        response = self.query(
            """
            mutation create_my_item($data: CreateMyItemInput!) {
              create_my_item(input: $data) {
                my_item { id name }
                errors { field messages }
              }
            }
            """,
            operation_name="create_my_item",
            variables=CREATE_DATA,
        )
        response_data = response.data
        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CREATE_RESPONSE)

    def test_list_my_items(self):
        response = self.query(
            """
            query my_items {
              my_items { edges { node { id name } } }
            }
            """,
            operation_name="my_items",
        )
        self.assertResponseNoErrors(response)

CREATE_DATA = {"data": {"name": "Test Item"}}
CREATE_RESPONSE = {
    "data": {
        "create_my_item": {
            "my_item": {"id": mock.ANY, "name": "Test Item"},
            "errors": None,
        }
    }
}
```

## Admin Graph Differences

For admin (system-scoped) schemas:

```python
# types.py — no access_by(), use staff_required
@strawberry.type
class SystemMyItemType:
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info, id: str) -> typing.Optional["SystemMyItemType"]:
        return models.SystemMyItem.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(info: Info, ...) -> utils.Connection["SystemMyItemType"]:
        queryset = filters.SystemMyItemFilter(
            _filter.to_dict(),
            models.SystemMyItem.objects.all(),  # No access_by()
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
```

## N+1 Prevention in GraphQL

Always add `select_related`/`prefetch_related` in custom managers or querysets:

```python
# models.py
class MyItemManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("created_by", "category")  # FK joins
            .prefetch_related("tags", "services")       # M2M / reverse FK
        )
```

See `.claude/rules/n1-prevention.md` for comprehensive patterns.

## Extension Module GraphQL

To add GraphQL from a `modules/` extension:

1. Create `modules/<name>/karrio/server/graph/schemas/<name>/` (same 4-file pattern)
2. Add namespace `__init__.py`: `__path__ = __import__("pkgutil").extend_path(__path__, __name__)`
3. Auto-discovered — no registration needed

For admin graph: use `karrio/server/admin/schemas/<name>/` instead.
