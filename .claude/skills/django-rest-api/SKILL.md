# Skill: Django REST API Development

Add REST endpoints following karrio's view, serializer, and router patterns.

## When to Use

- Adding new REST API endpoints
- Creating CRUD views for a model
- Adding endpoints from an extension module
- Building custom action endpoints

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                      REST API Request                         │
│                                                               │
│  Client ──> /api/v1/<resource>/ ──> urls.py ──> router.urls   │
│                                                               │
│  ┌─────────────────┐     ┌──────────────────┐                 │
│  │  GenericAPIView  │     │    APIView       │                 │
│  │  (List + Create) │     │  (Detail CRUD)   │                 │
│  │                  │     │                  │                 │
│  │  get_queryset()  │     │  access_by()     │                 │
│  │  ↓ access_by()   │     │  ↓               │                 │
│  │  filter_queryset()│     │                  │                 │
│  │  paginate_queryset│     │                  │                 │
│  └────────┬─────────┘     └────────┬─────────┘                 │
│           │                        │                           │
│           ▼                        ▼                           │
│  ┌──────────────────────────────────────────┐                  │
│  │  Serializer.map(data=request.data,       │                  │
│  │                  context=request)         │                  │
│  │  .save().instance                        │                  │
│  └──────────────────┬───────────────────────┘                  │
│                     │                                          │
│                     ▼                                          │
│  ┌──────────────────────────────────────────┐                  │
│  │  Response Serializer (EntitySerializer)  │                  │
│  │  Item(instance).data                     │                  │
│  └──────────────────────────────────────────┘                  │
└───────────────────────────────────────────────────────────────┘
```

## URL Convention

```
/api/v1/<resource>/              → List + Create (GenericAPIView)
/api/v1/<resource>/<str:pk>      → Retrieve + Update + Delete (APIView)
/api/v1/<resource>/<str:pk>/<action> → Custom actions (APIView)
```

## Step-by-Step: Add CRUD Endpoints

### Step 1: Create Router

```python
# karrio/server/<module>/router.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
```

### Step 2: Create URL Config

```python
# karrio/server/<module>/urls.py
from django.urls import include, path
from karrio.server.<module>.views import router

app_name = "karrio.server.<module>"
urlpatterns = [
    path("v1/", include(router.urls)),
]
```

### Step 3: Define Serializers

```python
# karrio/server/<module>/serializers.py
from karrio.server.serializers import (
    Serializer, EntitySerializer, ModelSerializer,
    PaginatedResult, owned_model_serializer,
    process_dictionaries_mutations,
)
import karrio.server.<module>.models as models

# Data serializer (input validation)
class ItemData(Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.PlainDictField(required=False, allow_null=True)

# Response serializer (output)
class Item(EntitySerializer, ItemData):
    object_type = serializers.CharField(default="item")
    created_at = serializers.DateTimeField(required=False)

# Paginated list serializer (auto-generated)
Items = PaginatedResult("ItemList", Item)

# Model serializer (handles create/update with ORM)
@owned_model_serializer
class ItemSerializer(ItemData):
    def create(self, validated_data: dict, **kwargs) -> models.Item:
        return models.Item.objects.create(**validated_data)

    def update(self, instance: models.Item, validated_data: dict, **kwargs) -> models.Item:
        data = process_dictionaries_mutations(["metadata"], validated_data, instance)
        for key, val in data.items():
            if hasattr(instance, key):
                setattr(instance, key, val)
        instance.save()
        return instance
```

**Key patterns:**
- `ItemData` = input validation (what the client sends)
- `Item(EntitySerializer, ItemData)` = response shape (inherits input fields + adds id, timestamps)
- `Items = PaginatedResult("ItemList", Item)` = paginated list wrapper
- `@owned_model_serializer` = handles `created_by` + `link_org()` for multi-tenancy
- `Serializer.map()` = elegant create/update with auto-validation

### Step 4: Create Views

```python
# karrio/server/<module>/views.py
from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.<module>.router import router
from karrio.server.<module>.serializers import (
    Items, Item, ItemData, ItemSerializer, ErrorResponse,
)
import karrio.server.<module>.models as models
import karrio.server.core.filters as filters
import karrio.server.openapi as openapi

ENDPOINT_ID = "$$"  # Unique prefix for operation IDs


class ItemList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.ItemFilter
    serializer_class = Items
    model = models.Item

    @openapi.extend_schema(
        tags=["Items"],
        operation_id=f"{ENDPOINT_ID}list",
        summary="List all items",
        responses={200: Items(), 500: ErrorResponse()},
    )
    def get(self, request: Request):
        items = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(Item(items, many=True).data)
        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Items"],
        operation_id=f"{ENDPOINT_ID}create",
        summary="Create an item",
        request=ItemData(),
        responses={201: Item(), 400: ErrorResponse()},
    )
    def post(self, request: Request):
        item = (
            ItemSerializer.map(data=request.data, context=request)
            .save()
            .instance
        )
        return Response(Item(item).data, status=status.HTTP_201_CREATED)


class ItemDetail(APIView):

    @openapi.extend_schema(
        tags=["Items"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        summary="Retrieve an item",
        responses={200: Item(), 404: ErrorResponse()},
    )
    def get(self, request: Request, pk: str):
        item = models.Item.access_by(request).get(pk=pk)
        return Response(Item(item).data)

    @openapi.extend_schema(
        tags=["Items"],
        operation_id=f"{ENDPOINT_ID}update",
        summary="Update an item",
        request=ItemData(),
        responses={200: Item(), 400: ErrorResponse()},
    )
    def patch(self, request: Request, pk: str):
        item = models.Item.access_by(request).get(pk=pk)
        ItemSerializer.map(item, data=request.data).save()
        return Response(Item(item).data)

    @openapi.extend_schema(
        tags=["Items"],
        operation_id=f"{ENDPOINT_ID}discard",
        summary="Delete an item",
        responses={200: Item(), 404: ErrorResponse()},
    )
    def delete(self, request: Request, pk: str):
        item = models.Item.access_by(request).get(pk=pk)
        item.delete(keep_parents=True)
        return Response(Item(item).data)


# Route registration at module level (self-registering pattern)
router.urls.append(path("items", ItemList.as_view(), name="item-list"))
router.urls.append(
    path("items/<str:pk>", ItemDetail.as_view(), name="item-details")
)
```

**Key patterns:**
- `GenericAPIView` for list views — has `get_queryset()` that auto-calls `model.access_by(request)`
- `APIView` for detail views — manually call `Model.access_by(request).get(pk=pk)`
- `@openapi.extend_schema()` for auto-generated API docs
- Routes registered at module level via `router.urls.append()`
- `Serializer.map(data=..., context=request).save().instance` for create
- `Serializer.map(instance, data=...).save()` for update (auto-sets `partial=True`)

### Step 5: Register URLs

For core modules, URLs are discovered via `KARRIO_CONF` in settings.

For extension modules:
```python
# karrio/server/settings/<module>.py
from karrio.server.settings.base import *
KARRIO_URLS += ["karrio.server.<module>.urls"]
```

## Advanced Patterns

### Custom Query Filtering

```python
class ItemList(GenericAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = getattr(self.request, "query_params", {})

        keyword = query_params.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(description__icontains=keyword)
            )
        return queryset
```

### Custom Action Endpoint

```python
class ItemAction(APIView):
    @openapi.extend_schema(
        tags=["Items"],
        operation_id=f"{ENDPOINT_ID}activate",
        summary="Activate an item",
        responses={200: Item()},
    )
    def post(self, request: Request, pk: str):
        item = models.Item.access_by(request).get(pk=pk)
        item.is_active = True
        item.save(update_fields=["is_active"])
        return Response(Item(item).data)

router.urls.append(
    path("items/<str:pk>/activate", ItemAction.as_view(), name="item-activate")
)
```

### N+1 Prevention in Views

Always optimize querysets in the model manager:

```python
class ItemManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("created_by", "category")
            .prefetch_related("tags")
        )
```

The `GenericAPIView.get_queryset()` calls `model.access_by(request)` which uses this manager — so N+1 prevention is automatic.

## Testing REST Endpoints

```python
from rest_framework.test import APITestCase
from rest_framework import status

class TestItemAPI(APITestCase):
    fixtures = ["fixtures"]

    def test_list_items(self):
        response = self.client.get("/api/v1/items")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)  # Debug — remove when passing
        self.assertIn("results", response.data)

    def test_create_item(self):
        response = self.client.post("/api/v1/items", data={"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test")
```
