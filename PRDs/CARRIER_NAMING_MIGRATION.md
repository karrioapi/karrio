# Progressive Migration: carrier_name to carrier_code & carrier_id to connection_name

<!-- REFACTORING -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-31 |
| Status | Planning |
| Owner | Karrio Core Team |
| Type | Refactoring |
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
8. [Implementation Plan](#implementation-plan) (7 phases)
9. [Testing Strategy](#testing-strategy)
10. [Risk Assessment](#risk-assessment)
11. [Migration & Rollback](#migration--rollback)
12. [Appendices](#appendices)
    - [A: Complete Rename Map](#appendix-a-complete-rename-map)
    - [B: Exhaustive Affected Files Audit](#appendix-b-exhaustive-affected-files-audit) (~460 files, ~2,100+ references)
    - [C: carrier_alias Generation Logic](#appendix-c-carrier_alias-generation-logic)
    - [D: Pre-existing Bugs to Fix](#appendix-d-pre-existing-bugs-to-fix-during-migration) (7 connector bugs)

---

## Executive Summary

This PRD proposes a progressive rename of carrier-related API fields across the entire Karrio stack to improve naming clarity and consistency. The current `carrier_name` (which holds a carrier type slug like `"fedex"`) is confusing because it sounds like a display name; it is renamed to `carrier_code`. The current `carrier_id` (which holds a user-defined friendly name for a connection) is confusing because it sounds like a database primary key; it is renamed to `connection_name`. A new readonly `carrier_alias` field is introduced as an auto-generated slug for stable programmatic reference. All renames maintain full backward compatibility: old field names are accepted in inputs and returned alongside new names in responses.

### Key Architecture Decisions

1. **`carrier_name` -> `carrier_code` (API surface)**: `carrier_code` already exists on the Django model with the same value. The rename is purely at the API/serializer/filter layer. Inputs accept `carrier_code`; responses return both `carrier_code` and `carrier_name`. Filters accept both.
2. **`carrier_id` -> `connection_name` (DB + API)**: The Django column is renamed via `RenameField`. API inputs accept `connection_name` (primary) with `carrier_id` fallback. Responses return both.
3. **`carrier_ids` -> `connection_ids` (list input param)**: The list parameter for shipment creation and rate requests is renamed. `carrier_ids` accepted for backward compat.
4. **`carrier_alias` (new readonly field)**: Auto-generated slug on connection models (`{carrier_code}_{short_hash}`). Migration populates from existing `carrier_id` values. Included in carrier snapshots.
5. **SDK models get new fields alongside old**: `carrier_code` alongside `carrier_name`, `connection_name` alongside `carrier_id`. Both pairs hold the same values.
6. **Carrier snapshots get new keys alongside old**: `carrier_code`, `connection_name`, `carrier_alias` added to snapshot JSON. Old keys (`carrier_name`, `carrier_id`) preserved.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Rename `carrier_name` -> `carrier_code` in API params, responses, filters | Removing old field names (kept for backward compat) |
| Rename `carrier_id` -> `connection_name` in DB + API | Changing the `carrier_code` DB column on CarrierConnection (already exists) |
| Rename `carrier_ids` -> `connection_ids` in rate/shipment inputs | Renaming `carrier_name` on RateSheet model (refers to carrier type, will become `carrier_code` in a future PR) |
| Rename `carrier_id` -> `connection_id` in tracking input | GraphQL subscription changes |
| New `carrier_alias` field on connection models + snapshots | API versioning (v1 -> v2) |
| SDK model field additions | |
| Carrier connector response construction (add new fields) | |
| Fix 7 connector bugs (`carrier_name=settings.carrier_id`) | |
| EE/Insiders modules (admin, automation, dtdc connector) | |
| TypeScript type updates + frontend component updates | |
| Backward compat shims for old param names | |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | API primary field for carrier type | `carrier_code` | Already exists on DB model; `carrier_name` is misleading (sounds like display name) | 2026-01-31 |
| D2 | API primary field for connection friendly name | `connection_name` | `carrier_id` is misleading (sounds like a primary key) | 2026-01-31 |
| D3 | List input param rename | `carrier_ids` -> `connection_ids` | Consistent with singular `connection_id`; the param accepts both PKs and friendly names | 2026-01-31 |
| D4 | Singular tracking input rename | `carrier_id` -> `connection_id` | Consistent with list param rename pattern | 2026-01-31 |
| D5 | DB migration approach | RenameField directly | Simpler than dual-column; all code changes in one pass | 2026-01-31 |
| D6 | SDK model strategy | Add new fields, keep old | `carrier_code` + `carrier_name` both present (same value); `connection_name` + `carrier_id` both present (same value) | 2026-01-31 |
| D7 | `carrier_alias` scope | Connection model + carrier snapshot | Not in SDK response models; lives on connection and in snapshot JSON | 2026-01-31 |
| D8 | `carrier_alias` generation pattern | `{carrier_code}_{short_hash}` | Readable; e.g., `"fedex_a1b2c3d4"`, `"dhl_express_e5f6g7h8"` | 2026-01-31 |
| D9 | Snapshot JSON update | Add new keys alongside old | `{carrier_code, carrier_name, connection_name, carrier_id, carrier_alias, ...}` all coexist | 2026-01-31 |
| D10 | Filter param rename | `carrier_name` -> `carrier_code` in REST + GraphQL | Backend accepts both; `carrier_name` fallback for backward compat | 2026-01-31 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Existing `carrier_id` values that are not valid slugs | `carrier_alias` migration must handle them | Use existing values as-is for migration; only new aliases use generated pattern | No |
| `carrier_alias` uniqueness collisions during migration | Two connections could have same `carrier_id` value | Add uniqueness constraint per org; append hash suffix on collision | No |
| Client sends both `carrier_name` and `carrier_code` in same request | Ambiguous input | `carrier_code` takes precedence; `carrier_name` ignored if both present | No |
| Client sends both `carrier_ids` and `connection_ids` in same request | Ambiguous input | `connection_ids` takes precedence; `carrier_ids` ignored if both present | No |

---

## Problem Statement

### Current State

The API uses `carrier_name` for the carrier type slug and `carrier_id` for the user-defined connection name. These names are semantically misleading:

```python
# SDK response model (modules/sdk/karrio/core/models.py:363-376)
@attr.s(auto_attribs=True)
class RateDetails:
    carrier_name: str    # Actually a carrier type CODE, e.g. "fedex", not a name
    carrier_id: str      # Actually a user-defined CONNECTION NAME, not a DB id
    service: str
    total_charge: float = 0.0
    # ...
```

```python
# Carrier connection model (modules/core/karrio/server/providers/models/carrier.py:103-107)
carrier_id = models.CharField(
    max_length=150,
    db_index=True,
    help_text="User-defined connection identifier",  # Misleading: "identifier" implies PK
)
```

```python
# REST filter (modules/core/karrio/server/core/filters.py:44)
carrier_name = CharFilter(choices=dataunits.CARRIER_NAMES)  # Actually filtering by code
```

```python
# Carrier snapshot (modules/core/karrio/server/core/utils.py:1213-1215)
carrier_name = carrier_code  # They're the same value, but exposed as "carrier_name"
```

```typescript
// TypeScript types (packages/types/rest/api.ts)
carrier_name: CarrierConnectionCarrierNameEnum;  // e.g., "fedex" - not a display name
carrier_id: string;                               // e.g., "my_fedex_account" - not a DB id
```

### Desired State

```python
# SDK response model - new fields alongside old for backward compat
@attr.s(auto_attribs=True)
class RateDetails:
    carrier_name: str        # Kept for backward compat (same value as carrier_code)
    carrier_code: str        # NEW: clear name for carrier type slug
    carrier_id: str          # Kept for backward compat (same value as connection_name)
    connection_name: str     # NEW: clear name for user-defined connection name
    service: str
    total_charge: float = 0.0
    # ...
```

```python
# Connection model - renamed column + new alias field
connection_name = models.CharField(  # Renamed from carrier_id
    max_length=150,
    db_index=True,
    help_text="User-defined connection name",
)
carrier_alias = models.CharField(  # NEW: auto-generated slug
    max_length=100,
    db_index=True,
    unique=True,
    help_text="Auto-generated unique slug for programmatic reference",
)
```

```python
# API input - accepts new names, falls back to old
connection_ids = serializers.StringListField(  # Primary
    required=False, default=[],
    help_text="List of carrier connections to get rates from.",
)
# Backend also checks for "carrier_ids" in input data for backward compat
```

```json
// API response - returns both old and new field names
{
  "carrier_code": "fedex",
  "carrier_name": "fedex",
  "connection_name": "my_fedex_account",
  "carrier_id": "my_fedex_account",
  "carrier_alias": "fedex_a1b2c3d4"
}
```

### Problems

1. **`carrier_name` is misleading**: It holds a type code (`"fedex"`) not a display name (`"Federal Express"`). Every new developer and API consumer expects a human-readable name.
2. **`carrier_id` is misleading**: It holds a user-defined friendly name (`"my_fedex_account"`) not a database primary key. API consumers expect it to be stable and system-generated.
3. **No stable programmatic reference**: Users can change `carrier_id` at any time. There is no system-generated stable slug for referencing connections programmatically (like workflow slugs).
4. **`carrier_name` and `carrier_code` have the same value**: The model already has `carrier_code` but the API surfaces `carrier_name`, creating unnecessary confusion about whether they differ.

---

## Goals & Success Criteria

### Goals

1. All API inputs (REST + GraphQL) accept `carrier_code`, `connection_name`, `connection_ids`, and `connection_id` as primary parameter names
2. All API responses include both old and new field names for full backward compatibility
3. Introduce `carrier_alias` as a readonly auto-generated slug on all connection types
4. Zero breaking changes for existing API consumers

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| All existing API tests pass without modification | 100% pass rate | Must-have |
| New field names accepted in all API inputs | Verified via new tests | Must-have |
| Old field names still accepted in all API inputs | Verified via backward compat tests | Must-have |
| Responses include both old and new field names | Verified via response assertions | Must-have |
| `carrier_alias` populated for all existing connections | Migration backfills 100% | Must-have |
| `carrier_alias` auto-generated for new connections | Verified via creation tests | Must-have |
| TypeScript types updated with new field names | Types compile successfully | Must-have |
| GraphQL schema includes new fields | Schema introspection verified | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] DB migration: `carrier_id` -> `connection_name` on all connection models
- [ ] DB migration: Add `carrier_alias` field to all connection models
- [ ] DB migration: Backfill `carrier_alias` from existing `carrier_id` values
- [ ] SDK models: Add `carrier_code` and `connection_name` fields
- [ ] Serializers: Accept new param names with old-name fallback
- [ ] Serializers: Return both old and new field names in responses
- [ ] Filters: Accept `carrier_code` with `carrier_name` fallback
- [ ] Carrier snapshots: Include new keys alongside old
- [ ] GraphQL: Add new fields, deprecate old
- [ ] TypeScript types: Add new field names
- [ ] All existing tests pass

**Nice-to-have (P1):**
- [ ] API documentation updated with new field names
- [ ] Deprecation notices in OpenAPI spec for old field names
- [ ] Dashboard UI labels use new names (separate PR)

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A) Progressive rename with dual fields** | Zero breaking changes; gradual migration; old names kept indefinitely | Responses are larger with duplicate fields; code complexity for fallback logic | **Selected** |
| **B) Hard rename in new API version (v2)** | Clean break; no duplicate fields | Forces all consumers to migrate at once; maintaining two API versions is expensive | Rejected |
| **C) Rename at serializer level only (no DB change)** | No migration needed; simpler | `carrier_id` column name remains misleading in DB; ORM queries still use old name | Rejected |
| **D) Add aliases only (keep old names as primary)** | Minimal change | Doesn't solve the core naming confusion; new developers still see misleading names first | Rejected |

### Trade-off Analysis

**Option A** was selected because:
- Karrio's API consumers (SDKs, webhooks, integrations) depend on field names. A hard break would cause widespread failures.
- The progressive approach allows consumers to migrate at their own pace while new code uses the clearer names.
- The DB rename (via `RenameField`) is clean and atomic. Django handles the column rename without data loss.
- The slight increase in response payload size (duplicate fields) is negligible for JSON APIs.

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `CarrierConnection` model | `modules/core/karrio/server/providers/models/carrier.py:62-304` | RenameField `carrier_id` -> `connection_name`; add `carrier_alias` |
| `SystemConnection` model | `modules/core/karrio/server/providers/models/connection.py:56-273` | Same rename + alias addition |
| `BrokeredConnection` model | `modules/core/karrio/server/providers/models/connection.py:311-500` | Same rename + alias addition; update `effective_carrier_id` -> `effective_connection_name` |
| `create_carrier_snapshot()` | `modules/core/karrio/server/core/utils.py:1160-1224` | Add new keys to snapshot dict |
| SDK response models | `modules/sdk/karrio/core/models.py:322-574` | Add `carrier_code` and `connection_name` fields |
| Serializer base classes | `modules/core/karrio/server/core/serializers.py` | Add new field names; implement fallback logic |
| Connection serializers | `modules/core/karrio/server/providers/serializers/base.py:49-179` | Rename fields; add `carrier_alias` |
| REST filters | `modules/core/karrio/server/core/filters.py:43-176` | Add `carrier_code` filter alongside `carrier_name` |
| GraphQL types | `modules/graph/karrio/server/graph/schemas/base/types.py:2131-2214` | Add new fields to `CarrierConnectionType` |
| GraphQL inputs | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Add new field names to filter/mutation inputs |
| Shipment serializer | `modules/manager/karrio/server/manager/serializers/shipment.py:1542-1548` | Rename `carrier_ids` -> `connection_ids` with fallback |
| Rate serializer | `modules/core/karrio/server/core/serializers.py:760-765` | Rename `carrier_ids` -> `connection_ids` with fallback |
| Tracking serializer | `modules/manager/karrio/server/manager/serializers/tracking.py:27-29` | Rename `carrier_id` -> `connection_id` with fallback |
| Gateway connections | `modules/core/karrio/server/core/gateway.py:150-163` | Update filter key names with fallback |
| `lib.to_slug()` | `modules/sdk/karrio/lib.py:121-126` | Reuse for `carrier_alias` generation |
| Workflow slug pattern | `ee/insiders/modules/automation/karrio/server/graph/schemas/automation/mutations.py:37` | Reference for slug generation pattern |
| TypeScript types | `packages/types/rest/api.ts`, `packages/types/graphql/types.ts` | Add new field names to interfaces |
| TypeScript constants | `packages/types/base.ts:169-171` | `CARRIER_NAMES` constant stays as-is |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         API LAYER                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT (accepts both old and new names):                             │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  carrier_code  OR  carrier_name  ──>  carrier_code       │       │
│  │  connection_ids OR carrier_ids   ──>  connection_ids     │       │
│  │  connection_id  OR carrier_id    ──>  connection_id      │       │
│  │  connection_name OR carrier_id   ──>  connection_name    │       │
│  └──────────────────────────────────────────────────────────┘       │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │              SERIALIZER / FILTER LAYER                    │       │
│  │  Normalizes input to new names; passes to gateway         │       │
│  └──────────────────────────────────────────────────────────┘       │
│                              │                                       │
│                              ▼                                       │
│  OUTPUT (returns both old and new names):                            │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  carrier_code + carrier_name    (same value)              │       │
│  │  connection_name + carrier_id   (same value)              │       │
│  │  carrier_alias                  (readonly slug)           │       │
│  └──────────────────────────────────────────────────────────┘       │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                      DATABASE LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CarrierConnection / SystemConnection / BrokeredConnection           │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  carrier_code      CharField (unchanged)                  │       │
│  │  connection_name   CharField (renamed from carrier_id)    │       │
│  │  carrier_alias     CharField (NEW, auto-generated slug)   │       │
│  └──────────────────────────────────────────────────────────┘       │
│                                                                      │
│  Carrier Snapshots (JSONField on Shipment, Tracking, etc.)           │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  carrier_code      (existing)                             │       │
│  │  carrier_name      (existing, same as carrier_code)       │       │
│  │  carrier_id        (existing, same as connection_name)    │       │
│  │  connection_name   (NEW, same as carrier_id)              │       │
│  │  carrier_alias     (NEW, from connection model)           │       │
│  │  connection_id     (existing, DB primary key)             │       │
│  │  connection_type   (existing)                             │       │
│  │  test_mode         (existing)                             │       │
│  └──────────────────────────────────────────────────────────┘       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram - Input Normalization

```
┌────────┐     ┌───────────┐     ┌────────────┐     ┌─────────┐
│ Client │     │Serializer │     │  Gateway   │     │   DB    │
└───┬────┘     └─────┬─────┘     └─────┬──────┘     └────┬────┘
    │                │                   │                  │
    │ POST /rates    │                   │                  │
    │ {carrier_ids:  │                   │                  │
    │  ["my_fedex"]} │                   │                  │
    │───────────────>│                   │                  │
    │                │                   │                  │
    │                │ 1. Check for      │                  │
    │                │    connection_ids  │                  │
    │                │    (not found)     │                  │
    │                │                   │                  │
    │                │ 2. Fallback to    │                  │
    │                │    carrier_ids    │                  │
    │                │    -> normalize   │                  │
    │                │    to             │                  │
    │                │    connection_ids │                  │
    │                │                   │                  │
    │                │ Connections.list  │                  │
    │                │ (connection_ids=  │                  │
    │                │  ["my_fedex"])    │                  │
    │                │──────────────────>│                  │
    │                │                   │ Q(id__in=ids) |  │
    │                │                   │ Q(connection_    │
    │                │                   │   name__in=ids)  │
    │                │                   │─────────────────>│
    │                │                   │                  │
    │                │                   │  connections     │
    │                │                   │<─────────────────│
    │                │  rates response   │                  │
    │                │<──────────────────│                  │
    │                │                   │                  │
    │ Response:      │                   │                  │
    │ {carrier_code, │                   │                  │
    │  carrier_name, │                   │                  │
    │  connection_   │                   │                  │
    │  name,         │                   │                  │
    │  carrier_id}   │                   │                  │
    │<───────────────│                   │                  │
    │                │                   │                  │
```

### Data Flow Diagram - carrier_alias Generation

```
┌──────────────────────────────────────────────────────────────────────┐
│                   EXISTING CONNECTIONS (Migration)                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐     ┌──────────────────┐     ┌───────────────┐ │
│  │ CarrierConnection│     │  RunPython       │     │ Result        │ │
│  │ carrier_id=      │────>│  migration       │────>│ connection_   │ │
│  │ "my_fedex"       │     │                  │     │   name=       │ │
│  │                  │     │ carrier_alias =  │     │   "my_fedex"  │ │
│  │                  │     │   carrier_id     │     │ carrier_alias=│ │
│  │                  │     │   (existing val) │     │   "my_fedex"  │ │
│  └─────────────────┘     └──────────────────┘     └───────────────┘ │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                   NEW CONNECTIONS (Runtime)                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐     ┌──────────────────┐     ┌───────────────┐ │
│  │ Create request   │     │  Serializer      │     │ Result        │ │
│  │ connection_name= │────>│  .create()       │────>│ connection_   │ │
│  │ "my_new_fedex"   │     │                  │     │   name=       │ │
│  │ carrier_code=    │     │ carrier_alias =  │     │   "my_new_    │ │
│  │ "fedex"          │     │ f"{carrier_code} │     │   fedex"      │ │
│  │                  │     │  _{uuid[:8]}"    │     │ carrier_alias=│ │
│  │                  │     │                  │     │   "fedex_     │ │
│  │                  │     │                  │     │   a1b2c3d4"   │ │
│  └─────────────────┘     └──────────────────┘     └───────────────┘ │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Models

**SDK Response Models** (add new fields to all response models):

```python
# modules/sdk/karrio/core/models.py
@attr.s(auto_attribs=True)
class RateDetails:
    carrier_name: str                   # Kept: carrier type slug (backward compat)
    carrier_code: str = None            # NEW: same value as carrier_name
    carrier_id: str                     # Kept: connection name (backward compat)
    connection_name: str = None         # NEW: same value as carrier_id
    service: str
    currency: str = None
    total_charge: float = 0.0
    extra_charges: List[ChargeDetails] = JList[ChargeDetails]
    estimated_delivery: str = None
    transit_days: int = None
    # ...
```

**Django Connection Models** (rename + new field):

```python
# modules/core/karrio/server/providers/models/carrier.py
class CarrierConnection(core.OwnedEntity):
    carrier_code = models.CharField(max_length=100, db_index=True, default="generic")
    connection_name = models.CharField(  # RENAMED from carrier_id
        max_length=150,
        db_index=True,
        help_text="User-defined connection name",
    )
    carrier_alias = models.CharField(  # NEW
        max_length=100,
        db_index=True,
        unique=True,
        help_text="Auto-generated unique slug for programmatic reference",
    )
    # ... rest unchanged
```

**Carrier Snapshot** (add new keys):

```python
# modules/core/karrio/server/core/utils.py - create_carrier_snapshot()
def create_carrier_snapshot(carrier, context=None):
    # ... existing logic ...
    return {
        "connection_id": str(carrier.id),
        "connection_type": connection_type,
        "carrier_code": carrier_code,
        "carrier_name": carrier_code,         # Kept for backward compat
        "carrier_id": carrier.connection_name, # Kept for backward compat
        "connection_name": carrier.connection_name,  # NEW
        "carrier_alias": carrier.carrier_alias,      # NEW
        "test_mode": carrier.test_mode,
    }
```

### Field Reference - Rename Map

| Current Name | New Name | Location | Type | Notes |
|---|---|---|---|---|
| `carrier_name` | `carrier_code` | API params, filters, responses | string | Same value; both returned in responses |
| `carrier_id` (model field) | `connection_name` | DB column, API responses | string | DB renamed via RenameField |
| `carrier_ids` (input list) | `connection_ids` | Shipment/rate request body | List[string] | Old name accepted for backward compat |
| `carrier_id` (tracking input) | `connection_id` | Tracking creation body | string | Old name accepted for backward compat |
| (new) | `carrier_alias` | Connection model + snapshot | string | Auto-generated readonly slug |

### Field Reference - carrier_alias

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `carrier_alias` | CharField(100) | Auto-generated | Unique slug. Migration: copied from old `carrier_id`. New: `{carrier_code}_{uuid.hex[:8]}` |

### API Changes

**Input Parameter Changes (all endpoints):**

| Old Param | New Param | Endpoints | Backward Compat |
|---|---|---|---|
| `carrier_name` (filter) | `carrier_code` | GET /shipments, GET /trackers, GET /pickups, GET /manifests, GET /connections | `carrier_name` still accepted |
| `carrier_ids` (body) | `connection_ids` | POST /shipments, POST /shipments/{id}/rates, POST /rates | `carrier_ids` still accepted |
| `carrier_id` (body) | `connection_id` | POST /trackers | `carrier_id` still accepted |
| `carrier_id` (body, connection) | `connection_name` | POST /connections, PATCH /connections/{id} | `carrier_id` still accepted |
| `carrier_name` (body, connection) | `carrier_code` | POST /connections | `carrier_name` still accepted |

**Response Changes (all endpoints):**

```json
// Before
{
  "carrier_name": "fedex",
  "carrier_id": "my_fedex_account"
}

// After (both old and new fields returned)
{
  "carrier_code": "fedex",
  "carrier_name": "fedex",
  "connection_name": "my_fedex_account",
  "carrier_id": "my_fedex_account",
  "carrier_alias": "fedex_a1b2c3d4"
}
```

**Connection Response Changes:**

```json
// Before
{
  "id": "car_abc123",
  "carrier_name": "fedex",
  "carrier_id": "my_fedex_account",
  "active": true,
  "test_mode": false
}

// After
{
  "id": "car_abc123",
  "carrier_code": "fedex",
  "carrier_name": "fedex",
  "connection_name": "my_fedex_account",
  "carrier_id": "my_fedex_account",
  "carrier_alias": "fedex_a1b2c3d4",
  "active": true,
  "test_mode": false
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Client sends `carrier_name` in filter (old name) | Works as before | Backend normalizes to `carrier_code` filter |
| Client sends `carrier_code` in filter (new name) | Uses new name directly | Primary path |
| Client sends BOTH `carrier_name` and `carrier_code` | `carrier_code` wins | Priority logic in filter/serializer |
| Client sends `carrier_ids` in request body (old name) | Works as before | Backend normalizes to `connection_ids` |
| Client sends `connection_ids` in request body (new name) | Uses new name directly | Primary path |
| Client sends BOTH `carrier_ids` and `connection_ids` | `connection_ids` wins | Priority logic in serializer |
| Existing `carrier_id` value contains special characters | `carrier_alias` migration copies value as-is | No slug transformation during migration |
| Two connections in same org have identical `carrier_id` values | `carrier_alias` collision | Append `_{uuid.hex[:4]}` suffix to resolve collision during migration |
| `carrier_alias` collision on new connection creation | Auto-generated alias conflicts | Retry with new UUID hex segment |
| SDK connector returns `carrier_name` but not `carrier_code` | Missing new field in response | Default `carrier_code = carrier_name` in model `__attrs_post_init__` |
| GraphQL query requests only `carrier_name` (old field) | Still works | Old fields are not removed from schema |
| Webhook payloads contain old field names | Consumers depend on them | Webhooks include both old and new field names |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Migration fails on RenameField | Connection model unusable | Test migration on staging first; RenameField is atomic |
| `carrier_alias` unique constraint violation during migration | Migration aborts | Handle collisions in RunPython step before adding unique constraint |
| Carrier connectors don't set `carrier_code` field | `None` in responses | Default `carrier_code = carrier_name` in SDK model post-init |
| Generated TypeScript types miss new fields | Frontend type errors | Regenerate types and verify compilation in CI |
| GraphQL schema changes break existing queries | Client query failures | Only ADD fields; never remove. Old fields stay |
| Snapshot JSON size increases | Slightly larger DB rows | Negligible (adds ~80 bytes per snapshot) |

### Security Considerations

- [x] No new user inputs that bypass existing validation
- [x] `carrier_alias` is readonly (system-generated, not user-modifiable)
- [x] Existing multi-tenancy scoping preserved (no query changes affect tenant isolation)
- [x] No secrets involved in rename

---

## Implementation Plan

### Phase 1: SDK Model & Connector Bug Fixes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `carrier_code` field to all 15 SDK response models (defaulting from `carrier_name`) | `modules/sdk/karrio/core/models.py` (see Appendix B.1.1) | Pending | M |
| Add `connection_name` field to all 13 SDK response models with `carrier_id` (defaulting from `carrier_id`) | `modules/sdk/karrio/core/models.py` (see Appendix B.1.1) | Pending | M |
| Add post-init logic to sync field pairs on all response models | `modules/sdk/karrio/core/models.py` | Pending | S |
| Update SDK Settings class: add `connection_name` alias for `carrier_id`, add `carrier_code` property | `modules/sdk/karrio/core/settings.py` (see Appendix B.1.2) | Pending | S |
| Update core datatypes: add new fields to all 7 dataclass types (Rate, Shipment, Pickup, etc.) | `modules/core/karrio/server/core/datatypes.py` (see Appendix B.3) | Pending | M |
| Fix 7 connector bugs: `carrier_name=settings.carrier_id` → `carrier_name=settings.carrier_name` | See Appendix D | Pending | S |

### Phase 2: Database Migration

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| RenameField `carrier_id` → `connection_name` on `CarrierConnection` | `modules/core/karrio/server/providers/migrations/` | Pending | S |
| RenameField `carrier_id` → `connection_name` on `SystemConnection` | `modules/core/karrio/server/providers/migrations/` | Pending | S |
| RenameField `carrier_id` → `connection_name` on `BrokeredConnection` | `modules/core/karrio/server/providers/migrations/` | Pending | S |
| RenameField `carrier_ids` → `connection_ids` on `Shipment` model | `modules/manager/karrio/server/manager/migrations/` | Pending | S |
| Add `carrier_alias` CharField to all three connection models | `modules/core/karrio/server/providers/migrations/` | Pending | S |
| RunPython: Backfill `carrier_alias` from existing `connection_name` values (with collision handling) | `modules/core/karrio/server/providers/migrations/` | Pending | M |
| Add unique constraint on `carrier_alias` (after backfill) | `modules/core/karrio/server/providers/migrations/` | Pending | S |
| Update `CarrierConnection` model: rename refs, add `carrier_alias`, update properties/`__str__`/`data` | `modules/core/karrio/server/providers/models/carrier.py` (see Appendix B.2.1) | Pending | M |
| Update `SystemConnection` model: rename refs, add `carrier_alias`, update properties | `modules/core/karrio/server/providers/models/connection.py` (see Appendix B.2.2) | Pending | M |
| Update `BrokeredConnection` model: rename `effective_carrier_id` → `effective_connection_name`, add `carrier_alias` | `modules/core/karrio/server/providers/models/connection.py` (see Appendix B.2.3) | Pending | M |
| Add `carrier_alias` auto-generation logic to model save/create | `modules/core/karrio/server/providers/models/carrier.py`, `connection.py` | Pending | M |
| Update manager model snapshot properties: add `carrier_code`, `connection_name` to 5 models | `modules/manager/karrio/server/manager/models.py` (see Appendix B.7.1) | Pending | M |

**Dependencies:** Phase 2 depends on Phase 1 (SDK models must have new fields before serializers reference them).

### Phase 3: Serializer, Filter & Gateway Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update connection input serializers (3 classes): `carrier_id` → `connection_name` with fallback | `modules/core/karrio/server/providers/serializers/base.py` (see Appendix B.4.2) | Pending | M |
| Update connection response serializers (5 classes): add `connection_name`, `carrier_code`, `carrier_alias` | `modules/core/karrio/server/providers/serializers/base.py` (see Appendix B.4.2) | Pending | M |
| Update 16 core serializer classes: add new field names to all carrier-related fields | `modules/core/karrio/server/core/serializers.py` (see Appendix B.4.1) | Pending | L |
| Update `carrier_ids` → `connection_ids` in shipment serializers with fallback (6+ references) | `modules/manager/karrio/server/manager/serializers/shipment.py` (see Appendix B.7.2) | Pending | M |
| Update `carrier_id` → `connection_id` in tracking serializer with fallback | `modules/manager/karrio/server/manager/serializers/tracking.py` (see Appendix B.7.2) | Pending | S |
| Update manifest serializer: `carrier_name` → `carrier_code` with fallback | `modules/manager/karrio/server/manager/serializers/manifest.py` (see Appendix B.7.2) | Pending | S |
| Update pickup serializer: rename filter keys | `modules/manager/karrio/server/manager/serializers/pickup.py` (see Appendix B.7.2) | Pending | S |
| Update document serializer: rename carrier ref in error message | `modules/manager/karrio/server/manager/serializers/document.py` (see Appendix B.7.2) | Pending | S |
| Update 6 REST filter classes: add `carrier_code` alongside `carrier_name` with fallback + OpenAPI params | `modules/core/karrio/server/core/filters.py` (see Appendix B.5) | Pending | M |
| Update `create_carrier_snapshot()`: add `connection_name`, `carrier_alias` keys | `modules/core/karrio/server/core/utils.py` (see Appendix B.6.2) | Pending | S |
| Update `Connections.list()` gateway: rename `carrier_ids`/`carrier_id`/`carrier_name` params with fallback | `modules/core/karrio/server/core/gateway.py` (see Appendix B.6.1) | Pending | M |
| Update `Rates.fetch()` and `Shipments.create()` gateway methods | `modules/core/karrio/server/core/gateway.py` (see Appendix B.6.1) | Pending | M |
| Update manager views: trackers.py (8 refs) and pickups.py (3 refs) | `modules/manager/karrio/server/manager/views/` (see Appendix B.7.3) | Pending | M |
| Update help text in schema view | `modules/core/karrio/server/core/views/schema.py` (see Appendix B.6.3) | Pending | S |
| Update pricing module: `Markup._is_applicable()` and `capture_fees_for_shipment()` | `modules/pricing/` (see Appendix B.9) | Pending | S |

### Phase 4: GraphQL & EE/Insiders Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add new fields to 11 GraphQL types (Message, Rate, CarrierSnapshot, Tracker, Manifest, Pickup, Shipment, RateSheet, SystemConnection, CarrierConnection) | `modules/graph/karrio/server/graph/schemas/base/types.py` (see Appendix B.8.1) | Pending | M |
| Update 8 GraphQL filter/mutation input types: add `carrier_code`/`connection_name` with fallback | `modules/graph/karrio/server/graph/schemas/base/inputs.py` (see Appendix B.8.2) | Pending | M |
| Update mutation resolvers: normalize input field names in CreateRateSheet/UpdateRateSheet | `modules/graph/karrio/server/graph/schemas/base/mutations.py` (see Appendix B.8.3) | Pending | S |
| Update EE admin types: `SystemCarrierConnectionType.resolve_list()` carrier_name → carrier_code | `ee/insiders/modules/admin/karrio/server/admin/schemas/base/types.py` (see Appendix B.11) | Pending | S |
| Update EE automation schemas: rename `carrier_id` → `connection_name` in ShippingRuleConditions/SelectServiceAction | `ee/insiders/modules/automation/karrio/server/automation/schemas.py` (see Appendix B.12.1) | Pending | S |
| Update EE rules engine: rate normalization, Rate creation, carrier matching | `ee/insiders/modules/automation/karrio/server/automation/services/rules_engine.py` (see Appendix B.12.2) | Pending | M |
| Update EE automation GraphQL types: add `connection_name` to SelectServiceActionType | `ee/insiders/modules/automation/karrio/server/graph/schemas/automation/types.py` (see Appendix B.12.3) | Pending | S |
| Update EE automation GraphQL inputs: add `connection_name` to 2 input types | `ee/insiders/modules/automation/karrio/server/graph/schemas/automation/inputs.py` (see Appendix B.12.4) | Pending | S |

### Phase 5: Carrier Connectors

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update all 28 standard connectors: add `carrier_code`, `connection_name` to response construction | `modules/connectors/*/` (see Appendix B.14) | Pending | L |
| Update EE dtdc connector: add new fields to all provider files | `ee/insiders/modules/connectors/dtdc/` (see Appendix B.13) | Pending | S |
| Update connector test fixtures: add new field names to expected output | `modules/connectors/*/tests/` | Pending | L |

**Note:** Since SDK models default new fields from old ones via post-init, connectors will work without changes. However, updating them to explicitly set the new fields is recommended for clarity and future-proofing.

### Phase 6: TypeScript & Frontend Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Regenerate REST API TypeScript types from OpenAPI spec (71 occurrences) | `packages/types/rest/api.ts` | Pending | S |
| Regenerate GraphQL TypeScript types (106 + 97 occurrences) | `packages/types/graphql/types.ts`, `packages/types/graphql/queries.ts` | Pending | S |
| Regenerate admin/EE GraphQL types (42 + 34 + 6 + 4 occurrences) | `packages/types/graphql/admin/`, `packages/types/graphql/ee/` | Pending | S |
| Update `packages/types/base.ts`: add new field names to error types, keep CARRIER_NAMES | `packages/types/base.ts` | Pending | S |
| Update 11 frontend hooks: carrier_ids → connection_ids, carrier_name → carrier_code, carrier_id → connection_name | `packages/hooks/` (see Appendix B.16) | Pending | M |
| Update 27+ UI components: carrier connection dialog, filters, forms, modals, badges | `packages/ui/` (see Appendix B.17) | Pending | L |
| Update 20 core module pages: Connections, Labels, Manifests, Orders, Pickups, Shipments, Trackers, ShippingRules | `packages/core/` (see Appendix B.18) | Pending | L |
| Update 7 other package files: admin, lib, developers, app-store | See Appendix B.19 | Pending | M |

### Phase 7: Test Data & Documentation Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update documents module test fixtures: add new keys to all sample data | `modules/documents/` (see Appendix B.10) | Pending | M |
| Update pricing module test data: add new fields to Rate objects | `modules/pricing/karrio/server/pricing/tests.py` (see Appendix B.9) | Pending | M |
| Add tests for new input param names | `modules/core/tests/`, `modules/manager/tests/` | Pending | M |
| Add backward compat tests for old input param names | `modules/core/tests/`, `modules/manager/tests/` | Pending | M |
| Add tests for `carrier_alias` generation and uniqueness | `modules/core/tests/` | Pending | M |
| Verify all existing tests pass without modification | All test directories | Pending | L |
| Verify TypeScript compilation | `packages/` | Pending | S |

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly as the original authors:
> - Use `unittest` for SDK/connector tests (NOT pytest)
> - Use Django tests via `karrio` for server tests
> - Add `print(response)` before assertions when debugging
> - Use `self.assertDictEqual` with `mock.ANY` for dynamic fields

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| SDK Model Tests | `modules/sdk/tests/` | New field defaults and sync |
| Migration Tests | `modules/core/tests/` | RenameField, backfill, uniqueness |
| Serializer Tests | `modules/core/tests/`, `modules/manager/tests/` | Input normalization, response shape |
| Filter Tests | `modules/core/tests/` | New and old param acceptance |
| Backward Compat Tests | `modules/core/tests/`, `modules/manager/tests/` | Old names still work everywhere |
| Existing Tests | All test directories | 100% pass rate unchanged |

### Test Cases

#### SDK Model Tests

```python
"""Test SDK model field sync between old and new names."""

import unittest
from karrio.core.models import RateDetails

class TestRateDetailsFields(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_carrier_code_defaults_from_carrier_name(self):
        """Verify carrier_code is set from carrier_name when not provided."""
        rate = RateDetails(
            carrier_name="fedex",
            carrier_id="my_fedex",
            service="express",
        )
        self.assertEqual(rate.carrier_code, "fedex")
        self.assertEqual(rate.carrier_name, "fedex")

    def test_connection_name_defaults_from_carrier_id(self):
        """Verify connection_name is set from carrier_id when not provided."""
        rate = RateDetails(
            carrier_name="fedex",
            carrier_id="my_fedex",
            service="express",
        )
        self.assertEqual(rate.connection_name, "my_fedex")
        self.assertEqual(rate.carrier_id, "my_fedex")
```

#### Serializer Backward Compat Tests

```python
"""Test backward compatibility for old input param names."""

import unittest
from unittest.mock import patch, ANY

class TestRateRequestBackwardCompat(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_connection_ids_accepted(self):
        """Verify new connection_ids param works."""
        response = self.client.post(
            "/v1/rates",
            data={
                "connection_ids": ["my_fedex"],
                "shipper": {"country_code": "US", "postal_code": "10001"},
                "recipient": {"country_code": "US", "postal_code": "90001"},
                "parcels": [{"weight": 1, "weight_unit": "LB"}],
            },
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)

    def test_carrier_ids_still_accepted(self):
        """Verify old carrier_ids param still works for backward compat."""
        response = self.client.post(
            "/v1/rates",
            data={
                "carrier_ids": ["my_fedex"],
                "shipper": {"country_code": "US", "postal_code": "10001"},
                "recipient": {"country_code": "US", "postal_code": "90001"},
                "parcels": [{"weight": 1, "weight_unit": "LB"}],
            },
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
```

#### Response Shape Tests

```python
"""Test that responses include both old and new field names."""

import unittest
from unittest.mock import ANY

class TestResponseFields(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_connection_response_includes_both_names(self):
        """Verify connection response has carrier_code, carrier_name, connection_name, carrier_id, carrier_alias."""
        response = self.client.get("/v1/connections")
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        connection = response.data["results"][0]
        # Both old and new names present
        self.assertIn("carrier_code", connection)
        self.assertIn("carrier_name", connection)
        self.assertIn("connection_name", connection)
        self.assertIn("carrier_id", connection)
        self.assertIn("carrier_alias", connection)
        # Old and new pairs have same value
        self.assertEqual(connection["carrier_code"], connection["carrier_name"])
        self.assertEqual(connection["connection_name"], connection["carrier_id"])

    def test_rate_response_includes_both_names(self):
        """Verify rate response has both old and new field names."""
        response = self.client.post("/v1/rates", data={...})
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        rate = response.data["rates"][0]
        self.assertIn("carrier_code", rate)
        self.assertIn("carrier_name", rate)
        self.assertEqual(rate["carrier_code"], rate["carrier_name"])
```

#### Filter Tests

```python
"""Test filter parameter acceptance."""

import unittest

class TestCarrierCodeFilter(unittest.TestCase):
    def test_carrier_code_filter_works(self):
        """Verify new carrier_code filter param is accepted."""
        response = self.client.get("/v1/shipments?carrier_code=fedex")
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)

    def test_carrier_name_filter_still_works(self):
        """Verify old carrier_name filter param still works."""
        response = self.client.get("/v1/shipments?carrier_name=fedex")
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run SDK tests
python -m unittest discover -v -f modules/sdk/tests

# Run server tests (core + manager)
karrio test --failfast karrio.server.core.tests
karrio test --failfast karrio.server.manager.tests

# Run all server tests
./bin/run-server-tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Existing API consumers break | High | Low | All old field names preserved in inputs and outputs; zero removal |
| DB migration fails on large dataset | High | Low | RenameField is metadata-only on PostgreSQL (no data rewrite); test on staging |
| `carrier_alias` backfill collision | Medium | Low | RunPython handles collisions by appending hash suffix |
| Carrier connectors don't populate new SDK fields | Medium | Medium | SDK model post-init defaults new fields from old ones; no connector changes needed |
| Generated TypeScript types break compilation | Medium | Low | Regenerate and verify in CI pipeline |
| GraphQL schema changes break client queries | Low | Low | Only additive changes; no fields removed or renamed in schema |
| Webhook consumers break | Medium | Low | Webhooks include both old and new field names in payloads |
| Performance impact from larger response payloads | Low | Low | ~80 extra bytes per response; negligible |
| Code complexity from dual-name support | Medium | Medium | Clear documentation; eventual deprecation of old names in future major version |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: All existing API consumers are unaffected. Old input param names are accepted everywhere. Old output field names are returned alongside new ones.
- **Data compatibility**: DB column rename is transparent. JSONField snapshots gain new keys but old keys are preserved. No data loss.
- **SDK compatibility**: Old fields on SDK models remain. New fields default from old ones. Carrier connectors need no changes.
- **Webhook compatibility**: Webhook payloads include both old and new field names.

### Data Migration

```python
# Migration: Backfill carrier_alias from existing connection_name values
def backfill_carrier_alias(apps, schema_editor):
    """Populate carrier_alias for existing connections."""
    import uuid

    CarrierConnection = apps.get_model("providers", "CarrierConnection")
    seen_aliases = set()

    for conn in CarrierConnection.objects.all():
        alias = conn.connection_name  # Was carrier_id before rename
        # Handle collision
        while alias in seen_aliases:
            alias = f"{alias}_{uuid.uuid4().hex[:4]}"
        seen_aliases.add(alias)
        conn.carrier_alias = alias
        conn.save(update_fields=["carrier_alias"])

    # Repeat for SystemConnection and BrokeredConnection
    # ...
```

**Migration Steps:**

1. Run `RenameField` migration for `carrier_id` -> `connection_name` on all connection models
2. Run `AddField` migration for `carrier_alias` (nullable initially)
3. Run `RunPython` migration to backfill `carrier_alias` from `connection_name` values
4. Run `AlterField` migration to make `carrier_alias` non-nullable + unique

### Rollback Procedure

1. **Identify issue**: Monitor API error rates after deployment; check for 400/500 responses on connection-related endpoints
2. **Stop rollout**: If issues found, halt deployment
3. **Revert code**: Revert serializer/filter/view changes (code is backward compatible in both directions)
4. **Revert migration**: Run reverse migration (Django `RenameField` is reversible; `carrier_alias` column dropped)
5. **Verify recovery**: Run full test suite; confirm old field names work as before

---

## Appendices

### Appendix A: Complete Rename Map

| Layer | Current | New (Primary) | Backward Compat |
|-------|---------|--------------|-----------------|
| API input (filter) | `carrier_name=fedex` | `carrier_code=fedex` | Accept both |
| API input (body list) | `carrier_ids: [...]` | `connection_ids: [...]` | Accept both |
| API input (body singular) | `carrier_id: "..."` | `connection_id: "..."` | Accept both |
| API input (connection create) | `carrier_id: "my_fedex"` | `connection_name: "my_fedex"` | Accept both |
| API input (connection create) | `carrier_name: "fedex"` | `carrier_code: "fedex"` | Accept both |
| API response (carrier type) | `carrier_name: "fedex"` | `carrier_code: "fedex"` | Return both |
| API response (connection name) | `carrier_id: "my_fedex"` | `connection_name: "my_fedex"` | Return both |
| API response (new) | N/A | `carrier_alias: "fedex_a1b2c3d4"` | New field |
| DB column | `carrier_id` | `connection_name` | Direct rename |
| DB column (new) | N/A | `carrier_alias` | New column |
| SDK model field | `carrier_name` | `carrier_code` | Both fields exist |
| SDK model field | `carrier_id` | `connection_name` | Both fields exist |
| Snapshot JSON key | `carrier_name` | `carrier_code` | Both keys exist |
| Snapshot JSON key | `carrier_id` | `connection_name` | Both keys exist |
| Snapshot JSON key (new) | N/A | `carrier_alias` | New key |
| GraphQL field | `carrier_name` | `carrier_code` | Both fields in schema |
| GraphQL field | `carrier_id` | `connection_name` | Both fields in schema |
| GraphQL filter | `carrier_name: [String]` | `carrier_code: [String]` | Both accepted |

### Appendix B: Exhaustive Affected Files Audit

> This appendix documents **every** file, class, field, property, filter, API view, GraphQL type/input/mutation,
> and frontend component affected by the carrier naming migration, organized by module.

---

#### B.1 SDK Layer (`modules/sdk/`)

##### B.1.1 SDK Response Models — `modules/sdk/karrio/core/models.py`

All 15 classes below need `carrier_code` (defaulting from `carrier_name`) and/or `connection_name` (defaulting from `carrier_id`) added:

| Line | Class | Has `carrier_name` | Has `carrier_id` | Action |
|------|-------|-------------------|------------------|--------|
| 322-331 | `Message` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 334-341 | `AddressValidationDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 362-375 | `RateDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 411-424 | `TrackingDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 450-462 | `ShipmentDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 465-478 | `PickupDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 488-496 | `ManifestDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 499-506 | `ConfirmationDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 509-520 | `DutiesCalculationDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 523-532 | `InsuranceDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 535-545 | `WebhookRegistrationDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 548-558 | `WebhookEventDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |
| 570-578 | `OAuthAuthorizeRequest` | Yes | No | Add `carrier_code` only |
| 875-899 | `RateSheet` | Yes | No | Add `carrier_code` only |
| 955-963 | `DocumentUploadDetails` | Yes | Yes | Add `carrier_code`, `connection_name` |

**Post-init sync logic**: Add `__attrs_post_init__` to default `carrier_code = carrier_name` and `connection_name = carrier_id` when not explicitly set.

##### B.1.2 SDK Settings — `modules/sdk/karrio/core/settings.py`

| Line | Class | Field | Action |
|------|-------|-------|--------|
| 13 | `Settings` | `carrier_id: str` | Rename to `connection_name`; add `carrier_id` as alias property |
| 23-25 | `Settings` | `carrier_name` (property) | Keep; add `carrier_code` property alongside |

---

#### B.2 Core Module — Models (`modules/core/`)

##### B.2.1 CarrierConnection — `modules/core/karrio/server/providers/models/carrier.py`

| Line | Element | Current | Action |
|------|---------|---------|--------|
| 103-107 | Field | `carrier_id` CharField(150) | **RenameField** → `connection_name` |
| 186 | `__str__()` | Returns `self.carrier_id` | Update to `self.connection_name` |
| 201 | `ext` property | Checks `"custom_carrier_name"` in credentials | No change (internal key) |
| 206-208 | `carrier_name` property | Returns carrier extension name | Keep; add `carrier_code` property alias |
| 218 | `display_name` property | Falls back to `self.carrier_id` | Update to `self.connection_name` |
| 240 | `data` property | `carrier_id=self.carrier_id` | Update to `connection_name=self.connection_name` |
| 241 | `data` property | `carrier_name=self.ext` | Keep (maps to SDK Settings.carrier_name) |
| 279 | `create_carrier_proxy()` | `carrier_name: str` param | No change (refers to carrier type code) |
| 284 | `create_carrier_proxy()` | `.filter(carrier_code=carrier_name)` | No change (internal) |
| — | (new) | — | **Add** `carrier_alias` CharField(100, unique, db_index) |
| — | (new) | — | **Add** `carrier_alias` auto-generation in `save()` |

##### B.2.2 SystemConnection — `modules/core/karrio/server/providers/models/connection.py`

| Line | Element | Current | Action |
|------|---------|---------|--------|
| 93-97 | Field | `carrier_id` CharField(150) | **RenameField** → `connection_name` |
| 176 | `__str__()` | Returns `f"{self.carrier_code}:{self.carrier_id}"` | Update to `self.connection_name` |
| 191 | `ext` property | Checks `"custom_carrier_name"` | No change (internal key) |
| 196-198 | `carrier_name` property | Returns ext | Keep; add `carrier_code` alias |
| 208 | `display_name` property | Falls back to `self.carrier_id` | Update to `self.connection_name` |
| 234 | `data` property | `carrier_id=self.carrier_id` | Update to `connection_name=self.connection_name` |
| 235 | `data` property | `carrier_name=self.ext` | Keep |
| — | (new) | — | **Add** `carrier_alias` field |

##### B.2.3 BrokeredConnection — `modules/core/karrio/server/providers/models/connection.py`

| Line | Element | Current | Action |
|------|---------|---------|--------|
| 362-367 | Field | `carrier_id` CharField(150, nullable) | **RenameField** → `connection_name` (user override) |
| 422 | `__str__()` | Uses `self.effective_carrier_id` | Update to `self.effective_connection_name` |
| 438-440 | Property | `effective_carrier_id` | **Rename** → `effective_connection_name`; add `effective_carrier_id` alias |
| 440 | Property body | `self.carrier_id or self.system_connection.carrier_id` | Update to `self.connection_name or self.system_connection.connection_name` |
| 448-450 | `carrier_name` property | Returns `self.ext` | Keep; add `carrier_code` alias |
| 455 | `display_name` property | Returns `self.effective_carrier_id` | Update to `self.effective_connection_name` |
| 541 | `data` property | `carrier_id=self.effective_carrier_id` | Update to `connection_name=self.effective_connection_name` |
| 542 | `data` property | `carrier_name=self.ext` | Keep |
| — | (new) | — | **Add** `carrier_alias` field |

---

#### B.3 Core Module — Datatypes (`modules/core/karrio/server/core/datatypes.py`)

| Line | Class | Field | Action |
|------|-------|-------|--------|
| 55-75 | `CarrierSettings.__init__()` | `carrier_name: str`, `carrier_id: str` params | Add `carrier_code`, `connection_name` params with fallback |
| 66 | `CarrierSettings` | `self.carrier_name = carrier_name` | Keep; add `self.carrier_code = carrier_code or carrier_name` |
| 68 | `CarrierSettings` | `self.carrier_id = carrier_id` | Keep; add `self.connection_name = connection_name or carrier_id` |
| 84 | `CarrierSettings.to_dict()` | Excludes `"carrier_name"` | Also exclude `"carrier_code"` |
| 205-206 | `Rate` dataclass | `carrier_name: str`, `carrier_id: str` | Add `carrier_code`, `connection_name` |
| 235 | `RateRequest` dataclass | `carrier_ids: List[str]` | Add `connection_ids` alias |
| 263-264 | `Shipment` dataclass | `carrier_id: str`, `carrier_name: str` | Add `connection_name`, `carrier_code` |
| 298-299 | `Pickup` dataclass | `carrier_id: str`, `carrier_name: str` | Add `connection_name`, `carrier_code` |
| 333-334 | `Tracking` dataclass | `carrier_name: str`, `carrier_id: str` | Add `carrier_code`, `connection_name` |
| 351-352 | `DocumentUploadResponse` dataclass | `carrier_name: str`, `carrier_id: str` | Add `carrier_code`, `connection_name` |
| 365-366 | `Manifest` dataclass | `carrier_id: str`, `carrier_name: str` | Add `connection_name`, `carrier_code` |

---

#### B.4 Core Module — Serializers

##### B.4.1 Core Serializers — `modules/core/karrio/server/core/serializers.py`

| Line | Class | Field | Type | Action |
|------|-------|-------|------|--------|
| 59-62 | `CarrierDetails` | `carrier_name` | ChoiceField | Add `carrier_code` alongside |
| 101-103 | `CarrierSettings` | `carrier_id` | CharField | Add `connection_name` alongside |
| 104-106 | `CarrierSettings` | `carrier_name` | ChoiceField | Add `carrier_code` alongside |
| 141-143 | `Message` | `carrier_name` | CharField | Add `carrier_code` |
| 144-146 | `Message` | `carrier_id` | CharField | Add `connection_name` |
| 760-765 | `RateRequest` | `carrier_ids` | StringListField | **Rename** → `connection_ids` with fallback |
| 837-841 | `TrackingData` | `carrier_name` | ChoiceField | Add `carrier_code` alongside |
| 1065-1068 | `PickupDetails` | `carrier_name`, `carrier_id` | CharField | Add `carrier_code`, `connection_name` |
| 1217-1223 | `TrackingDetails` | `carrier_name`, `carrier_id` | CharField | Add `carrier_code`, `connection_name` |
| 1369-1376 | `Rate` | `carrier_name`, `carrier_id` | CharField | Add `carrier_code`, `connection_name` |
| 1424-1562 | `ShipmentData` | `carrier_ids` (line 1549) | StringListField | **Rename** → `connection_ids` with fallback |
| 1564-1629 | `ShipmentDetails` | `carrier_name` (1571), `carrier_id` (1577) | CharField | Add `carrier_code`, `connection_name` |
| 1631-1783 | `ShipmentContent` | `carrier_ids` (1754) | StringListField | **Rename** → `connection_ids` with fallback |
| 1808-1828 | `ShipmentCancelRequest` | `carrier_id` (1819) | CharField | Add `connection_name` fallback |
| 1835-1867 | `ManifestRequestData` | `carrier_name` (1836) | CharField | Add `carrier_code` alongside |
| 1894-1917 | `ManifestDetails` | `carrier_name` (1899), `carrier_id` (1902) | CharField | Add `carrier_code`, `connection_name` |
| 1952-1962 | `OperationConfirmation` | `carrier_name` (1953), `carrier_id` (1956) | CharField | Add `carrier_code`, `connection_name` |
| 2058-2095 | `DocumentUploadRecord` | `carrier_name` (2059), `carrier_id` (2065) | CharField | Add `carrier_code`, `connection_name` |

##### B.4.2 Connection Serializers — `modules/core/karrio/server/providers/serializers/base.py`

| Line | Class | Field | Action |
|------|-------|-------|--------|
| 51-55 | `CarrierConnectionData` | `carrier_name` (ChoiceField) | Add `carrier_code` with `carrier_name` fallback |
| 56-59 | `CarrierConnectionData` | `carrier_id` (CharField) | **Rename** → `connection_name` with `carrier_id` fallback |
| 87-89 | `CarrierConnectionUpdateData` | `carrier_id` (CharField) | **Rename** → `connection_name` with fallback |
| 130-134 | `CarrierConnection` (output) | `carrier_name` (ChoiceField) | Add `carrier_code` field |
| 139-141 | `CarrierConnection` (output) | `carrier_id` (SerializerMethodField) | Add `connection_name` field; add `carrier_alias` field |
| 170-174 | `CarrierConnection` | `get_carrier_id()` method | Add `get_connection_name()` alias |
| 187-189 | `CarrierConnectionModelSerializer` | `carrier_name` (ChoiceField) | Add `carrier_code`; add `carrier_alias` |
| 273-361 | `SystemConnectionModelSerializer` | `carrier_name` (280) | Add `carrier_code`; add `carrier_alias` |
| 364-485 | `BrokeredConnectionModelSerializer` | `carrier_id` (385-390) | **Rename** → `connection_name` with fallback; add `carrier_alias` |
| 492-504 | `WebhookOperationResponse` | `carrier_name` (497), `carrier_id` (498) | Add `carrier_code`, `connection_name` |

---

#### B.5 Core Module — Filters (`modules/core/karrio/server/core/filters.py`)

| Line | Class | Filter Field | Action |
|------|-------|-------------|--------|
| 44-49 | `CarrierFilters` | `carrier_name` (CharFilter) | Add `carrier_code` filter; accept both |
| 69 | `CarrierFilters` | OpenAPI param `"carrier_name"` | Add `"carrier_code"` param |
| 119-124 | `CarrierConnectionFilter` | `carrier_name` (CharFilter) | Add `carrier_code` filter; accept both |
| 220-227 | `ShipmentFilters` | `carrier_name` (MultipleChoiceFilter) | Add `carrier_code` filter; accept both |
| 319-326 | `ShipmentFilters` | OpenAPI param for `carrier_name` | Add `carrier_code` param |
| 533-540 | `TrackerFilters` | `carrier_name` (MultipleChoiceFilter) | Add `carrier_code` filter; accept both |
| 567-574 | `TrackerFilters` | OpenAPI param for `carrier_name` | Add `carrier_code` param |
| 769-776 | `PickupFilters` | `carrier_name` (MultipleChoiceFilter) | Add `carrier_code` filter; accept both |
| 834-841 | `PickupFilters` | OpenAPI param for `carrier_name` | Add `carrier_code` param |
| 959-966 | `ManifestFilters` | `carrier_name` (MultipleChoiceFilter) | Add `carrier_code` filter; accept both |
| 980-987 | `ManifestFilters` | OpenAPI param for `carrier_name` | Add `carrier_code` param |

---

#### B.6 Core Module — Gateway & Utils

##### B.6.1 Gateway — `modules/core/karrio/server/core/gateway.py`

| Line | Method | Reference | Action |
|------|--------|-----------|--------|
| 106-109 | `Connections.list()` | `carrier_id` filter (matches by `id` OR `carrier_id`) | Update to filter by `connection_name`; accept `carrier_id` fallback |
| 150-163 | `Connections.list()` | `carrier_ids` list filter (matches by `id` OR `carrier_id`) | **Rename** param → `connection_ids`; accept `carrier_ids` fallback |
| 183-188 | `Connections.list()` | `carrier_name` filter (filters by `carrier_code`) | **Rename** → `carrier_code`; accept `carrier_name` fallback |
| 255 | `Address.validate()` | `provider.carrier_id` in error message | Update to `provider.connection_name` |
| 284 | `Shipments.create()` | `selected_rate.carrier_id` for carrier resolution | Update to `selected_rate.connection_name` |
| 324 | `Shipments.create()` | `carrier.carrier_name` in meta/rate_provider | Update to `carrier.carrier_code` or keep (same value) |
| 718 | `Rates.fetch()` | `carrier_ids` from payload | **Rename** → `connection_ids` with fallback |
| 751 | `Rates.fetch()` | `effective_carrier_id` on BrokeredConnection | Update to `effective_connection_name` |
| 768 | `Rates.fetch()` | `carrier_connection_id` in meta | Keep (this is the DB PK, not the renamed field) |

##### B.6.2 Utils — `modules/core/karrio/server/core/utils.py`

| Line | Function | Reference | Action |
|------|----------|-----------|--------|
| 1160-1225 | `create_carrier_snapshot()` | Returns dict with `carrier_code`, `carrier_id`, `carrier_name` | **Add** `connection_name`, `carrier_alias` keys; keep old keys |
| 1213 | `create_carrier_snapshot()` | `carrier_name = carrier_code` | Keep; also set `connection_name = carrier.connection_name` |
| 1215 | `create_carrier_snapshot()` | `"carrier_id": carrier.carrier_id` | Update to `carrier.connection_name`; add `"connection_name"` key |
| 1227-1316 | `resolve_carrier()` | Reads snapshot `connection_type`, `connection_id` | No change (these are not being renamed) |

##### B.6.3 Views — `modules/core/karrio/server/core/views/schema.py`

| Line | Context | Reference | Action |
|------|---------|-----------|--------|
| 223 | Help text | `"The 'carrier_id' is a friendly name..."` | Update help text to reference `connection_name` |

---

#### B.7 Manager Module (`modules/manager/`)

##### B.7.1 Models — `modules/manager/karrio/server/manager/models.py`

**Carrier snapshot properties on 5 models** (each reads from the `carrier` JSONField):

| Model | Lines | Properties | Action |
|-------|-------|-----------|--------|
| `Shipment` | 887-890 | `carrier_ids` JSONField definition | **Rename** field → `connection_ids` (DB migration) |
| `Shipment` | 947-950 | `carrier_id` property → `self.carrier.get("carrier_id")` | Add `connection_name` property alongside |
| `Shipment` | 953-956 | `carrier_name` property → `self.carrier.get("carrier_name")` | Add `carrier_code` property alongside |
| `Tracking` | 704-707 | `carrier_id` property → `self.carrier.get("carrier_id")` | Add `connection_name` property alongside |
| `Tracking` | 710-713 | `carrier_name` property → `self.carrier.get("carrier_name")` | Add `carrier_code` property alongside |
| `Pickup` | 552-555 | `carrier_id` property → `self.carrier.get("carrier_id")` | Add `connection_name` property alongside |
| `Pickup` | 558-561 | `carrier_name` property → `self.carrier.get("carrier_name")` | Add `carrier_code` property alongside |
| `Manifest` | 1181-1184 | `carrier_id` property → `self.carrier.get("carrier_id")` | Add `connection_name` property alongside |
| `Manifest` | 1187-1190 | `carrier_name` property → `self.carrier.get("carrier_name")` | Add `carrier_code` property alongside |
| `DocumentUploadRecord` | 1080-1083 | `carrier_id` property → `self.carrier.get("carrier_id")` | Add `connection_name` property alongside |
| `DocumentUploadRecord` | 1086-1089 | `carrier_name` property → `self.carrier.get("carrier_name")` | Add `carrier_code` property alongside |

##### B.7.2 Serializers — `modules/manager/karrio/server/manager/serializers/`

**shipment.py:**

| Line | Class/Function | Reference | Action |
|------|---------------|-----------|--------|
| 86 | `ShipmentSerializer.create()` | `carrier_ids = validated_data.get("carrier_ids")` | Update to `connection_ids` with fallback |
| 91-94 | `ShipmentSerializer.create()` | `resolve_alternative_service_carrier()` with `carrier_ids` | Update param name |
| 103-104 | `ShipmentSerializer.create()` | `carrier_ids=carrier_ids` gateway call | Update to `connection_ids` |
| 136-137 | `ShipmentSerializer.create()` | `carrier_ids` in secondary call | Update param |
| 310 | `ShipmentSerializer.update()` | `carrier_id=selected_rate.get("carrier_id")` | Update to `connection_name` |
| 440-446 | `ShipmentRateData` | `carrier_ids` StringListField | **Rename** → `connection_ids` with fallback |
| 560, 563 | `ShipmentPurchaseSerializer.create()` | `carrier_name=carrier_name` in tracking URL | Update to `carrier_code` |
| 612-613 | `fetch_shipment_rates()` | `carrier_ids = data.get("carrier_ids", [])` | Update to `connection_ids` with fallback |
| 619 | `fetch_shipment_rates()` | `carrier_ids=carrier_ids` gateway call | Update param |
| 662 | `buy_shipment_label()` | `carrier_id=selected_rate.get("carrier_id")` | Update to `connection_name` |
| 683 | `buy_shipment_label()` | `carrier.carrier_name == "ups"` check | Update to `carrier.carrier_code` (or keep; same value) |
| 880 | `create_shipment_tracker()` | `shipment.carrier_name` | Update to `shipment.carrier_code` |
| 887 | `create_shipment_tracker()` | `rate_provider != shipment.carrier_name` | Update |
| 906 | `create_shipment_tracker()` | `"dhl" in carrier.carrier_name` | Update to `carrier.carrier_code` |
| 910 | `create_shipment_tracker()` | `carrier_name="dhl_universal"` gateway param | Update to `carrier_code` |
| 974, 977 | `create_shipment_tracker()` | `carrier.carrier_name` in URL generation | Update to `carrier.carrier_code` |
| 1047 | `resolve_alternative_service_carrier()` | `carrier_ids: list` param | **Rename** → `connection_ids` |
| 1061-1072 | `resolve_alternative_service_carrier()` | `carrier_ids` variable | Update variable name |
| 1084-1089 | `resolve_alternative_service_carrier()` | `carrier_name` variable, `c.carrier_name` comparison | Update to `carrier_code` |
| 1105-1106 | `resolve_alternative_service_carrier()` | `"carrier_id": carrier.carrier_id`, `"carrier_name": carrier.carrier_name` | Add new keys alongside |

**tracking.py:**

| Line | Class/Function | Reference | Action |
|------|---------------|-----------|--------|
| 27 | `TrackingSerializer` | `carrier_id = serializers.CharField(required=False)` | **Rename** → `connection_id` with `carrier_id` fallback |
| 28 | `TrackingSerializer` | `carrier_name = serializers.CharField(required=False)` | Add `carrier_code` alongside |
| 132-133 | `TrackingSerializer.update()` | `current_carrier_id = ...get("connection_id")` | No change (reads snapshot `connection_id` = DB PK) |

**manifest.py:**

| Line | Class/Function | Reference | Action |
|------|---------------|-----------|--------|
| 21 | `ManifestSerializer.create()` | `carrier_name = data["carrier_name"]` | Update to `carrier_code` with fallback |
| 24 | `ManifestSerializer.create()` | `carrier_name=carrier_name` gateway param | Update to `carrier_code` |
| 32 | `ManifestSerializer.create()` | `carrier__carrier_code=carrier_name` filter | Keep (already uses `carrier_code` in DB query) |

**pickup.py:**

| Line | Class/Function | Reference | Action |
|------|---------------|-----------|--------|
| 170 | `PickupData.create()` | `carrier_filter["carrier_name"] = carrier_code` | Update key to `"carrier_code"` |
| 172 | `PickupData.create()` | `carrier_filter["carrier_id"] = connection_id` | Update key to `"connection_name"` |

**document.py:**

| Line | Class/Function | Reference | Action |
|------|---------------|-----------|--------|
| 125 | `can_upload_shipment_document()` | `carrier.carrier_id` in error message | Update to `carrier.connection_name` |

##### B.7.3 Views — `modules/manager/karrio/server/manager/views/`

**trackers.py:**

| Line | Class/Method | Reference | Action |
|------|-------------|-----------|--------|
| 42 | `TrackerList.get_queryset()` | `carrier_name = query_params.get("carrier_name")` | Add `carrier_code` param; fallback to `carrier_name` |
| 44-46 | `TrackerList.get_queryset()` | `Q(carrier__carrier_code=carrier_name)` | Update variable name |
| 113 | `TrackerList.post()` | `carrier_name = query.get("hub") if ... else data["carrier_name"]` | Update to `carrier_code` |
| 127 | `TrackerList.post()` | `"carrier_name": carrier_name` in filter dict | Update key |
| 133 | `TrackerList.post()` | `{"carrier": data["carrier_name"]}` in options | Update key |
| 174 | `TrackerList.post()` | `"carrier_name"` OpenAPI enum ref | Update to `"carrier_code"` |
| 189 | `TrackersCreate.get()` | `carrier_name: str` URL param | Update to `carrier_code` |
| 204 | `TrackersCreate.get()` | `"carrier_name": ...` filter dict | Update key |
| 420 | URL pattern | `"trackers/<str:carrier_name>/..."` | Keep for backward compat; add `carrier_code` route |

**pickups.py:**

| Line | Class/Method | Reference | Action |
|------|-------------|-----------|--------|
| 104 | `PickupRequest.post()` | `carrier_name: str` URL param | Update to `carrier_code` |
| 111 | `PickupRequest.post()` | `"carrier_name": carrier_name` filter dict | Update key |
| 203 | URL pattern | `"pickups/<str:carrier_name>/schedule"` | Keep for backward compat; add `carrier_code` route |

---

#### B.8 Graph Module (`modules/graph/`)

##### B.8.1 GraphQL Types — `modules/graph/karrio/server/graph/schemas/base/types.py`

| Line | Type | Fields | Action |
|------|------|--------|--------|
| 787-788 | `MessageType` | `carrier_name`, `carrier_id` | Add `carrier_code`, `connection_name` |
| 818-819 | `RateType` | `carrier_name`, `carrier_id` | Add `carrier_code`, `connection_name` |
| 1382-1397 | `CarrierSnapshotType` | `carrier_id`, `carrier_name` + `parse()` method | Add `connection_name`, `carrier_code`, `carrier_alias` |
| 1422-1427 | `TrackerType` | `carrier_id()`, `carrier_name()` resolver properties | Add `connection_name()`, `carrier_code()` resolvers |
| 1481-1486 | `ManifestType` | `carrier_id()`, `carrier_name()` resolvers | Add `connection_name()`, `carrier_code()` resolvers |
| 1547-1552 | `PickupType` | `carrier_id()`, `carrier_name()` resolvers | Add `connection_name()`, `carrier_code()` resolvers |
| 1662-1675 | `ShipmentType` | `carrier_id`, `carrier_name`, `carrier_ids` | Add `connection_name`, `carrier_code`, `connection_ids` |
| 1986 | `RateSheetType` | `carrier_name: CarrierNameEnum` | Add `carrier_code` |
| 2061-2072 | `SystemConnectionType` | `carrier_id`, `carrier_name()` resolver | Add `connection_name`, `carrier_code`, `carrier_alias` |
| 2126-2127 | `SystemConnectionType.resolve_list()` | Filters by `carrier_name` | Update to `carrier_code` |
| 2136-2138 | `CarrierConnectionType` | `carrier_id`, `carrier_code`, `carrier_name` | Add `connection_name`, `carrier_alias` |

##### B.8.2 GraphQL Inputs — `modules/graph/karrio/server/graph/schemas/base/inputs.py`

| Line | Input Type | Field | Action |
|------|-----------|-------|--------|
| 37 | `TrackerFilter` | `carrier_name: List[str]` | Add `carrier_code` filter; accept both |
| 48 | `ShipmentFilter` | `carrier_name` | Add `carrier_code`; accept both |
| 67 | `ManifestFilter` | `carrier_name` | Add `carrier_code`; accept both |
| 79 | `PickupFilter` | `carrier_name` | Add `carrier_code`; accept both |
| 110 | `CarrierFilter` | `carrier_name` | Add `carrier_code`; accept both |
| 697 | `CreateRateSheetMutationInput` | `carrier_name: CarrierNameEnum` | Add `carrier_code`; accept both |
| 734-735 | `CreateCarrierConnectionMutationInput` | `carrier_name`, `carrier_id` | Add `carrier_code`, `connection_name`; accept old |
| 747 | `UpdateCarrierConnectionMutationInput` | `carrier_id` (optional) | Add `connection_name`; accept both |

##### B.8.3 GraphQL Mutations — `modules/graph/karrio/server/graph/schemas/base/mutations.py`

| Line | Mutation | Reference | Action |
|------|---------|-----------|--------|
| 552 | `CreateRateSheetMutation` | `carrier_code=rate_sheet.carrier_name` | Update to use `carrier_code` input |
| 606 | `UpdateRateSheetMutation` | `carrier_code=rate_sheet.carrier_name` | Update to use `carrier_code` input |

---

#### B.9 Pricing Module (`modules/pricing/`)

| File | Line | Class/Function | Reference | Action |
|------|------|---------------|-----------|--------|
| `models.py` | 161 | `Markup._is_applicable()` | `rate.carrier_name in self.carrier_codes` | Update to `rate.carrier_code` |
| `signals.py` | 87 | `capture_fees_for_shipment()` | `carrier_code = meta.get("carrier_code") or selected_rate.get("carrier_name")` | Update fallback to `carrier_code` |
| `tests.py` | 87-665 | Multiple test cases | Rate objects with `carrier_name`, `carrier_id` | Add `carrier_code`, `connection_name` to test data |

---

#### B.10 Documents Module (`modules/documents/`)

| File | Line | Reference | Action |
|------|------|-----------|--------|
| `utils.py` | 270-271, 297-298, 304-305 | Sample shipment data with `carrier_name`, `carrier_id` | Add `carrier_code`, `connection_name` keys |
| `utils.py` | 574-1648 | Extensive test fixtures | Add new keys to all fixture dicts |
| `tests/test_generator.py` | 274-275 | Test data with `carrier_id`, `carrier_name` | Add new keys |

---

#### B.11 EE/Insiders — Admin Module

##### B.11.1 Admin Types — `ee/insiders/modules/admin/karrio/server/admin/schemas/base/types.py`

| Line | Class/Function | Reference | Action |
|------|---------------|-----------|--------|
| 398-399 | `SystemCarrierConnectionType.resolve_list()` | `carrier_code=_filter_data["carrier_name"]` | Update to read from `carrier_code` input |

##### B.11.2 Admin Inputs — `ee/insiders/modules/admin/karrio/server/admin/schemas/base/inputs.py`

No direct `carrier_name`/`carrier_id` field definitions found. Filter types inherit from base graph module.

---

#### B.12 EE/Insiders — Automation Module

##### B.12.1 Automation Schemas — `ee/insiders/modules/automation/karrio/server/automation/schemas.py`

| Line | Class | Field | Action |
|------|-------|-------|--------|
| 44 | `ShippingRuleConditions` | `carrier_id: Optional[str]` | **Rename** → `connection_name`; accept `carrier_id` fallback |
| 60 | `SelectServiceAction` | `carrier_id: Optional[str]` | **Rename** → `connection_name`; accept `carrier_id` fallback |

##### B.12.2 Rules Engine — `ee/insiders/modules/automation/karrio/server/automation/services/rules_engine.py`

| Line | Function | Reference | Action |
|------|----------|-----------|--------|
| 1658 | Rate normalization | Comment: "use carrier_name as carrier_id fallback" | Update comment and logic |
| 1661-1663 | Rate normalization | Ensures `carrier_id` and `carrier_name` in rate data | Add `connection_name`, `carrier_code` normalization |
| 1672-1673 | Rate creation | `Rate(carrier_id=..., carrier_name=...)` | Add `connection_name`, `carrier_code` |
| 1865-1868 | `_select_preferred_rate()` | Matches `carrier_code` against `carrier_name` | Update to match against `carrier_code` |

##### B.12.3 Automation GraphQL Types — `ee/insiders/modules/automation/karrio/server/graph/schemas/automation/types.py`

| Line | Type | Field | Action |
|------|------|-------|--------|
| 468 | `SelectServiceActionType` | `carrier_id: Optional[str]` | Add `connection_name` |
| 482 | `SelectServiceActionType` | `carrier_id` (resolver) | Add `connection_name` resolver |

##### B.12.4 Automation GraphQL Inputs — `ee/insiders/modules/automation/karrio/server/graph/schemas/automation/inputs.py`

| Line | Input Type | Field | Action |
|------|-----------|-------|--------|
| 227 | `ShippingRuleConditionsInput` | `carrier_id: Optional[str]` | Add `connection_name`; accept both |
| 241 | `SelectServiceActionInput` | `carrier_id: Optional[str]` | Add `connection_name`; accept both |

---

#### B.13 EE/Insiders — DTDC Connector (`ee/insiders/modules/connectors/dtdc/`)

| File | Pattern | Action |
|------|---------|--------|
| `karrio/mappers/dtdc/settings.py` | `carrier_id` field in Settings class | Update to `connection_name` |
| `karrio/providers/dtdc/error.py` | `carrier_name=settings.carrier_name, carrier_id=settings.carrier_id` | Add `carrier_code`, `connection_name` |
| `karrio/providers/dtdc/shipment/create.py` | `carrier_name=settings.carrier_name, carrier_id=settings.carrier_id` | Add `carrier_code`, `connection_name` |
| `karrio/providers/dtdc/shipment/cancel.py` | `carrier_name=settings.carrier_name, carrier_id=settings.carrier_id` | Add `carrier_code`, `connection_name` |
| `karrio/providers/dtdc/tracking.py` | `carrier_name=settings.carrier_name, carrier_id=settings.carrier_id` | Add `carrier_code`, `connection_name` |
| `karrio/providers/dtdc/utils.py` | Helper references | Update references |
| `tests/dtdc/test_shipment.py` | Test fixture data | Add new field names |
| `tests/dtdc/test_tracking.py` | Test fixture data | Add new field names |

---

#### B.14 Carrier Connectors (`modules/connectors/`)

**28 connectors**, each with the standard pattern `carrier_name=settings.carrier_name, carrier_id=settings.carrier_id` in response construction files.

**Standard files per connector that reference carrier fields:**

| File Pattern | Typical References | Action |
|-------------|-------------------|--------|
| `karrio/mappers/{connector}/settings.py` | `carrier_id` attribute (from base Settings class) | Inherits SDK Settings rename |
| `karrio/providers/{connector}/error.py` | `carrier_name=settings.carrier_name, carrier_id=settings.carrier_id` | Add `carrier_code`, `connection_name` |
| `karrio/providers/{connector}/rate.py` | Same pattern in RateDetails construction | Add new fields |
| `karrio/providers/{connector}/tracking.py` | Same pattern in TrackingDetails construction | Add new fields |
| `karrio/providers/{connector}/shipment/create.py` | Same pattern in ShipmentDetails construction | Add new fields |
| `karrio/providers/{connector}/shipment/cancel.py` | Same pattern in ConfirmationDetails construction | Add new fields |
| `karrio/providers/{connector}/manifest.py` | Same pattern in ManifestDetails construction | Add new fields |
| `karrio/providers/{connector}/document.py` | Same pattern in DocumentUploadDetails construction | Add new fields |
| `tests/{connector}/test_*.py` | Fixture data with `carrier_name`, `carrier_id` | Add new field names |

**Complete list of connectors:**
`asendia`, `australiapost`, `bpost`, `canadapost`, `chronopost`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dpd`, `dpd_meta`, `fedex`, `generic`, `gls`, `hermes`, `laposte`, `landmark`, `mydhl`, `parcelone`, `postat`, `purolator`, `seko`, `sendle`, `spring`, `teleship`, `ups`, `usps`, `usps_international`

**Total connector Python files with references:** ~333 files

---

#### B.15 Frontend — Type Definitions (`packages/types/`)

| File | Occurrences | Key Types/Interfaces | Action |
|------|------------|---------------------|--------|
| `rest/api.ts` | 71 | `CarrierConnection`, `CarrierConnectionData`, `CarrierDetails`, `PatchedCarrierConnectionData`; enums: `CarrierConnectionCarrierNameEnum`, `CarrierConnectionDataCarrierNameEnum`, `CarrierDetailsCarrierNameEnum`, etc. (12+ enum types); `TrackingDataCarrierNameEnum`, `CancelPickupCarrierNameEnum`, `SchedulePickupCarrierNameEnum`, `TrackShipmentCarrierNameEnum`, `UpdatePickupCarrierNameEnum`, `VoidLabelCarrierNameEnum` | **Regenerate** from OpenAPI spec (auto) |
| `graphql/types.ts` | 106 | All GraphQL type interfaces | **Regenerate** from schema (auto) |
| `graphql/queries.ts` | 97 | All GraphQL query fragments | **Regenerate** from schema (auto) |
| `graphql/admin/types.ts` | 42 | Admin GraphQL type interfaces | **Regenerate** (auto) |
| `graphql/admin/queries.ts` | 34 | Admin GraphQL query fragments | **Regenerate** (auto) |
| `graphql/ee/types.ts` | 6 | EE GraphQL types | **Regenerate** (auto) |
| `graphql/ee/queries.ts` | 4 | EE GraphQL queries | **Regenerate** (auto) |
| `base.ts` | 5 | `CARRIER_NAMES` constant; `PresetCollection` type; `ErrorMessage.carrier_id`/`.carrier_name`; `APIError.carrier_id`/`.carrier_name`; `CARRIER_THEMES`; `CARRIER_IMAGES` | Add `carrier_code`, `connection_name` to error types; keep `CARRIER_NAMES` |

---

#### B.16 Frontend — Hooks (`packages/hooks/`)

| File | Occurrences | Key References | Action |
|------|------------|---------------|--------|
| `carrier-connections.ts` | 8 | `OAuthCallbackResult.carrier_name`; `OAuthAuthorizeResponse.carrier_name`; `CarrierWebhookRegistrationResult.carrier_name`/`.carrier_id`; `CarrierWebhookDeregistrationResult.carrier_name`/`.carrier_id`; `useConnections` indexing by `carrier_name` | Add new field names; update primary references |
| `admin-shipments.ts` | 2+ | carrier_name filter params | Update to `carrier_code` |
| `bulk-shipments.ts` | 2+ | carrier_ids in payload | Update to `connection_ids` |
| `label-data.ts` | 2+ | carrier_ids in shipment data | Update to `connection_ids` |
| `manifests.ts` | 2+ | carrier_name in manifest calls | Update to `carrier_code` |
| `pickup.ts` | 2+ | carrier_name in pickup calls | Update to `carrier_code` |
| `shipment.ts` | 3+ | carrier_ids in rate/shipment calls | Update to `connection_ids` |
| `shipping-rules.ts` | 2+ | carrier_id in rule conditions | Update to `connection_name` |
| `tracker.ts` | 3+ | carrier_name, carrier_id in tracking calls | Update to `carrier_code`, `connection_id` |
| `user-connection.ts` | 3+ | carrier_id, carrier_name in connection CRUD | Update to `connection_name`, `carrier_code` |
| `workflow-templates.ts` | 1+ | carrier_id references | Update |

---

#### B.17 Frontend — UI Components (`packages/ui/`)

| File | Occurrences | Key Usage | Action |
|------|------------|----------|--------|
| `components/carrier-connection-dialog.tsx` | 43 | Connection create/update forms; carrier_id input, carrier_name selection | Update to `connection_name`, `carrier_code` |
| `core/modals/connect-provider-modal.tsx` | 29 | Legacy connection modal; carrier_id, carrier_name fields | Update to new names |
| `components/rate-sheet-editor.tsx` | 6 | Rate sheet carrier_name selection | Update to `carrier_code` |
| `core/modals/rate-sheet-editor.tsx` | 6 | Rate sheet editor carrier_name | Update |
| `core/modals/rate-sheet-edit-modal.tsx` | 3+ | Rate sheet carrier_name | Update |
| `core/forms/user-carrier-list.tsx` | 13 | Carrier list display; uses carrier_name, carrier_id | Update to new names |
| `core/forms/system-carrier-list.tsx` | 5+ | System carrier display | Update |
| `core/forms/rate-sheet-list.tsx` | 3+ | Rate sheet list | Update |
| `core/filters/shipments-filter.tsx` | 12 | Shipment filter by carrier_name | Update to `carrier_code` |
| `core/filters/trackers-filter.tsx` | 12 | Tracker filter by carrier_name | Update to `carrier_code` |
| `components/shipments-filter.tsx` | 5+ | Shipment filter component | Update |
| `components/trackers-filter.tsx` | 5+ | Tracker filter component | Update |
| `components/schedule-pickup-dialog.tsx` | 14 | Pickup scheduling; carrier_name | Update to `carrier_code` |
| `core/modals/track-shipment-modal.tsx` | 5+ | Track modal; carrier_name | Update |
| `components/track-shipment-dialog.tsx` | 5+ | Track dialog; carrier_name | Update |
| `core/components/carrier-badge.tsx` | 3+ | Badge display by carrier_name | Update |
| `core/components/carrier-image.tsx` | 3+ | Image lookup by carrier_name | Update |
| `core/components/carrier-name-badge.tsx` | 3+ | Name badge by carrier_name | Update |
| `core/components/connection-description.tsx` | 3+ | Connection display | Update |
| `core/components/rate-description.tsx` | 3+ | Rate display; carrier_name | Update |
| `core/components/shipment-menu.tsx` | 3+ | Shipment menu carrier refs | Update |
| `components/shipment-menu.tsx` | 3+ | Shipment menu carrier refs | Update |
| `components/activity-timeline.tsx` | 2+ | Timeline carrier display | Update |
| `components/notifier.tsx` | 2+ | Notification carrier refs | Update |
| `core/components/notifier.tsx` | 2+ | Notification carrier refs | Update |
| `components/tracking-preview-sheet.tsx` | 2+ | Tracking preview | Update |
| `components/template-editor.tsx` | 2+ | Template carrier refs | Update |
| `core/modals/webhook-test-modal.tsx` | 2+ | Webhook test data | Update |

---

#### B.18 Frontend — Core Modules (`packages/core/`)

| File | Key References | Action |
|------|---------------|--------|
| `modules/Connections/index.tsx` | carrier_name, carrier_id in connection list/table | Update |
| `modules/Connections/rate-sheets.tsx` | carrier_name in rate sheet list | Update |
| `modules/Connections/system.tsx` | carrier_name, carrier_id in system connections | Update |
| `modules/Labels/create_labels.tsx` | carrier_ids in label creation | Update to `connection_ids` |
| `modules/Manifests/create_manifests.tsx` | carrier_name in manifest creation | Update to `carrier_code` |
| `modules/Manifests/index.tsx` | carrier_name in manifest list display | Update |
| `modules/Orders/create_label.tsx` | carrier_ids in order label creation | Update to `connection_ids` |
| `modules/Orders/index.tsx` | carrier_name display | Update |
| `modules/Pickups/index.tsx` | carrier_name in pickup list | Update |
| `modules/Shipments/create_label.tsx` | carrier_ids in shipment creation | Update to `connection_ids` |
| `modules/Shipments/index.tsx` | carrier_name filter/display | Update |
| `modules/Shipments/shipment.tsx` | carrier_name, carrier_id in shipment detail | Update |
| `modules/Shippers/details.tsx` | carrier references | Update |
| `modules/Shippers/markups.tsx` | carrier_name in markup config | Update |
| `modules/ShippingRules/index.tsx` | carrier_id in rule conditions | Update to `connection_name` |
| `modules/Trackers/index.tsx` | carrier_name filter/display | Update |
| `modules/Trackers/tracking-page.tsx` | carrier_name in tracking page | Update |
| `components/shipping-rule-form.tsx` | carrier_id in rule form | Update to `connection_name` |
| `components/tracking-preview.tsx` | carrier_name display | Update |
| `context/image.ts` | carrier_name image lookup | Update |

---

#### B.19 Frontend — Other Packages

| File | Key References | Action |
|------|---------------|--------|
| `packages/admin/components/carrier-connections-table.tsx` | carrier_name, carrier_id in admin table | Update |
| `packages/admin/components/rate-sheets-table.tsx` | carrier_name in admin table | Update |
| `packages/admin/modules/carriers/index.tsx` | carrier_name, carrier_id in admin carrier page | Update |
| `packages/lib/carrier-utils.ts` | Carrier utility functions using carrier_name | Update |
| `packages/lib/helper.ts` | General helpers with carrier refs | Update |
| `packages/developers/components/views/logs-view.tsx` | carrier_name in log display | Update |
| `packages/developers/modules/log.tsx` | carrier_name in log detail | Update |
| `packages/app-store/apps/shopify/api/carrier-service/rates/[installationId]/route.ts` | carrier_name in Shopify integration | Update |

---

#### B.20 Migrations (New Files)

| File | Type | Description |
|------|------|-------------|
| `modules/core/karrio/server/providers/migrations/XXXX_rename_carrier_id_to_connection_name.py` | Add | `RenameField` on CarrierConnection, SystemConnection, BrokeredConnection |
| `modules/core/karrio/server/providers/migrations/XXXX_add_carrier_alias.py` | Add | `AddField` for `carrier_alias` on all connection models |
| `modules/core/karrio/server/providers/migrations/XXXX_backfill_carrier_alias.py` | Add | `RunPython` to populate `carrier_alias` from existing values |
| `modules/core/karrio/server/providers/migrations/XXXX_carrier_alias_unique.py` | Add | `AlterField` to add unique constraint after backfill |
| `modules/manager/karrio/server/manager/migrations/XXXX_rename_carrier_ids_to_connection_ids.py` | Add | `RenameField` on Shipment model (`carrier_ids` → `connection_ids`) |

---

#### B.21 Summary Statistics

| Layer | Files | Total References | Change Type |
|-------|-------|-----------------|-------------|
| SDK models (`modules/sdk/`) | 2 | 32 fields across 15 classes | Add new fields |
| Core models (`modules/core/providers/models/`) | 2 | 25+ field/property refs | RenameField + add alias |
| Core datatypes (`modules/core/core/datatypes.py`) | 1 | 16 dataclass attributes | Add new fields |
| Core serializers (`modules/core/`) | 2 | 35+ serializer fields | Rename + add + fallback |
| Core filters (`modules/core/core/filters.py`) | 1 | 12 filter fields + OpenAPI params | Add new filter + dual accept |
| Core gateway + utils | 2 | 15+ function params/refs | Rename + fallback |
| Manager models (`modules/manager/models.py`) | 1 | 12 properties (5 models × 2-3) | Add new properties |
| Manager serializers | 5 | 40+ references | Rename + fallback |
| Manager views | 2 | 15+ view params/filters | Rename + fallback |
| GraphQL types | 1 | 15 type fields/resolvers | Add new fields |
| GraphQL inputs | 1 | 10 input fields | Add new fields + dual accept |
| GraphQL mutations | 1 | 2 mutation refs | Update |
| Pricing module | 3 | 50+ (mostly tests) | Update refs + test data |
| Documents module | 2 | 100+ (mostly fixtures) | Update fixture data |
| EE admin module | 1 | 2 filter refs | Update |
| EE automation module | 5 | 15+ schema/engine refs | Rename + fallback |
| EE dtdc connector | 9 | 20+ provider/test refs | Add new fields |
| Carrier connectors (28) | ~333 | ~1000+ (pattern-based) | Add new fields to response construction |
| Frontend types | 8 | 365 | Regenerate (auto) |
| Frontend hooks | 11 | 40+ | Update field references |
| Frontend UI components | 27+ | 200+ | Update field references |
| Frontend core modules | 20 | 60+ | Update field references |
| Frontend other | 7 | 15+ | Update field references |
| Migrations (new) | 5 | — | New files |
| **TOTAL** | **~460 files** | **~2,100+ references** | — |

### Appendix C: carrier_alias Generation Logic

```python
import uuid
import karrio.lib as lib

def generate_carrier_alias(carrier_code: str) -> str:
    """Generate a unique carrier alias slug.

    Pattern: {carrier_code}_{8-char-hex}
    Examples: "fedex_a1b2c3d4", "dhl_express_e5f6g7h8"
    """
    short_hash = uuid.uuid4().hex[:8]
    return f"{lib.to_slug(carrier_code)}_{short_hash}"
```

### Appendix D: Pre-existing Bugs to Fix During Migration

The audit discovered 7 connector files with an incorrect assignment `carrier_name=settings.carrier_id` (should be `carrier_name=settings.carrier_name`). These should be fixed as part of the migration:

| File | Line | Current (Bug) | Fix |
|------|------|--------------|-----|
| `modules/connectors/ups/karrio/providers/ups/document.py` | 41 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |
| `modules/connectors/usps/karrio/providers/usps/manifest.py` | 40 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |
| `modules/connectors/fedex/karrio/providers/fedex/document.py` | 30 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |
| `modules/connectors/australiapost/karrio/providers/australiapost/manifest.py` | 36 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |
| `modules/connectors/usps_international/karrio/providers/usps_international/manifest.py` | 40 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |
| `modules/connectors/canadapost/karrio/providers/canadapost/manifest.py` | 34 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |
| `modules/connectors/seko/karrio/providers/seko/manifest.py` | 44 | `carrier_name=settings.carrier_id` | `carrier_name=settings.carrier_name` |

**Impact**: These bugs cause the user-defined connection name (e.g., `"my_fedex_account"`) to be stored where the carrier type code (e.g., `"fedex"`) should be, in manifest and document upload response objects. This can cause incorrect carrier identification in downstream processing.

**Fix timing**: Fix these bugs in the same PR as Phase 1 (SDK model changes), before adding the new `carrier_code` and `connection_name` fields to connector response construction.
