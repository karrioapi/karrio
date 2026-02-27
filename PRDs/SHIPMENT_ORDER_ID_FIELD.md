# Shipment `order_id` First-Class Field

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-27 |
| Status | Planning |
| Owner | Engineering |
| Type | Enhancement |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Open Questions & Decisions](#open-questions--decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Alternatives Considered](#alternatives-considered)
6. [Technical Design](#technical-design)
7. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
8. [Implementation Plan](#implementation-plan)
9. [Testing Strategy](#testing-strategy)
10. [Risk Assessment](#risk-assessment)
11. [Migration & Rollback](#migration--rollback)

---

## Executive Summary

Add an optional, nullable `order_id` string field directly to the `Shipment` Django model, replacing the informal `meta["orders"]` convention with a first-class, queryable, filterable column. This field will be fully exposed via REST and GraphQL APIs (create, read, update, filter), added to the SDK `ShipmentRequest` data model for carrier passthrough, and will include backward-compatible fallback to `meta["orders"]` during a deprecation period.

### Key Architecture Decisions

1. **First-class `CharField` on `Shipment`**: `order_id = CharField(max_length=50, null=True, blank=True, db_index=True)` — matches the `Order.order_id` field definition exactly, enabling direct DB-level filtering and joins.
2. **SDK model addition**: Add `order_id: str = ""` to `ShipmentRequest` so carriers that accept order/reference fields can receive it via the standard mapper passthrough pattern (same pattern as the existing `reference` field).
3. **Backward-compatible signal**: The existing `shipment_updated` signal in `orders/signals.py` will be updated to also populate `shipment.order_id` from linked `Order.order_id` when not explicitly set, maintaining compatibility while enabling the new field.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| `order_id` field on Shipment Django model | Removing the M2M `Order.shipments` relationship |
| Django migration with `db_index` | Multi-order support (shipment linked to multiple orders) |
| REST serializer read/write + filter | Frontend/dashboard UI changes |
| GraphQL type, mutation input, filter | Automatic backfill of historical shipments |
| SDK `ShipmentRequest.order_id` field | New carrier integrations |
| Carrier passthrough via mapper pattern | Changes to `Order` model or serializer |
| Signal-based auto-populate from linked Order | Webhook payload changes |
| Deprecation of `meta["orders"]` (documentation) | Removing `meta["orders"]` (future phase) |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Field type and max_length | `CharField(max_length=50)` | Matches `Order.order_id` definition exactly (`max_length=50, db_index=True`) | 2026-02-27 |
| D2 | Single `order_id` vs multi-order support | Single `order_id` string | Covers 95%+ of use cases; multi-order already handled by M2M relationship; keeps field simple and queryable | 2026-02-27 |
| D3 | Backward compat with `meta["orders"]` | Dual-write during transition, deprecate `meta["orders"]` over 2 releases | Avoids breaking existing API consumers that read `meta.orders` | 2026-02-27 |
| D4 | SDK field placement | `ShipmentRequest.order_id` (alongside existing `reference`) | Follows identical pattern to `reference: str = ""`; carriers map it independently | 2026-02-27 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Shipment linked to multiple orders via M2M | `order_id` can only hold one value | Store the first/primary order's `order_id`; full list remains in M2M relationship | No |
| `order_id` set explicitly AND shipment linked to different Order | Conflict between explicit and auto-populated value | Explicit value always wins; auto-populate only when `order_id` is null | No |

---

## Problem Statement

### Current State

Order identification on shipments is stored informally in the `meta` JSON field:

```python
# modules/orders/karrio/server/orders/signals.py:143-147
meta = {
    **(instance.meta or {}),
    "orders": ",".join([_.id for _ in related_orders]),  # Comma-separated internal IDs
}
manager.Shipment.objects.filter(id=instance.id).update(meta=meta)
```

```python
# Reading order_id from meta requires JSON traversal
order_ids = (shipment.meta or {}).get("orders", "")  # Returns "ord_abc,ord_def"
```

```typescript
// packages/ui/core/components/shipment-menu.tsx:57-59
if (!!shipment.meta?.orders) {
  router.push(
    p`${basePath}/orders/create_label?shipment_id=${shipment.id}&order_id=${shipment.meta.orders}`,
  );
}
```

### Desired State

```python
# Direct field access - clean and queryable
shipment.order_id  # "ORD-12345" or None

# Direct DB filtering
Shipment.objects.filter(order_id="ORD-12345")
Shipment.objects.filter(order_id__icontains="ORD")
```

```python
# REST API: create shipment with order_id
POST /api/v1/shipments
{
    "order_id": "ORD-12345",
    "shipper": {...},
    "recipient": {...},
    "parcels": [...]
}

# REST API: filter by order_id
GET /api/v1/shipments?order_id=ORD-12345
```

```graphql
# GraphQL: query with filter
query {
  shipments(filter: { order_id: "ORD-12345" }) {
    edges { node { id order_id tracking_number } }
  }
}

# GraphQL: update shipment
mutation {
  partial_shipment_update(input: { id: "shp_...", order_id: "ORD-12345" }) {
    shipment { id order_id }
  }
}
```

### Problems

1. **Not queryable/filterable**: `meta["orders"]` is a JSON field key — filtering requires inefficient full-scan or complex JSON lookups (`meta__has_key`, value iteration). No `db_index` support.
2. **Inconsistent format**: `meta["orders"]` stores comma-separated internal IDs (`ord_abc,ord_def`), not the user-facing `order_id` string from the `Order` model. Consumers must parse and cross-reference.
3. **No carrier passthrough**: Carriers that accept `order_id`/`order_number`/`reference` fields (UPS, FedEx, USPS, Hermes, Sendle) have no standard way to receive the order identifier — it must be manually stuffed into `options` or `reference`.
4. **No REST/GraphQL write support**: There is no API-level mechanism to set an order identifier when creating or updating a shipment — it is only auto-populated by the `shipment_updated` signal.

---

## Goals & Success Criteria

### Goals

1. Add optional, nullable `order_id` field to `Shipment` model with database index for efficient filtering
2. Expose `order_id` as a read/write field on REST API (create, update, list/filter) and GraphQL API (type, mutation inputs, filter)
3. Add `order_id` to SDK `ShipmentRequest` data model so carrier mappers can pass it to carrier APIs
4. Auto-populate `order_id` from linked `Order.order_id` when not explicitly provided
5. Maintain backward compatibility with `meta["orders"]` during transition period

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| `order_id` field on Shipment model with `db_index=True` | Migration applied, field available | Must-have |
| REST API: create/update shipment with `order_id` | 201/200 responses with field persisted | Must-have |
| REST API: filter shipments by `order_id` | `?order_id=X` returns matching shipments | Must-have |
| GraphQL: `ShipmentType.order_id` exposed | Field in schema and queryable | Must-have |
| GraphQL: mutation input accepts `order_id` | `PartialShipmentMutationInput.order_id` | Must-have |
| SDK: `ShipmentRequest.order_id` field | Available in carrier mappers | Must-have |
| Signal auto-populate from Order | `shipment.order_id` set when linked to Order | Must-have |
| `meta["orders"]` still written during transition | Existing consumers unaffected | Must-have |
| Carrier passthrough for 1+ carrier (UPS reference) | `order_id` mapped to carrier field | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] Django migration passes on SQLite, PostgreSQL
- [ ] All existing shipment tests pass
- [ ] New tests for `order_id` CRUD + filter on REST and GraphQL
- [ ] SDK model updated with `order_id` field
- [ ] Signal auto-populates `order_id` from linked Order

**Nice-to-have (P1):**
- [ ] At least one carrier mapper uses `order_id` (e.g., UPS `ReferenceNumber`)
- [ ] OpenAPI documentation updated with `order_id` parameter descriptions

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A. First-class `CharField` on model** | Queryable, indexable, filterable, simple API, matches `Order.order_id` pattern | Requires migration; single-value (not multi-order) | **Selected** |
| **B. Keep using `meta["orders"]`** | Zero migration; already works | Not queryable, inconsistent format, no carrier passthrough, no API write support | Rejected |
| **C. Dedicated `ShipmentOrder` link model** | Supports M2M with metadata | Over-engineered for the use case; M2M already exists via `Order.shipments` | Rejected |
| **D. Use existing `reference` field** | Zero migration; already in SDK | Overloads `reference` semantics; `reference` is a general-purpose field, not order-specific | Rejected |

### Trade-off Analysis

**Option A** is selected because it provides the best developer experience (direct field access, standard ORM filtering, clean API), aligns with the existing `Order.order_id` field pattern, and follows the same nullable `CharField` convention used by `tracking_number`, `reference`, and `shipment_identifier` on the Shipment model. The M2M relationship via `Order.shipments` already handles multi-order scenarios, so a single `order_id` string covers the primary use case of "which order is this shipment for?" without duplication.

---

## Technical Design

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `Shipment` model | `modules/manager/karrio/server/manager/models.py:755` | Add field following `reference` pattern (line 836) |
| `Shipment.DIRECT_PROPS` | Same file, line 758 | Add `"order_id"` to the list |
| `ShippingData` serializer | `modules/core/karrio/server/core/serializers.py:1447` | Add `order_id` field following `reference` pattern (line 1532) |
| `ShipmentSerializer` | `modules/manager/karrio/server/manager/serializers/shipment.py:58` | Inherits from `ShipmentData` → `ShippingData`; field auto-exposed |
| `ShipmentFilters` | `modules/core/karrio/server/core/filters.py:193` | Add `order_id` filter following `reference` pattern (line 228) |
| `ShipmentType` (GraphQL) | `modules/graph/karrio/server/graph/schemas/base/types.py:1666` | Add field following `reference` pattern (line 1679) |
| `PartialShipmentMutationInput` | `modules/graph/karrio/server/graph/schemas/base/inputs.py:488` | Add field following `reference` pattern (line 501) |
| `ShipmentFilter` (GraphQL) | `modules/graph/karrio/server/graph/schemas/base/inputs.py:46` | Add field following `reference` pattern (line 54) |
| `ShipmentRequest` (SDK) | `modules/sdk/karrio/core/models.py:124` | Add field following `reference` pattern (line 139) |
| `shipment_updated` signal | `modules/orders/karrio/server/orders/signals.py:126` | Extend to populate `order_id` from linked Order |
| UPS shipment mapper | `modules/connectors/ups/karrio/providers/ups/shipment/create.py` | Reference pattern for carrier passthrough |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        API Layer                                      │
│  ┌──────────────┐   ┌──────────────────┐   ┌──────────────────────┐  │
│  │  REST API    │   │   GraphQL API    │   │   SDK ShipmentReq    │  │
│  │  order_id    │   │   order_id       │   │   order_id           │  │
│  │  (serializer)│   │   (type+input)   │   │   (data model)       │  │
│  └──────┬───────┘   └───────┬──────────┘   └──────────┬───────────┘  │
│         │                   │                          │              │
│         └───────────────────┼──────────────────────────┘              │
│                             │                                         │
│                    ┌────────▼────────┐                                │
│                    │  Shipment Model │                                │
│                    │  order_id field │                                │
│                    │  (CharField)    │                                │
│                    └────────┬────────┘                                │
│                             │                                         │
│              ┌──────────────┼──────────────┐                         │
│              │              │              │                          │
│     ┌────────▼───┐  ┌──────▼──────┐  ┌───▼──────────┐              │
│     │  DB Index  │  │   Signal    │  │   Carrier    │              │
│     │  (filter)  │  │ auto-pop    │  │  Passthrough │              │
│     └────────────┘  │ from Order  │  │  (mappers)   │              │
│                     └─────────────┘  └──────────────┘              │
└──────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram: Shipment Creation with `order_id`

```
┌────────┐     ┌────────────┐     ┌──────────┐     ┌────────┐     ┌────────┐
│ Client │     │  REST API  │     │Serializer│     │  Model │     │ Signal │
└───┬────┘     └─────┬──────┘     └────┬─────┘     └───┬────┘     └───┬────┘
    │                │                  │               │              │
    │ POST /shipments│                  │               │              │
    │ {order_id: X}  │                  │               │              │
    │───────────────>│                  │               │              │
    │                │  validate(data)  │               │              │
    │                │─────────────────>│               │              │
    │                │                  │  create()     │              │
    │                │                  │──────────────>│              │
    │                │                  │               │  post_save   │
    │                │                  │               │─────────────>│
    │                │                  │               │  if order_id │
    │                │                  │               │  is null:    │
    │                │                  │               │  auto-pop    │
    │                │                  │               │<─────────────│
    │                │  Shipment        │               │              │
    │                │<─────────────────│               │              │
    │  201 {order_id}│                  │               │              │
    │<───────────────│                  │               │              │
    │                │                  │               │              │
```

### Sequence Diagram: Carrier Passthrough

```
┌─────────┐     ┌────────┐     ┌────────────┐     ┌─────────┐
│ Gateway │     │ Mapper │     │   Carrier  │     │Carrier  │
│         │     │        │     │   Schema   │     │  API    │
└────┬────┘     └───┬────┘     └─────┬──────┘     └────┬────┘
     │              │                │                  │
     │ ShipmentReq  │                │                  │
     │ {order_id}   │                │                  │
     │─────────────>│                │                  │
     │              │  Map order_id  │                  │
     │              │  to carrier    │                  │
     │              │  reference     │                  │
     │              │───────────────>│                  │
     │              │                │  HTTP POST       │
     │              │                │─────────────────>│
     │              │                │                  │
     │              │                │  Response        │
     │              │                │<─────────────────│
     │              │  Parse         │                  │
     │              │<───────────────│                  │
     │ ShipmentDet  │                │                  │
     │<─────────────│                │                  │
     │              │                │                  │
```

### Data Models

#### 1. Django Model Change

```python
# modules/manager/karrio/server/manager/models.py
# Add to Shipment class, after 'reference' field (line 836):

order_id = models.CharField(
    max_length=50,
    null=True,
    blank=True,
    db_index=True,
    help_text="The order identifier associated with this shipment",
)
```

Add `"order_id"` to `DIRECT_PROPS` list (after `"reference"`, line 774).

#### 2. REST Serializer Change

```python
# modules/core/karrio/server/core/serializers.py
# Add to ShippingData class, after 'reference' field (line 1538):

order_id = serializers.CharField(
    required=False,
    allow_blank=True,
    allow_null=True,
    max_length=50,
    help_text="The order identifier associated with this shipment",
)
```

#### 3. REST Filter Change

```python
# modules/core/karrio/server/core/filters.py
# Add to ShipmentFilters class, after 'reference' filter (line 232):

order_id = filters.CharFilter(
    field_name="order_id",
    lookup_expr="icontains",
    help_text="an order identifier",
)
```

Add corresponding `openapi.OpenApiParameter` for API documentation.

#### 4. GraphQL Type Change

```python
# modules/graph/karrio/server/graph/schemas/base/types.py
# Add to ShipmentType class, after 'reference' (line 1679):

order_id: typing.Optional[str]
```

#### 5. GraphQL Mutation Input Change

```python
# modules/graph/karrio/server/graph/schemas/base/inputs.py
# Add to PartialShipmentMutationInput, after 'reference' (line 501):

order_id: typing.Optional[str] = strawberry.UNSET
```

#### 6. GraphQL Filter Input Change

```python
# modules/graph/karrio/server/graph/schemas/base/inputs.py
# Add to ShipmentFilter, after 'reference' (line 54):

order_id: typing.Optional[str] = strawberry.UNSET
```

#### 7. SDK Data Model Change

```python
# modules/sdk/karrio/core/models.py
# Add to ShipmentRequest, after 'reference' (line 139):

@attr.s(auto_attribs=True)
class ShipmentRequest:
    """shipment request unified data type."""

    service: str
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]
    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    return_address: Address = JStruct[Address]
    billing_address: Address = JStruct[Address]
    options: Dict = {}
    reference: str = ""
    order_id: str = ""       # NEW: order identifier for carrier passthrough
    label_type: str = None
    is_return: bool = False
    metadata: Dict = {}
```

### Field Reference

| Layer | Field | Type | Required | Default | Index | Description |
|-------|-------|------|----------|---------|-------|-------------|
| Django Model | `order_id` | `CharField(50)` | No | `null` | `db_index=True` | User-facing order identifier |
| REST Serializer | `order_id` | `CharField` | No | `null` | — | Read/write on create and update |
| REST Filter | `order_id` | `CharFilter` | No | — | — | `icontains` lookup |
| GraphQL Type | `order_id` | `Optional[str]` | No | — | — | Exposed on `ShipmentType` |
| GraphQL Input | `order_id` | `Optional[str]` | No | `UNSET` | — | On `PartialShipmentMutationInput` |
| GraphQL Filter | `order_id` | `Optional[str]` | No | `UNSET` | — | On `ShipmentFilter` |
| SDK Model | `order_id` | `str` | No | `""` | — | On `ShipmentRequest` |

### API Changes

**REST Endpoints:**

| Method | Endpoint | Change |
|--------|----------|--------|
| POST | `/api/v1/shipments` | Accepts `order_id` in request body |
| GET | `/api/v1/shipments` | Accepts `?order_id=X` query parameter |
| PUT | `/api/v1/shipments/{id}` | Accepts `order_id` in request body |
| GET | `/api/v1/shipments/{id}` | Returns `order_id` in response |

**Request/Response:**

```json
// POST /api/v1/shipments (create)
{
    "order_id": "ORD-12345",
    "shipper": { "...": "..." },
    "recipient": { "...": "..." },
    "parcels": [{ "...": "..." }]
}

// GET /api/v1/shipments/{id} (response)
{
    "id": "shp_abc123",
    "order_id": "ORD-12345",
    "status": "draft",
    "reference": null,
    "tracking_number": null,
    "...": "..."
}

// GET /api/v1/shipments?order_id=ORD-12345 (filter)
{
    "count": 1,
    "results": [
        { "id": "shp_abc123", "order_id": "ORD-12345", "...": "..." }
    ]
}
```

### Carrier Passthrough Pattern

Carrier mappers that support order/reference fields can optionally map `payload.order_id` to carrier-specific fields. The pattern follows the existing `payload.reference` passthrough:

```python
# Example: UPS carrier mapper passthrough
# modules/connectors/ups/karrio/providers/ups/shipment/create.py

# Existing pattern for reference (line 402-409):
ReferenceNumber=lib.identity(
    ups.ReferenceNumberType(
        Value=payload.reference,
    )
    if (country_pair not in ["US/US", "PR/PR"])
    and any(payload.reference or "")
    else None
),

# Proposed: carrier mappers can use payload.order_id as an additional reference
# or fall back to payload.reference when order_id is not set.
# This is opt-in per carrier — no carrier changes are required in Phase 1.
```

### Order Auto-Populate via Signal

```python
# modules/orders/karrio/server/orders/signals.py
# Extend shipment_updated signal (line 126-161):

def shipment_updated(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    has_json_links = bool(instance.parcels)
    if not has_json_links:
        return

    related_orders = _find_related_orders_from_json(instance)

    if related_orders.exists():
        updates = {}

        # Existing: store order IDs in meta (backward compat)
        meta = {
            **(instance.meta or {}),
            "orders": ",".join([_.id for _ in related_orders]),
        }
        updates["meta"] = meta

        # NEW: auto-populate order_id from first linked Order if not explicitly set
        if not instance.order_id:
            first_order = related_orders.first()
            if first_order and first_order.order_id:
                updates["order_id"] = first_order.order_id

        manager.Shipment.objects.filter(id=instance.id).update(**updates)

    # ... rest of existing signal logic unchanged
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| `order_id` is `null` (not provided) | Field is `null` in DB and API response | Standard nullable field — no special handling |
| `order_id` set to empty string `""` | Treated as `null` (no order) | Serializer `allow_blank=True`; Django stores as empty string; filter ignores blanks |
| Shipment linked to multiple Orders via M2M | `order_id` stores first Order's `order_id` | Signal picks `related_orders.first()`; M2M preserves full relationship |
| Explicit `order_id` conflicts with linked Order | Explicit value wins | Signal only auto-populates when `instance.order_id` is falsy |
| `order_id` longer than 50 chars | Validation error at serializer level | `max_length=50` on both model and serializer |
| Duplicate `order_id` across shipments | Allowed — not unique constraint | Same order can produce multiple shipments (reships, returns) |
| Order deleted but `order_id` remains on shipment | `order_id` string persists (denormalized) | Intentional — `order_id` is a reference string, not a FK |
| `meta["orders"]` and `order_id` out of sync | Both are written; `order_id` is authoritative | Signal updates both; `meta["orders"]` deprecated |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Migration fails on large shipments table | Downtime during deploy | Nullable field = instant `ALTER TABLE ADD COLUMN`; no table rewrite needed |
| Existing API consumers send unexpected `order_id` | Silent storage of junk data | `max_length=50` validation; no format enforcement (user-defined IDs vary) |
| Signal race condition: concurrent save and signal | `order_id` may not be set on first read | Signal uses `filter().update()` — atomic at DB level |
| Carrier rejects `order_id` value | Carrier-specific error | Carrier mappers validate/truncate per carrier requirements |

---

## Implementation Plan

### Phase 1: Model & Migration

| Task | Files | Effort |
|------|-------|--------|
| Add `order_id` field to Shipment model | `modules/manager/karrio/server/manager/models.py` | S |
| Add `"order_id"` to `DIRECT_PROPS` | Same file | S |
| Generate and verify Django migration | `modules/manager/karrio/server/manager/migrations/` | S |
| Verify migration on SQLite and PostgreSQL | — | S |

### Phase 2: REST API

| Task | Files | Effort |
|------|-------|--------|
| Add `order_id` to `ShippingData` serializer | `modules/core/karrio/server/core/serializers.py` | S |
| Add `order_id` filter to `ShipmentFilters` | `modules/core/karrio/server/core/filters.py` | S |
| Add OpenAPI parameter documentation | Same file | S |
| Add REST API tests (create, update, filter) | `modules/manager/karrio/server/manager/tests/test_shipments.py` | M |

### Phase 3: GraphQL API

| Task | Files | Effort |
|------|-------|--------|
| Add `order_id` to `ShipmentType` | `modules/graph/karrio/server/graph/schemas/base/types.py` | S |
| Add `order_id` to `PartialShipmentMutationInput` | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | S |
| Add `order_id` to `ShipmentFilter` | Same file | S |
| Add GraphQL mutation tests | `modules/graph/karrio/server/graph/tests/test_partial_shipments.py` | M |

### Phase 4: SDK & Signal

| Task | Files | Effort |
|------|-------|--------|
| Add `order_id` to `ShipmentRequest` | `modules/sdk/karrio/core/models.py` | S |
| Update `shipment_updated` signal for auto-populate | `modules/orders/karrio/server/orders/signals.py` | S |
| Add signal test for auto-populate behavior | `modules/orders/karrio/server/orders/tests/` | M |

### Phase 5: Carrier Passthrough (P1)

| Task | Files | Effort |
|------|-------|--------|
| Document carrier passthrough pattern | This PRD / code comments | S |
| (Optional) Map `order_id` in UPS mapper | `modules/connectors/ups/karrio/providers/ups/shipment/create.py` | M |

**Dependencies:** Phase 2-4 depend on Phase 1. Phase 5 depends on Phase 4.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Django model tests | `modules/manager/karrio/server/manager/tests/test_shipments.py` | Create, update, filter with `order_id` |
| GraphQL mutation tests | `modules/graph/karrio/server/graph/tests/test_partial_shipments.py` | Mutation and query with `order_id` |
| Signal tests | `modules/orders/karrio/server/orders/tests/` | Auto-populate from linked Order |
| SDK unit tests | `modules/sdk/` | `ShipmentRequest` serialization with `order_id` |

### Test Cases

#### REST API Tests

```python
"""REST API tests for order_id field on Shipment."""

from unittest import mock

class TestShipmentOrderId(TestShipmentFixture):
    def test_create_shipment_with_order_id(self):
        """Verify shipment creation with order_id."""
        data = {
            **SHIPMENT_DATA,
            "order_id": "ORD-12345",
        }
        response = self.client.post("/api/shipments", data=data, format="json")
        print(response)
        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["order_id"], "ORD-12345")

    def test_create_shipment_without_order_id(self):
        """Verify shipment creation without order_id returns null."""
        response = self.client.post("/api/shipments", data=SHIPMENT_DATA, format="json")
        print(response)
        self.assertResponseNoErrors(response)
        self.assertIsNone(response.data["order_id"])

    def test_update_shipment_order_id(self):
        """Verify shipment order_id can be updated."""
        response = self.client.put(
            f"/api/shipments/{self.shipment.pk}",
            data={"order_id": "ORD-99999"},
            format="json",
        )
        print(response)
        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["order_id"], "ORD-99999")

    def test_filter_shipments_by_order_id(self):
        """Verify shipments can be filtered by order_id."""
        self.shipment.order_id = "ORD-FILTER-TEST"
        self.shipment.save(update_fields=["order_id"])

        response = self.client.get("/api/shipments?order_id=ORD-FILTER")
        print(response)
        self.assertResponseNoErrors(response)
        self.assertGreaterEqual(response.data["count"], 1)
```

#### GraphQL Mutation Tests

```python
"""GraphQL tests for order_id field on Shipment."""

class TestShipmentOrderIdGraphQL(GraphTestCase):
    def test_partial_update_order_id(self):
        """Verify order_id can be set via GraphQL mutation."""
        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  order_id
                }
                errors { field messages }
              }
            }
            """,
            variables={
                "data": {
                    "id": self.shipment.id,
                    "order_id": "ORD-GQL-TEST",
                }
            },
        )
        print(response)
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["partial_shipment_update"]["shipment"]["order_id"],
            "ORD-GQL-TEST",
        )
```

#### Signal Auto-Populate Test

```python
"""Signal tests for order_id auto-population."""

class TestShipmentOrderIdSignal(TestCase):
    def test_auto_populate_order_id_from_linked_order(self):
        """Verify order_id is auto-populated when shipment is linked to an Order."""
        order = Order.objects.create(order_id="ORD-AUTO-TEST", ...)
        shipment = Shipment.objects.create(order_id=None, ...)
        # Link shipment to order and trigger signal
        order.shipments.add(shipment)
        shipment.refresh_from_db()
        self.assertEqual(shipment.order_id, "ORD-AUTO-TEST")

    def test_explicit_order_id_not_overwritten(self):
        """Verify explicitly set order_id is not overwritten by signal."""
        order = Order.objects.create(order_id="ORD-FROM-ORDER", ...)
        shipment = Shipment.objects.create(order_id="ORD-EXPLICIT", ...)
        order.shipments.add(shipment)
        shipment.refresh_from_db()
        self.assertEqual(shipment.order_id, "ORD-EXPLICIT")
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run shipment REST tests
karrio test --failfast karrio.server.manager.tests.test_shipments

# Run GraphQL tests
karrio test --failfast karrio.server.graph.tests.test_partial_shipments

# Run order signal tests
karrio test --failfast karrio.server.orders.tests

# Run all server tests
./bin/run-server-tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Migration on large `shipments` table causes lock | Medium | Low | Nullable `CharField` = instant `ADD COLUMN` on PostgreSQL (no rewrite) |
| Existing tests break due to unexpected `order_id` in response | Medium | Medium | Add `order_id` to test fixtures; use `mock.ANY` for optional fields |
| `meta["orders"]` consumers break if removed too early | High | Low | Keep dual-write for 2 releases; document deprecation timeline |
| `order_id` filter causes performance issues | Low | Low | `db_index=True` on the field; `icontains` on indexed column is efficient |
| SDK model change breaks carrier mappers | Medium | Low | `order_id` defaults to `""` — existing mappers ignore it unless they explicitly use it |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: `order_id` is optional and nullable — existing API consumers that don't send it are unaffected. Responses include the new field as `null`.
- **Data compatibility**: Existing shipments have `order_id = null`. No data migration required.
- **`meta["orders"]` compatibility**: The signal continues to write `meta["orders"]` during the transition period. Existing consumers reading `meta.orders` are unaffected.
- **SDK compatibility**: `order_id` defaults to `""` in `ShipmentRequest` — existing carrier mappers that don't reference it are unaffected.

### Deprecation Path for `meta["orders"]`

| Phase | Release | Action |
|-------|---------|--------|
| 1 | Current | Add `order_id` field; signal writes both `order_id` and `meta["orders"]` |
| 2 | Current + 1 | Add deprecation notice to API docs for `meta["orders"]`; recommend `order_id` |
| 3 | Current + 2 | Stop writing `meta["orders"]` in signal; field remains read-only for historical data |

### Rollback Procedure

1. **Identify issue**: Monitor API error rates and test suite after deploy
2. **Stop rollout**: If migration or serializer issues arise, halt deploy
3. **Revert changes**: Revert the commit; run reverse migration (`migrations.RemoveField`)
4. **Verify recovery**: Run full test suite; confirm `meta["orders"]` still works as before

---

## Appendices

### Appendix A: Files to Modify (Complete List)

| # | File | Change |
|---|------|--------|
| 1 | `modules/manager/karrio/server/manager/models.py` | Add `order_id` field + `DIRECT_PROPS` entry |
| 2 | `modules/manager/karrio/server/manager/migrations/XXXX_*.py` | Auto-generated migration |
| 3 | `modules/core/karrio/server/core/serializers.py` | Add `order_id` to `ShippingData` |
| 4 | `modules/core/karrio/server/core/filters.py` | Add `order_id` filter + OpenAPI param |
| 5 | `modules/graph/karrio/server/graph/schemas/base/types.py` | Add to `ShipmentType` |
| 6 | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Add to `PartialShipmentMutationInput` + `ShipmentFilter` |
| 7 | `modules/sdk/karrio/core/models.py` | Add to `ShipmentRequest` |
| 8 | `modules/orders/karrio/server/orders/signals.py` | Extend `shipment_updated` signal |
| 9 | `modules/manager/karrio/server/manager/tests/test_shipments.py` | Add REST tests |
| 10 | `modules/graph/karrio/server/graph/tests/test_partial_shipments.py` | Add GraphQL tests |

### Appendix B: Carrier Reference Field Mappings

Carriers that accept order/reference fields and could use `order_id` in future phases:

| Carrier | Carrier Field | Current Source | Future Source |
|---------|---------------|----------------|---------------|
| UPS | `ReferenceNumber.Value` | `payload.reference` | `payload.order_id` or `payload.reference` |
| FedEx | `documentReference` | `payload.reference` | `payload.order_id` or `payload.reference` |
| USPS | `customerReference[].referenceNumber` | `payload.reference` | `payload.order_id` or `payload.reference` |
| Hermes | `shipment_order_id` (response) | Carrier response | Read-only from carrier |
| Sendle | `order_id` (response) | Carrier response | Read-only from carrier |
| Australia Post | `order_id` (manifest) | Carrier response | Read-only from carrier |
