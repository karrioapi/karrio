# Cancellation by `request_id` & Resource Archiving (Soft-Delete)

<!-- ENHANCEMENT + ARCHITECTURE: API enhancement + cross-cutting model/manager change -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-03-20 |
| Status | Planning |
| Owner | Karrio Core Team |
| Type | Enhancement / Architecture |
| Reference | [AGENTS.md](../../AGENTS.md) |

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

This PRD proposes two closely related features: **(1)** allowing callers to cancel shipments, trackers, pickups, and orders using the `request_id` they supplied at creation time (via the `X-Request-ID` header), in addition to the existing internal `id`-based cancellation; and **(2)** introducing `is_archived` / `archived_at` fields on those same four resource types so that completed, cancelled, or stale resources can be hidden from default queries and excluded from background processing without being permanently deleted.

These features are linked: `request_id`-based cancellation solves the "I don't know the internal ID" problem (timeout recovery, async workflows), while archiving solves the "cancelled/completed resources clutter my lists and consume background job slots" problem. Together they complete the resource lifecycle management story.

### Key Architecture Decisions

1. **`request_id` lives in `meta` JSONField on all four models**: stored at `meta["request_id"]`, already indexed for filter queries. No schema migration needed for Feature 1.
2. **`request_id` lookup extends existing mutations/endpoints**: no separate endpoints or mutations; the existing cancel operations accept an optional `request_id` parameter alongside `id`.
3. **Archiving uses a custom manager pattern**: `objects` manager excludes `is_archived=True` by default; `all_objects` manager includes everything. No scattered `filter(is_archived=False)` in views/serializers/resolvers.
4. **Background tracker jobs filter on `is_archived`**: the `update_trackers` dispatcher query adds `is_archived=False` to exclude archived trackers from polling.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| `request_id` as alternative lookup key for cancel operations | Cancellation by other metadata fields |
| REST + GraphQL cancel by `request_id` for Shipment, Tracker, Pickup, Order | New bulk cancellation endpoints |
| `is_archived` + `archived_at` fields on Shipment, Tracking, Pickup, Order | Hard-delete / GDPR purge workflow |
| Default manager exclusion of archived records | Archiving for other models (Manifest, DocumentUploadRecord, etc.) |
| Background job exclusion of archived trackers | Automatic archiving rules / retention policies |
| REST + GraphQL archive/unarchive mutations + list filters | Dashboard UI for archive actions (separate PRD) |
| Idempotent cancel (already-cancelled returns success) | Carrier-side tracking stop notification |

---

## Open Questions & Decisions

### Pending Questions

| # | Question | Context | Options | Status |
|---|----------|---------|---------|--------|
| Q1 | Should `request_id` lookup be scoped to the authenticated tenant only? | `request_id` is user-supplied; two tenants could theoretically send the same value. Tenant-scoping is safer but `request_id` is already set via `X-Request-ID` header which callers control. | A) Tenant-scoped only (use `access_by`), B) Globally unique lookup | Pending |
| Q2 | For GraphQL cancellation by `request_id` — extend existing mutation input or add a separate mutation? | Extending keeps the API surface small; a separate mutation is more explicit. | A) Add optional `request_id: String` to existing mutation input, B) New `cancel_shipment_by_request_id` mutation | Pending |
| Q3 | Should archiving cascade to child resources? | e.g., archiving a shipment could also archive its linked tracker. | A) No cascade (archive each independently), B) Cascade to direct children (shipment -> tracker), C) Configurable | Pending |
| Q4 | Should archived records be included in analytics/reporting queries? | Some reporting may need full history; excluding archived records could skew metrics. | A) Always exclude (use `all_objects` explicitly for reports), B) Include by default in reporting, C) Separate reporting manager | Pending |
| Q5 | Is unarchiving always allowed, or only for non-cancelled records? | Users might want to unarchive a cancelled shipment for audit review. | A) Always allowed, B) Only non-cancelled, C) Only within a time window | Pending |
| Q6 | Should we emit webhook events for archive/unarchive? | Integrators may want to sync archive state to external systems. | A) Yes (new event types: `shipment.archived`, etc.), B) No (local-only operation) | Pending |
| Q7 | What happens if you try to cancel an archived record? | Archiving and cancellation are independent concepts, but the interaction needs defining. | A) Allow (unarchive is not required first), B) Reject with 409, C) Auto-unarchive then cancel | Pending |
| Q8 | For trackers: should archiving immediately stop background updates or wait for next cycle? | Immediate stop requires signaling the in-flight Huey task; next-cycle is simpler. | A) Next cycle (simpler, up to `DEFAULT_TRACKERS_UPDATE_INTERVAL` delay), B) Immediate (cancel in-flight task) | Pending |
| Q9 | Should the `DELETE /v1/trackers/{id}` endpoint archive instead of hard-delete? | Currently `DELETE` calls `tracker.delete(keep_parents=True)` which is a hard delete. Changing to archive would be a breaking change. | A) Keep hard-delete, add separate archive endpoint, B) Change DELETE to archive (breaking), C) Add `?permanent=true` param | Pending |
| Q10 | Should `request_id` lookup return an error when multiple records match, or use the most recent? | `request_id` is not enforced as unique per tenant. Multiple records could share the same value if the caller reuses IDs. | A) Error 409 "ambiguous request_id", B) Most recent record, C) Error unless exactly one match | Pending |
| Q11 | Should auto-created trackers (from shipment purchase) be archivable independently of their shipment? | Auto-trackers are created as a side effect of purchasing a shipment. Independent archiving could leave orphaned tracker references. | A) Independent, B) Only via shipment archive cascade, C) Warn but allow | Pending |
| Q12 | For the Order model, should archiving affect the order counter sequence? | Archived orders still occupy a sequence number. Callers might expect contiguous numbering. | A) No effect (archived orders keep their number), B) Archived orders release their number | Pending |

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| `request_id` matches records across multiple tenants | Security: tenant A could cancel tenant B's resource | Always scope lookup to authenticated tenant via `access_by` | Yes (Q1) |
| Caller provides both `id` and `request_id` and they resolve to different records | Ambiguous intent | `id` takes precedence; `request_id` is ignored when `id` is present | No |
| Archiving a tracker that is mid-update in a Huey batch | Race condition: save after archive could unset `is_archived` | Background task should skip trackers where `is_archived=True` at save time | No |
| Cancelling an already-archived record | UX: should archived records be cancellable? | Depends on Q7 decision | Yes (Q7) |

---

## Problem Statement

### Current State

**Problem 1: Callers must know the internal karrio ID to cancel resources**

When a caller creates a shipment via `POST /v1/shipments`, the response contains the internal ID (e.g., `shp_a1b2c3...`). If the HTTP response is lost (timeout, network failure), the caller has no way to cancel the resource without first searching for it. The caller's own correlation ID — the `X-Request-ID` header, stored as `meta["request_id"]` — cannot be used in cancellation endpoints.

```python
# Current: cancel requires the internal karrio ID
# POST /v1/shipments/{shp_a1b2c3}/cancel

class ShipmentCancel(APIView):
    def post(self, request, pk):
        shipment = models.Shipment.access_by(request).get(pk=pk)  # pk = shp_*
        # ... cancel logic
```

```python
# Desired: cancel also accepts request_id
# POST /v1/shipments/cancel  (with request_id in body)
# OR
# POST /v1/shipments/{shp_a1b2c3}/cancel  (unchanged, still works)
```

**Problem 2: No way to "close" a tracker without deleting it**

Trackers that are no longer needed continue consuming background polling slots. The only option is hard-delete (`DELETE /v1/trackers/{id}`), which loses all tracking history. There is no soft-close / archive operation.

```python
# Current: background job polls ALL non-delivered trackers
# modules/events/.../tracking.py:107
models.Tracking.objects.filter(
    delivered=False,
    updated_at__lt=timezone.now() - delta,
    created_at__gt=max_age_cutoff,
)
# No is_archived filter — archived trackers would still be polled
```

**Problem 3: Cancelled and completed resources clutter list views**

Shipments, orders, and pickups that are cancelled or fulfilled remain in default list queries indefinitely. There is no built-in way to move them out of the active working set while preserving them for audit.

### Desired State

```python
# Cancel by request_id
# POST /v1/shipments/cancel
# Body: {"request_id": "req_abc123"}
shipment = models.Shipment.access_by(request).get(meta__request_id=request_id)
# ... cancel logic (same as today)

# Archive a tracker — stops background polling, keeps history
# POST /v1/trackers/{trk_xyz}/archive
tracker.is_archived = True
tracker.archived_at = timezone.now()
tracker.save(update_fields=["is_archived", "archived_at", "updated_at"])

# Background job automatically skips archived trackers
models.Tracking.objects.filter(
    delivered=False,
    is_archived=False,  # NEW — excludes archived
    updated_at__lt=timezone.now() - delta,
    created_at__gt=max_age_cutoff,
)

# Default list queries exclude archived records (via manager)
# GET /v1/shipments  → only non-archived
# GET /v1/shipments?is_archived=true  → only archived
```

### Problems

1. **No `request_id`-based cancellation**: callers who lose the HTTP response (timeout, crash) cannot cancel resources without first listing/searching to recover the internal ID
2. **No idempotent cancel by correlation ID**: retrying a cancel-by-`request_id` after a timeout should return success if the resource is already cancelled, enabling safe retry loops
3. **Stale trackers consume background job capacity**: trackers that are no longer needed (carrier lost, shipment delivered weeks ago, test data) continue being polled every `DEFAULT_TRACKERS_UPDATE_INTERVAL` seconds
4. **No soft-delete/archive for audit trail**: hard-deleting a tracker destroys tracking history; there is no middle ground between "active" and "gone"
5. **List view clutter**: cancelled shipments, fulfilled orders, and expired pickups remain in default list queries, requiring manual client-side filtering

---

## Goals & Success Criteria

### Goals

1. Enable cancellation of any resource (Shipment, Tracker, Pickup, Order) using `request_id` as an alternative to internal `id`
2. Make cancel-by-`request_id` idempotent: already-cancelled resources return success
3. Add `is_archived` + `archived_at` to Shipment, Tracking, Pickup, Order with default manager exclusion
4. Exclude archived trackers from background polling jobs
5. Expose archive/unarchive operations via REST and GraphQL
6. Add `is_archived` filter to all list queries (REST + GraphQL)

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Cancel by `request_id` works for all 4 resource types | 100% coverage | Must-have |
| Idempotent cancel returns 200/202 (not error) for already-cancelled | All 4 types | Must-have |
| Archived trackers excluded from background polling | Zero archived trackers polled | Must-have |
| Default list queries exclude archived records | All 4 types | Must-have |
| `is_archived` filter available in REST + GraphQL | All 4 types | Must-have |
| Archive/unarchive REST + GraphQL endpoints | All 4 types | Must-have |
| All migrations reversible | 100% | Must-have |
| No N+1 queries introduced | Zero new N+1 patterns | Must-have |
| Dashboard archive UI | Tabs + actions | Nice-to-have (separate PRD) |

### Launch Criteria

**Must-have (P0):**
- [ ] Cancel by `request_id` for Shipment, Tracker, Pickup, Order
- [ ] `is_archived` + `archived_at` fields with migrations
- [ ] Default manager excludes archived records
- [ ] Background tracker job excludes archived trackers
- [ ] REST + GraphQL archive/unarchive endpoints
- [ ] `is_archived` filter on all list queries
- [ ] Comprehensive test coverage

**Nice-to-have (P1):**
- [ ] Webhook events for archive/unarchive
- [ ] Bulk archive/unarchive endpoints
- [ ] Dashboard archive UI (tabs, actions, badges)

---

## Alternatives Considered

### Feature 1: Cancellation by `request_id`

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| A) Extend existing cancel endpoints with optional `request_id` param | Minimal API surface change; backward compatible | Slightly more complex lookup logic in existing handlers | **Selected** |
| B) Separate cancel-by-request-id endpoints (`POST /v1/shipments/cancel-by-request-id`) | Very explicit; no risk of breaking existing behavior | Doubles the number of cancel endpoints; divergent code paths | Rejected |
| C) Generic `/v1/cancel` endpoint that accepts `{resource_type, request_id}` | Single endpoint for all types | Non-RESTful; harder to document and permission | Rejected |

### Feature 2: Archiving

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| A) Custom default manager excluding `is_archived=True` | Centralised; no scattered filters; follows `test_mode` pattern | Requires `all_objects` for admin/reporting; `select_related` needs care | **Selected** |
| B) Soft-delete via `django-safedelete` library | Battle-tested; handles cascades | External dependency; may conflict with existing `OwnedEntity` pattern | Rejected |
| C) `status = "archived"` (reuse existing status field) | No new fields | Overloads status semantics; a cancelled shipment can also be archived; mixing lifecycle + visibility | Rejected |
| D) Separate archive table (move records) | Clean separation; fast default queries | Complex migration; breaks ForeignKey references; two-phase lookup | Rejected |

### Trade-off Analysis

**Approach A (extend existing endpoints)** was chosen for cancellation because it adds the feature with minimal API surface change. Callers who don't use `request_id` see zero difference.

**Approach A (custom manager)** was chosen for archiving because it mirrors the existing `test_mode` filtering pattern in `ControlledAccessModel.access_by()` and centralises the filter in one place. The `all_objects` escape hatch provides explicit opt-in for admin and reporting contexts.

---

## Technical Design

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `ControlledAccessModel.access_by()` | `modules/core/karrio/server/core/models/base.py:24-52` | Model for `is_archived` integration into access filtering |
| `test_mode` filtering pattern | `modules/core/karrio/server/core/models/base.py:42-45` | Exact pattern to replicate for `is_archived` |
| `ShipmentCancelSerializer.update()` | `modules/manager/karrio/server/manager/serializers/shipment.py:589-612` | Add `request_id` lookup before existing cancel logic |
| `TrackersDetails.delete()` | `modules/manager/karrio/server/manager/views/trackers.py:300-308` | Add `request_id` lookup alternative |
| `PickupCancel` view | `modules/manager/karrio/server/manager/views/pickups.py:184-210` | Add `request_id` lookup |
| `OrderCancel` view | `modules/orders/karrio/server/orders/views.py:165-186` | Add `request_id` lookup |
| `update_trackers()` dispatcher | `modules/events/karrio/server/events/task_definitions/base/tracking.py:76-139` | Add `is_archived=False` filter at line 107 |
| `_retire_aged_out_trackers()` | `modules/events/karrio/server/events/task_definitions/base/tracking.py:60-73` | Add `is_archived=False` filter |
| `ShipmentFilters` | `modules/core/karrio/server/core/filters.py:193-547` | Add `is_archived` filter field |
| `TrackerFilters` | `modules/core/karrio/server/core/filters.py:549-661` | Add `is_archived` filter field |
| `OrderFilters` | `modules/orders/karrio/server/orders/filters.py:10-245` | Add `is_archived` filter field |
| `ShipmentFilter` (GraphQL) | `modules/graph/karrio/server/graph/schemas/base/inputs.py:47-67` | Add `is_archived` field |
| `TrackerFilter` (GraphQL) | `modules/graph/karrio/server/graph/schemas/base/inputs.py:36-43` | Add `is_archived` field |
| `request_id` storage | `meta["request_id"]` on Shipment, Tracking, Pickup, Order | Used as lookup key for cancel-by-request-id |
| `ShipmentManager` | `modules/manager/karrio/server/manager/models.py` | Extend with `is_archived` default exclusion |
| `TrackingManager` | `modules/manager/karrio/server/manager/models.py` | Extend with `is_archived` default exclusion |
| `PickupManager` | `modules/manager/karrio/server/manager/models.py` | Extend with `is_archived` default exclusion |
| `OrderManager` | `modules/orders/karrio/server/orders/models.py` | Extend with `is_archived` default exclusion |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CLIENT / DASHBOARD                               │
│                                                                         │
│  Cancel by ID (existing)    Cancel by request_id (NEW)    Archive (NEW) │
│  POST /shipments/{id}/cancel   POST /shipments/cancel     POST /ship.. │
│  DELETE /trackers/{id}         body: {request_id: "..."}   .../{id}/arc │
└──────────┬──────────────────────────┬───────────────────────────┬───────┘
           │                          │                           │
           ▼                          ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          REST / GraphQL Layer                           │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ Lookup Logic                                                      │ │
│  │                                                                    │ │
│  │  if id provided:                                                   │ │
│  │      resource = Model.access_by(request).get(pk=id)               │ │
│  │  elif request_id provided:                                         │ │
│  │      resource = Model.access_by(request).get(meta__request_id=..) │ │
│  │  else:                                                             │ │
│  │      return 400 "id or request_id required"                       │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌─────────────────────┐  ┌──────────────────────┐                     │
│  │ Cancel Serializer   │  │ Archive Helper        │                    │
│  │ (existing + lookup) │  │ archive_resource()    │                    │
│  └─────────────────────┘  │ unarchive_resource()  │                    │
│                            └──────────────────────┘                     │
└──────────┬──────────────────────────────────────────────────┬───────────┘
           │                                                  │
           ▼                                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            Model Layer                                  │
│                                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────┐  ┌──────────┐│
│  │   Shipment     │  │   Tracking     │  │   Pickup    │  │  Order   ││
│  │ + is_archived  │  │ + is_archived  │  │ + is_archived│  │+ is_arch ││
│  │ + archived_at  │  │ + archived_at  │  │ + archived_at│  │+ arch_at ││
│  └────────────────┘  └────────────────┘  └─────────────┘  └──────────┘│
│                                                                         │
│  objects = NotArchivedManager()     all_objects = models.Manager()      │
│  (default: is_archived=False)       (includes everything)               │
└──────────┬──────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Background Jobs                                  │
│                                                                         │
│  update_trackers()                                                      │
│    └─ Tracking.objects.filter(                                          │
│          delivered=False,                                                │
│          is_archived=False,  ◄── NEW FILTER                             │
│          updated_at__lt=...,                                            │
│          created_at__gt=...,                                            │
│       )                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram: Cancel by `request_id`

```
┌────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐     ┌─────────┐
│ Client │     │  REST   │     │ Serializer│     │  Model   │     │ Carrier │
└───┬────┘     └────┬────┘     └─────┬─────┘     └────┬─────┘     └────┬────┘
    │               │                │                 │                │
    │ POST /v1/shipments/cancel      │                 │                │
    │ {request_id: "req_abc123"}     │                 │                │
    │──────────────>│                │                 │                │
    │               │                │                 │                │
    │               │ 1. Lookup by request_id          │                │
    │               │ access_by(req).get(              │                │
    │               │   meta__request_id="req_abc123") │                │
    │               │───────────────────────────────>  │                │
    │               │                │                 │                │
    │               │  2. Shipment found               │                │
    │               │ <───────────────────────────────  │                │
    │               │                │                 │                │
    │               │ 3. Already cancelled?            │                │
    │               │────> if status=="cancelled":     │                │
    │               │      return 202 (idempotent)     │                │
    │               │                │                 │                │
    │               │ 4. Delegate to serializer        │                │
    │               │───────────────>│                 │                │
    │               │                │ 5. Call carrier void API         │
    │               │                │────────────────────────────────> │
    │               │                │                 │                │
    │               │                │ 6. Carrier confirms              │
    │               │                │ <──────────────────────────────  │
    │               │                │                 │                │
    │               │                │ 7. Update status="cancelled"     │
    │               │                │────────────────>│                │
    │               │                │                 │                │
    │  8. 200 OK {shipment}         │                 │                │
    │ <──────────────│                │                 │                │
    │               │                │                 │                │
```

### Sequence Diagram: Archive Resource

```
┌────────┐     ┌─────────┐     ┌──────────────────┐     ┌──────────┐
│ Client │     │  REST   │     │ archive_resource()│     │  Model   │
└───┬────┘     └────┬────┘     └────────┬─────────┘     └────┬─────┘
    │               │                   │                     │
    │ POST /v1/trackers/{trk_x}/archive │                     │
    │──────────────>│                   │                     │
    │               │                   │                     │
    │               │ 1. Lookup tracker │                     │
    │               │ access_by(req).get(pk=trk_x)           │
    │               │────────────────────────────────────────>│
    │               │                   │                     │
    │               │ 2. Tracker found  │                     │
    │               │ <────────────────────────────────────── │
    │               │                   │                     │
    │               │ 3. Already archived?                    │
    │               │────> if is_archived:                    │
    │               │      return 200 (idempotent)            │
    │               │                   │                     │
    │               │ 4. archive_resource(tracker)            │
    │               │──────────────────>│                     │
    │               │                   │ is_archived = True  │
    │               │                   │ archived_at = now() │
    │               │                   │ save(update_fields) │
    │               │                   │────────────────────>│
    │               │                   │                     │
    │  5. 200 OK {tracker}             │                     │
    │ <──────────────│                   │                     │
    │               │                   │                     │
```

### Data Models

#### New Fields (added to Shipment, Tracking, Pickup, Order)

```python
# Added to each model class
is_archived = models.BooleanField(
    default=False,
    db_index=True,
    help_text="Archived records are excluded from default queries and background jobs.",
)
archived_at = models.DateTimeField(
    null=True,
    blank=True,
    help_text="Timestamp when the record was archived. Null if not archived.",
)
```

#### Manager Pattern

```python
# modules/core/karrio/server/core/models/entity.py (or a new managers.py)

class NotArchivedQuerySet(models.QuerySet):
    """Default queryset that excludes archived records."""

    def include_archived(self):
        """Opt-in to include archived records in the queryset."""
        return self.model.all_objects.filter(pk__in=self)  # escape to unfiltered

    def archived_only(self):
        """Return only archived records."""
        return self.model.all_objects.filter(is_archived=True)


class NotArchivedManager(models.Manager):
    """Default manager that excludes archived records."""

    def get_queryset(self):
        return NotArchivedQuerySet(self.model, using=self._db).filter(
            is_archived=False
        )
```

Each model's existing custom manager (e.g., `ShipmentManager`, `TrackingManager`) will inherit from `NotArchivedManager` instead of `models.Manager`:

```python
class ShipmentManager(NotArchivedManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("created_by", "manifest")
            .prefetch_related(
                "shipment_tracker",
                *(("org",) if settings.MULTI_ORGANIZATIONS else tuple()),
            )
            .defer("label", "invoice", "validation")
        )

# On the model:
class Shipment(core.OwnedEntity):
    objects = ShipmentManager()
    all_objects = models.Manager()  # includes archived
    # ...
```

#### Shared Archive Helper

```python
# modules/core/karrio/server/core/utils.py (or similar)

import typing
from django.utils import timezone
from django.db import models

def archive_resource(instance: models.Model) -> models.Model:
    """Archive a resource by setting is_archived=True and archived_at."""
    instance.is_archived = True
    instance.archived_at = timezone.now()
    instance.save(update_fields=["is_archived", "archived_at", "updated_at"])
    return instance

def unarchive_resource(instance: models.Model) -> models.Model:
    """Unarchive a resource by clearing is_archived and archived_at."""
    instance.is_archived = False
    instance.archived_at = None
    instance.save(update_fields=["is_archived", "archived_at", "updated_at"])
    return instance
```

#### `request_id` Lookup Helper

```python
# modules/core/karrio/server/core/utils.py (or similar)

import typing
from django.db import models

def resolve_by_id_or_request_id(
    queryset: models.QuerySet,
    id: typing.Optional[str] = None,
    request_id: typing.Optional[str] = None,
) -> models.Model:
    """Resolve a resource by id or request_id (id takes precedence).

    Raises:
        ValidationError: if neither id nor request_id provided
        Model.DoesNotExist: if no match found
        Model.MultipleObjectsReturned: if request_id matches multiple records
    """
    if id:
        return queryset.get(pk=id)
    if request_id:
        return queryset.get(meta__request_id=request_id)
    raise serializers.ValidationError("id or request_id is required")
```

### Field Reference

#### `request_id` Storage by Model

| Model | Field Path | Storage | Filter Syntax | Indexed |
|-------|-----------|---------|---------------|---------|
| Shipment | `meta["request_id"]` | JSONField (`meta`) | `meta__request_id=value` | Via JSON key lookup |
| Tracking | `meta["request_id"]` | JSONField (`meta`) | `meta__request_id=value` | Via JSON key lookup |
| Pickup | `meta["request_id"]` | JSONField (`meta`) | `meta__request_id=value` | Via JSON key lookup |
| Order | `meta["request_id"]` | JSONField (`meta`) | `meta__request_id=value` | Via JSON key lookup |

#### New Fields

| Field | Type | Default | Index | Null | Description |
|-------|------|---------|-------|------|-------------|
| `is_archived` | `BooleanField` | `False` | `db_index=True` | No | Soft-delete flag |
| `archived_at` | `DateTimeField` | `None` | No | Yes | Archive timestamp |

### API Changes

#### Feature 1: Cancel by `request_id`

**Shipment Cancel (REST)**

| Method | Endpoint | Description | Change |
|--------|----------|-------------|--------|
| POST | `/v1/shipments/{id}/cancel` | Cancel by ID | Unchanged |
| POST | `/v1/shipments/cancel` | Cancel by request_id | **NEW** |

```json
// NEW: POST /v1/shipments/cancel
// Request
{
  "request_id": "req_abc123"
}

// Response: 200 OK (same as existing cancel response)
{
  "id": "shp_a1b2c3...",
  "status": "cancelled",
  "meta": {"request_id": "req_abc123"},
  ...
}

// Response: 202 Accepted (already cancelled — idempotent)
{
  "id": "shp_a1b2c3...",
  "status": "cancelled",
  ...
}
```

**Tracker Discard (REST)**

| Method | Endpoint | Description | Change |
|--------|----------|-------------|--------|
| DELETE | `/v1/trackers/{id_or_tracking_number}` | Discard by ID or tracking number | Unchanged |
| DELETE | `/v1/trackers/by-request-id/{request_id}` | Discard by request_id | **NEW** |

**Pickup Cancel (REST)**

| Method | Endpoint | Description | Change |
|--------|----------|-------------|--------|
| POST | `/v1/pickups/{id}/cancel` | Cancel by ID | Unchanged |
| POST | `/v1/pickups/cancel` | Cancel by request_id | **NEW** |

```json
// NEW: POST /v1/pickups/cancel
// Request
{
  "request_id": "req_def456"
}
```

**Order Cancel (REST)**

| Method | Endpoint | Description | Change |
|--------|----------|-------------|--------|
| POST | `/v1/orders/{id}/cancel` | Cancel by ID | Unchanged |
| POST | `/v1/orders/cancel` | Cancel by request_id | **NEW** |

```json
// NEW: POST /v1/orders/cancel
// Request
{
  "request_id": "req_ghi789"
}
```

**GraphQL Mutations (all resource types)**

```graphql
# Extend existing mutation inputs with optional request_id
# (pending decision Q2 — shown here as extended input approach)

mutation {
  cancel_shipment(input: {
    # Provide either id or request_id (id takes precedence)
    id: "shp_a1b2c3"       # optional if request_id provided
    request_id: "req_abc"   # NEW — optional if id provided
  }) {
    id
    status
  }
}
```

#### Feature 2: Archive / Unarchive

**REST Endpoints (all resource types)**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/shipments/{id}/archive` | Archive shipment |
| POST | `/v1/shipments/{id}/unarchive` | Unarchive shipment |
| POST | `/v1/trackers/{id}/archive` | Archive tracker |
| POST | `/v1/trackers/{id}/unarchive` | Unarchive tracker |
| POST | `/v1/pickups/{id}/archive` | Archive pickup |
| POST | `/v1/pickups/{id}/unarchive` | Unarchive pickup |
| POST | `/v1/orders/{id}/archive` | Archive order |
| POST | `/v1/orders/{id}/unarchive` | Unarchive order |

```json
// POST /v1/shipments/{id}/archive
// Request: empty body
// Response: 200 OK
{
  "id": "shp_a1b2c3...",
  "is_archived": true,
  "archived_at": "2026-03-20T12:00:00Z",
  ...
}

// POST /v1/shipments/{id}/unarchive
// Request: empty body
// Response: 200 OK
{
  "id": "shp_a1b2c3...",
  "is_archived": false,
  "archived_at": null,
  ...
}
```

**REST List Filters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `is_archived` | boolean | `false` | When `true`, return only archived records. When `false` (default), return only non-archived records. |

```
GET /v1/shipments                      → non-archived only (default)
GET /v1/shipments?is_archived=true     → archived only
```

**GraphQL Mutations**

```graphql
mutation {
  archive_shipment(id: "shp_a1b2c3") { id, is_archived, archived_at }
  unarchive_shipment(id: "shp_a1b2c3") { id, is_archived, archived_at }
  archive_tracker(id: "trk_x1y2z3") { id, is_archived, archived_at }
  unarchive_tracker(id: "trk_x1y2z3") { id, is_archived, archived_at }
  archive_pickup(id: "pck_m1n2o3") { id, is_archived, archived_at }
  unarchive_pickup(id: "pck_m1n2o3") { id, is_archived, archived_at }
  archive_order(id: "ord_p1q2r3") { id, is_archived, archived_at }
  unarchive_order(id: "ord_p1q2r3") { id, is_archived, archived_at }
}
```

**GraphQL List Filters**

```graphql
query {
  shipments(filter: { is_archived: true }) {
    edges { node { id, status, is_archived, archived_at } }
  }
  trackers(filter: { is_archived: true }) {
    edges { node { id, status, is_archived, archived_at } }
  }
}
```

### Background Job Changes

**File:** `modules/events/karrio/server/events/task_definitions/base/tracking.py`

```python
# update_trackers() — line 104-112, add is_archived=False filter:
qs = (
    models.Tracking.objects.filter(id__in=tracker_ids)
    if tracker_ids
    else models.Tracking.objects.filter(
        delivered=False,
        is_archived=False,  # NEW — skip archived trackers
        updated_at__lt=timezone.now() - delta,
        created_at__gt=max_age_cutoff,
    )
)

# _retire_aged_out_trackers() — line 66-73, add is_archived=False:
return models.Tracking.objects.filter(
    delivered=False,
    is_archived=False,  # NEW — don't retire already-archived
    created_at__lt=max_age_cutoff,
).update(
    status="unknown",
    delivered=None,
    updated_at=timezone.now(),
)
```

**Note:** The `update_trackers()` dispatcher already uses `models.Tracking.objects` (the default manager). Once the default manager excludes `is_archived=True`, the explicit `is_archived=False` filter becomes redundant but serves as documentation. However, the `_retire_aged_out_trackers` function uses `models.Tracking.objects.filter(...)` directly — after the manager change, this will automatically exclude archived trackers. **The explicit filter is belt-and-suspenders for clarity.** If `tracker_ids` are passed explicitly, the caller is assumed to have already validated them.

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| `request_id` matches zero records | 404 Not Found | Standard Django `DoesNotExist` → DRF 404 |
| `request_id` matches multiple records (same tenant) | Error | Return 409 "Multiple resources match this request_id" (pending Q10) |
| `request_id` provided with `id` | `id` takes precedence | `request_id` is ignored; documented in API docs |
| Cancel already-cancelled resource by `request_id` | 200/202 (idempotent) | Return current state; no carrier API call |
| Archive already-archived resource | 200 (idempotent) | Return current state; no `archived_at` update |
| Unarchive non-archived resource | 200 (idempotent) | Return current state |
| Archive a resource then list without filter | Resource not in results | Default manager excludes `is_archived=True` |
| Archive tracker mid-Huey-batch | No race condition | `_save_results` bulk_update only touches tracking fields, not `is_archived` |
| Cancel an archived resource | Depends on Q7 | Proposed: allow (archiving ≠ cancellation) |
| `all_objects` used in admin | Shows all records including archived | Expected; admin needs full view |
| `select_related` on archived FK target | Returns archived related object | `select_related` bypasses manager; this is correct behavior |
| Webhook delivery for archived resource | Webhooks still fire | Archiving is a visibility filter, not a lifecycle change |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Migration fails on large table (adding `is_archived` column) | Downtime during `ALTER TABLE` | Use `AddField` with `default=False`; Django handles this efficiently. Consider `RunSQL` with `IF NOT EXISTS` for zero-downtime on PostgreSQL (but must remain cross-DB compatible) |
| `all_objects` manager forgotten in admin/reporting | Archived records invisible in admin | Document clearly; add admin mixin that uses `all_objects` |
| N+1 introduced by manager chain | Performance regression | `NotArchivedManager` inherits from base `Manager`; model-specific managers extend it with their `select_related`/`prefetch_related` |
| `request_id` collision across tenants | Cancel wrong tenant's resource | Always scope through `access_by(request)` — tenant isolation guaranteed |
| Archived tracker re-activated by external webhook | Unexpected behavior | Webhook handler should check `is_archived` and skip or log a warning |

### Security Considerations

- [ ] `request_id` lookup always scoped through `access_by(request)` — no cross-tenant leakage
- [ ] Archive/unarchive endpoints require authentication
- [ ] No secrets or PII exposed in new fields
- [ ] `is_archived` filter does not bypass multi-tenancy

---

## Implementation Plan

### Phase 1: Data Model & Migrations

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `is_archived`, `archived_at` to Shipment model | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Add `is_archived`, `archived_at` to Tracking model | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Add `is_archived`, `archived_at` to Pickup model | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Add `is_archived`, `archived_at` to Order model | `modules/orders/karrio/server/orders/models.py` | Pending | S |
| Generate migrations for manager app | `modules/manager/karrio/server/manager/migrations/` | Pending | S |
| Generate migrations for orders app | `modules/orders/karrio/server/orders/migrations/` | Pending | S |
| Verify migrations are reversible | — | Pending | S |

### Phase 2: Manager / Queryset Defaults

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `NotArchivedManager` base class | `modules/core/karrio/server/core/models/` | Pending | M |
| Update `ShipmentManager` to extend `NotArchivedManager` | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Update `TrackingManager` to extend `NotArchivedManager` | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Update `PickupManager` to extend `NotArchivedManager` | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Update `OrderManager` to extend `NotArchivedManager` | `modules/orders/karrio/server/orders/models.py` | Pending | S |
| Add `all_objects = models.Manager()` to each model | All 4 model files | Pending | S |
| Create shared `archive_resource()` / `unarchive_resource()` helpers | `modules/core/karrio/server/core/utils.py` | Pending | S |

**Dependencies:** Phase 2 depends on Phase 1 completion.

### Phase 3: Background Job Exclusion

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `is_archived=False` filter to `update_trackers()` | `modules/events/.../tracking.py` | Pending | S |
| Add `is_archived=False` filter to `_retire_aged_out_trackers()` | `modules/events/.../tracking.py` | Pending | S |
| Verify no other background tasks need updating | `modules/events/karrio/server/events/task_definitions/` | Pending | S |

**Dependencies:** Phase 3 depends on Phase 2 completion (manager changes).

### Phase 4: REST API + GraphQL — Cancel by `request_id`

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `resolve_by_id_or_request_id()` utility | `modules/core/karrio/server/core/utils.py` | Pending | S |
| Add `POST /v1/shipments/cancel` endpoint (request_id body) | `modules/manager/.../views/shipments.py` | Pending | M |
| Add `DELETE /v1/trackers/by-request-id/{request_id}` endpoint | `modules/manager/.../views/trackers.py` | Pending | M |
| Add `POST /v1/pickups/cancel` endpoint (request_id body) | `modules/manager/.../views/pickups.py` | Pending | M |
| Add `POST /v1/orders/cancel` endpoint (request_id body) | `modules/orders/.../views.py` | Pending | M |
| Update URL router for new endpoints | `modules/manager/.../router.py`, `modules/orders/.../router.py` | Pending | S |
| Add `request_id` to GraphQL cancel mutation inputs | `modules/graph/.../schemas/base/mutations.py` | Pending | M |
| Update GraphQL cancel mutation resolvers | `modules/graph/.../schemas/base/mutations.py` | Pending | M |

### Phase 5: REST API + GraphQL — Archive / Unarchive

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add archive/unarchive views for Shipment | `modules/manager/.../views/shipments.py` | Pending | M |
| Add archive/unarchive views for Tracker | `modules/manager/.../views/trackers.py` | Pending | M |
| Add archive/unarchive views for Pickup | `modules/manager/.../views/pickups.py` | Pending | M |
| Add archive/unarchive views for Order | `modules/orders/.../views.py` | Pending | M |
| Update URL routers for archive/unarchive | Router files | Pending | S |
| Add `is_archived` to REST filter classes | `modules/core/.../filters.py`, `modules/orders/.../filters.py` | Pending | S |
| Add `is_archived` to GraphQL filter inputs | `modules/graph/.../schemas/base/inputs.py` | Pending | S |
| Add archive/unarchive GraphQL mutations | `modules/graph/.../schemas/base/mutations.py` | Pending | M |
| Add `is_archived`, `archived_at` to serializers / GraphQL types | Serializer + type files | Pending | S |

### Phase 6: Tests

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Unit tests: model `is_archived` default, manager exclusion | Manager test files | Pending | M |
| Integration tests: cancel by `request_id` (REST) | `modules/manager/.../tests/`, `modules/orders/.../tests/` | Pending | L |
| Integration tests: archive/unarchive (REST) | Test files | Pending | L |
| Background job tests: archived trackers skipped | `modules/events/.../tests/test_tracking_tasks.py` | Pending | M |
| GraphQL tests: cancel by `request_id`, archive mutations, filters | `modules/graph/.../tests/` | Pending | L |
| Idempotency tests | Test files | Pending | M |

### Phase 7: Dashboard UI (P1 — separate PRD recommended)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| "Archived" tab on Shipments, Trackers, Pickups, Orders list pages | `apps/dashboard/src/modules/` | Pending | L |
| Archive action in row context menu | Components | Pending | M |
| Bulk archive action | Components | Pending | M |
| Archived badge on detail pages | Components | Pending | S |
| Unarchive action on archived records | Components | Pending | S |

---

## Testing Strategy

> **CRITICAL**: All tests follow `AGENTS.md` guidelines — `unittest` for SDK, `karrio test` for server. No pytest.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Model unit tests | `modules/manager/karrio/server/manager/tests/` | Manager exclusion, field defaults |
| REST integration tests | `modules/manager/karrio/server/manager/tests/`, `modules/orders/.../tests/` | All new endpoints |
| GraphQL integration tests | `modules/graph/karrio/server/graph/tests/` | All new mutations + filters |
| Background job tests | `modules/events/karrio/server/events/tests/test_tracking_tasks.py` | Archived tracker exclusion |

### Test Cases

#### Cancel by `request_id`

```python
class TestCancelByRequestId(APITestCase):
    def test_cancel_shipment_by_request_id(self):
        """Cancel a shipment using its request_id instead of internal ID."""
        # Create shipment (request_id stored in meta automatically)
        shipment = create_test_shipment(request_id="req_test_001")

        response = self.client.post(
            "/v1/shipments/cancel",
            data={"request_id": "req_test_001"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "cancelled")

    def test_cancel_shipment_by_request_id_not_found(self):
        """Return 404 when request_id matches no records."""
        response = self.client.post(
            "/v1/shipments/cancel",
            data={"request_id": "req_nonexistent"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_cancel_shipment_by_request_id_idempotent(self):
        """Return 202 when shipment is already cancelled."""
        shipment = create_test_shipment(request_id="req_test_002", status="cancelled")

        response = self.client.post(
            "/v1/shipments/cancel",
            data={"request_id": "req_test_002"},
            format="json",
        )

        self.assertEqual(response.status_code, 202)

    def test_cancel_scoped_to_tenant(self):
        """request_id lookup must be scoped to the authenticated tenant."""
        # Create shipment as tenant A
        shipment = create_test_shipment(request_id="req_shared", org=self.org_a)

        # Attempt cancel as tenant B
        self.client.force_authenticate(self.user_b)
        response = self.client.post(
            "/v1/shipments/cancel",
            data={"request_id": "req_shared"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)  # Not found in tenant B's scope
```

#### Archiving

```python
class TestArchiving(APITestCase):
    def test_archive_shipment(self):
        """Archive a shipment and verify it's excluded from default list."""
        shipment = create_test_shipment()

        # Archive
        response = self.client.post(f"/v1/shipments/{shipment.id}/archive")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_archived"])
        self.assertIsNotNone(response.data["archived_at"])

        # Verify excluded from default list
        list_response = self.client.get("/v1/shipments")
        ids = [s["id"] for s in list_response.data["results"]]
        self.assertNotIn(shipment.id, ids)

        # Verify included with is_archived filter
        archived_response = self.client.get("/v1/shipments?is_archived=true")
        ids = [s["id"] for s in archived_response.data["results"]]
        self.assertIn(shipment.id, ids)

    def test_unarchive_shipment(self):
        """Unarchive a shipment and verify it reappears in default list."""
        shipment = create_test_shipment(is_archived=True)

        response = self.client.post(f"/v1/shipments/{shipment.id}/unarchive")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_archived"])
        self.assertIsNone(response.data["archived_at"])

    def test_archive_idempotent(self):
        """Archiving an already-archived resource returns 200."""
        shipment = create_test_shipment(is_archived=True)

        response = self.client.post(f"/v1/shipments/{shipment.id}/archive")
        self.assertEqual(response.status_code, 200)

    def test_model_default_is_archived_false(self):
        """New records have is_archived=False by default."""
        shipment = Shipment.objects.create(...)
        self.assertFalse(shipment.is_archived)
        self.assertIsNone(shipment.archived_at)

    def test_manager_excludes_archived(self):
        """Default objects manager excludes archived records."""
        active = create_test_shipment(is_archived=False)
        archived = create_test_shipment(is_archived=True)

        qs = Shipment.objects.all()
        self.assertIn(active, qs)
        self.assertNotIn(archived, qs)

    def test_all_objects_includes_archived(self):
        """all_objects manager includes all records."""
        archived = create_test_shipment(is_archived=True)

        qs = Shipment.all_objects.all()
        self.assertIn(archived, qs)
```

#### Background Job Tests

```python
class TestArchivedTrackerExclusion(TestCase):
    def test_archived_tracker_excluded_from_update(self):
        """Archived trackers are not polled by background_trackers_update."""
        active_tracker = create_test_tracker(delivered=False, is_archived=False)
        archived_tracker = create_test_tracker(delivered=False, is_archived=True)

        # Run update_trackers dispatcher
        update_trackers(delta=datetime.timedelta(seconds=0))

        # Verify only active tracker was updated
        active_tracker.refresh_from_db()
        archived_tracker.refresh_from_db()
        # archived_tracker.updated_at should not have changed
        self.assertGreater(active_tracker.updated_at, archived_tracker.updated_at)

    def test_archived_tracker_not_retired(self):
        """Archived trackers are not marked as retired by age-out logic."""
        old_archived = create_test_tracker(
            delivered=False,
            is_archived=True,
            created_at=timezone.now() - datetime.timedelta(days=100),
        )

        _retire_aged_out_trackers(
            max_age_cutoff=timezone.now() - datetime.timedelta(days=90)
        )

        old_archived.refresh_from_db()
        self.assertFalse(old_archived.delivered is None)  # status unchanged
```

### Running Tests

```bash
source bin/activate-env

# All manager tests (includes new archive + cancel-by-request-id tests)
karrio test --failfast karrio.server.manager.tests

# Order-specific tests
karrio test --failfast karrio.server.orders.tests

# Background job tests
karrio test --failfast karrio.server.events.tests

# GraphQL tests
karrio test --failfast karrio.server.graph.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Manager change breaks existing queries that expect to see all records | High | Medium | Audit all `.objects` usages; add `all_objects` escape hatch; comprehensive test suite |
| Migration lock on large `shipments` / `tracking` tables in production | High | Low | `BooleanField(default=False)` is a cheap `ALTER TABLE` on PostgreSQL; test on staging with production-scale data |
| `request_id` collision within a tenant (non-unique) | Medium | Low | Document that `request_id` should be unique per tenant; return 409 on ambiguous matches (pending Q10) |
| Breaking change to `DELETE /v1/trackers/{id}` if changed to archive | High | Low | Keep hard-delete behavior unchanged; add separate archive endpoint (pending Q9) |
| Admin panel shows only non-archived records | Medium | Medium | Override admin with `all_objects` manager; document in admin mixin |
| `select_related` / `prefetch_related` loads archived related objects | Low | High | Expected behavior — FK traversal should not be filtered. Document this. |
| GraphQL schema change requires client SDK regeneration | Medium | Low | New fields are additive (non-breaking); new mutations are additive |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: All existing endpoints remain unchanged. New `request_id`-based cancel and archive endpoints are additive. No existing field semantics change.
- **Data compatibility**: Existing records default to `is_archived=False`. No data migration needed. All existing records continue to appear in default queries.
- **Manager compatibility**: `objects` manager changes default behavior (excludes archived). Any code using `Model.objects.all()` will no longer see archived records. This is the intended behavior but requires auditing all usages.
- **Feature flags**: Consider gating `is_archived` manager exclusion behind a setting for phased rollout: `KARRIO_ARCHIVE_FILTER_ENABLED = True/False`

### Data Migration

No data migration is required. The migration is purely additive:

```python
# Auto-generated migration (example for manager app)
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("manager", "XXXX_previous"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipment",
            name="is_archived",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name="shipment",
            name="archived_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tracking",
            name="is_archived",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name="tracking",
            name="archived_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="pickup",
            name="is_archived",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name="pickup",
            name="archived_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
```

### Rollback Procedure

1. **Identify issue**: Monitor error rates on list endpoints and background tracker job after deploy
2. **Stop rollout**: If manager exclusion causes unexpected behavior, disable with feature flag: `KARRIO_ARCHIVE_FILTER_ENABLED = False`
3. **Revert changes**: Revert code changes. Migrations are reversible (`RemoveField` is safe for nullable/default fields). Run `python manage.py migrate manager XXXX_previous` to reverse.
4. **Verify recovery**: Confirm all list endpoints return expected results; confirm background tracker job processes all non-delivered trackers.

---

## Appendices

### Appendix A: Current Cancel Endpoint Summary

| Resource | REST Endpoint | Method | Lookup Field | Handler Location |
|----------|--------------|--------|-------------|-----------------|
| Shipment | `/v1/shipments/{id}/cancel` | POST | `pk` (shp_*) | `modules/manager/.../views/shipments.py:163` |
| Tracker | `/v1/trackers/{id_or_tracking_number}` | DELETE | `pk` or `tracking_number` | `modules/manager/.../views/trackers.py:300` |
| Pickup | `/v1/pickups/{pk}/cancel` | POST | `pk` (pck_*) | `modules/manager/.../views/pickups.py:184` |
| Order | `/v1/orders/{pk}/cancel` | POST | `pk` (ord_*) | `modules/orders/.../views.py:165` |

### Appendix B: Background Tracker Job Architecture

```
background_trackers_update (periodic, every DEFAULT_TRACKERS_UPDATE_INTERVAL=7200s)
  └─ update_trackers()
       ├─ _retire_aged_out_trackers()  ← needs is_archived=False filter
       ├─ Query: Tracking.objects.filter(delivered=False, ...)  ← needs is_archived=False
       └─ For each carrier group:
            └─ process_carrier_tracking_batch() (Huey sub-task)
                 └─ process_carrier_trackers()
                      └─ Batches of TRACKER_BATCH_SIZE=10
                           ├─ _process_batch() → fetch from carrier
                           └─ _save_results() → bulk_update
```

### Appendix C: Code Guidelines (for implementation phase)

- **Functional & declarative style**: no nested ifs, no nested loops; use `map`, `filter`, comprehensions
- **DRY**: shared `archive_resource()` / `unarchive_resource()` helpers across all 4 models
- **Centralised filtering**: `is_archived=False` lives ONLY in the manager — never in views, serializers, or resolvers
- **Clean type annotations**: all new functions fully typed
- **All migrations reversible**: use `AddField` only (no `RunSQL`, no `RunPython` for this feature)
- **`import karrio.lib as lib`**: always; never legacy utilities
- **No scattered `filter(is_archived=False)`**: if you see it in a view or resolver, it's a bug — the manager handles it
