# Product Requirements Document: Enhanced TrackingEvent Fields

**Project**: TrackingEvent Enhancement - timestamp, status, reason fields + picked_up status
**Version**: 1.1
**Date**: 2025-12-16
**Status**: Planning
**Owner**: Engineering Team
**Reference**: All implementation must follow `AGENTS.md` coding guidelines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Success Criteria](#goals--success-criteria)
4. [Technical Architecture](#technical-architecture)
5. [SDK/Core Changes](#sdkcore-changes)
6. [Carrier Integration Changes](#carrier-integration-changes)
7. [Server-Side Changes](#server-side-changes)
8. [Testing Strategy](#testing-strategy)
9. [Implementation Plan](#implementation-plan)
10. [Migration Strategy](#migration-strategy)
11. [Risk Assessment](#risk-assessment)

---

## Executive Summary

This document outlines the enhancement of the `TrackingEvent` model and `TrackerStatus` enum to provide richer tracking information:

### New TrackingEvent Fields
1. **`timestamp`**: ISO 8601 formatted datetime string (e.g., `2025-12-04T07:16:00.000Z`) - the canonical datetime for each event
2. **`status`**: Normalized tracking status per event using `TrackerStatus` enum values
3. **`reason`**: Normalized incident/exception reason using new `TrackingIncidentReason` enum

### New TrackerStatus Value
4. **`picked_up`**: New status representing the first milestone after `pending` - when the carrier has physically picked up the package (before `in_transit`)

### Key Architecture Decisions

1. **Backward Compatible**: Keep existing `date` and `time` fields alongside new `timestamp` field
2. **Unified Status Enum**: Reuse and extend existing `TrackerStatus` enum for event-level status
3. **New Reason Enum**: Create `TrackingIncidentReason` enum following the `TrackingStatus` pattern with `.map()` functionality
4. **Normalized Only**: The `reason` field will contain only normalized enum values (not raw carrier text)
5. **Universal Application**: Code processes all events, but returns `None` for non-exception events

**Timeline**: 2-3 weeks
**Risk Level**: LOW (additive changes, backward compatible)
**User Impact**: Enhanced tracking visibility with standardized event statuses and failure reasons

---

## Problem Statement

### Current State

**TrackingEvent Model** (Current):
```python
@attr.s(auto_attribs=True)
class TrackingEvent:
    date: str           # "2025-12-04" - date only
    description: str    # Carrier's text description
    code: str = None    # Carrier's raw event code
    time: str = None    # "07:16 AM" - time only, inconsistent format
    reason: str = None  # Free-form text (rarely used)
    location: str = None
    latitude: float = None
    longitude: float = None
```

**TrackerStatus Enum** (Current):
```python
class TrackerStatus(utils.Enum):
    pending = "pending"
    unknown = "unknown"
    on_hold = "on_hold"
    cancelled = "cancelled"
    delivered = "delivered"
    in_transit = "in_transit"           # <-- No distinction between pickup and transit
    delivery_delayed = "delivery_delayed"
    out_for_delivery = "out_for_delivery"
    ready_for_pickup = "ready_for_pickup"
    delivery_failed = "delivery_failed"
    return_to_sender = "return_to_sender"
```

**Problems**:

1. **No Unified Timestamp**: `date` and `time` are separate fields with inconsistent formats across carriers
2. **No Event-Level Status**: Status is only available at tracker level, not per-event
3. **Missing Pickup Milestone**: No way to distinguish between "info received" (`pending`) and "physically picked up" - both fall under `pending` or jump straight to `in_transit`
4. **Unstandardized Reasons**: `reason` field contains free-form text or is empty, making it difficult to:
   - Filter events by failure type
   - Build analytics on delivery issues
   - Create automated responses to specific failure categories

### Desired State

**TrackingEvent Model** (Enhanced):
```python
@attr.s(auto_attribs=True)
class TrackingEvent:
    date: str                    # Keep for backward compatibility
    description: str             # Carrier's original description
    code: str = None             # Carrier's raw event code
    time: str = None             # Keep for backward compatibility
    timestamp: str = None        # NEW: "2025-12-04T07:16:00.000Z" ISO 8601
    status: str = None           # NEW: Normalized status (TrackerStatus enum)
    reason: str = None           # ENHANCED: Normalized reason (TrackingIncidentReason enum)
    location: str = None
    latitude: float = None
    longitude: float = None
```

**TrackerStatus Enum** (Enhanced):
```python
class TrackerStatus(utils.Enum):
    pending = "pending"              # Shipment info received, awaiting pickup
    picked_up = "picked_up"          # NEW: Package physically picked up by carrier
    unknown = "unknown"
    on_hold = "on_hold"
    cancelled = "cancelled"
    delivered = "delivered"
    in_transit = "in_transit"        # Package moving through carrier network
    delivery_delayed = "delivery_delayed"
    out_for_delivery = "out_for_delivery"
    ready_for_pickup = "ready_for_pickup"
    delivery_failed = "delivery_failed"
    return_to_sender = "return_to_sender"
```

### Tracking Status Lifecycle

```
pending → picked_up → in_transit → out_for_delivery → delivered
                  ↓           ↓              ↓
              on_hold    delivery_delayed  delivery_failed
                  ↓           ↓              ↓
            ready_for_pickup  ←  return_to_sender
```

---

## Goals & Success Criteria

### Goals

1. **Standardize Event Timestamps**: Provide a single, consistent ISO 8601 timestamp field
2. **Event-Level Status**: Enable per-event status tracking for detailed shipment journey visualization
3. **Capture Pickup Milestone**: Distinguish between "info received" and "physically picked up"
4. **Categorize Delivery Issues**: Normalize carrier-specific failure codes into standard categories
5. **Enable Analytics**: Support querying/filtering events by status and failure reason

### Success Criteria

| Metric | Target |
|--------|--------|
| All connectors updated | 100% of active connectors |
| Backward compatibility | Zero breaking changes to existing API consumers |
| Reason coverage | 80%+ of carrier exception codes mapped |
| Test coverage | Unit tests for all new enum mappings |
| Server tests passing | All Django tests pass |
| SDK tests passing | All unittest tests pass |

---

## Technical Architecture

### TrackerStatus Enum Update

Update `karrio/core/units.py` and `karrio/server/core/serializers.py`:

```python
class TrackingStatus(utils.Enum):
    pending = ["pending"]
    picked_up = ["picked_up"]        # NEW: After pending, before in_transit
    on_hold = ["on_hold"]
    cancelled = ["cancelled"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
    return_to_sender = ["return_to_sender"]
    unknown = ["unknown"]
```

### New TrackingIncidentReason Enum

Following the `TrackingStatus` pattern, create a new enum in `karrio/core/units.py`:

```python
class TrackingIncidentReason(utils.Enum):
    """Normalized tracking incident/exception reason codes.

    Categories:
    - carrier_*: Issues caused by the carrier during handling/transit
    - retailer_*: Issues caused by the shipper/retailer
    - consignee_*: Issues caused by or related to the recipient
    - customs_*: Customs-related delays or issues
    - weather_*: Weather-related delays
    - other_*: Miscellaneous issues
    """

    # Carrier-caused issues
    carrier_damaged_parcel = ["carrier_damaged_parcel"]
    carrier_sorting_error = ["carrier_sorting_error"]
    carrier_address_not_found = ["carrier_address_not_found"]
    carrier_parcel_lost = ["carrier_parcel_lost"]
    carrier_not_enough_time_in_timeslot = ["carrier_not_enough_time_in_timeslot"]
    carrier_vehicle_issue = ["carrier_vehicle_issue"]
    carrier_capacity_exceeded = ["carrier_capacity_exceeded"]

    # Retailer/Shipper-caused issues
    retailer_delivery_cancelled_by_store = ["retailer_delivery_cancelled_by_store"]
    retailer_incorrect_delivery_data = ["retailer_incorrect_delivery_data"]
    retailer_parcel_not_ready_at_pickup = ["retailer_parcel_not_ready_at_pickup"]
    retailer_parcel_not_correct = ["retailer_parcel_not_correct"]
    retailer_incorrect_size_registered = ["retailer_incorrect_size_registered"]
    retailer_packaging_issue = ["retailer_packaging_issue"]

    # Consignee/Recipient-caused issues
    consignee_refused_at_door = ["consignee_refused_at_door"]
    consignee_company_closed = ["consignee_company_closed"]
    consignee_not_delivered = ["consignee_not_delivered"]
    consignee_customer_not_home = ["consignee_customer_not_home"]
    consignee_cancelled_by_customer = ["consignee_cancelled_by_customer"]
    consignee_verification_failed = ["consignee_verification_failed"]
    consignee_incorrect_address = ["consignee_incorrect_address"]
    consignee_access_restricted = ["consignee_access_restricted"]
    consignee_safe_place_not_available = ["consignee_safe_place_not_available"]

    # Customs-related issues
    customs_clearance_delay = ["customs_clearance_delay"]
    customs_documentation_required = ["customs_documentation_required"]
    customs_duties_unpaid = ["customs_duties_unpaid"]
    customs_prohibited_items = ["customs_prohibited_items"]
    customs_inspection_required = ["customs_inspection_required"]

    # Weather/Force majeure
    weather_delay = ["weather_delay"]
    natural_disaster = ["natural_disaster"]
    force_majeure = ["force_majeure"]

    # Other issues
    other_parcel_being_researched = ["other_parcel_being_researched"]
    other_security_issue = ["other_security_issue"]
    other_regulatory_hold = ["other_regulatory_hold"]
    other_unknown = ["other_unknown"]
```

### Enum Mapping Pattern

Each carrier connector will define enums in their `units.py` following the established pattern:

```python
# In karrio/providers/{carrier}/units.py

class TrackingStatus(lib.Enum):
    """Maps {CARRIER} status codes to normalized TrackingStatus."""

    pending = ["LABEL_CREATED", "SHIPMENT_INFORMATION_RECEIVED"]
    picked_up = ["PU", "PICKED_UP", "PICKUP_SCAN", "OR"]  # NEW
    in_transit = ["IT", "IN_TRANSIT", "DEPARTED", "ARRIVED"]
    # ... more mappings

class TrackingIncidentReason(lib.Enum):
    """Maps {CARRIER} exception codes to normalized TrackingIncidentReason."""

    carrier_damaged_parcel = ["DMG", "DAMAGED", "PKG_DAMAGE"]
    consignee_customer_not_home = ["NAH", "NOT_HOME", "RECIPIENT_ABSENT"]
    consignee_refused_at_door = ["REF", "REFUSED", "DELIVERY_REFUSED"]
    carrier_address_not_found = ["ANF", "ADDR_NOT_FOUND", "BAD_ADDRESS"]
    # ... more mappings
```

---

## SDK/Core Changes

### 1. Update `karrio/core/models.py`

```python
@attr.s(auto_attribs=True)
class TrackingEvent:
    """Karrio unified tracking event data type."""

    date: str
    description: str
    code: str = None
    time: str = None
    timestamp: str = None      # NEW: ISO 8601 format "2025-12-04T07:16:00.000Z"
    status: str = None         # NEW: TrackerStatus enum value name
    reason: str = None         # ENHANCED: TrackingIncidentReason enum value name
    location: str = None

    # Geolocation
    latitude: float = None
    longitude: float = None
```

### 2. Update `karrio/core/units.py`

Update `TrackingStatus` and add `TrackingIncidentReason`:

```python
class TrackingStatus(utils.Enum):
    pending = ["pending"]
    picked_up = ["picked_up"]        # NEW
    on_hold = ["on_hold"]
    cancelled = ["cancelled"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
    return_to_sender = ["return_to_sender"]
    unknown = ["unknown"]


class TrackingIncidentReason(utils.Enum):
    """Normalized tracking incident/exception reason codes."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["carrier_damaged_parcel"]
    carrier_sorting_error = ["carrier_sorting_error"]
    carrier_address_not_found = ["carrier_address_not_found"]
    carrier_parcel_lost = ["carrier_parcel_lost"]
    carrier_not_enough_time = ["carrier_not_enough_time"]
    carrier_vehicle_issue = ["carrier_vehicle_issue"]
    carrier_capacity_exceeded = ["carrier_capacity_exceeded"]
    carrier_mechanical_delay = ["carrier_mechanical_delay"]

    # Retailer/Shipper-caused issues
    retailer_cancelled = ["retailer_cancelled"]
    retailer_incorrect_data = ["retailer_incorrect_data"]
    retailer_not_ready = ["retailer_not_ready"]
    retailer_incorrect_parcel = ["retailer_incorrect_parcel"]
    retailer_incorrect_dimensions = ["retailer_incorrect_dimensions"]
    retailer_packaging_issue = ["retailer_packaging_issue"]

    # Consignee/Recipient-caused issues
    consignee_refused = ["consignee_refused"]
    consignee_business_closed = ["consignee_business_closed"]
    consignee_not_available = ["consignee_not_available"]
    consignee_not_home = ["consignee_not_home"]
    consignee_cancelled = ["consignee_cancelled"]
    consignee_verification_failed = ["consignee_verification_failed"]
    consignee_incorrect_address = ["consignee_incorrect_address"]
    consignee_access_restricted = ["consignee_access_restricted"]
    consignee_safe_place_unavailable = ["consignee_safe_place_unavailable"]

    # Customs-related issues
    customs_delay = ["customs_delay"]
    customs_documentation = ["customs_documentation"]
    customs_duties_unpaid = ["customs_duties_unpaid"]
    customs_prohibited = ["customs_prohibited"]
    customs_inspection = ["customs_inspection"]

    # Weather/Force majeure
    weather_delay = ["weather_delay"]
    natural_disaster = ["natural_disaster"]
    force_majeure = ["force_majeure"]

    # Other issues
    parcel_being_researched = ["parcel_being_researched"]
    security_issue = ["security_issue"]
    regulatory_hold = ["regulatory_hold"]
    unknown = ["unknown"]
```

### 3. Update `karrio/lib.py`

Add helper function for timestamp generation:

```python
def ftimestamp(
    date_str: str = None,
    time_str: str = None,
    current_format: str = None,
    try_formats: list = None,
) -> str:
    """Convert date and time strings to ISO 8601 timestamp.

    Args:
        date_str: Date string or combined datetime string
        time_str: Optional time string (if separate from date)
        current_format: Expected format of the input
        try_formats: List of formats to try parsing

    Returns:
        ISO 8601 format string "2025-12-04T07:16:00.000Z" or None
    """
    if not date_str:
        return None

    # Implementation using functional style per AGENTS.md
    import datetime

    formats_to_try = try_formats or [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]

    combined = f"{date_str} {time_str}".strip() if time_str else date_str

    parsed = next(
        (
            datetime.datetime.strptime(combined, fmt)
            for fmt in formats_to_try
            if _try_parse(combined, fmt)
        ),
        None,
    )

    return parsed.strftime("%Y-%m-%dT%H:%M:%S.000Z") if parsed else None


def _try_parse(date_str: str, fmt: str) -> bool:
    """Attempt to parse a date string with given format."""
    try:
        datetime.datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False
```

### 4. Update CLI Template `karrio_cli/templates/tracking.py`

Update the template to include new fields with functional style:

```python
def _extract_details(data, settings, tracking_number):
    # ... existing code ...

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event["date"]),
                time=lib.flocaltime(event["time"]),
                timestamp=lib.ftimestamp(event["date"], event["time"]),
                status=provider_units.TrackingStatus.map(event["code"]).name,
                code=event["code"],
                location=event["location"],
                description=event["description"],
                reason=provider_units.TrackingIncidentReason.map(event["code"]).name,
            )
            for event in events
        ],
        # ...
    )
```

---

## Carrier Integration Changes

### Finding Carrier Event Code Documentation

> **IMPORTANT**: When mapping carrier event codes to normalized statuses and reasons:
>
> 1. **Check the connection extension vendor folder first** (when it exists):
>    - `modules/connectors/{carrier}/vendor/` - May contain carrier API documentation, event code references, or status mapping guides
>    - `community/plugins/{carrier}/vendor/` - Same for community plugins
>    - `ee/insiders/modules/connectors/{carrier}/vendor/` - Same for insiders connectors
>
> 2. **Reuse existing codes from `units.py`**: If the connector already has a `TrackingStatus` enum defined, use those existing carrier code mappings as the foundation and extend them with `picked_up` and `TrackingIncidentReason` mappings.
>
> 3. **Carrier API documentation**: Consult official carrier API docs for comprehensive event/status code lists when vendor folder doesn't exist.

### Pattern for Each Connector

Each carrier connector needs to be updated in two files:

#### 1. `units.py` - Update TrackingStatus and add TrackingIncidentReason

```python
class TrackingStatus(lib.Enum):
    """Maps {CARRIER} status codes to normalized TrackingStatus."""

    pending = ["M", "MV", "LABEL_CREATED"]
    picked_up = ["PU", "OR", "PICKED_UP", "PICKUP_SCAN"]  # NEW
    in_transit = ["I", "IT", "DP", "AA", "AR"]
    delivered = ["D", "DL", "DELIVERED"]
    # ... more mappings


class TrackingIncidentReason(lib.Enum):
    """Maps {CARRIER} exception codes to normalized TrackingIncidentReason."""

    carrier_damaged_parcel = ["DMG", "PACKAGE_DAMAGED"]
    consignee_not_home = ["NAH", "RECIPIENT_NOT_HOME", "12"]
    consignee_refused = ["REF", "DELIVERY_REFUSED"]
    # ... carrier-specific mappings
```

#### 2. `tracking.py` - Update event extraction

```python
def _extract_details(data, settings, tracking_number):
    # Functional style per AGENTS.md - use comprehensions, avoid nested if/for

    events = [
        models.TrackingEvent(
            date=lib.fdate(e.date),
            time=lib.flocaltime(e.time),
            timestamp=lib.ftimestamp(e.date, e.time),
            status=provider_units.TrackingStatus.map(e.code).name,
            code=e.code,
            location=e.location,
            description=e.description,
            reason=provider_units.TrackingIncidentReason.map(e.code).name,
        )
        for e in raw_events
    ]

    return models.TrackingDetails(
        # ...
        events=events,
        status=events[0].status if events else "pending",
    )
```

### Connectors to Update

#### Core Connectors (`modules/connectors/`)
| Connector | Priority | Notes |
|-----------|----------|-------|
| ups | HIGH | Add `picked_up` codes: PU, OR |
| fedex | HIGH | Add `picked_up` codes: PU, OC |
| dhl_express | HIGH | Add `picked_up` codes: PU, PL |
| canadapost | HIGH | Add `picked_up` codes: 100-199 range |
| usps | HIGH | Add `picked_up` codes: PU, PICKED_UP |
| purolator | MEDIUM | |
| dhl_parcel_de | MEDIUM | |
| sendle | MEDIUM | |
| aramex | MEDIUM | |

#### Community Plugins (`community/plugins/`)
| Connector | Priority | Notes |
|-----------|----------|-------|
| easypost | LOW | Aggregator |
| shippo | LOW | Aggregator |

---

## Server-Side Changes

### 1. Update `karrio/server/core/serializers.py`

#### Add TrackerStatus enum constant update:

```python
class TrackerStatus(utils.Enum):
    pending = "pending"
    picked_up = "picked_up"          # NEW
    unknown = "unknown"
    on_hold = "on_hold"
    cancelled = "cancelled"
    delivered = "delivered"
    in_transit = "in_transit"
    delivery_delayed = "delivery_delayed"
    out_for_delivery = "out_for_delivery"
    ready_for_pickup = "ready_for_pickup"
    delivery_failed = "delivery_failed"
    return_to_sender = "return_to_sender"


TRACKER_STATUS = [(c.name, c.name) for c in list(TrackerStatus)]
TRACKING_INCIDENT_REASONS = [(c.name, c.name) for c in list(units.TrackingIncidentReason)]
```

#### Update TrackingEvent serializer:

```python
class TrackingEvent(serializers.Serializer):
    date = serializers.CharField(
        required=False,
        help_text="The tracking event's date. Format: `YYYY-MM-DD`"
    )
    time = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The tracking event's time. Format: `HH:MM AM/PM`",
    )
    timestamp = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The tracking event's timestamp. Format: `YYYY-MM-DDTHH:MM:SS.sssZ` (ISO 8601)",
    )
    status = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        allow_null=True,
        choices=TRACKER_STATUS,
        help_text="The normalized status of this specific event",
    )
    code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The tracking event's code",
    )
    reason = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        allow_null=True,
        choices=TRACKING_INCIDENT_REASONS,
        help_text="The normalized incident reason (for exception events only)",
    )
    description = serializers.CharField(
        required=False,
        help_text="The tracking event's description"
    )
    location = serializers.CharField(
        required=False,
        help_text="The tracking event's location"
    )
    latitude = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="The tracking event's latitude.",
    )
    longitude = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="The tracking event's longitude.",
    )
```

### 2. Update `karrio/server/manager/models.py`

The `Tracking` model uses a JSONField for `events`, so no schema migration is needed. However, ensure the model's `status` field choices include `picked_up`:

```python
# In the Tracking model class
status = models.CharField(
    max_length=25,
    choices=serializers.TRACKER_STATUS,  # Will include picked_up after serializer update
    default=serializers.TRACKER_STATUS[0][0],
    db_index=True,
)
```

### 3. Update `karrio/server/manager/serializers/tracking.py`

Update any status mapping logic in `update_shipment_tracker`:

```python
def update_shipment_tracker(tracker: models.Tracking):
    try:
        status_mapping = {
            TrackerStatus.delivered.value: ShipmentStatus.delivered.value,
            TrackerStatus.pending.value: tracker.shipment.status,
            TrackerStatus.picked_up.value: ShipmentStatus.shipped.value,  # NEW
            TrackerStatus.out_for_delivery.value: ShipmentStatus.out_for_delivery.value,
            TrackerStatus.delivery_failed.value: ShipmentStatus.delivery_failed.value,
        }

        status = status_mapping.get(
            tracker.status,
            (
                ShipmentStatus.needs_attention.value
                if tracker.status in [TrackerStatus.on_hold.value, TrackerStatus.delivery_delayed.value]
                else ShipmentStatus.in_transit.value
            ),
        )

        if tracker.shipment is not None and tracker.shipment.status != status:
            tracker.shipment.status = status
            tracker.shipment.save(update_fields=["status"])
    except Exception as e:
        logger.exception("Failed to update the tracked shipment", error=str(e))
```

### 4. Update GraphQL Types (if applicable)

Update `karrio/server/graph/schemas/base/types.py` if GraphQL types exist for tracking.

---

## Testing Strategy

> **IMPORTANT**: All tests must follow `AGENTS.md` guidelines:
> - Use `unittest` for carrier integrations (NOT pytest)
> - Use Django tests via `karrio` for server tests
> - Run tests from repository root
> - Use functional, declarative style
> - Prefer comprehensive `assertDictEqual`/`assertListEqual` over multiple single assertions
> - Use `mock.ANY` for dynamic fields

### SDK/Connector Tests

#### File: `modules/connectors/{carrier}/tests/test_tracking.py`

```python
"""Test {CARRIER} tracking with enhanced fields."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{Carrier}Tracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_parse_tracking_response_with_enhanced_fields(self):
        """Verify tracking response includes timestamp, status, and reason fields."""
        with patch("karrio.mappers.{carrier}.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_with_exception_event(self):
        """Verify reason field is populated for exception events."""
        with patch("karrio.mappers.{carrier}.proxy.lib.request") as mock:
            mock.return_value = TrackingExceptionResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            # Verify reason is populated for delivery_failed status
            events = parsed_response[0][0]["events"]
            failed_event = next(
                (e for e in events if e["status"] == "delivery_failed"), None
            )
            self.assertIsNotNone(failed_event)
            self.assertIsNotNone(failed_event["reason"])

    def test_parse_tracking_picked_up_status(self):
        """Verify picked_up status is correctly identified."""
        with patch("karrio.mappers.{carrier}.proxy.lib.request") as mock:
            mock.return_value = TrackingPickedUpResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            events = parsed_response[0][0]["events"]
            picked_up_event = next(
                (e for e in events if e["status"] == "picked_up"), None
            )
            self.assertIsNotNone(picked_up_event)


if __name__ == "__main__":
    unittest.main()


# Test fixtures
TrackingPayload = {
    "tracking_numbers": ["1Z999999999999999"],
}

TrackingResponse = """..."""  # Carrier-specific response

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "{carrier}",
            "carrier_name": "{carrier}",
            "tracking_number": "1Z999999999999999",
            "status": "in_transit",
            "delivered": False,
            "events": [
                {
                    "date": "2025-12-04",
                    "time": "07:16 AM",
                    "timestamp": "2025-12-04T07:16:00.000Z",
                    "status": "in_transit",
                    "code": "IT",
                    "reason": None,
                    "description": "In Transit",
                    "location": "New York, NY",
                    "latitude": None,
                    "longitude": None,
                },
                {
                    "date": "2025-12-03",
                    "time": "09:30 AM",
                    "timestamp": "2025-12-03T09:30:00.000Z",
                    "status": "picked_up",
                    "code": "PU",
                    "reason": None,
                    "description": "Picked Up",
                    "location": "Los Angeles, CA",
                    "latitude": None,
                    "longitude": None,
                },
            ],
            "estimated_delivery": ANY,
            "meta": ANY,
        }
    ],
    [],
]
```

### Server/Django Tests

#### File: `modules/manager/karrio/server/manager/tests/test_tracking.py`

```python
"""Test tracking serializers and models with enhanced fields."""

from django.test import TestCase
from unittest.mock import patch, ANY

from karrio.server.core.serializers import TrackerStatus, TrackingEvent
from karrio.server.manager.serializers.tracking import (
    TrackingSerializer,
    update_shipment_tracker,
)


class TrackingEnhancedFieldsTestCase(TestCase):
    """Test enhanced tracking event fields."""

    def test_tracker_status_includes_picked_up(self):
        """Verify TrackerStatus enum includes picked_up value."""
        status_values = [s.value for s in TrackerStatus]
        self.assertIn("picked_up", status_values)

    def test_tracking_event_serializer_fields(self):
        """Verify TrackingEvent serializer includes new fields."""
        serializer = TrackingEvent()
        field_names = set(serializer.fields.keys())
        expected_fields = {
            "date", "time", "timestamp", "status", "code",
            "reason", "description", "location", "latitude", "longitude"
        }
        self.assertEqual(field_names, expected_fields)

    def test_tracking_event_serializer_validates_status(self):
        """Verify status field accepts valid TrackerStatus values."""
        data = {
            "date": "2025-12-04",
            "status": "picked_up",
            "description": "Package picked up",
        }
        serializer = TrackingEvent(data=data)
        self.assertTrue(serializer.is_valid())

    def test_tracking_event_serializer_validates_reason(self):
        """Verify reason field accepts valid TrackingIncidentReason values."""
        data = {
            "date": "2025-12-04",
            "status": "delivery_failed",
            "reason": "consignee_not_home",
            "description": "Delivery failed - not home",
        }
        serializer = TrackingEvent(data=data)
        self.assertTrue(serializer.is_valid())

    def test_update_shipment_tracker_picked_up_status(self):
        """Verify picked_up status maps to shipped shipment status."""
        # Setup mock tracker and shipment
        # ...
        pass


class TrackingResponseTestCase(TestCase):
    """Test full tracking response with enhanced fields."""

    def test_tracking_response_structure(self):
        """Verify API response includes all enhanced fields."""
        # Use assertDictEqual for comprehensive comparison per AGENTS.md
        expected_event = {
            "date": "2025-12-04",
            "time": "07:16 AM",
            "timestamp": "2025-12-04T07:16:00.000Z",
            "status": "in_transit",
            "code": "IT",
            "reason": None,
            "description": "In Transit",
            "location": "New York, NY",
            "latitude": None,
            "longitude": None,
        }
        # ... test implementation
        pass
```

### Running Tests

```bash
# From repository root - per AGENTS.md

# Activate environment first
source bin/activate-env

# Run all SDK/connector tests
./bin/run-sdk-tests

# Run single carrier tests
python -m unittest discover -v -f modules/connectors/ups/tests

# Run all server tests
./bin/run-server-tests

# Run single module server tests
karrio test --failfast karrio.server.manager.tests
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)

| Task | Files | Status |
|------|-------|--------|
| Add `picked_up` to `TrackingStatus` enum | `karrio/core/units.py` | Pending |
| Add `TrackingIncidentReason` enum | `karrio/core/units.py` | Pending |
| Update `TrackingEvent` model | `karrio/core/models.py` | Pending |
| Add `lib.ftimestamp()` helper | `karrio/lib.py` | Pending |
| Update CLI tracking template | `karrio_cli/templates/tracking.py` | Pending |
| Update `TrackerStatus` enum | `karrio/server/core/serializers.py` | Pending |
| Update `TrackingEvent` serializer | `karrio/server/core/serializers.py` | Pending |
| Update shipment tracker mapping | `karrio/server/manager/serializers/tracking.py` | Pending |
| Add SDK unit tests | `modules/sdk/tests/` | Pending |
| Add server unit tests | `modules/manager/karrio/server/manager/tests/` | Pending |

### Phase 2: Priority Connectors (Week 1-2)

| Connector | units.py | tracking.py | tests |
|-----------|----------|-------------|-------|
| ups | Update TrackingStatus + add TrackingIncidentReason | Update extraction | Update test_tracking.py |
| fedex | Update TrackingStatus + add TrackingIncidentReason | Update extraction | Update test_tracking.py |
| dhl_express | Update TrackingStatus + add TrackingIncidentReason | Update extraction | Update test_tracking.py |
| canadapost | Update TrackingStatus + add TrackingIncidentReason | Update extraction | Update test_tracking.py |
| usps | Update TrackingStatus + add TrackingIncidentReason | Update extraction | Update test_tracking.py |

### Phase 3: Secondary Connectors (Week 2-3)

| Connector | Status |
|-----------|--------|
| All remaining connectors | Apply same pattern |

### Phase 4: Final Testing & Documentation (Week 3)

| Task | Status |
|------|--------|
| Run full test suite | Pending |
| Update API documentation | Pending |
| Update changelog | Pending |

---

## Migration Strategy

### Database Migration

**No schema migration required** - The `events` field is a JSONField in the `Tracking` model. New fields will be added to new events automatically.

### Existing Data

Existing tracking events will have:
- `timestamp`: `null` (until re-fetched)
- `status`: `null` (until re-fetched)
- `reason`: existing value or `null`

### Backfill Strategy (Optional)

If backfill is desired:
1. Query all trackers with `delivered = False`
2. Re-fetch tracking data from carriers
3. Update events with new field values

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Carrier API changes | Low | Medium | Version-specific mappings |
| Incomplete reason mapping | Medium | Low | Default to `unknown` |
| Performance impact | Low | Low | Enum lookups are O(n) but n is small |
| Breaking changes | Low | High | Keep backward compatible |
| Test failures | Medium | Medium | Run full test suite before merge |

---

## Appendix A: Tracking Status Lifecycle

```
                                    ┌──────────────┐
                                    │   pending    │
                                    │ (info recv)  │
                                    └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │  picked_up   │ ◄── NEW
                                    │ (with carrier)│
                                    └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
              ┌────────────────────►│  in_transit  │◄────────────────────┐
              │                     │   (moving)   │                     │
              │                     └──────┬───────┘                     │
              │                            │                             │
              │                            ▼                             │
              │                     ┌──────────────┐                     │
              │                     │out_for_deliv │                     │
              │                     │  (last mile) │                     │
              │                     └──────┬───────┘                     │
              │                            │                             │
              │            ┌───────────────┼───────────────┐             │
              │            ▼               ▼               ▼             │
      ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
      │  on_hold  │  │ delivered │  │del_failed │  │del_delayed│────────┘
      │ (waiting) │  │  (done!)  │  │  (issue)  │  │  (slow)   │
      └─────┬─────┘  └───────────┘  └─────┬─────┘  └───────────┘
            │                             │
            │                             ▼
            │                      ┌───────────┐
            └─────────────────────►│return_2_snd│
                                   │ (going back)│
                                   └───────────┘
```

---

## Appendix B: TrackingIncidentReason Reference

### Carrier-Caused Issues
| Reason | Description |
|--------|-------------|
| `carrier_damaged_parcel` | Package was damaged during handling |
| `carrier_sorting_error` | Misrouted or sorting mistake |
| `carrier_address_not_found` | Carrier couldn't locate address |
| `carrier_parcel_lost` | Package is lost |
| `carrier_not_enough_time` | Driver ran out of time |
| `carrier_vehicle_issue` | Vehicle breakdown |

### Consignee-Caused Issues
| Reason | Description |
|--------|-------------|
| `consignee_refused` | Recipient refused delivery |
| `consignee_business_closed` | Business was closed |
| `consignee_not_home` | Recipient not available |
| `consignee_cancelled` | Recipient cancelled order |
| `consignee_incorrect_address` | Address provided was wrong |
| `consignee_access_restricted` | Couldn't access delivery location |

### Retailer-Caused Issues
| Reason | Description |
|--------|-------------|
| `retailer_cancelled` | Shipper cancelled shipment |
| `retailer_incorrect_data` | Wrong shipping data provided |
| `retailer_not_ready` | Package wasn't ready for pickup |
| `retailer_packaging_issue` | Packaging didn't meet requirements |

### Customs Issues
| Reason | Description |
|--------|-------------|
| `customs_delay` | Held at customs |
| `customs_documentation` | Missing documentation |
| `customs_duties_unpaid` | Duties not paid |
| `customs_prohibited` | Prohibited items |

### Other Issues
| Reason | Description |
|--------|-------------|
| `weather_delay` | Weather-related delay |
| `force_majeure` | Force majeure event |
| `unknown` | Unknown/unmapped reason |

---

## Appendix C: Example API Response

```json
{
  "id": "trk_abc123",
  "tracking_number": "1Z999999999999999",
  "carrier_name": "ups",
  "carrier_id": "ups_account",
  "status": "in_transit",
  "delivered": false,
  "estimated_delivery": "2025-12-06",
  "events": [
    {
      "date": "2025-12-04",
      "time": "02:30 PM",
      "timestamp": "2025-12-04T14:30:00.000Z",
      "status": "in_transit",
      "code": "IT",
      "reason": null,
      "description": "In Transit - On Time",
      "location": "Chicago, IL, US",
      "latitude": null,
      "longitude": null
    },
    {
      "date": "2025-12-03",
      "time": "09:15 AM",
      "timestamp": "2025-12-03T09:15:00.000Z",
      "status": "picked_up",
      "code": "PU",
      "reason": null,
      "description": "Picked Up",
      "location": "Los Angeles, CA, US",
      "latitude": null,
      "longitude": null
    },
    {
      "date": "2025-12-02",
      "time": "04:00 PM",
      "timestamp": "2025-12-02T16:00:00.000Z",
      "status": "pending",
      "code": "MP",
      "reason": null,
      "description": "Shipment information received",
      "location": "Los Angeles, CA, US",
      "latitude": null,
      "longitude": null
    }
  ],
  "meta": {},
  "messages": []
}
```

### Example with Delivery Exception

```json
{
  "tracking_number": "1Z999999999999999",
  "status": "delivery_failed",
  "events": [
    {
      "date": "2025-12-04",
      "time": "03:45 PM",
      "timestamp": "2025-12-04T15:45:00.000Z",
      "status": "delivery_failed",
      "code": "NA1",
      "reason": "consignee_not_home",
      "description": "The receiver was not available at the time of delivery",
      "location": "New York, NY, US"
    }
  ]
}
```
