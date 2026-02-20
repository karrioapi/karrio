# X-Request-ID: End-to-End Request Correlation

<!-- ARCHITECTURE: System design PRD for cross-cutting request correlation -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-18 |
| Status | Planning |
| Owner | Karrio Core Team |
| Type | Architecture |
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

This PRD introduces a unified `X-Request-ID` header system that generates, propagates, and stores a `req_<uuid>` correlation identifier across every layer of the Karrio platform—from the initial HTTP request through API logs, domain objects, tracing records, background tasks, and external monitoring tools (Sentry, OTEL, Datadog). When a client sends `X-Request-ID`, the server honors it; when absent, the server auto-generates one. The ID is returned in every response header and stored on all key entities, enabling operators to query any object, log, or trace by a single correlation ID.

### Key Architecture Decisions

1. **Prefixed UUID format (`req_<uuid4>`)**: Consistent with Karrio's existing prefix conventions (`shp_`, `trk_`, `trace_`). Human-readable and sortable in logs.
2. **Storage in `meta` JSON field on domain objects**: No new columns on Shipment/Tracker/Order/Pickup—leverages existing `meta` JSONField with indexed JSON key lookups.
3. **Dedicated `request_id` column on `APILogIndex`**: The primary correlation table gets a proper indexed column for fast lookups since it's the main entry point for debugging.
4. **Internal-only propagation**: X-Request-ID is NOT forwarded to carrier APIs to avoid compatibility issues. Carrier API calls retain their internal `_request_id` for request/response trace pairing.
5. **Async task linking via `parent_request_id`**: Background tasks (webhooks, batch processing, scheduled tracker updates) generate their own `req_` ID but carry a `parent_request_id` linking to the originating API call.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Django middleware for X-Request-ID generation/extraction | Forwarding X-Request-ID to carrier APIs |
| Response header injection on ALL responses | Modifying carrier connector HTTP clients |
| Storage on APILogIndex (dedicated column) | Changing existing `_request_id` in SDK helpers |
| Storage on domain objects via `meta` field | Adding new columns to Shipment/Tracker/etc. |
| TracingRecord `meta.request_id` propagation | Modifying the TracingRecord schema |
| Sentry tag + breadcrumb + transaction context | OpenTelemetry trace context W3C propagation |
| REST API filtering by `request_id` | UI/dashboard for request_id exploration |
| GraphQL filtering by `request_id` | |
| Background task request_id generation + parent linking | |
| Client-provided ID validation and sanitization | |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | ID format | Prefixed UUID (`req_<uuid4>`) | Consistent with Karrio conventions (`shp_`, `trk_`), human-readable | 2026-02-18 |
| D2 | Domain object storage | `meta` JSON field | No schema migrations needed on domain models; existing pattern | 2026-02-18 |
| D3 | Carrier API propagation | Internal only (no) | Avoids carrier compatibility issues; SDK already has internal correlation | 2026-02-18 |
| D4 | Response header | Always return on ALL responses | Industry standard (Stripe, GitHub, AWS); essential for client debugging | 2026-02-18 |
| D5 | Request scope | One per HTTP request | Simpler; clients can correlate workflows by sending same header | 2026-02-18 |
| D6 | APILogIndex storage | Dedicated indexed column | Primary lookup table; needs fast query performance | 2026-02-18 |
| D7 | ID prefix | `req_` | Short, clear, matches existing patterns | 2026-02-18 |
| D8 | API filtering | On API logs + all key objects | Full traceability from any angle | 2026-02-18 |
| D9 | Client ID validation | Accept if valid, else generate | Max 200 chars, alphanumeric + dashes + underscores; auto-generate on invalid | 2026-02-18 |
| D10 | Sentry depth | Tag + breadcrumb + transaction | Maximum correlation capability; enables search by request_id in Sentry | 2026-02-18 |
| D11 | Async tasks | Generate own ID + link to parent | `parent_request_id` in context for causal chain tracing | 2026-02-18 |
| D12 | Rollout strategy | Big bang (all at once) | Ship everything in one release | 2026-02-18 |

---

## Problem Statement

### Current State

There is no unified correlation identifier tying together an incoming API request, the API log it produces, the domain objects it creates/modifies, the carrier API calls it triggers, the tracing records captured, and the monitoring events recorded in Sentry.

```python
# Current: No correlation ID flows through the system
class SessionContext:
    def __call__(self, request):
        tracer = Tracer()                      # tracer.id = random UUID (internal, not exposed)
        request.tracer = tracer
        response = self.get_response(request)
        self._save_tracing_records(request)     # tracer_id saved in TracingRecord.meta
        return response                         # No X-Request-ID in response headers

# Current: API log has no request_id
class LoggingMixin(mixins.LoggingMixin):
    def handle_log(self):
        log = APILogIndex(entity_id=entity_id, test_mode=test_mode, ...)
        # No request_id stored
        log.save()

# Current: CORS allows x-request-id but nothing reads it
CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-request-id",    # Accepted but never processed
    ...
]
```

### Desired State

```python
# Desired: Request ID extracted/generated in middleware, flows everywhere
class RequestIDMiddleware:
    def __call__(self, request):
        request_id = self._extract_or_generate(request)
        request.request_id = request_id
        response = self.get_response(request)
        response["X-Request-ID"] = request_id   # Always in response
        return response

# Desired: API log stores request_id
class LoggingMixin(mixins.LoggingMixin):
    def handle_log(self):
        log = APILogIndex(
            entity_id=entity_id,
            request_id=self.request.request_id,  # Stored and indexed
            ...
        )

# Desired: Domain objects carry request_id in meta
shipment.meta = {
    ...existing_meta,
    "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
}

# Desired: TracingRecord carries request_id
tracing_record.meta = {
    "tracer_id": "...",
    "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
    "request_log_id": 12345,
    "object_id": "shp_abc123",
    ...
}

# Desired: Sentry event tagged with request_id
sentry_sdk.set_tag("request_id", "req_550e8400-e29b-41d4-a716-446655440000")
```

### Problems

1. **No end-to-end traceability**: When a user reports an issue with a shipment creation, support must manually cross-reference timestamps, user IDs, and entity IDs across API logs, tracing records, and Sentry events. There is no single identifier to retrieve everything related to one operation.

2. **No client-side correlation**: API responses don't include a request ID, so clients cannot correlate their request with server-side logs when reporting issues. They must provide timestamps and hope for a match.

3. **Disconnected monitoring**: Sentry captures errors but has no correlation to Karrio's own API logs or tracing records. An error in Sentry cannot be directly linked to the specific API log entry or carrier API trace that caused it.

4. **No async task lineage**: When a webhook fires or a batch job processes items, there is no way to trace back to the original API request that triggered the chain. Background tasks are orphaned from their causal request.

5. **Incomplete CORS setup**: `x-request-id` is in `CORS_ALLOW_HEADERS` but no middleware processes it, giving a false impression that request correlation is supported.

---

## Goals & Success Criteria

### Goals

1. Every API request (synchronous and async) has a `req_<uuid>` identifier, either client-provided or server-generated
2. Every API response includes `X-Request-ID` in its headers
3. All API logs, domain objects, tracing records, and monitoring events are queryable by `request_id`
4. Background tasks carry a `parent_request_id` linking to the originating API call
5. Sentry events are searchable by `request_id` tag

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| API responses with X-Request-ID header | 100% of responses | Must-have |
| API logs with request_id populated | 100% of logged requests | Must-have |
| Domain objects with request_id in meta | 100% of created/modified objects | Must-have |
| TracingRecords with request_id in meta | 100% of trace records | Must-have |
| Sentry events with request_id tag | 100% of events (when Sentry enabled) | Must-have |
| Client-provided IDs honored | 100% (when valid) | Must-have |
| Filter by request_id on API logs endpoint | Available | Must-have |
| Filter by request_id on object endpoints | Available | Nice-to-have |
| Background tasks with parent_request_id | 100% of triggered tasks | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] `RequestIDMiddleware` generates/extracts `req_` IDs
- [ ] All API responses include `X-Request-ID` header
- [ ] `APILogIndex.request_id` column populated and indexed
- [ ] `TracingRecord.meta.request_id` populated
- [ ] Sentry tag `request_id` set on all events
- [ ] REST API filter: `GET /v1/logs?request_id=req_...`
- [ ] Domain objects (`meta.request_id`) populated on create/update

**Nice-to-have (P1):**
- [ ] REST API filter on shipments, trackers, orders, pickups by `request_id`
- [ ] GraphQL filter by `request_id`
- [ ] Background task `parent_request_id` propagation
- [ ] Dedicated `GET /v1/requests/{request_id}` aggregation endpoint

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A) Prefixed UUID in middleware** (selected) | Consistent with Karrio conventions, human-readable, simple implementation | Slightly larger than raw UUID | **Selected** |
| B) Use existing `tracer.id` as the request ID | No new ID generation; already exists | Not client-settable, not prefixed, internal-only UUID, not in response headers | Rejected |
| C) W3C Trace Context (`traceparent` header) | Industry standard for distributed tracing | Complex format, overkill for Karrio's use case, requires full OTEL propagation | Rejected |
| D) Dedicated `request_id` column on every domain model | Fast SQL queries per model | Requires migrations on 6+ models, schema bloat, redundant with `meta` field | Rejected |
| E) Separate correlation table | Clean separation, supports many-to-many relationships | Adds JOINs on every query, more complex schema | Rejected |

### Trade-off Analysis

Option A was chosen because:
- **Performance**: Middleware adds negligible overhead (one UUID generation, one header read)
- **Maintenance**: Single middleware class, one migration on `APILogIndex`, no model schema changes
- **Migration**: Zero data migration for domain objects (new requests get `meta.request_id`, old ones don't)
- **Developer experience**: `req_` prefix makes IDs instantly recognizable in logs, Sentry, and API responses

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `SessionContext` middleware | `modules/core/karrio/server/core/middleware.py` | Extend to inject `request_id` into tracer context |
| `LoggingMixin.handle_log()` | `modules/core/karrio/server/core/views/api.py` | Add `request_id` to `APILogIndex` creation |
| `Tracer` class | `modules/sdk/karrio/core/utils/tracing.py` | Use `tracer.context` for `request_id` propagation |
| `set_tracing_context()` | `modules/core/karrio/server/tracing/utils.py` | Add `request_id` to tracing context calls |
| `save_tracing_records()` | `modules/core/karrio/server/tracing/utils.py` | Read `request_id` from tracer context into `TracingRecord.meta` |
| `_inject_telemetry()` | `modules/core/karrio/server/core/middleware.py` | Add `request_id` Sentry tag |
| `APILogIndex` model | `modules/core/karrio/server/core/models/third_party.py` | Add `request_id` field |
| CORS config | `apps/api/karrio/server/settings/base.py` | Already allows `x-request-id` |
| `uuid()` helper | `modules/sdk/karrio/core/utils/` | Reuse for ID generation |
| Sentry `before_send` | `apps/api/karrio/server/settings/apm.py` | Inject `request_id` tag |
| Shipment/Tracker/Order meta | `modules/manager/karrio/server/manager/models.py` | Write `request_id` into `meta` on create/update |

### Architecture Overview

```
┌──────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│   Client     │────>│  RequestIDMiddleware │────>│  SessionContext   │
│  (optional   │     │  - Extract/Generate  │     │  - Create Tracer  │
│   X-Request  │     │  - Validate          │     │  - Inject into    │
│   -ID header)│     │  - Set on request    │     │    tracer.context │
└──────────────┘     └─────────────────────┘     └──────────────────┘
                              │                          │
                              │                          ▼
                     ┌────────▼──────────┐     ┌──────────────────┐
                     │  Response         │     │  View Layer       │
                     │  X-Request-ID     │     │  - LoggingMixin   │
                     │  header (always)  │     │  - APILogIndex    │
                     └───────────────────┘     │    .request_id    │
                                               └──────────────────┘
                                                        │
                          ┌─────────────────────────────┼──────────────────┐
                          │                             │                  │
                          ▼                             ▼                  ▼
                  ┌───────────────┐          ┌──────────────┐    ┌────────────────┐
                  │ Domain Object │          │TracingRecord │    │    Sentry      │
                  │ .meta = {     │          │ .meta = {    │    │  tag:          │
                  │   request_id  │          │   request_id │    │   request_id   │
                  │ }             │          │ }            │    │  breadcrumb    │
                  └───────────────┘          └──────────────┘    └────────────────┘
                  (Shipment, Tracker,
                   Order, Pickup, etc.)

                          ┌──────────────────────────────────────┐
                          │          Background Tasks             │
                          │  request_id = req_<new_uuid>          │
                          │  parent_request_id = req_<original>   │
                          └──────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌───────────┐     ┌───────────┐     ┌─────────┐     ┌─────────┐     ┌────────┐
│ Client │     │ RequestID │     │  Session   │     │  View   │     │ Tracing │     │ Sentry │
│        │     │ Middleware│     │  Context   │     │ (API)   │     │  Utils  │     │        │
└───┬────┘     └─────┬─────┘     └─────┬─────┘     └────┬────┘     └────┬────┘     └───┬────┘
    │                │                  │                 │               │              │
    │  POST /v1/shipments              │                 │               │              │
    │  X-Request-ID: req_abc123        │                 │               │              │
    │───────────────>│                  │                 │               │              │
    │                │                  │                 │               │              │
    │                │ 1. Validate ID   │                 │               │              │
    │                │    (valid: use)  │                 │               │              │
    │                │ request.request_id = "req_abc123"  │               │              │
    │                │─────────────────>│                 │               │              │
    │                │                  │                 │               │              │
    │                │                  │ 2. Create Tracer               │              │
    │                │                  │    tracer.context["request_id"]                │
    │                │                  │────────────────────────────────────────────────>│
    │                │                  │ 3. Sentry tag("request_id", "req_abc123")      │
    │                │                  │                 │               │              │
    │                │                  │────────────────>│               │              │
    │                │                  │                 │               │              │
    │                │                  │                 │ 4. Create shipment           │
    │                │                  │                 │    shp.meta["request_id"] = "req_abc123"
    │                │                  │                 │               │              │
    │                │                  │                 │ 5. Carrier API call          │
    │                │                  │                 │   (internal _request_id)     │
    │                │                  │                 │               │              │
    │                │                  │                 │ 6. Save APILogIndex          │
    │                │                  │                 │    .request_id = "req_abc123"│
    │                │                  │                 │               │              │
    │                │                  │                 │ 7. set_tracing_context(      │
    │                │                  │                 │      request_id="req_abc123")│
    │                │                  │                 │──────────────>│              │
    │                │                  │                 │               │              │
    │                │                  │ 8. save_tracing_records()      │              │
    │                │                  │    TracingRecord.meta["request_id"]            │
    │                │                  │──────────────────────────────>│               │
    │                │                  │                 │               │              │
    │                │ 9. Set response header             │               │              │
    │                │    X-Request-ID: req_abc123        │               │              │
    │<───────────────│                  │                 │               │              │
    │                │                  │                 │               │              │
    │  201 Created   │                  │                 │               │              │
    │  X-Request-ID: req_abc123        │                 │               │              │
    │                │                  │                 │               │              │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           REQUEST ID FLOW                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────┐    ┌──────────────────┐    ┌───────────────┐                  │
│  │ Client    │───>│ RequestIDMiddle  │───>│ request       │                  │
│  │ Header    │    │ ware: validate   │    │ .request_id   │                  │
│  │ (or null) │    │ or generate      │    │ = "req_..."   │                  │
│  └───────────┘    └──────────────────┘    └───────┬───────┘                  │
│                                                    │                          │
│                    ┌───────────────────────────────┼────────────────────┐     │
│                    │                               │                    │     │
│                    ▼                               ▼                    ▼     │
│           ┌───────────────┐             ┌──────────────────┐  ┌────────────┐ │
│           │ APILogIndex   │             │ Tracer.context   │  │ Sentry     │ │
│           │ .request_id   │             │ ["request_id"]   │  │ .set_tag() │ │
│           │ (DB column)   │             │ (in-memory)      │  │ .breadcrumb│ │
│           └───────┬───────┘             └────────┬─────────┘  └────────────┘ │
│                   │                              │                            │
│                   │                    ┌─────────┼──────────────┐             │
│                   │                    │         │              │             │
│                   │                    ▼         ▼              ▼             │
│                   │           ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│                   │           │ Tracing  │ │ Domain   │ │ Background Task  │ │
│                   │           │ Record   │ │ Object   │ │ .parent_request  │ │
│                   │           │ .meta    │ │ .meta    │ │ _id = "req_..."  │ │
│                   │           │ {req_id} │ │ {req_id} │ │ .request_id =   │ │
│                   │           └──────────┘ └──────────┘ │  "req_<new>"     │ │
│                   │                                      └──────────────────┘ │
│                   │                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                           RESPONSE FLOW                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────┐    ┌──────────────────┐    ┌───────────────┐                  │
│  │ Client    │<───│ RequestIDMiddle  │<───│ Django        │                  │
│  │ receives  │    │ ware: set header │    │ Response      │                  │
│  │ X-Request │    │ X-Request-ID:    │    │               │                  │
│  │ -ID header│    │ req_...          │    │               │                  │
│  └───────────┘    └──────────────────┘    └───────────────┘                  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### New Middleware: `RequestIDMiddleware`

```python
# modules/core/karrio/server/core/middleware.py

import re
import uuid


# Validation: alphanumeric, dashes, underscores, dots. Max 200 chars.
_REQUEST_ID_RE = re.compile(r"^[a-zA-Z0-9_\-\.]{1,200}$")


def _generate_request_id() -> str:
    return f"req_{uuid.uuid4().hex}"


def _is_valid_request_id(value: str) -> bool:
    return bool(value) and bool(_REQUEST_ID_RE.match(value))


class RequestIDMiddleware:
    """Middleware to extract or generate X-Request-ID for every request.

    Reads the X-Request-ID header from the incoming request. If present and
    valid (alphanumeric + dashes + underscores, max 200 chars), uses it.
    Otherwise generates a new `req_<uuid>` identifier.

    The request_id is:
    - Set on `request.request_id`
    - Added to the response as `X-Request-ID` header
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract or generate request ID
        client_id = request.META.get("HTTP_X_REQUEST_ID", "").strip()
        request.request_id = (
            client_id if _is_valid_request_id(client_id)
            else _generate_request_id()
        )

        response = self.get_response(request)

        # Always set response header
        response["X-Request-ID"] = request.request_id

        return response
```

#### Modified `APILogIndex` Model

```python
# modules/core/karrio/server/core/models/third_party.py

class APILogIndex(APILog):
    entity_id = models.CharField(max_length=50, null=True, db_index=True)
    request_id = models.CharField(max_length=200, null=True, db_index=True)
    test_mode = models.BooleanField(
        default=True, null=True, help_text="execution context"
    )
```

#### Modified `SessionContext` (telemetry injection)

```python
# In SessionContext.__call__ (after RequestIDMiddleware has run):

def __call__(self, request):
    tracer = Tracer()
    self._inject_telemetry(tracer, request)
    request.tracer = tracer

    # Propagate request_id into tracer context
    request_id = getattr(request, "request_id", None)
    if request_id:
        tracer.add_context({"request_id": request_id})

    # ... rest of existing logic ...

# In _inject_telemetry:
def _inject_telemetry(self, tracer: Tracer, request):
    # ... existing telemetry setup ...

    # Add request_id tag to Sentry
    request_id = getattr(request, "request_id", None)
    if request_id:
        tracer.set_tag("request_id", request_id)
        tracer.add_breadcrumb(
            f"Request {request_id}",
            "http",
            {"request_id": request_id, "method": request.method, "path": request.path},
        )
```

#### Modified `LoggingMixin.handle_log()`

```python
# modules/core/karrio/server/core/views/api.py

def handle_log(self):
    # ... existing data preparation ...

    request_id = getattr(self.request, "request_id", None)

    log = APILogIndex(
        **{
            **self.log,
            "data": data,
            "response": response,
            "entity_id": entity_id,
            "request_id": request_id,       # NEW
            "test_mode": test_mode,
            "query_params": query_params,
        }
    )

    log.save()
    link_org(log, self.request)

    set_tracing_context(
        request_log_id=getattr(log, "id", None),
        request_id=request_id,              # NEW
        object_id=failsafe(lambda: (self.log.get("response") or {}).get("id")),
    )
```

#### Modified `save_tracing_records()`

```python
# modules/core/karrio/server/tracing/utils.py
# In the records.append() block, add request_id to meta:

records.append(
    models.TracingRecord(
        key=record.key,
        record=record.data,
        timestamp=record.timestamp,
        created_by_id=getattr(actor, "id", None),
        test_mode=connection.get("test_mode", False),
        meta=lib.to_dict(
            {
                "tracer_id": tracer.id,
                "request_id": tracer.context.get("request_id"),     # NEW
                "object_id": tracer.context.get("object_id"),
                "carrier_account_id": connection.get("id"),
                "carrier_id": connection.get("carrier_id"),
                "carrier_name": connection.get("carrier_name"),
                "request_log_id": tracer.context.get("request_log_id"),
            }
        ),
    )
)
```

#### Domain Object Meta Injection

The `request_id` is injected into domain objects' `meta` field during creation/update operations. This happens in serializer `create()` and `update()` methods.

```python
# Pattern for all serializers that create/update domain objects
# e.g., modules/manager/karrio/server/manager/serializers/shipment.py

from karrio.server.core.middleware import SessionContext

def _get_request_id():
    """Get current request_id from the active request context."""
    request = SessionContext.get_current_request()
    return getattr(request, "request_id", None) if request else None

# In create/update methods, inject into meta:
meta = {**(instance.meta or {}), "request_id": _get_request_id()}
```

#### Background Task Request ID

```python
# Pattern for background tasks (webhooks, batch processing, scheduled updates)

def _generate_task_request_id(parent_request_id: str = None) -> dict:
    """Generate a request context for background tasks."""
    return {
        "request_id": f"req_{uuid.uuid4().hex}",
        "parent_request_id": parent_request_id,
    }

# When dispatching a background task from a view:
request_id = getattr(request, "request_id", None)
task.apply_async(
    args=[...],
    kwargs={
        "request_context": _generate_task_request_id(parent_request_id=request_id),
    },
)
```

### Field Reference

| Field | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| `X-Request-ID` | Header | HTTP Request | No | Client-provided correlation ID |
| `X-Request-ID` | Header | HTTP Response | Always | Server-confirmed correlation ID |
| `request.request_id` | str | Django request | Always | In-memory request attribute |
| `APILogIndex.request_id` | CharField(200) | DB column | No (nullable) | Indexed for fast lookups |
| `TracingRecord.meta.request_id` | str | JSON field | No | Propagated from tracer context |
| `Shipment.meta.request_id` | str | JSON field | No | Set on create/update |
| `Tracker.meta.request_id` | str | JSON field | No | Set on create/update |
| `Order.meta.request_id` | str | JSON field | No | Set on create/update |
| `Pickup.meta.request_id` | str | JSON field | No | Set on create/update |
| `Manifest.meta.request_id` | str | JSON field | No | Set on create/update |
| `BatchOperation.meta.request_id` | str | JSON field | No | Set on create |
| `tracer.context["request_id"]` | str | In-memory | Always | Tracer context propagation |
| `parent_request_id` | str | Task kwargs | No | Links async task to originating request |

### API Changes

**New filter parameter on existing endpoints:**

| Method | Endpoint | New Parameter | Description |
|--------|----------|---------------|-------------|
| GET | `/v1/logs` | `?request_id=req_...` | Filter API logs by request_id |
| GET | `/v1/shipments` | `?request_id=req_...` | Filter shipments by meta.request_id |
| GET | `/v1/trackers` | `?request_id=req_...` | Filter trackers by meta.request_id |
| GET | `/v1/orders` | `?request_id=req_...` | Filter orders by meta.request_id |
| GET | `/v1/pickups` | `?request_id=req_...` | Filter pickups by meta.request_id |
| GET | `/v1/traces` | `?request_id=req_...` | Filter tracing records by meta.request_id |

**Response header (all endpoints):**

```
HTTP/1.1 201 Created
X-Request-ID: req_550e8400e29b41d4a716446655440000
Content-Type: application/json

{
  "id": "shp_abc123",
  "meta": {
    "request_id": "req_550e8400e29b41d4a716446655440000",
    ...
  },
  ...
}
```

### Middleware Ordering

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "karrio.server.core.middleware.RequestIDMiddleware",          # NEW - before auth
    "karrio.server.core.authentication.AuthenticationMiddleware",
    "karrio.server.core.authentication.TwoFactorAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "karrio.server.core.middleware.SessionContext",               # Reads request.request_id
]
```

`RequestIDMiddleware` is placed **before** `AuthenticationMiddleware` so that even failed auth requests get a request_id in the response, aiding client-side debugging.

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| No `X-Request-ID` header sent | Server generates `req_<uuid>` | `_generate_request_id()` in middleware |
| Client sends empty `X-Request-ID: ""` | Server generates new ID | Treated as missing after `.strip()` |
| Client sends invalid ID (special chars, >200 chars) | Server generates new ID, ignores invalid | `_is_valid_request_id()` returns False |
| Client sends valid non-prefixed ID (e.g., `my-custom-id-123`) | Server honors it as-is | Valid per regex, no `req_` prefix required for client IDs |
| Same `X-Request-ID` sent twice (retry) | Both requests use the same ID | Two API log entries with same `request_id`; this is expected and useful for idempotency debugging |
| GraphQL batch query (multiple operations) | Single request_id for the batch | One HTTP request = one request_id |
| WebSocket connections | Not applicable initially | WebSocket middleware not in scope |
| Health check / readiness probe requests | request_id generated but not logged | Logging only on POST/PUT/PATCH/DELETE; middleware still sets header |
| Request fails before reaching SessionContext | Response still has X-Request-ID | RequestIDMiddleware runs before SessionContext |
| Concurrent requests with same client ID | Both honored independently | Each creates its own API log, objects, traces |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| RequestIDMiddleware raises exception | Request fails with 500 | Wrap in try/except; fallback to generated ID |
| DB migration fails on `APILogIndex.request_id` | Deploy blocked | Column is nullable; migration is additive only |
| `meta` JSON field update race condition | Last writer wins; request_id could be overwritten | Acceptable: request_id reflects the last mutating operation |
| Sentry tag cardinality explosion | Sentry performance degradation | request_id has bounded cardinality (one per request); Sentry handles high-cardinality tags |
| Client sends extremely long valid ID (200 chars) | Stored in DB, slightly larger storage | 200 char limit is generous but bounded |
| Background task loses parent_request_id | Async task orphaned from parent | Log warning; task still has its own request_id |

### Security Considerations

- [x] Input validation: regex validation on client-provided IDs (alphanumeric + dashes + underscores, max 200 chars)
- [x] No secrets in code or logs: request_id is an opaque correlation identifier
- [x] No authentication bypass: RequestIDMiddleware runs before auth but doesn't affect auth decisions
- [x] No injection: request_id is validated before storage; never interpolated into SQL (uses ORM parameterized queries)
- [x] Information disclosure: request_id in response headers reveals no sensitive data; it's a correlation token

---

## Implementation Plan

### Phase 1: Core Middleware & Storage

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `RequestIDMiddleware` class | `modules/core/karrio/server/core/middleware.py` | Pending | S |
| Register middleware in settings | `apps/api/karrio/server/settings/base.py` | Pending | S |
| Add `request_id` column to `APILogIndex` | `modules/core/karrio/server/core/models/third_party.py` | Pending | S |
| Create DB migration for `APILogIndex.request_id` | `modules/core/karrio/server/core/migrations/` | Pending | S |
| Update `LoggingMixin.handle_log()` to store request_id | `modules/core/karrio/server/core/views/api.py` | Pending | S |
| Inject request_id into `tracer.context` in SessionContext | `modules/core/karrio/server/core/middleware.py` | Pending | S |
| Add Sentry tag/breadcrumb for request_id | `modules/core/karrio/server/core/middleware.py` | Pending | S |

### Phase 2: TracingRecord & Domain Object Propagation

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `request_id` to TracingRecord meta in `save_tracing_records()` | `modules/core/karrio/server/tracing/utils.py` | Pending | S |
| Add `request_id` to TracingRecord meta in `bulk_save_tracing_records()` | `modules/core/karrio/server/tracing/utils.py` | Pending | S |
| Inject `request_id` into Shipment `meta` on create/update | `modules/manager/karrio/server/manager/serializers/shipment.py` | Pending | M |
| Inject `request_id` into Tracker `meta` on create/update | `modules/manager/karrio/server/manager/serializers/tracker.py` | Pending | S |
| Inject `request_id` into Order `meta` on create/update | `modules/orders/karrio/server/orders/serializers/order.py` | Pending | S |
| Inject `request_id` into Pickup `meta` on create/update | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Inject `request_id` into Manifest `meta` on create/update | `modules/manager/karrio/server/manager/serializers/manifest.py` | Pending | S |
| Inject `request_id` into BatchOperation `meta` on create | `modules/data/karrio/server/data/serializers/batch.py` | Pending | S |
| Create shared `_get_request_id()` utility | `modules/core/karrio/server/core/utils.py` | Pending | S |

### Phase 3: API Filtering & Background Tasks

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `request_id` filter to API logs list endpoint | `modules/core/karrio/server/core/views/` + serializers | Pending | S |
| Add `request_id` filter to TracingRecord list endpoint | `modules/core/karrio/server/tracing/views.py` + serializers | Pending | S |
| Add `request_id` filter to Shipment list endpoint | `modules/manager/karrio/server/manager/views/shipments.py` | Pending | M |
| Add `request_id` filter to Tracker list endpoint | `modules/manager/karrio/server/manager/views/trackers.py` | Pending | S |
| Add `request_id` filter to Order list endpoint | `modules/orders/karrio/server/orders/views/orders.py` | Pending | S |
| Add `request_id` filter to Pickup list endpoint | `modules/manager/karrio/server/manager/views/pickups.py` | Pending | S |
| Add `request_id` filter to GraphQL types | `modules/graph/karrio/server/graph/schemas/base/types.py` | Pending | M |
| Add background task request_id generation + parent linking | `modules/core/karrio/server/core/utils.py` + task dispatch sites | Pending | M |
| Update webhook dispatch to carry parent_request_id | `modules/events/karrio/server/events/` | Pending | M |

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/core/karrio/server/core/tests/` | RequestIDMiddleware, validation logic |
| Integration Tests | `modules/core/karrio/server/core/tests/` | End-to-end request → log → trace flow |
| Server Tests | `karrio test` | API endpoint filtering, response headers |

### Test Cases

#### Unit Tests

```python
"""Test RequestIDMiddleware behavior."""

import unittest
from unittest.mock import MagicMock, patch, ANY
from karrio.server.core.middleware import (
    RequestIDMiddleware,
    _generate_request_id,
    _is_valid_request_id,
)


class TestRequestIDValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_valid_uuid_format(self):
        """Verify standard UUID is accepted."""
        self.assertTrue(_is_valid_request_id("550e8400-e29b-41d4-a716-446655440000"))

    def test_valid_prefixed_format(self):
        """Verify req_ prefixed ID is accepted."""
        self.assertTrue(_is_valid_request_id("req_550e8400e29b41d4a716446655440000"))

    def test_valid_custom_format(self):
        """Verify client custom ID with dashes and underscores is accepted."""
        self.assertTrue(_is_valid_request_id("my-app_request-123"))

    def test_invalid_special_characters(self):
        """Verify IDs with special chars are rejected."""
        self.assertFalse(_is_valid_request_id("req_abc<script>alert(1)</script>"))

    def test_invalid_too_long(self):
        """Verify IDs over 200 chars are rejected."""
        self.assertFalse(_is_valid_request_id("a" * 201))

    def test_invalid_empty_string(self):
        """Verify empty string is rejected."""
        self.assertFalse(_is_valid_request_id(""))

    def test_generated_id_format(self):
        """Verify generated IDs follow req_<hex> format."""
        request_id = _generate_request_id()
        self.assertTrue(request_id.startswith("req_"))
        self.assertEqual(len(request_id), 36)  # "req_" + 32 hex chars


class TestRequestIDMiddleware(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.get_response = MagicMock(return_value=MagicMock())
        self.middleware = RequestIDMiddleware(self.get_response)

    def test_client_provided_valid_id(self):
        """Verify client-provided valid ID is honored."""
        request = MagicMock()
        request.META = {"HTTP_X_REQUEST_ID": "req_abc123"}

        response = self.middleware(request)

        self.assertEqual(request.request_id, "req_abc123")
        self.assertEqual(response["X-Request-ID"], "req_abc123")

    def test_missing_header_generates_id(self):
        """Verify missing header triggers generation."""
        request = MagicMock()
        request.META = {}

        response = self.middleware(request)

        self.assertTrue(request.request_id.startswith("req_"))
        self.assertEqual(response["X-Request-ID"], request.request_id)

    def test_invalid_header_generates_id(self):
        """Verify invalid header triggers generation."""
        request = MagicMock()
        request.META = {"HTTP_X_REQUEST_ID": "<script>alert(1)</script>"}

        response = self.middleware(request)

        self.assertTrue(request.request_id.startswith("req_"))
        self.assertNotEqual(request.request_id, "<script>alert(1)</script>")
```

#### Integration Tests

```python
"""Test end-to-end request_id flow through API."""

import unittest
from django.test import TestCase, RequestFactory
from karrio.server.core.models import APILogIndex


class TestRequestIDIntegration(TestCase):
    def test_api_log_stores_request_id(self):
        """Verify API log entry includes request_id."""
        response = self.client.post(
            "/v1/shipments",
            data={...},
            HTTP_X_REQUEST_ID="req_test123",
            content_type="application/json",
        )
        print(response)  # Debug: print before assertions

        # Verify response header
        self.assertEqual(response["X-Request-ID"], "req_test123")

        # Verify API log stored the request_id
        log = APILogIndex.objects.filter(request_id="req_test123").first()
        self.assertIsNotNone(log)

    def test_filter_logs_by_request_id(self):
        """Verify API logs are filterable by request_id."""
        response = self.client.get("/v1/logs?request_id=req_test123")
        print(response)
        self.assertEqual(response.status_code, 200)
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run middleware unit tests
python -m unittest discover -v -f modules/core/karrio/server/core/tests/

# Run server integration tests
karrio test --failfast karrio.server.core.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Middleware exception breaks all requests | High | Low | Wrap in try/except with fallback to generated ID |
| Migration conflict with other branches | Medium | Medium | Coordinate migration numbering; nullable column is safe |
| Performance overhead of middleware | Low | Low | Single UUID generation + header read is negligible |
| Sentry tag cardinality | Low | Low | One tag per request is within Sentry's design parameters |
| Client sends same request_id for different operations | Low | Medium | Expected behavior for retries; API logs show distinct entries |
| JSON meta field query performance | Medium | Medium | Add GIN index on `meta->>'request_id'` for key models |
| Breaking change to API response headers | Low | Low | Adding headers is backward-compatible; no existing header modified |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: Adding `X-Request-ID` response header is additive; no existing headers modified. Clients not sending the header are unaffected (server generates ID).
- **Data compatibility**: `APILogIndex.request_id` is nullable; existing rows remain untouched. Domain object `meta` is a JSON field; existing meta is preserved with `{**existing_meta, "request_id": ...}`.
- **No feature flags**: Ship all at once per decision D12. The feature is passive (generates IDs for new requests) and doesn't affect existing behavior.

### Data Migration

```python
# Migration: Add request_id to APILogIndex
# modules/core/karrio/server/core/migrations/XXXX_add_request_id_to_apilogindex.py

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "XXXX_previous_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="apilogindex",
            name="request_id",
            field=models.CharField(max_length=200, null=True, db_index=True),
        ),
    ]
```

No data backfill is needed—existing log entries will have `request_id=NULL`. Only new requests will populate the field.

### Rollback Procedure

1. **Identify issue**: Monitor for increased error rates or performance degradation after deploy
2. **Stop rollout**: Revert the middleware registration in `MIDDLEWARE` list (remove `RequestIDMiddleware`)
3. **Revert changes**: Revert the code changes. The `APILogIndex.request_id` column can remain (nullable, harmless). Domain object `meta.request_id` keys are informational and don't affect behavior.
4. **Verify recovery**: Confirm API responses no longer include `X-Request-ID` header; confirm request throughput returns to baseline

---

## Appendices

### Appendix A: Typical Usage Scenarios

**Scenario 1: Client-side error reporting**
```
Client sends: POST /v1/shipments
              X-Request-ID: req_my-app-uuid-123
Server responds: 201 Created
                 X-Request-ID: req_my-app-uuid-123

Client logs: "Shipment created, request_id=req_my-app-uuid-123"
Later, client reports issue: "Request req_my-app-uuid-123 returned wrong rate"

Support queries:
  GET /v1/logs?request_id=req_my-app-uuid-123        → API log entry
  GET /v1/traces?request_id=req_my-app-uuid-123      → Carrier API calls
  GET /v1/shipments?request_id=req_my-app-uuid-123   → Created shipment
  Sentry: search tag request_id=req_my-app-uuid-123  → Error events
```

**Scenario 2: Debugging failed carrier API call**
```
1. User reports: "My shipment creation failed with error X"
2. Find the request_id from API logs or Sentry
3. Query TracingRecords by request_id to see exact carrier request/response
4. Identify carrier-side issue from raw HTTP traces
```

**Scenario 3: Batch operation tracing**
```
1. Client creates batch: POST /v1/batches
   X-Request-ID: req_batch-creation-001
2. Server creates BatchOperation with meta.request_id = req_batch-creation-001
3. Background workers process items:
   - Each worker gets own request_id: req_<worker-uuid>
   - Each worker carries parent_request_id: req_batch-creation-001
4. Query all workers by parent_request_id to see full batch execution
```

**Scenario 4: Webhook debugging**
```
1. Shipment status update triggers webhook
   - Original shipment created with request_id: req_original-abc
   - Webhook dispatch task gets: request_id=req_webhook-xyz, parent_request_id=req_original-abc
2. Webhook delivery fails
3. Trace back: webhook task → parent request → original shipment creation
```

### Appendix B: Industry Standards Reference

| Service | Header Name | Format | Response | Notes |
|---------|-------------|--------|----------|-------|
| Stripe | `Request-Id` | `req_<alphanum>` | Always | Prefixed UUID |
| GitHub | `X-GitHub-Request-Id` | UUID | Always | Standard UUID |
| AWS | `x-amzn-RequestId` | UUID | Always | Standard UUID |
| Heroku | `X-Request-Id` | UUID | Always | Standard UUID |
| Cloudflare | `cf-ray` | Hex ID | Always | Custom format |
| Shopify | `X-Request-Id` | UUID | Always | Standard UUID |

Karrio's `req_<uuid-hex>` format follows Stripe's convention most closely.

### Appendix C: JSON Meta Index Considerations

For filtering domain objects by `meta.request_id`, PostgreSQL GIN indexes on JSONB fields are recommended:

```sql
-- Optional: Add partial GIN index for request_id lookups on high-volume tables
CREATE INDEX CONCURRENTLY idx_shipment_meta_request_id
ON manager_shipment ((meta->>'request_id'))
WHERE meta->>'request_id' IS NOT NULL;

CREATE INDEX CONCURRENTLY idx_tracker_meta_request_id
ON manager_tracking ((meta->>'request_id'))
WHERE meta->>'request_id' IS NOT NULL;
```

These indexes are optional and should be added based on query volume. The `APILogIndex.request_id` column index handles the most common lookup pattern.
