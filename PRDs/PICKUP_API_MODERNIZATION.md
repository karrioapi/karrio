# Pickup API Modernization: Carrier-Agnostic Endpoint & `options.connection_id`

<!-- REFACTORING + ENHANCEMENT -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-31 |
| Status | Planning |
| Owner | Karrio Core Team |
| Type | Refactoring / Enhancement |
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
12. [Appendices](#appendices)

---

## Executive Summary

This PRD proposes modernizing the Pickup API to align with the carrier-agnostic pattern already established by the Shipments API. The current `POST /v1/pickups/{carrier_name}/schedule` endpoint embeds the carrier identifier in the URL path, which is inconsistent with the rest of the API surface. This change introduces a new `POST /v1/pickups` endpoint where the carrier is identified via a top-level `carrier_code` field and an optional `options.connection_id` for precise carrier connection targeting. The legacy endpoint is deprecated but preserved for backward compatibility.

### Key Architecture Decisions

1. **New `POST /v1/pickups` endpoint**: Replaces `POST /v1/pickups/{carrier_name}/schedule` with a carrier-agnostic URL, consistent with `POST /v1/shipments`
2. **Top-level `carrier_code` field**: Moves carrier identification from the URL path into the request body as a required field
3. **`options.connection_id` for connection targeting**: Allows specifying a specific carrier connection UUID when multiple connections exist for the same carrier, reusing the existing `Connections.first()` resolution pattern
4. **Deprecate, don't remove**: The legacy `POST /v1/pickups/{carrier_name}/schedule` endpoint is preserved with a deprecation header, giving consumers a migration window

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| New `POST /v1/pickups` endpoint | Multi-carrier pickup rate comparison |
| Top-level `carrier_code` request field | Changes to pickup update/cancel endpoints |
| `options.connection_id` for connection targeting | Changes to the SDK/core pickup interface |
| Deprecation of `POST /v1/pickups/{carrier_name}/schedule` | Removal of the legacy endpoint |
| Frontend dashboard updates (hook, dialog, types) | Pickup recurrence logic changes |
| REST API client regeneration | GraphQL schema changes (reads-only, unaffected) |
| OpenAPI spec updates | Changes to carrier connector pickup implementations |

---

## Open Questions & Decisions

### Pending Questions

| # | Question | Context | Options | Status |
|---|----------|---------|---------|--------|
| Q1 | Should `carrier_code` be strictly required on the new endpoint, or can it be inferred from `options.connection_id` alone? | If `connection_id` uniquely identifies a connection, `carrier_code` is redundant but useful for validation | A) Both required, B) `carrier_code` optional if `connection_id` provided, C) `carrier_code` always required for explicitness | :hourglass: Pending |
| Q2 | What deprecation timeline for the legacy endpoint? | Affects API versioning and client migration | A) Immediate deprecation + removal in next major, B) Deprecation warning for 2 releases then remove, C) Keep indefinitely as alias | :hourglass: Pending |
| Q3 | Should the update endpoint (`POST /v1/pickups/{pk}`) also accept `carrier_code` for future consistency? | Currently uses carrier snapshot from the existing pickup | A) No change needed (carrier already resolved from snapshot), B) Accept but ignore (forward-compat) | :hourglass: Pending |

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | URL pattern for new endpoint | `POST /v1/pickups` | Matches `POST /v1/shipments` pattern exactly | 2026-01-31 |
| D2 | Carrier identification field name | `carrier_code` (top-level) | Consistent with `carrier_code` in carrier snapshots and existing model properties | 2026-01-31 |
| D3 | Connection targeting field location | `options.connection_id` | Options dict is already the established pattern for carrier-specific overrides; `carrier_connection_id` is already used in rate meta | 2026-01-31 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| User provides `connection_id` that doesn't match `carrier_code` | Ambiguous carrier selection | Validate that resolved connection's `carrier_code` matches the provided `carrier_code`; return 400 on mismatch | No |
| User provides neither `carrier_code` nor `connection_id` | Cannot resolve carrier | Return 400 with clear error message | No |
| Multiple active connections for same `carrier_code`, no `connection_id` | Ambiguous connection | Use `Connections.first()` (existing behavior: returns first active match) | No |

---

## Problem Statement

### Current State

The pickup schedule endpoint requires the carrier name as a URL path parameter:

```python
# URL pattern (views/pickups.py:166-171)
path(
    "pickups/<str:carrier_name>/schedule",
    PickupRequest.as_view(),
    name="shipment-pickup-request",
)

# View extracts carrier_name from URL (views/pickups.py:74-86)
def post(self, request: Request, carrier_name: str):
    carrier_filter = {
        "carrier_name": carrier_name,  # <-- from URL path
    }
    pickup = (
        PickupData.map(data=request.data, context=request)
        .save(carrier_filter=carrier_filter)
        .instance
    )
```

```typescript
// Frontend constructs URL with carrier_name (hooks/pickup.ts:138-146)
const schedulePickup = useMutation(
  ({ carrierName, data }: { carrierName: string; data: any }) =>
    handleFailure(
      karrio.pickups
        .schedule({ carrierName, pickupData: data })  // carrierName goes into URL
        .then(({ data }) => data),
    ),
);

// REST client builds URL (types/rest/api.ts)
const localVarPath = `/v1/pickups/{carrier_name}/schedule`
    .replace(`{${"carrier_name"}}`, encodeURIComponent(String(carrierName)));
```

### Desired State

The new pickup endpoint follows the same carrier-agnostic pattern as shipments:

```python
# New URL pattern
path("pickups", PickupSchedule.as_view(), name="shipment-pickup-schedule")

# View reads carrier from request body
def post(self, request: Request):
    pickup = (
        PickupData.map(data=request.data, context=request)
        .save()
        .instance
    )
```

```json
// New request body
{
  "carrier_code": "canadapost",
  "pickup_date": "2025-02-01",
  "ready_time": "09:00",
  "closing_time": "17:00",
  "address": { "..." },
  "tracking_numbers": ["123456789012"],
  "options": {
    "connection_id": "conn_abc123"
  }
}
```

```typescript
// Frontend passes carrier in body, not URL
const schedulePickup = useMutation(
  (data: PickupData) =>
    handleFailure(
      karrio.pickups
        .schedule({ pickupData: data })  // carrier_code inside data
        .then(({ data }) => data),
    ),
);
```

### Problems

1. **API inconsistency**: The Shipments API (`POST /v1/shipments`) is carrier-agnostic while the Pickups API embeds `carrier_name` in the URL, forcing different patterns for the same client
2. **No connection targeting**: When a user has multiple connections for the same carrier (e.g., two FedEx accounts), there is no way to specify which connection to use for a pickup. The current implementation just uses `Connections.first()` which returns the first active match
3. **Poor client ergonomics**: REST clients must construct dynamic URLs for pickups but use static URLs for all other resources. The generated TypeScript client requires a separate `carrierName` parameter instead of a unified request body
4. **Naming inconsistency**: The URL uses `carrier_name` but the carrier snapshot and model properties use `carrier_code`. These refer to the same value but the inconsistent naming is confusing

---

## Goals & Success Criteria

### Goals

1. Provide a `POST /v1/pickups` endpoint that accepts `carrier_code` in the request body, consistent with the shipment API pattern
2. Support `options.connection_id` to allow targeting a specific carrier connection when multiple exist
3. Deprecate `POST /v1/pickups/{carrier_name}/schedule` with proper HTTP deprecation headers
4. Update the dashboard to use the new endpoint

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| New `POST /v1/pickups` endpoint functional | All existing pickup tests pass against new endpoint | Must-have |
| `options.connection_id` resolves correct connection | Unit test with multiple connections for same carrier | Must-have |
| Legacy endpoint returns `Deprecation` header | Header present on all responses | Must-have |
| Dashboard uses new endpoint | No `carrierName` in URL construction | Must-have |
| OpenAPI spec updated | New endpoint documented, legacy marked deprecated | Must-have |
| Backward compatibility | Legacy endpoint continues to work | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] `POST /v1/pickups` endpoint with `carrier_code` body field
- [ ] `options.connection_id` support in carrier resolution
- [ ] Legacy endpoint deprecated with `Deprecation` HTTP header
- [ ] Dashboard updated to use new endpoint
- [ ] REST client types regenerated
- [ ] All existing pickup tests pass

**Nice-to-have (P1):**
- [ ] Migration guide in API documentation
- [ ] API changelog entry
- [ ] Dashboard shows deprecation warning if legacy endpoint used via direct API

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A) `carrier_code` in body + `options.connection_id`** | Matches shipment pattern; clear separation of carrier type vs connection instance; backward compatible | Requires new endpoint + deprecation of old | **Selected** |
| **B) `carrier_id` in body (like shipment `carrier_ids`)** | Direct reuse of shipment pattern | `carrier_id` is the user-defined connection identifier, not the carrier type code; confusing overlap with existing `carrier_id` semantics | Rejected |
| **C) Keep URL param, add `connection_id` as query param** | Minimal change | Still inconsistent with shipments; query params for POST selection is unusual | Rejected |
| **D) Only `connection_id` in body, infer carrier** | Simplest request body | Requires extra lookup; carrier_code is useful for validation and readability; breaks if connection deleted | Rejected |

### Trade-off Analysis

**Option A** was selected because:
- It creates a 1:1 pattern match with `POST /v1/shipments` for API consistency
- `carrier_code` (e.g., `"canadapost"`, `"fedex"`) is already the established carrier identifier in snapshots, model properties, and filter parameters
- `options.connection_id` follows the existing pattern where `options` carries operational overrides (similar to how `carrier_connection_id` appears in rate meta)
- The deprecation approach preserves backward compatibility while guiding migration

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `Connections.first()` | `modules/core/karrio/server/core/gateway.py:23-231` | Reuse directly; already supports `carrier_name` and `carrier_id` filters |
| `create_carrier_snapshot()` | `modules/core/karrio/server/core/utils.py:1160-1224` | Reuse as-is; already stores `carrier_code` and `connection_id` |
| `resolve_carrier()` | `modules/core/karrio/server/core/utils.py:1227-1315` | Reuse for update/cancel (no changes needed) |
| `DEFAULT_CARRIER_FILTER` | `modules/manager/karrio/server/manager/serializers/pickup.py:23` | Reuse `dict(active=True, capability="pickup")` |
| `PickupSerializer` | `modules/manager/karrio/server/manager/serializers/pickup.py:68-153` | Extend with `carrier_code` field |
| `PickupData.create()` | `modules/manager/karrio/server/manager/serializers/pickup.py:157-245` | Modify carrier resolution to use body fields |
| `PickupRequest` view | `modules/manager/karrio/server/manager/views/pickups.py:58-88` | Reference pattern for new view |
| `ShipmentList.post()` | `modules/manager/karrio/server/manager/views/shipments.py:89-99` | Pattern to follow: body-only carrier selection |
| `PickupsApi.schedule()` | `packages/types/rest/api.ts:12251-12257` | Regenerate from OpenAPI spec |
| `usePickupMutation` | `packages/hooks/pickup.ts:120-164` | Update to remove `carrierName` from URL |
| `SchedulePickupDialog` | `packages/ui/components/schedule-pickup-dialog.tsx` | Update submission to include `carrier_code` in body |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         API LAYER                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  NEW: POST /v1/pickups                                              │
│  ┌──────────────┐     ┌──────────────────┐     ┌────────────────┐  │
│  │ PickupCreate  │────>│   PickupData     │────>│  Connections   │  │
│  │   (view)      │     │  (serializer)    │     │   .first()     │  │
│  │              │     │                  │     │                │  │
│  │ No URL params │     │ carrier_code     │     │ carrier_name=  │  │
│  │              │     │ options.          │     │   carrier_code │  │
│  │              │     │   connection_id   │     │ carrier_id=    │  │
│  │              │     │                  │     │   connection_id │  │
│  └──────────────┘     └──────────────────┘     └────────────────┘  │
│                                                        │           │
│  DEPRECATED: POST /v1/pickups/{carrier_name}/schedule   │           │
│  ┌──────────────┐     ┌──────────────────┐             │           │
│  │PickupRequest │────>│   PickupData     │─────────────┘           │
│  │   (view)     │     │  (serializer)    │                         │
│  │              │     │                  │                         │
│  │ carrier_name │     │ carrier_filter   │                         │
│  │  from URL    │     │  from URL param  │                         │
│  └──────────────┘     └──────────────────┘                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                      GATEWAY LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐     ┌──────────────────┐                      │
│  │ Pickups.schedule │────>│  karrio.Pickup   │                      │
│  │    (gateway)     │     │   .schedule()    │                      │
│  │                  │     │    (SDK)         │                      │
│  │ carrier resolved │     │                  │                      │
│  │ from serializer  │     │ carrier.gateway  │                      │
│  └─────────────────┘     └──────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────────┐     ┌───────────┐     ┌────────────┐     ┌─────────┐
│ Client │     │PickupCreate│     │PickupData │     │Connections │     │ Gateway │
└───┬────┘     └─────┬──────┘     └─────┬─────┘     └─────┬──────┘     └────┬────┘
    │                │                   │                  │                 │
    │ POST /v1/      │                   │                  │                 │
    │ pickups        │                   │                  │                 │
    │ {carrier_code, │                   │                  │                 │
    │  options: {    │                   │                  │                 │
    │   connection_  │                   │                  │                 │
    │   id}, ...}    │                   │                  │                 │
    │───────────────>│                   │                  │                 │
    │                │                   │                  │                 │
    │                │ .map(data).save() │                  │                 │
    │                │──────────────────>│                  │                 │
    │                │                   │                  │                 │
    │                │                   │ 1. Extract       │                 │
    │                │                   │    carrier_code  │                 │
    │                │                   │    + connection_ │                 │
    │                │                   │    id from opts  │                 │
    │                │                   │                  │                 │
    │                │                   │ 2. Connections   │                 │
    │                │                   │    .first(       │                 │
    │                │                   │     carrier_name,│                 │
    │                │                   │     carrier_id)  │                 │
    │                │                   │─────────────────>│                 │
    │                │                   │                  │                 │
    │                │                   │   carrier conn   │                 │
    │                │                   │<─────────────────│                 │
    │                │                   │                  │                 │
    │                │                   │ 3. Validate      │                 │
    │                │                   │    carrier_code  │                 │
    │                │                   │    matches conn  │                 │
    │                │                   │                  │                 │
    │                │                   │ 4. Pickups       │                 │
    │                │                   │    .schedule()   │                 │
    │                │                   │─────────────────────────────────>  │
    │                │                   │                  │                 │
    │                │                   │   PickupResponse │                 │
    │                │                   │<─────────────────────────────────  │
    │                │                   │                  │                 │
    │                │   pickup instance │                  │                 │
    │                │<──────────────────│                  │                 │
    │                │                   │                  │                 │
    │  201 Pickup    │                   │                  │                 │
    │<───────────────│                   │                  │                 │
    │                │                   │                  │                 │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         REQUEST FLOW                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌───────────────┐    ┌───────────────────────┐ │
│  │  Client POST  │    │  PickupData   │    │  Connections.first()  │ │
│  │  /v1/pickups  │───>│  Serializer   │───>│                       │ │
│  │               │    │               │    │  carrier_name=        │ │
│  │ {carrier_code │    │ Extract:      │    │    carrier_code       │ │
│  │  options: {   │    │  carrier_code │    │  carrier_id=          │ │
│  │   connection_ │    │  connection_  │    │    connection_id      │ │
│  │   id}}        │    │  id           │    │  active=True          │ │
│  └──────────────┘    └───────────────┘    │  capability="pickup"  │ │
│                                            └───────────┬───────────┘ │
│                                                        │             │
│                                                ┌───────▼───────┐     │
│                                                │ Carrier Conn  │     │
│                                                │  (resolved)   │     │
│                                                └───────┬───────┘     │
│                                                        │             │
│  ┌──────────────┐    ┌───────────────┐    ┌────────────▼──────────┐ │
│  │   Pickup     │<───│   Gateway     │<───│  karrio.Pickup        │ │
│  │   Model      │    │   Pickups     │    │  .schedule()          │ │
│  │   (saved)    │    │   .schedule() │    │  .from_(gateway)      │ │
│  └──────────────┘    └───────────────┘    └───────────────────────┘ │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                     CARRIER RESOLUTION DETAIL                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  carrier_code provided ──> filters by carrier_name (carrier type)    │
│  connection_id provided ──> filters by carrier_id (connection UUID)  │
│  Both provided ──> filters by both (most precise)                    │
│  Neither provided ──> 400 Bad Request                                │
│                                                                      │
│  Resolution chain (Connections.first):                               │
│  1. CarrierConnection (user-owned accounts)                          │
│  2. BrokeredConnection (user-enabled system connections)             │
│  3. SystemConnection (admin-provided connections)                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Models

**No new database models or migrations required.** The Pickup model already stores `carrier_code` in its carrier snapshot JSON field.

New/modified serializer fields:

```python
# Addition to PickupSerializer (serializers/pickup.py)
class PickupSerializer(PickupRequest):
    carrier_code = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        help_text=(
            "The carrier code for the pickup (e.g., 'canadapost', 'fedex'). "
            "Required when using POST /v1/pickups."
        ),
    )
    # ... existing fields unchanged
```

The `options` dict gains a documented (but not schema-enforced) key:

```python
# options dict structure (documented, not enforced by serializer)
{
    "connection_id": "conn_abc123",  # NEW: target a specific carrier connection
    # ... existing carrier-specific options
}
```

### Field Reference

| Field | Type | Required | Location | Description |
|-------|------|----------|----------|-------------|
| `carrier_code` | string | Yes (new endpoint) | Request body (top-level) | Carrier type code (e.g., `"canadapost"`, `"fedex"`). Maps to `carrier_name` filter in `Connections.first()` |
| `options.connection_id` | string | No | Request body (`options` dict) | UUID or ID of a specific carrier connection. Maps to `carrier_id` filter in `Connections.first()` |

### API Changes

**New Endpoint:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/pickups` | Schedule a new pickup (carrier-agnostic) |

**Deprecated Endpoint:**

| Method | Endpoint | Description | Deprecation |
|--------|----------|-------------|-------------|
| POST | `/v1/pickups/{carrier_name}/schedule` | Schedule a pickup (legacy) | `Deprecation: true` header |

**Unchanged Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/pickups` | List all pickups |
| GET | `/v1/pickups/{id}` | Retrieve a pickup |
| POST | `/v1/pickups/{id}` | Update a pickup |
| POST | `/v1/pickups/{id}/cancel` | Cancel a pickup |

**New Endpoint - Request:**

```json
{
  "carrier_code": "canadapost",
  "pickup_date": "2025-02-01",
  "ready_time": "09:00",
  "closing_time": "17:00",
  "address": {
    "address_line1": "125 Church St",
    "person_name": "John Doe",
    "company_name": "A corp.",
    "phone_number": "514 000 0000",
    "city": "Moncton",
    "country_code": "CA",
    "postal_code": "E1C4Z8",
    "state_code": "NB",
    "email": "john@a.com"
  },
  "tracking_numbers": ["123456789012"],
  "pickup_type": "one_time",
  "options": {
    "connection_id": "conn_abc123"
  },
  "metadata": {}
}
```

**New Endpoint - Response (201):**

```json
{
  "id": "pck_...",
  "object_type": "pickup",
  "carrier_name": "canadapost",
  "carrier_id": "canadapost",
  "confirmation_number": "27241",
  "pickup_date": "2025-02-01",
  "ready_time": "09:00",
  "closing_time": "17:00",
  "test_mode": true,
  "pickup_type": "one_time",
  "recurrence": null,
  "address": { "..." },
  "parcels": [ "..." ],
  "metadata": {},
  "options": {},
  "meta": { "..." }
}
```

**Legacy Endpoint - Response Headers (added):**

```
Deprecation: true
Sunset: <TBD based on Q2 decision>
Link: </v1/pickups>; rel="successor-version"
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| `carrier_code` provided, no `connection_id` | Resolve first active connection for that carrier with pickup capability | Use `Connections.first(carrier_name=carrier_code, active=True, capability="pickup")` |
| `connection_id` provided, no `carrier_code` | Depends on Q1 decision; proposed: require `carrier_code` always | Return 400 with message: "carrier_code is required" |
| Both `carrier_code` and `connection_id` provided | Resolve connection by ID and validate it matches the carrier code | Use `Connections.first(carrier_name=carrier_code, carrier_id=connection_id, ...)` |
| `connection_id` doesn't match `carrier_code` | Mismatch between specified carrier and connection | `Connections.first()` returns None with both filters; raises NotFound |
| `connection_id` points to inactive connection | Connection exists but is disabled | `Connections.first()` filters `active=True`; raises NotFound |
| `connection_id` points to connection without pickup capability | Connection exists but can't do pickups | `Connections.first()` filters `capability="pickup"`; raises NotFound |
| Legacy endpoint used after deprecation | Still works, returns deprecation headers | Add `Deprecation` and `Sunset` headers to response |
| Request body sent to legacy endpoint with `carrier_code` | Ignore body `carrier_code`, use URL param | URL param takes precedence (legacy behavior preserved) |
| `carrier_code` is empty string or whitespace | Invalid carrier code | Serializer validation rejects blank values (`allow_blank=False`) |
| New endpoint called without `carrier_code` | Missing required field | Return 400: "carrier_code is required" |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| No active connection found for carrier_code | 404 returned to user | Clear error message: "No active {carrier_code} connection with pickup capability found" |
| Connection found but carrier API rejects pickup | 424 returned with carrier error messages | Existing behavior preserved; gateway returns carrier messages |
| Legacy clients break on endpoint removal | Clients fail to schedule pickups | Deprecation-only approach; legacy endpoint preserved indefinitely until explicit removal |
| OpenAPI spec regeneration misses new endpoint | Generated clients don't have new method | Verify generated types in CI; test both endpoints |
| Race condition: connection deactivated between validation and gateway call | Gateway call fails | Existing behavior: `Pickups.schedule()` handles carrier=None gracefully |

### Security Considerations

- [ ] `connection_id` validated against user's accessible connections (existing `Connections.first()` applies access control via `context`)
- [ ] `carrier_code` validated against known carrier codes (existing `Connections.first()` filters by `carrier_name`)
- [ ] No secrets exposed in deprecation headers
- [ ] Multi-tenancy preserved: `Connections.first()` already scopes by org context

---

## Implementation Plan

### Phase 1: Backend - New Endpoint & Serializer Changes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `carrier_code` field to `PickupSerializer` | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Modify `PickupData.create()` to build carrier filter from body fields | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | M |
| Extract `connection_id` from `options` and use as `carrier_id` filter | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Add new `PickupSchedule` view class (body-only carrier selection) | `modules/manager/karrio/server/manager/views/pickups.py` | Pending | S |
| Register new URL pattern `POST /v1/pickups` (reuse existing list path with method routing or new path) | `modules/manager/karrio/server/manager/views/pickups.py` | Pending | S |
| Add deprecation headers to legacy `PickupRequest` view | `modules/manager/karrio/server/manager/views/pickups.py` | Pending | S |
| Update OpenAPI schema annotations for new endpoint | `modules/manager/karrio/server/manager/views/pickups.py` | Pending | S |

### Phase 2: Frontend - Dashboard & Client Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Regenerate REST API types from updated OpenAPI spec | `packages/types/rest/api.ts` | Pending | S |
| Update `usePickupMutation.schedulePickup` to use new endpoint | `packages/hooks/pickup.ts` | Done | S |
| Update `SchedulePickupDialog` to pass `carrier_code` in body instead of URL | `packages/ui/components/schedule-pickup-dialog.tsx` | Done | M |
| Add `connection_id` selection to `SchedulePickupDialog` when multiple connections exist for same carrier | `packages/ui/components/schedule-pickup-dialog.tsx` | Done | M |
| Update TypeScript `PickupData` type to include `carrier_code` | `packages/types/rest/` (generated) | Pending | S |

### Phase 3: Testing & Documentation

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add unit tests for new endpoint with `carrier_code` | `modules/manager/tests/` | Pending | M |
| Add unit tests for `options.connection_id` resolution | `modules/manager/tests/` | Pending | M |
| Add test for legacy endpoint deprecation headers | `modules/manager/tests/` | Pending | S |
| Add test for `carrier_code` + `connection_id` mismatch | `modules/manager/tests/` | Pending | S |
| Verify existing pickup tests still pass against legacy endpoint | `modules/manager/tests/` | Pending | S |

**Dependencies:** Phase 2 depends on Phase 1 (OpenAPI spec must be updated first). Phase 3 can partially overlap with Phase 1.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly as the original authors:
> - Use Django tests via `karrio` for server tests
> - Use `unittest` for SDK tests (NOT pytest)
> - Add `print(response)` before assertions when debugging, remove when tests pass
> - Use `self.assertDictEqual` with `mock.ANY` for dynamic fields

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests (backend) | `modules/manager/tests/test_pickups.py` | New endpoint, carrier resolution, deprecation headers |
| Integration Tests | `modules/manager/tests/test_pickups.py` | End-to-end pickup scheduling via new endpoint |
| Existing Tests | `modules/manager/tests/` | All existing pickup tests pass unchanged |

### Test Cases

#### Unit Tests - New Endpoint

```python
"""Test new POST /v1/pickups endpoint."""

import unittest
from unittest.mock import patch, ANY

class TestPickupScheduleNewEndpoint(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_schedule_pickup_with_carrier_code(self):
        """Verify scheduling via new endpoint with carrier_code in body."""
        response = self.client.post(
            "/v1/pickups",
            data={
                "carrier_code": "canadapost",
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "address": {
                    "address_line1": "125 Church St",
                    "person_name": "John Doe",
                    "city": "Moncton",
                    "country_code": "CA",
                    "postal_code": "E1C4Z8",
                    "state_code": "NB",
                },
                "parcels_count": 1,
            },
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.data,
            {
                "id": ANY,
                "object_type": "pickup",
                "carrier_name": "canadapost",
                "carrier_id": ANY,
                "confirmation_number": ANY,
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "test_mode": ANY,
                "pickup_type": "one_time",
                "recurrence": None,
                "address": ANY,
                "parcels": ANY,
                "metadata": {},
                "options": {},
                "meta": ANY,
            },
        )

    def test_schedule_pickup_with_connection_id(self):
        """Verify connection_id in options targets specific connection."""
        response = self.client.post(
            "/v1/pickups",
            data={
                "carrier_code": "canadapost",
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "address": { "..." },
                "parcels_count": 1,
                "options": {
                    "connection_id": self.second_canadapost_connection.pk,
                },
            },
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, 201)
        # Verify the correct connection was used
        self.assertEqual(
            response.data["carrier_id"],
            self.second_canadapost_connection.carrier_id,
        )

    def test_schedule_pickup_missing_carrier_code(self):
        """Verify 400 when carrier_code missing on new endpoint."""
        response = self.client.post(
            "/v1/pickups",
            data={
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "parcels_count": 1,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_schedule_pickup_connection_id_mismatch(self):
        """Verify error when connection_id doesn't match carrier_code."""
        response = self.client.post(
            "/v1/pickups",
            data={
                "carrier_code": "fedex",
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "parcels_count": 1,
                "options": {
                    "connection_id": self.canadapost_connection.pk,
                },
            },
        )
        self.assertEqual(response.status_code, 404)
```

#### Unit Tests - Legacy Deprecation

```python
class TestPickupScheduleLegacyDeprecation(unittest.TestCase):
    def test_legacy_endpoint_returns_deprecation_header(self):
        """Verify deprecated endpoint includes Deprecation header."""
        response = self.client.post(
            "/v1/pickups/canadapost/schedule",
            data={
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "parcels_count": 1,
            },
        )
        # print(response)  # Uncomment for debugging
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Deprecation"], "true")
        self.assertIn("/v1/pickups", response.get("Link", ""))

    def test_legacy_endpoint_still_functional(self):
        """Verify deprecated endpoint continues to work."""
        response = self.client.post(
            "/v1/pickups/canadapost/schedule",
            data={
                "pickup_date": "2025-02-01",
                "ready_time": "09:00",
                "closing_time": "17:00",
                "parcels_count": 1,
                "address": { "..." },
            },
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, 201)
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run pickup-specific tests
karrio test --failfast karrio.server.manager.tests.test_pickups

# Run all manager tests (includes pickups)
karrio test --failfast karrio.server.manager.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Existing API consumers break | High | Low | Legacy endpoint preserved with deprecation headers only; no removal |
| OpenAPI spec regeneration breaks generated clients | Medium | Low | Regenerate and verify TypeScript types compile; test both old and new client methods |
| `connection_id` filter causes unexpected carrier resolution | Medium | Low | Add explicit `carrier_code` validation against resolved connection; comprehensive test coverage |
| Dashboard regression | Medium | Low | Update hooks and dialog in single PR; test scheduling flow end-to-end |
| URL conflict between `POST /v1/pickups` (schedule) and `GET /v1/pickups` (list) | Low | Medium | Use method-based routing on same URL (GET=list, POST=schedule); Django handles this naturally in the same view class |
| `carrier_code` vs `carrier_name` naming confusion | Low | Medium | Document clearly that `carrier_code` in request body maps to `carrier_name` filter internally; both refer to the carrier type identifier |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: Legacy `POST /v1/pickups/{carrier_name}/schedule` continues to work with added deprecation headers. No existing API consumer is broken.
- **Data compatibility**: No database schema changes. The Pickup model and carrier snapshot format are unchanged.
- **Feature flags**: Not needed. Both endpoints coexist. The new endpoint is additive.

### Migration Path for API Consumers

**Before (legacy):**
```bash
curl -X POST https://api.karrio.io/v1/pickups/canadapost/schedule \
  -H "Authorization: Token ..." \
  -d '{
    "pickup_date": "2025-02-01",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "parcels_count": 1,
    "address": { ... }
  }'
```

**After (new):**
```bash
curl -X POST https://api.karrio.io/v1/pickups \
  -H "Authorization: Token ..." \
  -d '{
    "carrier_code": "canadapost",
    "pickup_date": "2025-02-01",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "parcels_count": 1,
    "address": { ... },
    "options": {
      "connection_id": "conn_abc123"
    }
  }'
```

**Migration steps for consumers:**
1. Move `carrier_name` from URL path to `carrier_code` in request body
2. (Optional) Add `options.connection_id` if targeting a specific connection
3. Change URL from `/v1/pickups/{carrier_name}/schedule` to `/v1/pickups`
4. Update HTTP method handling (same POST method, just different URL)

### Rollback Procedure

1. **Identify issue**: Monitor error rates on new `POST /v1/pickups` endpoint
2. **Stop rollout**: Revert frontend to use legacy endpoint (single hook change)
3. **Revert changes**: Remove new view class and URL pattern; serializer changes are backward compatible
4. **Verify recovery**: Confirm legacy endpoint works as before (it was never modified, only extended)

---

## Appendices

### Appendix A: Carrier Resolution Matrix

| `carrier_code` | `options.connection_id` | `Connections.first()` Filters | Result |
|-----------------|--------------------------|-------------------------------|--------|
| `"canadapost"` | (not provided) | `carrier_name="canadapost", active=True, capability="pickup"` | First active Canada Post connection with pickup |
| `"canadapost"` | `"conn_abc123"` | `carrier_name="canadapost", carrier_id="conn_abc123", active=True, capability="pickup"` | Specific connection if it matches |
| (not provided) | `"conn_abc123"` | Error: 400 Bad Request | `carrier_code` required |
| `"fedex"` | `"conn_abc123"` (Canada Post) | `carrier_name="fedex", carrier_id="conn_abc123", active=True, capability="pickup"` | No match found; 404 |

### Appendix B: Comparison with Shipment API Pattern

| Aspect | Shipments (current) | Pickups (current) | Pickups (proposed) |
|--------|---------------------|--------------------|--------------------|
| Create URL | `POST /v1/shipments` | `POST /v1/pickups/{carrier_name}/schedule` | `POST /v1/pickups` |
| Carrier in URL | No | Yes | No |
| Carrier in body | `carrier_ids` (list), `service` | No | `carrier_code` (string) |
| Connection targeting | Via `carrier_ids` (connection IDs) | Not supported | `options.connection_id` |
| Multi-carrier | Yes (rate shopping) | No (single carrier) | No (single carrier) |
| List URL | `GET /v1/shipments` | `GET /v1/pickups` | `GET /v1/pickups` (unchanged) |

### Appendix C: Affected File Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `modules/manager/karrio/server/manager/views/pickups.py` | Modify | Add new `PickupSchedule` view; add deprecation headers to `PickupRequest` |
| `modules/manager/karrio/server/manager/serializers/pickup.py` | Modify | Add `carrier_code` field; modify `PickupData.create()` carrier resolution |
| `modules/core/karrio/server/core/serializers.py` | Modify | Add `carrier_code` to `PickupRequest` base serializer |
| `packages/types/rest/api.ts` | Regenerate | New `schedule()` method signature without `carrierName` URL param |
| `packages/hooks/pickup.ts` | Modify | Update `schedulePickup` mutation to pass `carrier_code` in body |
| `packages/ui/components/schedule-pickup-dialog.tsx` | Modify | Include `carrier_code` in payload; add `connection_id` to options |
| `modules/manager/tests/test_pickups.py` | Add/Modify | Tests for new endpoint, connection_id, deprecation headers |
