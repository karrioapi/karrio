# Return Shipment Data Support for Shipping API

<!--
PRD TYPE MARKERS:
<!-- ENHANCEMENT: Include for feature enhancements -->
-->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-06 |
| Status | In Progress |
| Owner | Daniel Kobina |
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
12. [Appendices](#appendices)

---

## Executive Summary

This PRD proposes adding structured return shipment data to the Karrio Shipping API response. When carriers support requesting a return label upfront during shipment creation (like DHL Parcel DE's `dhlRetoure` option), the API will capture and expose return-specific tracking information alongside the return label document.

### Key Architecture Decisions

1. **Nested Object Structure**: Return data will be encapsulated in a `return_shipment` object on `ShipmentDetails` containing `tracking_number`, `shipment_identifier`, `tracking_url`, and `service`
2. **No Auto-Tracker Creation**: Return tracking numbers will be exposed but not automatically tracked; users create trackers manually if needed
3. **Unified Document List**: Return labels continue to use `shipping_documents` with `category="return_label"`, maintaining current behavior
4. **Upfront Returns Only**: Scope limited to return labels requested during outbound shipment creation

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Capture return tracking number from carrier responses | Standalone return shipment creation (swap shipper/recipient) |
| Add `return_shipment` object to ShipmentDetails | Auto-creation of Tracker for return shipments |
| Expose return data in shipment serializers | Return shipment void/cancel operations |
| Update DHL Parcel DE to parse `returnShipmentNo` | New carrier-specific return request options |
| Update other carriers that return similar data | Return pickup scheduling |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Return data structure | Nested `return_shipment` object (`ReturnShipment` class) | Cleaner organization, easier to extend, avoids cluttering ShipmentDetails | 2026-02-06 |
| D2 | Auto-tracker creation | No, manual only | Keeps tracking intentional, avoids unexpected resource creation | 2026-02-06 |
| D3 | Feature scope | Upfront return labels only | Focused scope, standalone returns can be a future enhancement | 2026-02-06 |
| D4 | Document structure | Same `shipping_documents` list with category | Maintains current behavior, avoids API fragmentation | 2026-02-06 |

---

## Problem Statement

### Current State

When a return label is requested during shipment creation (e.g., via DHL Parcel DE's `dhlRetoure` option), the carrier API returns:
- A return label document
- A return tracking number
- Potentially other return-specific metadata

Currently, Karrio only captures the return label document in `extra_documents`:

```python
# Current implementation in dhl_parcel_de/shipment/create.py
extra_documents = [
    ("return_label", shipment.returnLabel),  # Captured
    ("cod_document", shipment.codLabel),
]

# BUT returnShipmentNo is IGNORED:
# shipment.returnShipmentNo  # "340434310428091700" - NOT captured!
```

The return label appears in the response, but the return tracking information is lost:

```json
{
  "tracking_number": "123456789",
  "shipping_documents": [
    {"category": "label", "format": "PDF", "base64": "..."},
    {"category": "return_label", "format": "PDF", "base64": "..."}
  ]
  // No return_tracking_number!
  // No return_shipment_identifier!
}
```

### Desired State

The shipment response should include structured return information:

```python
# New models.py
@attr.s(auto_attribs=True)
class ReturnShipment:
    """Return shipment details when requested with outbound shipment."""

    tracking_number: str = None
    shipment_identifier: str = None
    tracking_url: str = None
    service: str = None
    reference: str = None
    meta: dict = None

@attr.s(auto_attribs=True)
class ShipmentDetails:
    # ... existing fields ...
    return_shipment: ReturnShipment = JStruct[ReturnShipment]  # NEW
```

```json
{
  "tracking_number": "123456789",
  "shipping_documents": [
    {"category": "label", "format": "PDF", "base64": "..."},
    {"category": "return_label", "format": "PDF", "base64": "..."}
  ],
  "return_shipment": {
    "tracking_number": "340434310428091700",
    "shipment_identifier": "340434310428091700",
    "tracking_url": "https://tracking.dhl.de/340434310428091700",
    "service": "dhl_parcel_de_paket",
    "reference": null,
    "meta": {}
  }
}
```

### Problems

1. **Data Loss**: Return tracking numbers from carrier responses are discarded
2. **Incomplete API Response**: Users cannot track return shipments without external lookups
3. **Manual Correlation**: Users must manually correlate return labels with tracking data from carrier portals
4. **Inconsistent Experience**: Outbound shipments have full tracking info, returns have only the label

---

## Goals & Success Criteria

### Goals

1. Capture and expose return tracking data from carrier responses when available
2. Provide a consistent, typed structure for return shipment information
3. Maintain backward compatibility with existing API consumers
4. Enable future extension for additional return-related features

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Return tracking number captured from DHL Parcel DE | 100% when returnShipmentNo present | Must-have |
| New `return_shipment` field in API response | Present when return data exists | Must-have |
| Backward compatibility maintained | No breaking changes to existing fields | Must-have |
| TypeScript types updated | @karrio/types includes ReturnShipment | Must-have |
| Other carriers updated (FedEx, UPS, etc.) | At least 2 additional carriers | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [x] `ReturnShipment` model added to `karrio.core.models`
- [x] `return_shipment` field on `ShipmentDetails`
- [x] DHL Parcel DE updated to capture `returnShipmentNo`
- [x] Django shipment model updated with `return_shipment` JSONField
- [x] Serializers expose `return_shipment` in API response
- [ ] TypeScript types updated

**Nice-to-have (P1):**
- [x] Update FedEx return label parsing
- [x] Update UPS return label parsing
- [x] Update USPS return label parsing
- [x] Update Canada Post return tracking pin parsing
- [ ] GraphQL schema updated

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Nested `return_shipment` object** | Clean, extensible, self-documenting | Slightly more complex to parse | **Selected** |
| Flat fields on ShipmentDetails | Simple access pattern | Clutters model, harder to extend | Rejected |
| Store in `meta` dict | No model changes | Untyped, inconsistent access | Rejected |
| Separate return_documents list | Clear separation | API fragmentation, duplicate patterns | Rejected |

### Trade-off Analysis

The nested object approach was selected because:
- **Extensibility**: Easy to add fields like `return_carrier`, `return_billing_number` later
- **Type Safety**: Strongly typed in both Python and TypeScript
- **Documentation**: Self-documenting structure vs. hidden meta keys
- **Consistency**: Follows patterns like `selected_rate`, `docs` which are nested objects

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| ShipmentDetails model | `modules/sdk/karrio/core/models.py:451-462` | Extend with return_shipment field |
| Documents/ShippingDocument | `modules/sdk/karrio/core/models.py:428-447` | No changes, reuse for return labels |
| DHL Parcel DE parser | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` | Update to capture returnShipmentNo |
| Django Shipment model | `modules/manager/karrio/server/manager/models.py:755-1019` | Add return_shipment JSONField |
| Shipment serializers | `modules/manager/karrio/server/manager/serializers/shipment.py` | Expose return_shipment |
| JStruct pattern | `karrio.lib` | Use for optional nested object |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SHIPMENT CREATION FLOW                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────┐│
│  │   Client    │────>│   Karrio    │────>│   Carrier API               ││
│  │   Request   │     │   Gateway   │     │   (e.g., DHL Parcel DE)     ││
│  │             │     │             │     │                             ││
│  │ options:    │     │             │     │   Response includes:        ││
│  │  dhlRetoure │     │             │     │   - shipmentNo              ││
│  │             │     │             │     │   - returnShipmentNo  ←NEW  ││
│  │             │     │             │     │   - returnLabel             ││
│  └─────────────┘     └─────────────┘     └─────────────────────────────┘│
│                                                   │                     │
│                                                   ▼                     │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                        RESPONSE PARSING                             ││
│  ├─────────────────────────────────────────────────────────────────────┤│
│  │                                                                     ││
│  │  ShipmentDetails(                                                   ││
│  │      tracking_number="123456789",                                   ││
│  │      shipment_identifier="123456789",                               ││
│  │      docs=Documents(                                                ││
│  │          label="...",                                               ││
│  │          extra_documents=[                                          ││
│  │              ShippingDocument(category="return_label", ...)         ││
│  │          ]                                                          ││
│  │      ),                                                             ││
│  │      return_shipment=ReturnShipment(  ←─────────── NEW           ││
│  │          tracking_number="340434310428091700",                      ││
│  │          shipment_identifier="340434310428091700",                  ││
│  │          tracking_url="https://tracking.dhl.de/...",                ││
│  │          service="dhl_parcel_de_paket",                             ││
│  │          reference=None,                                            ││
│  │          meta={},                                                   ││
│  │      ),                                                             ││
│  │  )                                                                  ││
│  │                                                                     ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐     ┌────────┐
│ Client │     │   API    │     │ Gateway  │     │ Mapper  │     │Carrier │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬────┘     └───┬────┘
    │               │                │                │              │
    │  1. POST      │                │                │              │
    │  /shipments   │                │                │              │
    │  (with return │                │                │              │
    │   options)    │                │                │              │
    │──────────────>│                │                │              │
    │               │  2. Gateway    │                │              │
    │               │  dispatch      │                │              │
    │               │───────────────>│                │              │
    │               │                │  3. Create     │              │
    │               │                │  request       │              │
    │               │                │───────────────>│              │
    │               │                │                │  4. API call │
    │               │                │                │─────────────>│
    │               │                │                │              │
    │               │                │                │  5. Response │
    │               │                │                │  (includes   │
    │               │                │                │  returnNo)   │
    │               │                │                │<─────────────│
    │               │                │  6. Parse      │              │
    │               │                │  response      │              │
    │               │                │  (extract      │              │
    │               │                │  return_shipment)              │
    │               │                │<───────────────│              │
    │               │  7. Save &     │                │              │
    │               │  serialize     │                │              │
    │               │<───────────────│                │              │
    │  8. Response  │                │                │              │
    │  with         │                │                │              │
    │  return_shipment                │                │              │
    │<──────────────│                │                │              │
    │               │                │                │              │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           REQUEST FLOW                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────────┐│
│  │ ShipmentRequest│───>│    Mapper     │───>│  Carrier Request          ││
│  │               │    │  (transform)  │    │  (e.g., DHL ShipmentType) ││
│  │ options:      │    │               │    │                           ││
│  │  dhlRetoure:  │    │               │    │  services:                ││
│  │    enabled    │    │               │    │    dhlRetoure:            ││
│  │    receiverId │    │               │    │      billingNumber: ...   ││
│  └───────────────┘    └───────────────┘    └───────────────────────────┘│
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                           RESPONSE FLOW                                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────────────────┐│
│  │ShipmentDetails│<───│   Provider    │<───│  Carrier Response         ││
│  │               │    │   (parse)     │    │  (e.g., DHL ItemType)     ││
│  │ return_shipment:    │               │    │                           ││
│  │   tracking_number  │  ┌──────────┐ │    │  shipmentNo: "123..."     ││
│  │   shipment_id      │  │ Extract  │ │    │  returnShipmentNo: "340.."││
│  │   tracking_url     │  │ return   │ │    │  returnLabel: {...}       ││
│  │   service          │  │ data     │ │    │                           ││
│  │                    │  └──────────┘ │    │                           ││
│  └───────────────┘    └───────────────┘    └───────────────────────────┘│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### Python Models (karrio.core.models)

```python
@attr.s(auto_attribs=True)
class ReturnShipment:
    """Return shipment details when a return label is requested with outbound shipment."""

    tracking_number: str = None      # Return shipment tracking number
    shipment_identifier: str = None  # Carrier's internal return shipment ID
    tracking_url: str = None         # URL to track the return shipment
    service: str = None              # Service code used for return (if known)
    reference: str = None            # Return shipment reference (e.g., carrier ref number)
    meta: dict = None                # Carrier-specific return metadata


@attr.s(auto_attribs=True)
class ShipmentDetails:
    """Karrio unified shipment details data type."""

    carrier_name: str
    carrier_id: str
    tracking_number: str
    shipment_identifier: str
    docs: Documents = JStruct[Documents, REQUIRED]
    selected_rate: RateDetails = JStruct[RateDetails]
    label_type: str = None
    meta: dict = None
    id: str = None
    return_shipment: ReturnShipment = JStruct[ReturnShipment]  # NEW
```

#### Django Model (karrio.server.manager.models)

```python
class Shipment(OwnedEntity):
    # ... existing fields ...

    # NEW: Return shipment details (JSONField)
    return_shipment = models.JSONField(
        blank=True,
        null=True,
        default=None,
        help_text="Return shipment details when a return label was requested",
    )
```

#### TypeScript Types (@karrio/types)

```typescript
export interface ReturnShipment {
  tracking_number?: string;
  shipment_identifier?: string;
  tracking_url?: string;
  service?: string;
  reference?: string;
  meta?: object;
}

export interface ShipmentType {
  // ... existing fields ...
  return_shipment?: ReturnShipment;
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `return_shipment.tracking_number` | string | No | Tracking number for the return shipment |
| `return_shipment.shipment_identifier` | string | No | Carrier's internal identifier for the return |
| `return_shipment.tracking_url` | string | No | Direct URL to track the return shipment |
| `return_shipment.service` | string | No | Service code used for the return (e.g., `dhl_parcel_de_paket`) |
| `return_shipment.reference` | string | No | Return shipment reference (e.g., carrier ref number) |
| `return_shipment.meta` | dict | No | Carrier-specific return metadata (e.g., billing number, return reason) |

### API Changes

**Endpoints affected:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/shipments` | Returns `return_shipment` when return label requested |
| GET | `/v1/shipments/{id}` | Includes `return_shipment` if present |
| POST | `/v1/proxy/shipping` | Returns `return_shipment` when return label requested |

**Response example:**

```json
{
  "id": "shp_abc123",
  "status": "purchased",
  "tracking_number": "123456789012",
  "shipment_identifier": "123456789012",
  "carrier_name": "dhl_parcel_de",
  "carrier_id": "dhl_parcel_de_account",
  "shipping_documents": [
    {
      "category": "label",
      "format": "PDF",
      "base64": "JVBERi0xLjQK..."
    },
    {
      "category": "return_label",
      "format": "PDF",
      "base64": "JVBERi0xLjQK..."
    }
  ],
  "return_shipment": {
    "tracking_number": "340434310428091700",
    "shipment_identifier": "340434310428091700",
    "tracking_url": "https://www.dhl.de/de/privatkunden/dhl-sendungsverfolgung.html?piececode=340434310428091700",
    "service": "dhl_parcel_de_paket"
  }
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Return label requested but carrier doesn't return tracking number | `return_shipment` is `null`, return label still in documents | Check if returnShipmentNo exists before creating ReturnShipment |
| Multi-piece shipment with return | Each piece may have return data | Use `to_multi_piece_shipment` to combine, take first return_shipment |
| Return label without tracking URL | `tracking_url` is `null`, other fields populated | All fields optional |
| Carrier returns only partial return data | Populate available fields, leave others null | All fields optional |
| Return option requested but carrier doesn't support it | No return label, no return_shipment | Carrier returns error or ignores option |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| returnShipmentNo parsing fails | return_shipment is null | Use `lib.failsafe()` for extraction |
| tracking_url format incorrect | Broken link in UI | Validate URL format, fallback to null |
| Meta key collision | Data overwrite | Use dedicated field instead of meta |
| Migration fails on existing data | Rollback needed | JSONField with null default is safe |

---

## Implementation Plan

### Phase 1: Core Model Changes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `ReturnShipment` model | `modules/sdk/karrio/core/models.py` | Pending | S |
| Add `return_shipment` to `ShipmentDetails` | `modules/sdk/karrio/core/models.py` | Pending | S |
| Add `return_shipment` to Django Shipment | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Create Django migration | `modules/manager/karrio/server/manager/migrations/` | Pending | S |
| Update shipment serializers | `modules/manager/karrio/server/manager/serializers/shipment.py` | Pending | M |

### Phase 2: Carrier Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update DHL Parcel DE response parser | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` | Done | M |
| Update DHL Parcel DE tests | `modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/test_shipment.py` | Done | M |
| Wire FedEx return shipment detail | `modules/connectors/fedex/karrio/providers/fedex/shipment/create.py` | Done | M |
| Wire UPS return shipment parsing | `modules/connectors/ups/karrio/providers/ups/shipment/create.py` | Done | M |
| Wire USPS return label metadata | `modules/connectors/usps/karrio/providers/usps/shipment/create.py` | Done | M |
| Wire Canada Post return tracking pin | `modules/connectors/canadapost/karrio/providers/canadapost/shipment/create.py` | Done | M |

### Phase 3: Frontend & Types

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add TypeScript types | `packages/types/base.ts` | Pending | S |
| Update GraphQL types (if applicable) | `modules/graph/karrio/server/graph/schemas/` | Pending | M |
| Update dashboard UI (if needed) | `apps/dashboard/src/` | Pending | M |

**Dependencies:** Phase 2 depends on Phase 1. Phase 3 depends on Phase 1.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/connectors/dhl_parcel_de/tests/` | Return data parsing |
| Integration Tests | `modules/manager/karrio/server/manager/tests/` | API response structure |

### Test Cases

#### Unit Tests - DHL Parcel DE

```python
"""Test return shipment details parsing."""

import unittest
from unittest.mock import ANY

class TestDHLParcelDEShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_parse_shipment_response_with_return_shipment(self):
        """Verify return details are extracted from DHL response."""
        from karrio.providers.dhl_parcel_de.shipment.create import (
            parse_shipment_response,
        )

        response = lib.Deserializable({
            "items": [{
                "sstatus": {"statusCode": 200},
                "shipmentNo": "123456789012",
                "returnShipmentNo": "340434310428091700",
                "label": {"b64": "...", "fileFormat": "PDF"},
                "returnLabel": {"b64": "...", "fileFormat": "PDF"},
            }]
        })

        shipment, messages = parse_shipment_response(response, settings)

        # print(shipment)  # Debug
        self.assertIsNotNone(shipment)
        self.assertIsNotNone(shipment.return_shipment)
        self.assertEqual(
            shipment.return_shipment.tracking_number,
            "340434310428091700"
        )

    def test_parse_shipment_response_without_return(self):
        """Verify return_shipment is None when no return requested."""
        response = lib.Deserializable({
            "items": [{
                "sstatus": {"statusCode": 200},
                "shipmentNo": "123456789012",
                "label": {"b64": "...", "fileFormat": "PDF"},
                # No returnShipmentNo or returnLabel
            }]
        })

        shipment, messages = parse_shipment_response(response, settings)

        self.assertIsNone(shipment.return_shipment)
```

#### Integration Tests - Django API

```python
"""Test shipment API with return details."""

from unittest import mock

class TestShipmentAPIWithReturns(APITestCase):
    def test_shipment_response_includes_return_shipment(self):
        """Verify API response includes return_shipment when present."""
        # Create shipment with mocked carrier response that includes return data
        response = self.client.post('/api/shipments', data={...})

        # print(response.data)  # Debug
        self.assertResponseNoErrors(response)
        self.assertIn('return_shipment', response.data)
        self.assertDictEqual(
            response.data['return_shipment'],
            {
                'tracking_number': mock.ANY,
                'shipment_identifier': mock.ANY,
                'tracking_url': mock.ANY,
                'service': mock.ANY,
            }
        )
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run DHL Parcel DE tests
python -m unittest discover -v -f modules/connectors/dhl_parcel_de/tests

# Run manager tests
karrio test --failfast karrio.server.manager.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking change to API response | High | Low | Additive change only, new optional field |
| Carrier response format changes | Medium | Low | Use failsafe extraction, graceful fallback |
| Migration fails on production | High | Low | JSONField with null default is safe |
| TypeScript type mismatch | Medium | Medium | Coordinate type updates with model changes |
| Multi-carrier inconsistency | Medium | Medium | Document carrier-specific behaviors |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: New `return_shipment` field is optional and nullable - existing clients unaffected
- **Data compatibility**: Existing shipments will have `return_shipment: null`
- **Feature flags**: Not needed - additive change with graceful degradation

### Data Migration

```python
# Migration is simple - just add the JSONField with null default
# No data backfill needed for existing shipments

from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('manager', 'previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='return_shipment',
            field=models.JSONField(blank=True, null=True, default=None),
        ),
    ]
```

### Rollback Procedure

1. **Identify issue**: Monitor for API errors or data inconsistencies
2. **Stop rollout**: Revert carrier provider changes first (return `return_shipment=None`)
3. **Revert changes**: Remove field from serializers, then migration
4. **Verify recovery**: Confirm existing shipment endpoints work correctly

---

## Appendices

### Appendix A: Carrier Return Support Matrix

| Carrier | Return Label Support | Return Tracking Number | Field Name | Pattern |
|---------|---------------------|------------------------|------------|---------|
| DHL Parcel DE | Yes | Yes | `returnShipmentNo` | Pattern B — separate tracking number |
| FedEx | Yes | Yes (same as outbound) | `returnShipmentDetail` | Pattern A — same tracking number |
| UPS | Yes | Yes (same as outbound) | `ReturnService` + response URLs | Pattern A — same tracking number |
| USPS | Yes | Yes | `returnLabelMetadata.trackingNumber` | Pattern B — separate tracking number |
| Asendia | Yes | TBD | TBD | TBD |
| Canada Post | Yes | Yes | `return-tracking-pin` | Pattern B — separate tracking number |

### Appendix B: DHL Parcel DE Response Sample

```json
{
  "status": {
    "title": "ok",
    "statusCode": 200
  },
  "items": [
    {
      "sstatus": {
        "title": "ok",
        "statusCode": 200
      },
      "shipmentNo": "123456789012",
      "returnShipmentNo": "340434310428091700",
      "shipmentRefNo": "REF-123",
      "label": {
        "b64": "JVBERi0xLjQK...",
        "fileFormat": "PDF",
        "printFormat": "A4"
      },
      "returnLabel": {
        "b64": "JVBERi0xLjQK...",
        "fileFormat": "PDF",
        "printFormat": "A4",
        "url": "https://api-dev.dhl.com/..."
      }
    }
  ]
}
```

### Appendix C: Implementation Checklist

- [x] ReturnShipment model added
- [x] ShipmentDetails.return_shipment field added
- [x] Django migration created
- [x] Shipment serializer updated
- [x] DHL Parcel DE parser updated
- [x] DHL Parcel DE tests updated
- [x] FedEx return shipment detail wired
- [x] UPS return shipment parsing wired
- [x] USPS return label metadata parsed
- [x] Canada Post return tracking pin extracted
- [ ] TypeScript types updated
- [ ] GraphQL types updated (if applicable)
- [ ] API documentation updated

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [x] All pending questions in "Open Questions & Decisions" have been asked
- [x] All user decisions documented with rationale and date
- [x] Edge cases requiring input have been resolved
- [x] "Open Questions & Decisions" section cleaned up (all resolved)

CODE ANALYSIS:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (JStruct, lib.failsafe, etc.)

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
