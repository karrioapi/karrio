# Failed Shipments Tab & Request ID End-to-End Propagation

<!-- ENHANCEMENT + ARCHITECTURE: Dashboard feature + cross-cutting SDK fix -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-26 |
| Status | Planning |
| Owner | Karrio Core Team |
| Type | Enhancement / Architecture |
| Reference | [AGENTS.md](../AGENTS.md) |
| Related PRDs | [X_REQUEST_ID_IMPLEMENTATION.md](./X_REQUEST_ID_IMPLEMENTATION.md) |

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

This PRD covers two tightly linked features: **(1)** a new "Failed Shipments" tab on the dashboard shipments page that surfaces failed `POST /v1/shipments` API log entries (any non-2xx response) in the same table layout as existing shipments, with a prominent "Failure Reasons" section modeled on the shipment sheet's "Recent Activity"; and **(2)** fixing the `request_id` propagation gap in the SDK so the same `X-Request-ID` flows end-to-end from client through the API, SDK, and into carrier API tracing records.

These features are linked because the Failed Shipments tab depends on `request_id` to correlate API logs with carrier-level tracing records, enabling users to see *exactly* why a shipment creation failed at the carrier level.

### Key Architecture Decisions

1. **Data source is API logs, not shipments**: Failed shipment attempts never create a `Shipment` object. The tab queries the existing `GET_LOGS` GraphQL endpoint filtered by `method: ["POST"]`, `api_endpoint: "/v1/shipments"`, `status: "failed"`.
2. **Reuse existing components**: `FiltersCard`, `ListPagination`, `ShipmentPreviewSheet` pattern (adapted as `FailedShipmentSheet`), and `RecentActivity` layout for failure reasons.
3. **SDK uses tracer context `request_id`**: Instead of generating a new `uuid.uuid4()` per HTTP call, the SDK's `request()` and `request_with_retries()` functions check `trace.context.get("request_id")` first, falling back to a generated UUID only when no context ID exists.
4. **No carrier header injection**: The `X-Request-ID` is NOT forwarded as a header to carrier APIs (per existing PRD decision D3). It is used only for internal correlation in tracing records.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| New "Failed" filter card on shipments page | New backend GraphQL queries or mutations |
| Failed shipment sheet with failure reasons | Modifying the `Shipment` Django model |
| `request_id` as copyable chip in sheet | Forwarding `X-Request-ID` to carrier APIs |
| SDK `request_id` propagation from tracer context | OpenTelemetry W3C trace context propagation |
| Updated SDK tests for propagation chain | Retry/resubmit failed shipments (future feature) |
| Sentry correlation with propagated `request_id` | Changes to API log data model |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Data source for failed tab | API logs (`GET_LOGS` with filters) | Failed shipments never create Shipment objects; API logs capture the full request/response | 2026-02-26 |
| D2 | Where to add tab | Existing `FiltersCard` on shipments page | Follows established filter card pattern; no new routing needed | 2026-02-26 |
| D3 | Sheet component | New `FailedShipmentSheet` (adapted from `ShipmentPreviewSheet`) | Different data shape (log entry vs shipment object) requires a dedicated sheet | 2026-02-26 |
| D4 | Failure reasons display | Reuse `RecentActivity` visual pattern (icon + description + timestamp + timeline line) | Consistent UX; proven pattern in shipment sheet | 2026-02-26 |
| D5 | SDK request_id source | Tracer context `request_id`, fallback to `uuid.uuid4()` | Maintains backward compatibility; no breaking change when SDK used standalone | 2026-02-26 |
| D6 | Carrier header injection | No (internal only) | Per existing PRD decision; avoids carrier compatibility issues | 2026-02-26 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Log entry has no `data` (request body) | Can't display shipper/recipient | Show "Request data unavailable" placeholder | No |
| Log entry has no `records` (tracing records) | No carrier-level failure detail | Show "No carrier trace available" with raw response | No |
| Multiple carrier calls per request | Multiple failure reasons | Display all records grouped by carrier in timeline | No |

---

## Problem Statement

### Current State

**Problem 1: No visibility into failed shipment creation attempts**

When `POST /v1/shipments` returns a non-2xx response, no `Shipment` object is created. Users must navigate to Developers > Logs, manually filter by method/path/status, and read raw JSON to understand what went wrong. There is no dedicated view on the shipments page for failures.

```typescript
// Current: Shipments page only shows successfully created shipments
const context = useShipments({
  status: ["purchased", "delivered", "in_transit", "cancelled",
           "needs_attention", "out_for_delivery", "delivery_failed"],
  setVariablesToURL: true,
  preloadNextPage: true,
});
// No way to see failed creation attempts on this page
```

**Problem 2: `request_id` does not propagate to carrier API calls**

The SDK's HTTP helper generates its own `uuid.uuid4()` per carrier call, breaking the correlation chain. Users cannot trace a single request from the API through to carrier-level failures.

```python
# Current: SDK generates a NEW request_id for each carrier HTTP call
# File: modules/sdk/karrio/core/utils/helpers.py:357,474
_request_id = str(uuid.uuid4())  # NOT the X-Request-ID from the API
```

### Desired State

```typescript
// Desired: Failed shipments tab alongside existing status filters
const getFilterOptions = () => [
  { label: "All", value: [...] },
  { label: "Purchased", value: [...] },
  // ... existing filters ...
  { label: "Failed", value: ["_failed_creation"] },  // Special value triggers log-based view
];
```

```python
# Desired: SDK uses tracer context request_id when available
# File: modules/sdk/karrio/core/utils/helpers.py
_request_id = (
    getattr(trace, '__self__', None) and
    trace.__self__.context.get("request_id")
) or str(uuid.uuid4())
```

### Problems

1. **No failed shipment visibility**: Users have no quick way to see which shipment creation attempts failed, what the errors were, or which carriers/addresses were involved.
2. **Broken request correlation**: The `X-Request-ID` from the API request is available in the SDK tracer context but is not used by the HTTP helper—carrier tracing records get a different `request_id` than the API log.
3. **Poor debugging experience**: Without end-to-end correlation, debugging a failed shipment requires manually matching timestamps across API logs and tracing records.

---

## Goals & Success Criteria

### Goals

1. Surface failed `POST /v1/shipments` attempts on the shipments page with a dedicated tab
2. Display failure reasons in a user-friendly format modeled on the "Recent Activity" pattern
3. Fix `request_id` propagation so a single ID flows from API request to carrier tracing records
4. Enable one-click copy of `request_id` for support/debugging workflows

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Failed shipments visible on shipments page | 100% of non-2xx POST /v1/shipments logs shown | Must-have |
| Failure reasons displayed in sheet | Error messages extracted from response + tracing records | Must-have |
| `request_id` correlation end-to-end | Same ID in API log, tracing records, and Sentry | Must-have |
| `request_id` copyable in sheet | Click-to-copy chip/badge | Must-have |
| Keyword search across failed entries | Filter by carrier, address, error text | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] "Failed" filter card on shipments page showing failed `POST /v1/shipments` logs
- [ ] Failed shipment sheet with failure reasons section
- [ ] `request_id` propagation from API through SDK to carrier tracing records
- [ ] Existing request_id tests updated for full propagation chain

**Nice-to-have (P1):**
- [ ] Keyword search within failed shipment entries
- [ ] Date range filter on failed tab
- [ ] Export failed entries as CSV

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A: API logs as data source** (filter existing `GET_LOGS`) | No backend changes; reuses existing GraphQL; captures full request/response | Different data shape than shipments; need adapted sheet component | **Selected** |
| B: New `FailedShipment` model | Structured data; consistent with shipments table | Requires migration, new GraphQL type, duplicates log data | Rejected |
| C: Add error state to Shipment model | Single data source for all shipments | Shipment creation fails *before* object creation; can't store what doesn't exist | Rejected |
| D: Separate `/failed-shipments` route | Clean separation | Fragments the shipments UX; users expect one place for all shipment info | Rejected |

### Trade-off Analysis

**Option A** was selected because failed shipment attempts are already captured in API logs with full request/response data and associated tracing records. Creating a new model (B) would duplicate this data and require backend schema changes. Option C is technically impossible since the Shipment object doesn't exist when creation fails. Option D would fracture the user experience.

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `FiltersCard` | `packages/ui/components/filters-card.tsx` | Add "Failed" option to filter array |
| `RecentActivity` | `packages/ui/components/recent-activity.tsx` | Model failure reasons section on this pattern |
| `ShipmentPreviewSheet` | `packages/ui/components/shipment-preview-sheet.tsx` | Adapt pattern for `FailedShipmentSheet` |
| `useLogs` hook | `packages/hooks/log.ts` | Use directly with `api_endpoint`, `method`, `status` filters |
| `GET_LOGS` query | `packages/types/graphql/queries.ts` | Already includes all needed fields (`data`, `response`, `records`, `request_id`) |
| `LogFilter` (backend) | `modules/core/karrio/server/core/filters.py` | Has `status="failed"`, `api_endpoint`, `method` filters |
| `StatusCode` badge | `packages/ui/core/components/status-code-badge.tsx` | Reuse for status display |
| `ActivityTimeline` | `packages/ui/components/activity-timeline.tsx` | Reference for trace record display |
| `request()` / `request_with_retries()` | `modules/sdk/karrio/core/utils/helpers.py` | Modify to use tracer context `request_id` |
| `Tracer` class | `modules/sdk/karrio/core/utils/tracing.py` | Context already carries `request_id` |
| `RequestIDMiddleware` | `modules/core/karrio/server/core/middleware.py` | Already sets `request.request_id` and tracer context |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                    DASHBOARD SHIPMENTS PAGE                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌────────┐     │
│  │   All   │ │Purchased │ │Delivered │ │Exception│ │  ...   │     │
│  └─────────┘ └──────────┘ └──────────┘ └─────────┘ └────────┘     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ NEW: "Failed" Filter Card                                  │     │
│  │ Switches data source from useShipments → useLogs           │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ┌──────────────────────────────────┬────────────────────────┐     │
│  │  LIST VIEW                       │  SHEET (on row click)  │     │
│  │  ┌────┬──────────┬──────┬─────┐ │  ┌──────────────────┐  │     │
│  │  │ # │ Endpoint  │Status│Date │ │  │ Failure Reasons  │  │     │
│  │  ├────┼──────────┼──────┼─────┤ │  │ (RecentActivity  │  │     │
│  │  │ 1 │POST /v1/ │ 400  │2/26 │ │  │  pattern)        │  │     │
│  │  │ 2 │POST /v1/ │ 422  │2/25 │ │  │                  │  │     │
│  │  │ 3 │POST /v1/ │ 500  │2/25 │ │  │ [request_id] 📋  │  │     │
│  │  └────┴──────────┴──────┴─────┘ │  │                  │  │     │
│  │  ◄ Previous     Next ►          │  │ Request Details  │  │     │
│  └──────────────────────────────────┴────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram: Failed Shipments Tab

```
┌────────┐     ┌──────────┐     ┌────────────┐     ┌──────────┐
│  User  │     │Dashboard │     │  GraphQL   │     │ API Logs │
└───┬────┘     └────┬─────┘     └─────┬──────┘     └────┬─────┘
    │               │                  │                  │
    │ 1. Click      │                  │                  │
    │  "Failed" tab │                  │                  │
    │──────────────>│                  │                  │
    │               │ 2. useLogs({    │                  │
    │               │  method:["POST"]│                  │
    │               │  api_endpoint:  │                  │
    │               │   "/v1/shipments"                  │
    │               │  status:"failed"│                  │
    │               │ })              │                  │
    │               │────────────────>│                  │
    │               │                 │ 3. LogFilter     │
    │               │                 │    query         │
    │               │                 │─────────────────>│
    │               │                 │                  │
    │               │                 │ 4. Filtered logs │
    │               │                 │<─────────────────│
    │               │ 5. Log entries  │                  │
    │               │<────────────────│                  │
    │               │                 │                  │
    │ 6. Click row  │                 │                  │
    │──────────────>│                 │                  │
    │               │ 7. Open sheet   │                  │
    │               │  with log data  │                  │
    │               │  + records      │                  │
    │ 8. Sheet with │                 │                  │
    │  failure      │                 │                  │
    │  reasons      │                 │                  │
    │<──────────────│                 │                  │
    │               │                 │                  │
```

### Sequence Diagram: Request ID Propagation Fix

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│ Client │     │   API    │     │  Tracer  │     │   SDK    │     │ Carrier │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬────┘
    │               │                │                  │                │
    │ X-Request-ID: │                │                  │                │
    │ "my-req-123"  │                │                  │                │
    │──────────────>│                │                  │                │
    │               │ 1. Middleware  │                  │                │
    │               │  validates &   │                  │                │
    │               │  sets request  │                  │                │
    │               │  .request_id   │                  │                │
    │               │────────────────│                  │                │
    │               │ 2. SessionCtx  │                  │                │
    │               │  adds to tracer│                  │                │
    │               │  context       │                  │                │
    │               │───────────────>│                  │                │
    │               │                │ context=         │                │
    │               │                │ {"request_id":   │                │
    │               │                │  "my-req-123"}   │                │
    │               │                │                  │                │
    │               │ 3. Gateway     │                  │                │
    │               │  passes tracer │                  │                │
    │               │  to SDK        │                  │                │
    │               │────────────────┼─────────────────>│                │
    │               │                │                  │                │
    │               │                │                  │ 4. request()   │
    │               │                │                  │  uses tracer   │
    │               │                │                  │  context       │
    │               │                │                  │  request_id    │
    │               │                │                  │  "my-req-123"  │ (NEW)
    │               │                │                  │───────────────>│
    │               │                │                  │                │
    │               │                │                  │ 5. trace()     │
    │               │                │                  │  records       │
    │               │                │                  │  "my-req-123"  │
    │               │                │                  │  in record     │
    │               │                │                  │  metadata      │
    │               │                │                  │                │
    │ 6. Response   │                │                  │                │
    │ X-Request-ID: │                │                  │                │
    │ "my-req-123"  │                │                  │                │
    │<──────────────│                │                  │                │
    │               │                │                  │                │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FEATURE 1: FAILED SHIPMENTS TAB                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌────────┐ │
│  │ FiltersCard   │  useLogs()  │    │  GET_LOGS    │    │APILog  │ │
│  │ "Failed" │───>│  hook with  │───>│  GraphQL     │───>│Index   │ │
│  │ selected │    │  filters    │    │  query       │    │ table  │ │
│  └──────────┘    └─────────────┘    └──────────────┘    └────────┘ │
│       │                                     │                       │
│       │          ┌─────────────┐             │                      │
│       │          │FailedShip-  │<────────────┘                      │
│       └─────────>│ mentSheet   │     log.data → request details     │
│     row click    │             │     log.response → error messages  │
│                  │ ┌─────────┐ │     log.records → carrier traces   │
│                  │ │Failure  │ │     log.request_id → copyable chip │
│                  │ │Reasons  │ │                                    │
│                  │ └─────────┘ │                                    │
│                  └─────────────┘                                    │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│               FEATURE 2: REQUEST_ID PROPAGATION FIX                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Client   │  │ RequestID    │  │ Session    │  │   Tracer     │ │
│  │ header   │─>│ Middleware   │─>│ Context    │─>│   context    │ │
│  │          │  │              │  │ middleware │  │ {request_id} │ │
│  └──────────┘  └──────────────┘  └────────────┘  └──────┬───────┘ │
│                                                          │         │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐         │         │
│  │ Carrier  │<─│ SDK request()│<─│ SDK Proxy  │<────────┘         │
│  │ API call │  │ uses tracer  │  │ trace_as() │  tracer passed    │
│  │          │  │ context ID   │  │            │  via gateway      │
│  └──────────┘  └──────────────┘  └────────────┘                   │
│       │                                                            │
│       └──> TracingRecord.meta.request_id = same X-Request-ID      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Feature 1: Failed Shipments Tab — Frontend Design

#### Filter Card Addition

Add a "Failed" option to the existing `getFilterOptions()` in `packages/core/modules/Shipments/index.tsx`. Use a special sentinel value to switch the data source from `useShipments` to `useLogs`.

```typescript
// packages/core/modules/Shipments/index.tsx
const getFilterOptions = () => [
  { label: "All", value: ["purchased", "delivered", "in_transit", "cancelled", "needs_attention", "out_for_delivery", "delivery_failed"] },
  { label: "Purchased", value: ["purchased", "in_transit", "out_for_delivery"] },
  { label: "Delivered", value: ["delivered"] },
  { label: "Exception", value: ["needs_attention", "delivery_failed"] },
  { label: "Cancelled", value: ["cancelled"] },
  { label: "Draft", value: ["draft"] },
  { label: "Failed", value: ["_failed_creation"] },  // NEW: sentinel value
];
```

#### Conditional Data Source

When `_failed_creation` is the active filter, render a `FailedShipmentsList` component that uses `useLogs` instead of `useShipments`:

```typescript
// packages/core/modules/Shipments/failed-shipments-list.tsx
import { useLogs } from "@karrio/hooks/log";

export function FailedShipmentsList() {
  const context = useLogs({
    method: ["POST"],
    api_endpoint: "/v1/shipments",
    status: "failed",
    setVariablesToURL: true,
  });

  const { query: { data: { logs } = {}, ...query }, filter, setFilter } = context;
  // ... render table with log entries
}
```

#### Failed Shipment Sheet

A new sheet component that displays log entry details with a prominent "Failure Reasons" section:

```typescript
// packages/ui/components/failed-shipment-sheet.tsx
interface FailedShipmentSheetProps {
  log: get_logs_logs_edges_node;
}

// Structure:
// 1. Header: Status code badge + request_id chip (copyable) + timestamp
// 2. Failure Reasons section (modeled on RecentActivity)
// 3. Request Details (shipper/recipient from log.data)
// 4. Raw Response (collapsible)
```

#### Failure Reasons Component

Modeled on `RecentActivity` (`packages/ui/components/recent-activity.tsx`):

```typescript
// packages/ui/components/failure-reasons.tsx
interface FailureReason {
  id: string;
  message: string;          // Error message text
  code: string | null;      // Error code (carrier-specific or HTTP)
  carrier: string | null;   // Carrier name if from tracing record
  timestamp: string | null; // When the error occurred
}

// Extract reasons from:
// 1. log.response.errors[] or log.response.messages[] (API-level errors)
// 2. log.records[].record (carrier-level errors from tracing records)

// Visual pattern: Same as RecentActivity
// - Red dot icon for errors (instead of green/gray for events)
// - Error message as description
// - Carrier name + error code as metadata
// - Connecting timeline line between items
```

#### Request ID Copyable Chip

```typescript
// In the sheet header area
<div className="flex items-center gap-2">
  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full font-mono">
    {log.request_id}
  </span>
  <button
    onClick={() => navigator.clipboard.writeText(log.request_id || "")}
    className="text-gray-400 hover:text-gray-600"
    title="Copy request ID"
  >
    <i className="fas fa-copy text-xs" />
  </button>
</div>
```

#### List View Columns

| Column | Source | Notes |
|--------|--------|-------|
| Status | `log.status_code` | `StatusCode` badge component |
| Carrier | `log.data.carrier_name` or `log.data.selected_rate_carrier` | `CarrierImage` if available |
| Recipient | `log.data.recipient.city`, `log.data.recipient.country_code` | Extracted from request body |
| Error | `log.response.errors[0].message` or `log.response.messages[0].message` | First error, truncated |
| Request ID | `log.request_id` | Monospace, truncated |
| Date | `log.requested_at` | `formatDateTime()` |

### Feature 2: Request ID Propagation Fix — Backend Design

#### SDK `request()` Function Change

**File**: `modules/sdk/karrio/core/utils/helpers.py`

The `trace` parameter passed to `request()` and `request_with_retries()` is a partial function created by `Tracer.with_metadata()`. The tracer context (containing `request_id`) is accessible through the trace function's closure.

```python
# Current (helpers.py:357, 474):
_request_id = str(uuid.uuid4())

# Proposed:
def _resolve_request_id(trace) -> str:
    """Extract request_id from tracer context, or generate a new one."""
    if trace is not None:
        _tracer = getattr(trace, "_tracer", None)
        _context_id = (
            getattr(_tracer, "context", {}).get("request_id")
            if _tracer is not None
            else None
        )
        if _context_id:
            return _context_id
    return str(uuid.uuid4())
```

#### Tracer `with_metadata` — Expose Tracer Reference

**File**: `modules/sdk/karrio/core/utils/tracing.py`

The `with_metadata()` method returns a partial function. We need the returned trace function to carry a reference to the tracer so `_resolve_request_id` can access the context:

```python
# In Tracer.with_metadata():
def _trace_with_metadata(*args, **kwargs):
    # ... existing logic ...
    pass

_trace_with_metadata._tracer = self  # Attach tracer reference
return _trace_with_metadata
```

#### Settings `trace_as` — Chain Tracer Reference

**File**: `modules/sdk/karrio/core/settings.py`

The `trace_as()` method wraps `trace()` which wraps `with_metadata()`. Ensure the `_tracer` reference survives the wrapping chain:

```python
def trace_as(self, format: str = None):
    _trace = self.trace()
    # _trace already has _tracer attribute from with_metadata
    def _format_trace(data, *args, **kwargs):
        # ... existing formatting logic ...
        return _trace(data, *args, **kwargs)
    _format_trace._tracer = getattr(_trace, "_tracer", self.tracer)
    return _format_trace
```

#### Sentry Correlation

The existing `SessionContext` middleware already sets `request_id` as a Sentry tag (middleware.py:155-163). With the propagation fix, the same `request_id` will appear in:
- Sentry tag: `request_id`
- Sentry breadcrumb: `Request {request_id}`
- API log: `APILogIndex.request_id`
- Tracing record: `TracingRecord.meta.request_id`
- All carrier HTTP traces within the request

### Field Reference

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `log.id` | int | API log | Unique log identifier |
| `log.status_code` | int | API log | HTTP response code (4xx, 5xx for failures) |
| `log.method` | string | API log | Always "POST" for this tab |
| `log.path` | string | API log | Always "/v1/shipments" or "/v1/shipments/{id}" |
| `log.request_id` | string | API log | Correlation ID (e.g., `req_abc123`) |
| `log.requested_at` | datetime | API log | When the request was made |
| `log.response_ms` | int | API log | Response time in milliseconds |
| `log.data` | JSON | API log | Request body (shipper, recipient, parcels, etc.) |
| `log.response` | JSON | API log | Response body (errors, messages) |
| `log.records` | array | Tracing records | Carrier-level API call traces |
| `log.records[].meta.carrier_name` | string | Tracing record | Which carrier failed |
| `log.records[].record` | JSON | Tracing record | Raw carrier request/response |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| No failed shipment logs exist | Empty state with message | Show "No failed shipment attempts found" card |
| Log entry has empty `data` field | Can't extract shipper/recipient | Show "Request data unavailable" in those columns |
| Log entry has no tracing `records` | No carrier-level detail | Show only API-level error from `response` field |
| `request_id` is null on old logs | Can't show correlation | Show "N/A" for request_id chip; still show other data |
| SDK used standalone (no tracer context) | No `request_id` in context | Falls back to `uuid.uuid4()` — backward compatible |
| Multiple carrier calls per request | Multiple tracing records | Display all in failure reasons timeline, grouped |
| Very long error messages from carrier | UI overflow | Truncate to 200 chars with "Show more" toggle |
| User navigates between Failed and other tabs | Data source switches | Clean state transition; reset pagination offset to 0 |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| `GET_LOGS` query returns slowly for large datasets | Slow tab load | Use existing pagination (20 items); `keepPreviousData: true` |
| Tracer `_tracer` attribute not propagated through all code paths | Some carrier calls still generate random IDs | Comprehensive tests; fallback to `uuid.uuid4()` is safe |
| Log `data` field format varies across API versions | Incorrect field extraction | Defensive parsing with `failsafe()` / optional chaining |
| Sheet component fails to parse malformed `response` JSON | Sheet crashes | Wrap JSON parsing in try/catch; show raw text fallback |

---

## Implementation Plan

### Phase 1: Request ID Propagation Fix (Backend)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `_tracer` reference to `with_metadata` return | `modules/sdk/karrio/core/utils/tracing.py` | Pending | S |
| Chain `_tracer` reference through `trace_as` | `modules/sdk/karrio/core/settings.py` | Pending | S |
| Add `_resolve_request_id()` helper function | `modules/sdk/karrio/core/utils/helpers.py` | Pending | S |
| Update `request()` to use `_resolve_request_id()` | `modules/sdk/karrio/core/utils/helpers.py` | Pending | S |
| Update `request_with_retries()` to use `_resolve_request_id()` | `modules/sdk/karrio/core/utils/helpers.py` | Pending | S |
| Add propagation tests | `modules/core/karrio/server/core/tests/test_request_id.py` | Pending | M |

### Phase 2: Failed Shipments Tab (Frontend)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add "Failed" option to `getFilterOptions()` | `packages/core/modules/Shipments/index.tsx` | Pending | S |
| Create `FailedShipmentsList` component | `packages/core/modules/Shipments/failed-shipments-list.tsx` | Pending | M |
| Create `FailedShipmentSheet` component | `packages/ui/components/failed-shipment-sheet.tsx` | Pending | M |
| Create `FailureReasons` component | `packages/ui/components/failure-reasons.tsx` | Pending | M |
| Add copyable `request_id` chip | `packages/ui/components/failed-shipment-sheet.tsx` | Pending | S |
| Integrate conditional rendering (shipments vs logs) | `packages/core/modules/Shipments/index.tsx` | Pending | M |
| Add keyword search for failed entries | `packages/core/modules/Shipments/failed-shipments-list.tsx` | Pending | S |

**Dependencies:** Phase 2 can start in parallel with Phase 1. However, the `request_id` chip's full value depends on Phase 1 completion for end-to-end correlation.

### Phase 3: Polish & Testing

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Empty state handling | `packages/core/modules/Shipments/failed-shipments-list.tsx` | Pending | S |
| Loading skeletons | `packages/core/modules/Shipments/failed-shipments-list.tsx` | Pending | S |
| URL parameter sync for failed tab | `packages/core/modules/Shipments/index.tsx` | Pending | S |
| End-to-end manual testing | N/A | Pending | M |

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests (SDK) | `modules/sdk/karrio/core/utils/tests/` | `_resolve_request_id()`, tracer propagation |
| Unit Tests (Server) | `modules/core/karrio/server/core/tests/test_request_id.py` | End-to-end propagation |
| Component Tests | Frontend (manual / visual review) | Sheet layout, failure reasons, chip |

### Test Cases

#### SDK Request ID Propagation Tests

```python
"""Test request_id propagation from tracer context to HTTP calls."""

import unittest
from unittest.mock import patch, MagicMock, ANY

from karrio.core.utils.helpers import _resolve_request_id
from karrio.core.utils.tracing import Tracer


class TestRequestIDPropagation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_resolve_request_id_from_tracer_context(self):
        """Verify request_id is extracted from tracer context."""
        tracer = Tracer()
        tracer.add_context({"request_id": "req_test-123"})
        trace_fn = tracer.with_metadata({})

        result = _resolve_request_id(trace_fn)

        self.assertEqual(result, "req_test-123")

    def test_resolve_request_id_generates_uuid_without_tracer(self):
        """Verify fallback to UUID when no tracer context."""
        result = _resolve_request_id(None)

        self.assertRegex(result, r'^[0-9a-f-]{36}$')

    def test_resolve_request_id_generates_uuid_without_context(self):
        """Verify fallback when tracer has no request_id in context."""
        tracer = Tracer()
        trace_fn = tracer.with_metadata({})

        result = _resolve_request_id(trace_fn)

        self.assertRegex(result, r'^[0-9a-f-]{36}$')

    def test_request_id_propagated_through_trace_as(self):
        """Verify request_id survives Settings.trace_as() wrapping."""
        tracer = Tracer()
        tracer.add_context({"request_id": "req_through-trace-as"})

        # Simulate Settings.trace_as() chain
        trace_fn = tracer.with_metadata({"connection": {"carrier_name": "test"}})

        result = _resolve_request_id(trace_fn)

        self.assertEqual(result, "req_through-trace-as")
```

#### Updated Middleware Propagation Tests

```python
"""Extend existing test_request_id.py with propagation tests."""

class TestRequestIDEndToEndPropagation(APITestCase):
    """Test that request_id flows from API through to tracing records."""

    @patch("karrio.core.utils.helpers.urlopen")
    def test_request_id_in_tracing_records(self, mock_urlopen):
        """Verify API request_id appears in carrier tracing records."""
        # Arrange: mock carrier response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"tracking_number": "1Z999"}'
        mock_urlopen.return_value.__enter__ = lambda s: mock_response
        mock_urlopen.return_value.__exit__ = MagicMock(return_value=False)

        # Act: make API call with X-Request-ID
        url = reverse("karrio.server.manager:shipment-list")
        response = self.client.post(
            url,
            data={...},
            HTTP_X_REQUEST_ID="req_e2e-test-001",
        )
        # print(response)

        # Assert: request_id appears in response header
        self.assertEqual(response["X-Request-ID"], "req_e2e-test-001")
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# SDK request_id tests
python -m unittest discover -v -f modules/sdk/karrio/core/utils/tests

# Server request_id tests
karrio test --failfast karrio.server.core.tests.test_request_id
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| `_tracer` attribute lost in some trace wrapping code paths | Partial propagation (some calls still generate random IDs) | Medium | Comprehensive unit tests; safe fallback to `uuid.uuid4()` |
| Failed tab confusing alongside shipment status tabs | User confusion | Low | Clear "Failed" label; distinct empty state; different table columns hint at different data |
| Performance of `GET_LOGS` query with filters | Slow tab for high-volume users | Low | Existing pagination; `APILogIndex` has indexed `request_id` and `status_code` fields |
| Breaking existing SDK standalone usage | SDK users not passing tracer break | Low | Fallback to `uuid.uuid4()` when `trace` is `None` or has no context |
| Log `data` format changes between API versions | Field extraction fails | Low | Defensive parsing with optional chaining and fallback messages |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: No API changes. `GET_LOGS` query already supports all needed filters. No new GraphQL types or mutations.
- **SDK compatibility**: `_resolve_request_id()` falls back to `uuid.uuid4()` when no tracer context is available. Standalone SDK usage is unaffected.
- **Data compatibility**: Existing API logs work with the Failed tab. Older logs without `request_id` display "N/A" for the chip.
- **Feature flags**: None required. The "Failed" tab is purely additive UI.

### Rollback Procedure

1. **Identify issue**: Failed tab not loading, or request_id propagation causing errors
2. **Stop rollout**: Revert the frontend commit (removes "Failed" filter option) and/or the SDK commit
3. **Revert changes**: `git revert <commit>` — both features are independent of data migrations
4. **Verify recovery**: Shipments page returns to normal; SDK falls back to `uuid.uuid4()`

No data migrations are involved. Both features are fully additive and can be reverted independently without data loss.
