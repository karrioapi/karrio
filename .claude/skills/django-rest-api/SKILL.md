# Skill: Django REST API Development

Add REST endpoints that follow karrio's view, serializer, router, and OpenAPI conventions.

## When to Use

- Adding new REST API endpoints to a core or extension module
- Creating CRUD + custom-action views for a model
- Wiring a new resource into the karrio URL namespace
- Producing OpenAPI metadata for the public karrio-api spec

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                       REST API Request                         │
│                                                                │
│  Client ──> /api/v1/<resource> ──> <module>/urls.py            │
│                                    ↳ include(router.urls)      │
│                                                                │
│  ┌───────────────────────────────┐   ┌───────────────────────┐ │
│  │ core.views.api.GenericAPIView │   │ core.views.api.APIView │ │
│  │   (list + create)             │   │   (detail CRUD +      │ │
│  │   get_queryset() → access_by  │   │    custom actions)    │ │
│  │   filter_queryset()           │   │                       │ │
│  │   paginate_queryset()         │   │   Model.access_by(req)│ │
│  └──────────┬────────────────────┘   └────────┬──────────────┘ │
│             │                                 │                │
│             ▼                                 ▼                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Serializer.map(data=request.data, context=request)      │  │
│  │    .save().instance                                      │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                             ▼                                  │
│  Response(Entity(instance).data, status=...)                   │
└────────────────────────────────────────────────────────────────┘
```

Relevant files:

- `modules/manager/karrio/server/manager/views/shipments.py` — canonical reference (full CRUD + rate + purchase + cancel + documents)
- `modules/orders/karrio/server/orders/views.py` — extension-module reference
- `modules/core/karrio/server/core/views/api.py` — `GenericAPIView`, `APIView`, `LoggingMixin`
- `modules/core/karrio/server/core/authentication.py` — `AccessMixin`, token / JWT / OAuth2 authenticators
- `modules/core/karrio/server/serializers/abstract.py` — `Serializer`, `EntitySerializer`, `PaginatedResult`, `owned_model_serializer`
- `modules/core/karrio/server/core/serializers.py` — `ErrorResponse`, `ErrorMessages`, enums (`ShipmentStatus`, …)
- `modules/core/karrio/server/filters/abstract.py` — `FilterSet`, `CharInFilter`, `DateTimeFilter`
- `modules/core/karrio/server/openapi.py` — `extend_schema` decorator for OpenAPI metadata

## URL Convention

```
/api/v1/<resource>                    → GenericAPIView: GET (list) + POST (create)
/api/v1/<resource>/<str:pk>           → APIView: GET + PATCH/PUT + DELETE
/api/v1/<resource>/<str:pk>/<action>  → APIView: POST (custom action)
```

All endpoints live under `/api/v1/` (the `urls.py` mounts `router.urls` at `v1/`).

## Step-by-Step: Add CRUD Endpoints

### Step 1 — Create the module router

```python
# modules/<module>/karrio/server/<module>/router.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
```

Each module instantiates its own `DefaultRouter`. Views append themselves to `router.urls` at module load time (self-registering pattern — see next step).

### Step 2 — Wire `urls.py`

```python
# modules/<module>/karrio/server/<module>/urls.py
"""
karrio server <module> urls
"""
from django.urls import include, path
from karrio.server.<module>.views import router

app_name = "karrio.server.<module>"
urlpatterns = [
    path("v1/", include(router.urls)),
]
```

The import side-effect of `from karrio.server.<module>.views import router` triggers view modules to `router.urls.append(...)` themselves. `app_name` must match the dotted module path — `reverse("karrio.server.<module>:<name>")` uses this namespace.

### Step 3 — Define serializers

Serializers use karrio's 3-tier pattern (input / entity / model) plus `PaginatedResult` for list responses. Lay out:

```
modules/<module>/karrio/server/<module>/serializers/
├── __init__.py     # re-exports
├── base.py         # Data + Entity serializers (shapes)
└── <resource>.py   # ModelSerializer + helpers (mutations)
```

```python
# serializers/base.py
from rest_framework import serializers
from karrio.server.serializers import (
    Serializer,
    EntitySerializer,
    PaginatedResult,
    process_dictionaries_mutations,
    owned_model_serializer,
)
import karrio.server.<module>.models as models


# 1) Input data shape (what the client POSTs)
class WidgetData(Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.PlainDictField(required=False, allow_null=True)


# 2) Output entity shape (response body) — inherits input + adds id/timestamps
class Widget(EntitySerializer, WidgetData):
    object_type = serializers.CharField(default="widget")


# 3) Paginated list (auto-generated wrapper with count/next/previous/results)
#    Conventionally instantiated in the view module instead of here — see Step 4.
```

```python
# serializers/widget.py
@owned_model_serializer
class WidgetSerializer(WidgetData):
    def create(self, validated_data, **kwargs) -> models.Widget:
        return models.Widget.objects.create(**validated_data)

    def update(self, instance, validated_data, **kwargs) -> models.Widget:
        data = process_dictionaries_mutations(["metadata"], validated_data, instance)
        for key, val in data.items():
            if hasattr(instance, key):
                setattr(instance, key, val)
        instance.save()
        return instance
```

Karrio conventions:

- `WidgetData` (inputs) stays free of id / timestamps — used as request schema.
- `Widget` (entity) inherits `WidgetData` and adds the fields `EntitySerializer` provides (id, object_type, created_at, updated_at).
- `@owned_model_serializer` attaches `created_by` and calls `link_org(...)` for multi-tenancy. Never omit it for tenant-scoped models.
- Use `Serializer.map(data=..., context=request).save().instance` in views — this is karrio's idiomatic create/update call (see `modules/core/karrio/server/serializers/abstract.py`). `.map(instance, data=...)` auto-sets `partial=True`.
- For JSON fields (`metadata`, `options`, `config`), always route through `process_dictionaries_mutations([...], payload, instance)` — it merges partial updates instead of clobbering.

### Step 4 — Create views

```python
# modules/<module>/karrio/server/<module>/views.py
from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.serializers import PaginatedResult, process_dictionaries_mutations
from karrio.server.<module>.router import router
from karrio.server.<module>.serializers import (
    Widget,
    WidgetData,
    WidgetSerializer,
)
import karrio.server.<module>.models as models
import karrio.server.<module>.filters as filters
import karrio.server.openapi as openapi
from karrio.server.core.serializers import ErrorResponse

ENDPOINT_ID = "$$$$$"  # 5-char unique hash — keeps operation_id stable & collision-free
Widgets = PaginatedResult("WidgetList", Widget)


class WidgetList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.WidgetFilters
    serializer_class = Widgets
    model = models.Widget

    @openapi.extend_schema(
        tags=["Widgets"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listWidgets"},
        summary="List all widgets",
        responses={200: Widgets(), 500: ErrorResponse()},
    )
    def get(self, _: Request):
        """Retrieve all widgets."""
        widgets = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(Widget(widgets, many=True).data)
        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Widgets"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createWidget"},
        summary="Create a widget",
        request=WidgetData(),
        responses={201: Widget(), 400: ErrorResponse(), 500: ErrorResponse()},
    )
    def post(self, request: Request):
        """Create a new widget instance."""
        widget = (
            WidgetSerializer.map(data=request.data, context=request).save().instance
        )
        return Response(Widget(widget).data, status=status.HTTP_201_CREATED)


class WidgetDetails(APIView):

    @openapi.extend_schema(
        tags=["Widgets"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveWidget"},
        summary="Retrieve a widget",
        responses={200: Widget(), 404: ErrorResponse(), 500: ErrorResponse()},
    )
    def get(self, request: Request, pk: str):
        widget = models.Widget.access_by(request).get(pk=pk)
        return Response(Widget(widget).data)

    @openapi.extend_schema(
        tags=["Widgets"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateWidget"},
        summary="Update a widget",
        request=WidgetData(),
        responses={200: Widget(), 400: ErrorResponse(), 404: ErrorResponse()},
    )
    def patch(self, request: Request, pk: str):
        widget = models.Widget.access_by(request).get(pk=pk)
        payload = WidgetData.map(data=request.data).data
        update = (
            WidgetSerializer.map(
                widget,
                context=request,
                data=process_dictionaries_mutations(["metadata"], payload, widget),
            )
            .save()
            .instance
        )
        return Response(Widget(update).data)

    @openapi.extend_schema(
        tags=["Widgets"],
        operation_id=f"{ENDPOINT_ID}discard",
        extensions={"x-operationId": "discardWidget"},
        summary="Delete a widget",
        responses={200: Widget(), 404: ErrorResponse()},
    )
    def delete(self, request: Request, pk: str):
        widget = models.Widget.access_by(request).get(pk=pk)
        widget.delete(keep_parents=True)
        return Response(Widget(widget).data)


# Self-register at module load time — urls.py imports this module so router.urls is populated.
router.urls.append(path("widgets", WidgetList.as_view(), name="widget-list"))
router.urls.append(
    path("widgets/<str:pk>", WidgetDetails.as_view(), name="widget-details")
)
```

Karrio conventions:

- **Base classes**: always `karrio.server.core.views.api.GenericAPIView` / `APIView`, never raw DRF `generics.GenericAPIView` / `views.APIView`. Karrio's base classes inject `LoggingMixin`, token / JWT / OAuth2 auth, throttling, and `access_by`-aware `get_queryset()`.
- **`ENDPOINT_ID`**: set a 5-character prefix (e.g. `"$$$$$"`, `"&&&&&"`, `"@@@@@"`) at the top of each view module. It is concatenated with `list` / `create` / `retrieve` / `update` / `discard` etc. to keep operation-IDs unique across modules. Duplicates silently break the OpenAPI schema.
- **`extensions={"x-operationId": "camelCaseName"}`**: provides a stable, human-readable operation id for the public OpenAPI spec and SDK generation.
- **`extend_schema(request=..., responses={...: ErrorResponse()})`**: document both input and error shapes. `ErrorResponse` and `ErrorMessages` come from `karrio.server.core.serializers`.
- **Filtering**: `filter_backends = (DjangoFilterBackend,)` + `filterset_class = filters.WidgetFilters`. The filterset lives in your module's `filters.py` and extends `karrio.server.filters.FilterSet`.
- **Pagination**: subclass `LimitOffsetPagination` inline via `type("CustomPagination", (LimitOffsetPagination,), dict(default_limit=20))` — default limit 20 matches the rest of karrio.
- **Paginated serializer**: `PaginatedResult("WidgetList", Widget)` factory generates a `{count, next, previous, results}` wrapper. Attach it as `serializer_class` on the list view.
- **Tenant scoping**: `GenericAPIView.get_queryset()` calls `self.model.access_by(request)` when `model` is set (see `modules/core/karrio/server/core/views/api.py:99`). For `APIView` detail endpoints, call `Model.access_by(request).get(pk=pk)` manually — this is enforced everywhere (e.g. `shipments.py:120`, `orders/views.py:99`).
- **Route registration**: append to `router.urls` at module level. Prefer `path(...)` over `re_path(...)` unless you need regex groups (e.g. file extensions, see the `ShipmentDocs` example).

### Step 5 — Register the module

Extension modules opt in via their own settings file:

```python
# modules/<module>/karrio/server/settings/<module>.py
from karrio.server.settings.base import *  # noqa

KARRIO_URLS += ["karrio.server.<module>.urls"]
INSTALLED_APPS += ["karrio.server.<module>"]
```

`apps/api/karrio/server/settings/__init__.py` uses `importlib.util.find_spec()` to conditionally import this file, so it runs only when the module is actually installed.

Then:

- Add `-e ./modules/<module>` to `requirements.build.txt` (prod Docker) **and** `requirements.server.dev.txt` (dev).
- Add `karrio.server.<module>.tests` to `bin/run-server-tests` so CI picks it up.

See `.claude/rules/extension-patterns.md` for the full checklist.

## Advanced Patterns

### Custom action endpoint

Custom actions are POST endpoints under `/<resource>/<pk>/<action>`. The canonical example is shipment `cancel` / `purchase` / `rates` (`modules/manager/karrio/server/manager/views/shipments.py:163-286`).

```python
class WidgetArchive(APIView):

    @openapi.extend_schema(
        tags=["Widgets"],
        operation_id=f"{ENDPOINT_ID}archive",
        extensions={"x-operationId": "archiveWidget"},
        summary="Archive a widget",
        request=None,
        responses={200: Widget(), 404: ErrorResponse()},
    )
    def post(self, request: Request, pk: str):
        widget = models.Widget.access_by(request).get(pk=pk)
        widget.is_archived = True
        widget.save(update_fields=["is_archived"])
        return Response(Widget(widget).data)


router.urls.append(
    path("widgets/<str:pk>/archive", WidgetArchive.as_view(), name="widget-archive")
)
```

### Fallback lookup by `request_id`

Several karrio endpoints accept either the primary key or the idempotency key stored in `instance.meta["request_id"]` — see `ShipmentCancel` and `OrderCancel`:

```python
qs = models.Widget.access_by(request)
try:
    widget = qs.get(pk=pk)
except models.Widget.DoesNotExist:
    widget = qs.filter(meta__request_id=pk).order_by("-created_at").first()

if widget is None:
    raise models.Widget.DoesNotExist()
```

### Filtering with `filters.py`

```python
# modules/<module>/karrio/server/<module>/filters.py
import karrio.server.filters as filters
from django.db.models import Q
import karrio.server.<module>.models as models
import karrio.server.<module>.serializers as serializers


class WidgetFilters(filters.FilterSet):
    keyword = filters.CharFilter(method="keyword_filter")
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(s.value, s.value) for s in list(serializers.WidgetStatus)],
    )
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    metadata_key = filters.CharInFilter(
        field_name="metadata", method="metadata_key_filter"
    )

    parameters = [
        # Optional: OpenAPI parameter hints — see ShipmentFilters for the full pattern
    ]

    class Meta:
        model = models.Widget
        fields: list = []

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)
```

`karrio.server.filters` re-exports `django_filters.rest_framework` plus karrio helpers (`CharInFilter`). In the view, reference the filter class and pass `filters.ShipmentFilters.parameters` to `extend_schema(parameters=...)` to inherit OpenAPI parameter metadata.

### Document / file download

For label / invoice downloads, extend `django_downloadview.VirtualDownloadView` and mix `AccessMixin`:

```python
from karrio.server.core.authentication import AccessMixin
from django_downloadview import VirtualDownloadView


class WidgetDocs(AccessMixin, VirtualDownloadView):
    @openapi.extend_schema(exclude=True)  # exclude from public spec
    def get(self, request, pk, doc="file", format="pdf", **kwargs):
        ...
```

See `ShipmentDocs` in `manager/views/shipments.py:288-352` for the full pattern (resource-token validation, `lib.failsafe` ZPL-to-PDF conversion, `X-Frame-Options: ALLOWALL`).

### N+1 prevention in views

Push `select_related` / `prefetch_related` into the model manager's default queryset so both list + detail benefit automatically:

```python
class WidgetManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("created_by")
            .prefetch_related("tags")
        )
```

`GenericAPIView.get_queryset()` calls `model.access_by(request)`, which goes through your custom manager — no need to override on a per-view basis.

## Testing REST Endpoints

Tests use `karrio.server.core.tests.APITestCase` (see `modules/core/karrio/server/core/tests/base.py`) — it creates a class-level superuser, API token, and carrier fixtures.

```python
import json
from django.http.response import HttpResponse
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase


class TestWidgetFixture(APITestCase):
    def create_widget(self) -> tuple[HttpResponse, dict]:
        url = reverse("karrio.server.<module>:widget-list")
        response = self.client.post(url, WIDGET_DATA)
        return response, json.loads(response.content)


class TestWidgets(TestWidgetFixture):
    def test_create_widget(self):
        response, data = self.create_widget()
        # print(data)  # DEBUG — remove before committing
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(data, WIDGET_RESPONSE)


WIDGET_DATA = {"name": "Test widget"}
WIDGET_RESPONSE = {...}
```

Run:

```bash
karrio test --failfast karrio.server.<module>.tests
./bin/run-server-tests                       # the whole server suite
```

Karrio testing conventions:

- No `pytest` anywhere — `unittest` for SDK, `karrio test` for server (Django).
- `self.maxDiff = None` is already set by `APITestCase.setUp`.
- Always use `reverse("karrio.server.<module>:<url-name>")` — hardcoding paths like `/api/v1/widgets` breaks under URL-prefix changes.
- `lib.to_dict(...)` strips `None` / empty strings — expected fixtures should mirror that.
- Add `print(response.data)` before the assertion while diagnosing failures, then remove it when the test passes (see `.claude/rules/testing.md`).
