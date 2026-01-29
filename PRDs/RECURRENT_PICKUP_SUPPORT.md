# Recurrent vs One-Time Pickup Support

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2025-01-28 |
| Status | Planning |
| Owner | Engineering Team |
| Type | Enhancement |
| Reference | [AGENTS.md](../AGENTS.md), [CARRIER_INTEGRATION_GUIDE.md](../CARRIER_INTEGRATION_GUIDE.md) |

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

This PRD proposes adding support for **recurrent/standing pickups** alongside the existing one-time pickup functionality. Currently, Karrio only supports one-time pickup scheduling, but several carriers (UPS, CanadaPost, FedEx) support daily/recurring pickup arrangements that can reduce costs and simplify logistics for high-volume shippers.

### Key Architecture Decisions

1. **Unified `pickup_type` Enum**: Add a new `PickupType` enum to the SDK with values `one_time`, `daily`, `recurring` that maps to carrier-specific codes
2. **Carrier-Level Mapping**: Each carrier mapper handles translation between unified pickup types and carrier-specific codes (e.g., UPS "01" for daily, "06" for one-time)
3. **Backward Compatible**: Default to `one_time` when no pickup_type specified, preserving existing behavior
4. **Optional Recurrence Config**: Add `recurrence` options dict for carriers that support custom schedules (days of week, end date)

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Add `pickup_type` field to SDK PickupRequest model | Carrier account-level pickup preferences |
| Update all 12 carrier pickup implementations | Automated pickup scheduling based on shipment volume |
| GraphQL and REST API updates | Pickup cost optimization algorithms |
| Dashboard UI for pickup type selection | Third-party calendar integrations |
| Unit and integration tests for all carriers | Real-time pickup slot availability checking |

---

## Open Questions & Decisions

### Pending Questions

| # | Question | Context | Options | Status |
|---|----------|---------|---------|--------|
| - | - | - | - | - |

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Store recurrence metadata in Pickup model | Store in Pickup.meta JSON | Simpler implementation, no schema migration needed, flexible structure | 2025-01-28 |
| D2 | Handle unsupported pickup types | Return validation error | Clear feedback to API consumers, prevents silent failures | 2025-01-28 |
| D3 | end_date requirement for recurring pickups | Optional (not required) | Flexibility for carriers with different requirements, user convenience | 2025-01-28 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| User requests daily pickup on carrier that only supports one-time | Request would fail | Return validation error with supported types | No (Resolved: D2) |
| User updates recurring pickup to one-time | Carrier may not support conversion | Cancel existing and create new | No |
| Recurring pickup spans carrier account change | Schedule may be orphaned | Warn user, require explicit cancellation | No |

---

## Problem Statement

### Current State

```python
# modules/sdk/karrio/core/models.py
@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request unified data type."""

    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    parcels_count: int = None
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    options: Dict = {}
    metadata: Dict = {}
    # NO pickup_type field - all pickups are implicitly one-time
```

```python
# modules/connectors/ups/karrio/providers/ups/pickup/create.py
# UPS supports pickup types but they're not exposed
PickupPiece=ups.PickupPieceType(
    ServiceCode=options.ups_pickup_service_code.state or "001",  # Hardcoded default
    # ...
)
```

### Desired State

```python
# modules/sdk/karrio/core/models.py
@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request unified data type."""

    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    parcels_count: int = None
    pickup_type: str = "one_time"  # NEW: "one_time", "daily", "recurring"
    recurrence: Dict = {}  # NEW: {"days": ["MON", "WED", "FRI"], "end_date": "2025-12-31"}
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    options: Dict = {}
    metadata: Dict = {}
```

```python
# modules/connectors/ups/karrio/providers/ups/pickup/create.py
# UPS pickup type properly mapped
from karrio.providers.ups.units import PickupTypeCode

pickup_type_code = PickupTypeCode[payload.pickup_type].value  # Maps to "01" or "06"
PickupPiece=ups.PickupPieceType(
    ServiceCode=pickup_type_code,
    # ...
)
```

### Problems

1. **No Pickup Type Selection**: Users cannot specify whether they want a one-time or recurring pickup
2. **Carrier Capabilities Hidden**: Carriers like UPS, CanadaPost, FedEx support different pickup types but this isn't exposed
3. **Cost Inefficiency**: High-volume shippers pay per-pickup fees instead of using standing arrangements
4. **Manual Workarounds**: Users must contact carriers directly to set up recurring pickups

---

## Goals & Success Criteria

### Goals

1. Add unified `pickup_type` field to SDK PickupRequest model
2. Implement pickup type mapping for all 12 carriers with pickup support
3. Expose pickup type selection in GraphQL, REST API, and Dashboard
4. Maintain 100% backward compatibility with existing API consumers

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| All 12 carrier pickup tests pass | 100% | Must-have |
| Existing pickup API tests pass without changes | 100% | Must-have |
| New pickup_type field properly validated | Enum validation | Must-have |
| Dashboard shows pickup type selector | UI implemented | Must-have |
| Carrier-unsupported types return clear error | Error message | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] SDK PickupRequest model updated with pickup_type field
- [ ] All carrier mappers handle pickup_type (with fallback for unsupported)
- [ ] GraphQL PickupType and mutations updated
- [ ] REST API serializers updated
- [ ] Unit tests for each carrier's pickup type handling
- [ ] API-level integration tests

**Nice-to-have (P1):**
- [ ] Dashboard pickup type selector UI
- [ ] Recurrence configuration UI
- [ ] Pickup type availability per carrier in API metadata

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A) Unified pickup_type enum** | Clean API, carrier-agnostic | Requires mapping for each carrier | **Selected** |
| B) Carrier-specific options only | Simple implementation | Inconsistent API, hard to use | Rejected |
| C) Separate endpoints for recurring | Clear separation | Duplicate code, breaking change | Rejected |
| D) Boolean is_recurring flag | Simple | Not expressive enough for daily vs custom | Rejected |

### Trade-off Analysis

**Option A (Selected)** provides a clean, unified API that abstracts carrier differences while still allowing carrier-specific options when needed. The mapping complexity is isolated in each carrier's provider module, following the existing Karrio pattern for rate services and shipping options.

---

## Technical Design

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| PickupRequest model | `modules/sdk/karrio/core/models.py:184` | Extend with new fields |
| PickupSerializer | `modules/manager/karrio/server/manager/serializers/pickup.py` | Add pickup_type validation |
| GraphQL PickupType | `modules/graph/karrio/server/graph/schemas/base/types.py:1343` | Add pickup_type field |
| GraphQL PickupFilter | `modules/graph/karrio/server/graph/schemas/base/inputs.py:71` | Add pickup_type filter |
| UPS pickup provider | `modules/connectors/ups/karrio/providers/ups/pickup/create.py` | Map pickup_type to ServiceCode |
| CanadaPost pickup | `modules/connectors/canadapost/karrio/providers/canadapost/pickup/create.py` | Map to ON_DEMAND/SCHEDULED |
| FedEx pickup | `modules/connectors/fedex/karrio/providers/fedex/pickup/create.py` | Map to pickupType field |
| lib.StrEnum | `karrio.lib` | Use for PickupType enum |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PICKUP TYPE FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────┐     ┌───────────┐     ┌────────────┐     ┌──────────────┐   │
│   │ Dashboard│────>│  GraphQL  │────>│  REST API  │────>│   Gateway    │   │
│   │    UI    │     │  /pickup  │     │ /pickups   │     │              │   │
│   └──────────┘     └───────────┘     └────────────┘     └──────┬───────┘   │
│                                                                  │          │
│                                                                  ▼          │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                        CARRIER MAPPERS                               │  │
│   ├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────┤  │
│   │   UPS    │  FedEx   │CanadaPost│   DHL    │ Purolator│   Others     │  │
│   │  01/06   │ ON_CALL  │ON_DEMAND │   N/A    │   N/A    │    N/A       │  │
│   │ DAILY/   │ REGULAR  │SCHEDULED │ one_time │ one_time │  one_time    │  │
│   │ ONE_TIME │  _STOP   │          │  only    │   only   │    only      │  │
│   └──────────┴──────────┴──────────┴──────────┴──────────┴──────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────┐     ┌──────────┐     ┌────────┐     ┌────────┐
│ Client │     │  API   │     │Serializer│     │ Mapper │     │Carrier │
└───┬────┘     └───┬────┘     └────┬─────┘     └───┬────┘     └───┬────┘
    │              │               │               │              │
    │ POST /pickup │               │               │              │
    │ pickup_type: │               │               │              │
    │   "daily"    │               │               │              │
    │─────────────>│               │               │              │
    │              │  1. Validate  │               │              │
    │              │─────────────->│               │              │
    │              │               │               │              │
    │              │  2. Check     │               │              │
    │              │  carrier caps │               │              │
    │              │<─────────────-│               │              │
    │              │               │               │              │
    │              │      3. Map to carrier code   │              │
    │              │──────────────────────────────>│              │
    │              │               │               │              │
    │              │               │               │ 4. API call  │
    │              │               │               │  (code=01)   │
    │              │               │               │─────────────>│
    │              │               │               │              │
    │              │               │               │ 5. Response  │
    │              │               │               │<─────────────│
    │              │               │               │              │
    │  6. Pickup   │               │               │              │
    │    response  │               │               │              │
    │<─────────────│               │               │              │
    │              │               │               │              │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            PICKUP TYPE DATA FLOW                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  INPUT (Unified)              TRANSFORM                    OUTPUT (Carrier)   │
│  ┌─────────────────┐         ┌───────────────┐           ┌─────────────────┐ │
│  │ {                │         │               │           │ UPS:            │ │
│  │   pickup_type:   │         │  Carrier      │           │  ServiceCode:   │ │
│  │     "daily"      │────────>│  Mapper       │──────────>│    "01"         │ │
│  │   pickup_date:   │         │  Provider     │           │                 │ │
│  │     "2025-01-28" │         │               │           │ CanadaPost:     │ │
│  │   ...            │         │  Maps unified │           │  PickupType:    │ │
│  │ }                │         │  to carrier   │           │    "Scheduled"  │ │
│  └─────────────────┘         │  specific     │           │                 │ │
│                               │               │           │ FedEx:          │ │
│  ENUM VALUES:                 └───────────────┘           │  pickupType:    │ │
│  - one_time (default)                                     │    "REGULAR_    │ │
│  - daily                                                  │     STOP"       │ │
│  - recurring                                              └─────────────────┘ │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### SDK Model Changes

```python
# modules/sdk/karrio/core/models.py
import karrio.lib as lib

class PickupType(lib.StrEnum):
    """Unified pickup type enumeration."""
    one_time = "one_time"
    daily = "daily"
    recurring = "recurring"


@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request unified data type."""

    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    parcels_count: int = None
    pickup_type: str = "one_time"  # NEW FIELD
    recurrence: Dict = {}  # NEW FIELD: {"days": ["MON","TUE"], "end_date": "2025-12-31"}
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    options: Dict = {}
    metadata: Dict = {}
```

#### Server Serializer Changes

```python
# modules/core/karrio/server/core/serializers.py
class PickupRequest(serializers.Serializer):
    # ... existing fields ...

    pickup_type = serializers.ChoiceField(
        required=False,
        default="one_time",
        choices=[("one_time", "One Time"), ("daily", "Daily"), ("recurring", "Recurring")],
        help_text="The type of pickup: one_time, daily, or recurring",
    )
    recurrence = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="Recurrence configuration for recurring pickups: {days: [], end_date: ''}",
    )
```

#### GraphQL Type Changes

```python
# modules/graph/karrio/server/graph/schemas/base/types.py
import strawberry
from enum import Enum

@strawberry.enum
class PickupTypeEnum(Enum):
    one_time = "one_time"
    daily = "daily"
    recurring = "recurring"


@strawberry.type
class PickupType:
    """GraphQL type for Pickup model."""

    id: str
    object_type: str
    confirmation_number: typing.Optional[str]
    pickup_date: typing.Optional[str]
    pickup_type: typing.Optional[str]  # NEW FIELD
    recurrence: typing.Optional[utils.JSON]  # NEW FIELD
    ready_time: typing.Optional[str]
    closing_time: typing.Optional[str]
    # ... rest of fields
```

#### GraphQL Input Changes

```python
# modules/graph/karrio/server/graph/schemas/base/inputs.py
@strawberry.input
class PickupInput:
    # ... existing fields ...
    pickup_type: typing.Optional[PickupTypeEnum] = strawberry.UNSET
    recurrence: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class PickupFilter(utils.Paginated):
    # ... existing filters ...
    pickup_type: typing.Optional[typing.List[str]] = strawberry.UNSET  # NEW FILTER
```

### Carrier Pickup Type Mapping

| Carrier | Unified `one_time` | Unified `daily` | Unified `recurring` | Notes |
|---------|-------------------|-----------------|---------------------|-------|
| **UPS** | ServiceCode: "06" | ServiceCode: "01" | Not supported | Daily Pickup (01), One Time Pickup (06) |
| **CanadaPost** | PickupType: "OnDemand" | PickupType: "Scheduled" | Not supported | Scheduled = daily/standing |
| **FedEx** | pickupType: "ON_CALL" | pickupType: "REGULAR_STOP" | Not supported | Currently unused in implementation |
| **DHL Express** | RemotePickupFlag: "Y" | Not supported | Not supported | Only one-time supported |
| **DHL Parcel DE** | type: "Date" | Not supported | Not supported | Also has "ASAP" option |
| **MyDHL** | plannedPickupDateAndTime | Not supported | Not supported | One-time only |
| **Purolator** | Default (no type field) | Not supported | Not supported | One-time only |
| **USPS** | Default (no type field) | Not supported | Not supported | One-time only |
| **USPS Intl** | Default (no type field) | Not supported | Not supported | One-time only |
| **Teleship** | Default (no type field) | Not supported | Not supported | One-time only |
| **DPD Meta** | Default (no type field) | Not supported | Not supported | One-time only |
| **Hermes** | Default (no type field) | Not supported | Not supported | One-time only |

### Carrier Implementation Examples

#### UPS Provider Update

```python
# modules/connectors/ups/karrio/providers/ups/units.py
import karrio.lib as lib

class PickupTypeCode(lib.StrEnum):
    """UPS Pickup Type codes."""
    one_time = "06"  # One Time Pickup
    daily = "01"     # Daily Pickup
    # recurring not supported by UPS


# modules/connectors/ups/karrio/providers/ups/pickup/create.py
import karrio.lib as lib
from karrio.providers.ups.units import PickupTypeCode

def pickup_request(payload: models.PickupRequest, settings: Settings) -> lib.Serializable:
    options = lib.units.Options(payload.options, ShippingOption)

    # Map unified pickup_type to UPS code
    pickup_type = payload.pickup_type or "one_time"
    if pickup_type == "recurring":
        raise lib.FieldError({"pickup_type": "UPS does not support recurring pickups. Use 'daily' instead."})

    service_code = PickupTypeCode[pickup_type].value

    request = ups.PickupCreationRequest(
        # ...
        PickupPiece=ups.PickupPieceType(
            ServiceCode=service_code,  # Now dynamically mapped
            Quantity=str(len(payload.parcels)),
            # ...
        ),
        # ...
    )
    return lib.Serializable(request)
```

#### CanadaPost Provider Update

```python
# modules/connectors/canadapost/karrio/providers/canadapost/pickup/create.py
import karrio.lib as lib
from karrio.schemas.canadapost import pickuprequest as canadapost

def pickup_request(payload: models.PickupRequest, settings: Settings) -> lib.Serializable:
    # Map unified pickup_type to CanadaPost enum
    pickup_type = payload.pickup_type or "one_time"
    pickup_type_mapping = {
        "one_time": canadapost.PickupType.ON_DEMAND,
        "daily": canadapost.PickupType.SCHEDULED,
        "recurring": canadapost.PickupType.SCHEDULED,  # Treat recurring as scheduled
    }

    request = canadapost.PickupRequestDetails(
        pickup_type=pickup_type_mapping[pickup_type].value,
        # ...
    )
    return lib.Serializable(request)
```

#### Fallback for Unsupported Carriers

```python
# modules/connectors/purolator/karrio/providers/purolator/pickup/create.py
import karrio.lib as lib

def pickup_request(payload: models.PickupRequest, settings: Settings) -> lib.Serializable:
    # Purolator only supports one-time pickups
    pickup_type = payload.pickup_type or "one_time"
    if pickup_type != "one_time":
        raise lib.FieldError({
            "pickup_type": f"Purolator only supports 'one_time' pickups. Got '{pickup_type}'."
        })

    # ... rest of implementation unchanged
```

### API Changes

**REST Endpoints (unchanged paths, new fields):**

| Method | Endpoint | Changes |
|--------|----------|---------|
| POST | `/v1/pickups/{carrier_name}` | Accept `pickup_type`, `recurrence` in request body |
| GET | `/v1/pickups` | Add `pickup_type` filter parameter |
| GET | `/v1/pickups/{id}` | Response includes `pickup_type`, `recurrence` |

**Request Example:**

```json
{
  "pickup_date": "2025-01-30",
  "ready_time": "09:00",
  "closing_time": "17:00",
  "pickup_type": "daily",
  "recurrence": {
    "end_date": "2025-12-31"
  },
  "address": {
    "address_line1": "125 Church St",
    "city": "Moncton",
    "country_code": "CA",
    "postal_code": "E1C4Z8"
  },
  "parcels_count": 5
}
```

**Response Example:**

```json
{
  "id": "pck_abc123",
  "object_type": "pickup",
  "carrier_name": "ups",
  "carrier_id": "ups_account",
  "confirmation_number": "27241",
  "pickup_date": "2025-01-30",
  "pickup_type": "daily",
  "recurrence": {
    "end_date": "2025-12-31"
  },
  "ready_time": "09:00",
  "closing_time": "17:00",
  "address": {...},
  "parcels": [],
  "parcels_count": 5
}
```

**GraphQL Mutation:**

```graphql
mutation SchedulePickup($input: SchedulePickupMutationInput!) {
  schedule_pickup(input: $input) {
    pickup {
      id
      confirmation_number
      pickup_type
      recurrence
      pickup_date
    }
    errors {
      field
      messages
    }
  }
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| pickup_type not provided | Default to "one_time" | Serializer default value |
| daily/recurring on unsupported carrier | Return validation error | Carrier-specific validation in provider |
| recurring without end_date on carrier requiring it | Return validation error | Carrier-specific validation |
| Update from recurring to one_time | May require cancel + recreate | Document in API response |
| Empty recurrence dict | Ignored, use carrier defaults | No validation error |
| Invalid recurrence.days values | Return validation error | Validate against ["MON","TUE","WED","THU","FRI","SAT","SUN"] |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Carrier API rejects pickup type | Pickup creation fails | Clear error message with supported types |
| Carrier deprecates pickup type code | Silent failures | Monitor carrier API changes, integration tests |
| Database migration fails | Service disruption | Reversible migration, staged rollout |
| GraphQL schema mismatch | Client errors | Versioned schema, deprecation warnings |

---

## Implementation Plan

### Phase 1: SDK & Core Models (S)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add PickupType enum to SDK | `modules/sdk/karrio/core/models.py` | Pending | S |
| Add pickup_type field to PickupRequest | `modules/sdk/karrio/core/models.py` | Pending | S |
| Add recurrence field to PickupRequest | `modules/sdk/karrio/core/models.py` | Pending | S |
| Update server datatypes | `modules/core/karrio/server/core/datatypes.py` | Pending | S |
| Update core serializers | `modules/core/karrio/server/core/serializers.py` | Pending | S |

### Phase 2: Carrier Implementations (L)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| UPS pickup type mapping | `modules/connectors/ups/karrio/providers/ups/pickup/create.py` | Pending | M |
| UPS pickup type enum | `modules/connectors/ups/karrio/providers/ups/units.py` | Pending | S |
| CanadaPost pickup type mapping | `modules/connectors/canadapost/karrio/providers/canadapost/pickup/create.py` | Pending | M |
| FedEx pickup type mapping | `modules/connectors/fedex/karrio/providers/fedex/pickup/create.py` | Pending | M |
| DHL Express fallback | `modules/connectors/dhl_express/karrio/providers/dhl_express/pickup/create.py` | Pending | S |
| DHL Parcel DE fallback | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/pickup/create.py` | Pending | S |
| MyDHL fallback | `modules/connectors/mydhl/karrio/providers/mydhl/pickup/create.py` | Pending | S |
| Purolator fallback | `modules/connectors/purolator/karrio/providers/purolator/pickup/create.py` | Pending | S |
| USPS fallback | `modules/connectors/usps/karrio/providers/usps/pickup/create.py` | Pending | S |
| USPS Intl fallback | `modules/connectors/usps_international/karrio/providers/usps_international/pickup/create.py` | Pending | S |
| Teleship fallback | `modules/connectors/teleship/karrio/providers/teleship/pickup/schedule.py` | Pending | S |
| DPD Meta fallback | `modules/connectors/dpd_meta/karrio/providers/dpd_meta/pickup/create.py` | Pending | S |
| Hermes fallback | `modules/connectors/hermes/karrio/providers/hermes/pickup/create.py` | Pending | S |

### Phase 3: API & GraphQL (M)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update manager PickupSerializer | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | M |
| Update GraphQL PickupType | `modules/graph/karrio/server/graph/schemas/base/types.py` | Pending | S |
| Update GraphQL PickupInput | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Pending | S |
| Update GraphQL PickupFilter | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Pending | S |
| Add pickup_type to Pickup model filter | `modules/core/karrio/server/core/filters.py` | Pending | S |

### Phase 4: Dashboard UI (M)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add pickup type selector to dialog | `packages/ui/components/schedule-pickup-dialog.tsx` | Pending | M |
| Add recurrence options UI | `packages/ui/components/schedule-pickup-dialog.tsx` | Pending | M |
| Update pickup list to show type | `packages/core/modules/Pickups/` | Pending | S |
| Add pickup type filter to list | `packages/core/modules/Pickups/` | Pending | S |

### Phase 5: Tests (L)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| UPS pickup type tests | `modules/connectors/ups/tests/ups/test_pickup.py` | Pending | M |
| CanadaPost pickup type tests | `modules/connectors/canadapost/tests/canadapost/test_pickup.py` | Pending | M |
| FedEx pickup type tests | `modules/connectors/fedex/tests/fedex/test_pickup.py` | Pending | M |
| DHL Express pickup type tests | `modules/connectors/dhl_express/tests/dhl_express/test_pickup.py` | Pending | S |
| Remaining carrier tests (8) | Various test_pickup.py files | Pending | M |
| API integration tests | `modules/manager/karrio/server/manager/tests/test_pickups.py` | Pending | M |
| GraphQL pickup tests | `modules/graph/karrio/server/graph/tests/test_pickups.py` | Pending | M |

**Dependencies:** Phase 2 depends on Phase 1. Phase 3 depends on Phase 1. Phase 4 depends on Phase 3. Phase 5 can run in parallel with Phase 4.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Carrier Unit Tests | `modules/connectors/*/tests/*/test_pickup.py` | All 12 carriers |
| API Integration Tests | `modules/manager/karrio/server/manager/tests/test_pickups.py` | All pickup_type values |
| GraphQL Tests | `modules/graph/karrio/server/graph/tests/test_pickups.py` | Mutations and queries |

### Test Cases

#### Carrier Unit Test Example (UPS)

```python
# modules/connectors/ups/tests/ups/test_pickup.py
import unittest
from unittest.mock import patch, ANY
from karrio.providers.ups.pickup import create

class TestUPSPickupType(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_pickup_request_one_time(self):
        """Verify one_time pickup maps to ServiceCode 06."""
        request = create.pickup_request(
            PickupRequestOneTime,  # payload with pickup_type="one_time"
            SETTINGS,
        )
        serialized = request.serialize()

        self.assertEqual(
            serialized["PickupCreationRequest"]["PickupPiece"]["ServiceCode"],
            "06"
        )

    def test_pickup_request_daily(self):
        """Verify daily pickup maps to ServiceCode 01."""
        request = create.pickup_request(
            PickupRequestDaily,  # payload with pickup_type="daily"
            SETTINGS,
        )
        serialized = request.serialize()

        self.assertEqual(
            serialized["PickupCreationRequest"]["PickupPiece"]["ServiceCode"],
            "01"
        )

    def test_pickup_request_recurring_error(self):
        """Verify recurring pickup raises error for UPS."""
        with self.assertRaises(Exception) as context:
            create.pickup_request(
                PickupRequestRecurring,  # payload with pickup_type="recurring"
                SETTINGS,
            )

        self.assertIn("does not support recurring", str(context.exception))


# Test payloads
PickupRequestOneTime = {
    "pickup_date": "2025-01-30",
    "pickup_type": "one_time",
    # ... rest of fields
}

PickupRequestDaily = {
    "pickup_date": "2025-01-30",
    "pickup_type": "daily",
    # ... rest of fields
}

PickupRequestRecurring = {
    "pickup_date": "2025-01-30",
    "pickup_type": "recurring",
    "recurrence": {"end_date": "2025-12-31"},
    # ... rest of fields
}
```

#### API Integration Test

```python
# modules/manager/karrio/server/manager/tests/test_pickups.py
class TestPickupTypes(TestFixture):
    def test_schedule_pickup_daily(self):
        """Test scheduling a daily pickup."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="ups"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_DAILY_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA_DAILY)
            # print(response.content)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response_data["pickup_type"], "daily")

    def test_schedule_pickup_invalid_type_for_carrier(self):
        """Test validation error for unsupported pickup type."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="purolator"),
        )

        response = self.client.post(f"{url}", PICKUP_DATA_DAILY)
        # print(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("errors", response_data)


PICKUP_DATA_DAILY = {
    "pickup_date": "2025-01-30",
    "pickup_type": "daily",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "address": {...},
    "parcels_count": 3,
}

SCHEDULE_DAILY_RETURNED_VALUE = [
    PickupDetails(
        carrier_id="ups",
        carrier_name="ups",
        confirmation_number="27241",
        pickup_date="2025-01-30",
        meta={"pickup_type": "daily"},
    ),
    [],
]
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run single carrier pickup tests
python -m unittest discover -v -f modules/connectors/ups/tests

# Run all carrier pickup tests
for carrier in ups fedex canadapost dhl_express dhl_parcel_de mydhl purolator usps usps_international teleship dpd_meta hermes; do
  python -m unittest discover -v -f modules/connectors/$carrier/tests
done

# Run API tests
karrio test --failfast karrio.server.manager.tests.test_pickups

# Run GraphQL tests
karrio test --failfast karrio.server.graph.tests.test_pickups
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Carrier API changes pickup type codes | High | Low | Integration tests, monitoring, carrier changelog reviews |
| Breaking existing API consumers | High | Low | Default to one_time, backward compatible changes only |
| Database migration issues | Medium | Low | Reversible migration, no schema changes needed (uses existing options/meta) |
| UI complexity for users | Medium | Medium | Clear UI labels, tooltips, hide advanced options initially |
| Inconsistent carrier support | Low | High | Clear documentation, error messages listing supported types per carrier |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: Existing requests without `pickup_type` will default to `"one_time"`, preserving current behavior
- **Data compatibility**: No database schema changes required; pickup_type can be stored in existing `options` or `meta` JSON fields
- **Feature flags**: Not needed - additive change only

### Database Migration

No database migration required. The `pickup_type` and `recurrence` fields are:
1. Optional with defaults
2. Can be stored in existing `Pickup.meta` JSON field if persistence is needed
3. Primarily used for carrier API requests, not for record-keeping

### Rollback Procedure

1. **Identify issue**: Monitor error rates on pickup endpoints after deploy
2. **Stop rollout**: Revert frontend changes first (remove pickup_type selector)
3. **Revert changes**: Backend changes are backward compatible, can remain deployed
4. **Verify recovery**: Confirm existing pickup flows work normally

---

## Appendices

### Appendix A: Carrier Pickup Type Reference

| Carrier | API Documentation | Pickup Type Field | Supported Values |
|---------|-------------------|-------------------|------------------|
| UPS | [UPS Developer Kit](https://developer.ups.com) | `ServiceCode` | 01 (Daily), 06 (One Time) |
| CanadaPost | [Canada Post API](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/) | `pickup-type` | OnDemand, Scheduled |
| FedEx | [FedEx Developer Portal](https://developer.fedex.com) | `pickupType` | ON_CALL, PACKAGE_RETURN_PROGRAM, REGULAR_STOP |
| DHL Express | [DHL Developer Portal](https://developer.dhl.com) | `RemotePickupFlag` | Y (one-time only) |
| DHL Parcel DE | [DHL Parcel DE API](https://developer.dhl.com) | `type` in pickupDate | Date, ASAP |
| Purolator | [Purolator E-Ship](https://eship.purolator.com) | N/A | One-time only |
| USPS | [USPS Web Tools](https://www.usps.com/business/web-tools-apis/) | N/A | One-time only |

### Appendix B: Pickup Type Value Mapping

```python
# Complete mapping table for implementation reference
CARRIER_PICKUP_TYPE_MAPPING = {
    "ups": {
        "one_time": "06",
        "daily": "01",
        "recurring": None,  # Not supported
    },
    "canadapost": {
        "one_time": "OnDemand",
        "daily": "Scheduled",
        "recurring": "Scheduled",
    },
    "fedex": {
        "one_time": "ON_CALL",
        "daily": "REGULAR_STOP",
        "recurring": None,  # Not supported
    },
    "dhl_express": {
        "one_time": "Y",  # RemotePickupFlag
        "daily": None,
        "recurring": None,
    },
    "dhl_parcel_de": {
        "one_time": "Date",
        "daily": None,
        "recurring": None,
    },
    # All other carriers: one_time only (no type field)
    "mydhl": {"one_time": None, "daily": None, "recurring": None},
    "purolator": {"one_time": None, "daily": None, "recurring": None},
    "usps": {"one_time": None, "daily": None, "recurring": None},
    "usps_international": {"one_time": None, "daily": None, "recurring": None},
    "teleship": {"one_time": None, "daily": None, "recurring": None},
    "dpd_meta": {"one_time": None, "daily": None, "recurring": None},
    "hermes": {"one_time": None, "daily": None, "recurring": None},
}
```

### Appendix C: Files to Modify Summary

| Layer | Files | Change Type |
|-------|-------|-------------|
| SDK | `modules/sdk/karrio/core/models.py` | Add PickupType enum, add fields |
| Server Core | `modules/core/karrio/server/core/datatypes.py` | Add fields |
| Server Core | `modules/core/karrio/server/core/serializers.py` | Add fields with validation |
| Manager | `modules/manager/karrio/server/manager/serializers/pickup.py` | Handle new fields |
| GraphQL | `modules/graph/karrio/server/graph/schemas/base/types.py` | Add fields |
| GraphQL | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Add fields |
| Filters | `modules/core/karrio/server/core/filters.py` | Add pickup_type filter |
| UPS | `modules/connectors/ups/karrio/providers/ups/units.py` | Add PickupTypeCode enum |
| UPS | `modules/connectors/ups/karrio/providers/ups/pickup/create.py` | Map pickup_type |
| CanadaPost | `modules/connectors/canadapost/karrio/providers/canadapost/pickup/create.py` | Map pickup_type |
| FedEx | `modules/connectors/fedex/karrio/providers/fedex/pickup/create.py` | Map pickup_type |
| 9 Other Carriers | Various pickup/create.py files | Add validation/fallback |
| Tests (12 carriers) | Various test_pickup.py files | Add pickup type tests |
| API Tests | `modules/manager/karrio/server/manager/tests/test_pickups.py` | Add pickup type tests |
| GraphQL Tests | `modules/graph/karrio/server/graph/tests/test_pickups.py` | Add pickup type tests |
| Dashboard | `packages/ui/components/schedule-pickup-dialog.tsx` | Add pickup type selector |
| Dashboard | `packages/core/modules/Pickups/` | Update list and filters |

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [x] All pending questions in "Open Questions & Decisions" have been identified
- [x] All user decisions documented with rationale and date
- [x] Edge cases requiring input have been resolved

CODE ANALYSIS:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (karrio.lib, hooks, components)

CONTENT:
- [x] All required sections completed
- [x] Code examples follow AGENTS.md style EXACTLY as original authors
- [x] Architecture diagrams included (overview, sequence, dataflow - ASCII art)
- [x] Tables used for structured data (not prose)
- [x] Before/After code shown in Problem Statement
- [x] Success criteria are measurable
- [x] Alternatives considered and documented
- [x] Edge cases and failure modes identified

TESTING:
- [x] Test cases follow unittest patterns (NOT pytest)
- [x] Test examples use assertDictEqual/assertListEqual with mock.ANY

RISK & MIGRATION:
- [x] Risk assessment completed
- [x] Migration/rollback plan documented
-->
