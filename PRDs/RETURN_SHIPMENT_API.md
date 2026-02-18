# Return Shipment API — Standalone Return Label Creation

<!--
PRD TYPE MARKERS:
<!-- ENHANCEMENT: Include for feature enhancements -->
<!-- ARCHITECTURE: Include for system design PRDs -->
-->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-17 |
| Status | Planning |
| Owner | Daniel Kobina |
| Type | Enhancement / Architecture |
| Reference | [AGENTS.md](../AGENTS.md) |
| Related | [SHIPPING_RETURN_LABEL_SUPPORT.md](./SHIPPING_RETURN_LABEL_SUPPORT.md) — bundled return labels during outbound shipment |

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

This PRD proposes adding a **dedicated Return Shipment API** to Karrio that allows standalone creation of return labels — independent from outbound shipment creation. While the existing `SHIPPING_RETURN_LABEL_SUPPORT` PRD handles return labels bundled with outbound shipments (e.g., DHL Parcel DE's `dhlRetoure`), this API enables merchants to create return labels on-demand for e-commerce returns, RMA workflows, and customer-initiated returns.

The API uses the existing shipment model with an `is_return` flag (following EasyPost/Shippo patterns), while internally routing to a dedicated `create_return_shipment` Mapper/Proxy method that allows carriers with separate return APIs (DHL Parcel DE, Canada Post, USPS) to implement them cleanly.

### Key Architecture Decisions

1. **Explicit `is_return` field on ShipmentRequest**: A proper boolean field on the unified model (not hidden in options), propagated through all serializers
2. **Separate SDK method**: New `create_return_shipment` on Mapper/Proxy base classes — carriers with dedicated return APIs implement it separately; carriers that reuse shipment APIs delegate internally
3. **Auto-swap addresses**: When `is_return` is set, Karrio auto-swaps shipper/recipient so users provide addresses in outbound orientation
4. **Optional outbound reference**: An `outbound_shipment_id` or `outbound_tracking_number` links returns to original shipments
5. **Return-specific fields via carrier options**: `return_type`, `rma_number`, `charge_event` passed through carrier-specific options (not unified fields)
6. **QR code support (P1)**: Response model supports QR code URLs for label-less returns

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Standalone return label creation API | Return merchandise authorization (RMA) management system |
| New `create_return_shipment` Mapper/Proxy method | Return pickup scheduling (use existing Pickup API) |
| Auto-swap addresses for return direction | Return analytics/reporting |
| UPS, FedEx, DHL Parcel DE, DHL Express, Canada Post, USPS | Return status tracking (use existing Tracking API) |
| QR code / paperless return URL in response (P1) | Customer-facing return portal UI |
| Optional link to outbound shipment | Void/cancel return label (use existing cancel shipment) |
| Carrier-specific return options | Batch return label creation |

### Relationship to SHIPPING_RETURN_LABEL_SUPPORT

| Feature | SHIPPING_RETURN_LABEL_SUPPORT | This PRD (RETURN_SHIPMENT_API) |
|---------|------------------------------|-------------------------------|
| **When** | During outbound shipment creation | Any time after outbound shipment |
| **Trigger** | Carrier option (e.g., `dhlRetoure`) | `options.is_return: true` on shipment request |
| **Response** | `return_shipment` nested in `ShipmentDetails` | Full `ShipmentDetails` (the return IS the shipment) |
| **SDK Method** | `create_shipment` (existing) | `create_return_shipment` (new) |
| **Carrier API** | Same shipment creation call | May use same or dedicated return API |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | API surface | `is_return` flag on existing shipment endpoint | Minimal API surface, follows EasyPost/Shippo patterns | 2026-02-17 |
| D2 | SDK method | Separate `create_return_shipment` on Mapper/Proxy | 3 of 6 carriers have structurally different return APIs; clean separation | 2026-02-17 |
| D3 | Address handling | Auto-swap shipper/recipient | Less error-prone for users; EasyPost pattern | 2026-02-17 |
| D4 | P0 carriers | All 6 (UPS, FedEx, DHL Parcel DE, DHL Express, Canada Post, USPS) | Comprehensive coverage requested | 2026-02-17 |
| D5 | Outbound link | Optional `outbound_shipment_id` / `outbound_tracking_number` | Enables return-to-outbound association for carriers that support it | 2026-02-17 |
| D6 | Return-specific fields | `is_return` + `outbound_tracking_number` as explicit fields; carrier-specific details via options | `is_return` is universal; return_type codes vary per carrier so remain in options | 2026-02-17 |
| D7 | QR code support | In scope as P1 | DHL Parcel DE and FedEx support this natively | 2026-02-17 |
| D8 | Django model | Reuse `Shipment` model with `is_return` BooleanField | Simpler; reuses all existing serializers/views/hooks; follows EasyPost/Shippo pattern | 2026-02-17 |
| D9 | List filtering | Show all by default, filterable by `?is_return=true/false` | Most transparent; no hidden records | 2026-02-17 |
| D10 | Proxy endpoint | Same `/v1/proxy/shipping` endpoint | `is_return` field on request body determines routing; minimal API surface | 2026-02-17 |

### Pending Questions

_All questions resolved._

---

## Problem Statement

### Current State

Karrio currently supports return labels **only** when bundled with outbound shipment creation:

```python
# Current: Return label requested DURING outbound shipment creation
shipment_request = ShipmentRequest(
    service="dhl_parcel_de_paket",
    shipper=merchant_address,
    recipient=customer_address,
    parcels=[parcel],
    options={
        "dhl_parcel_de_dhl_retoure": {    # Carrier-specific option
            "receiver_id": "deu",
            "billing_number": "..."
        }
    },
)

# Response includes both outbound + return label
# shipment.return_shipment.tracking_number = "340434310428091700"
# shipment.docs.extra_documents = [{"category": "return_label", ...}]
```

There is **no way** to create a standalone return label:

```python
# NOT POSSIBLE TODAY:
# Customer wants to return an item 2 weeks after receiving it
# Merchant needs to generate a return label on-demand

# ❌ No return-specific API exists
# ❌ Cannot create a return label without creating an outbound shipment
# ❌ Cannot use carriers' dedicated return APIs (DHL Parcel DE /returns/v1/orders, Canada Post /authorizedreturn)
```

### Desired State

```python
# New: Standalone return label creation
return_request = ShipmentRequest(
    service="dhl_parcel_de_paket",
    shipper=merchant_address,      # Auto-swapped: becomes return destination
    recipient=customer_address,    # Auto-swapped: becomes return origin
    parcels=[parcel],
    is_return=True,                                  # Explicit field on model
    outbound_tracking_number="123456789012",         # Optional link to original shipment
    options={
        # Carrier-specific options as needed:
        "dhl_parcel_de_receiver_id": "deu",
    },
)

# Gateway detects is_return and routes to create_return_shipment
shipment, messages = karrio.Shipment.create(return_request).from_(gateway).parse()

# Response is a standard ShipmentDetails — the return IS the shipment
# shipment.tracking_number = "340434310428091700"
# shipment.docs.label = "JVBERi0xLjQK..."
# shipment.meta = {"is_return": True, "qr_code_url": "https://...", ...}
```

### Problems

1. **No on-demand return labels**: Merchants cannot generate return labels outside of outbound shipment creation
2. **Missing carrier APIs**: DHL Parcel DE, Canada Post, and USPS have dedicated return APIs that Karrio cannot access
3. **No return workflow support**: Common e-commerce flows (customer-initiated returns, RMA-based returns) are unsupported
4. **No QR code / paperless returns**: Cannot leverage carriers' label-less return capabilities
5. **No return-to-outbound linking**: Cannot associate a return with its original outbound shipment for carrier APIs that support this (FedEx `returnAssociationDetail`)

---

## Goals & Success Criteria

### Goals

1. Enable standalone return label creation through the existing shipment API with `is_return` flag
2. Add `create_return_shipment` Mapper/Proxy methods to cleanly support carriers with dedicated return APIs
3. Implement return support for all 6 target carriers (UPS, FedEx, DHL Parcel DE, DHL Express, Canada Post, USPS)
4. Support QR code / paperless return URLs in the response
5. Auto-swap addresses so users provide addresses in outbound orientation

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Return label creation works for all 6 carriers | 100% when carrier supports returns | Must-have |
| `is_return` flag detected and routed to `create_return_shipment` | Gateway routing works | Must-have |
| Address auto-swap works correctly | Addresses swapped before carrier API call | Must-have |
| Outbound shipment reference passed to carriers that support it | FedEx, Canada Post | Must-have |
| QR code URL returned when available | DHL Parcel DE, FedEx | Nice-to-have |
| Backward compatibility — existing shipment API unchanged | No breaking changes | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] `create_return_shipment` method on Mapper/Proxy base classes
- [ ] Gateway routing: `is_return` → `create_return_shipment`
- [ ] Address auto-swap logic
- [ ] UPS return shipment implementation
- [ ] FedEx return shipment implementation
- [ ] DHL Parcel DE dedicated return API implementation
- [ ] DHL Express return shipment implementation
- [ ] Canada Post authorized return implementation
- [ ] USPS return label implementation
- [ ] Server-side gateway and API endpoint support
- [ ] Django model updates (if new model) or `is_return` flag on Shipment
- [ ] TypeScript types updated

**Nice-to-have (P1):**
- [ ] QR code URL in response (`meta.qr_code_url`)
- [ ] `outbound_tracking_number` / `outbound_shipment_id` passed to carrier
- [ ] GraphQL schema updated
- [ ] Dashboard UI for creating return labels
- [ ] Canada Post Open Return support (in addition to Authorized Return)

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **`is_return` flag + separate SDK method** | Minimal API surface for users; clean internal routing for carriers with different APIs | Two layers of abstraction | **Selected** |
| Dedicated `/v1/returns` endpoint with new model | Clean separation; purpose-built data model | API fragmentation; duplicate shipment-like model; more frontend work | Rejected |
| Reuse `create_shipment` with `is_return` in options | Simplest implementation; no new SDK methods | DHL Parcel DE / Canada Post / USPS return APIs are structurally different — shoehorning them into `create_shipment_request` creates messy conditionals | Rejected |
| Separate `ReturnRequest` model (different from ShipmentRequest) | Type-safe; return-specific fields at top level | Too many new types; return requests are fundamentally similar to shipment requests | Rejected |

### Trade-off Analysis

The selected approach balances **user simplicity** (same shipment endpoint, just add `is_return`) with **carrier flexibility** (separate SDK method for structurally different APIs).

- **UPS, FedEx, DHL Express**: `create_return_shipment` internally delegates to `create_shipment` with return flags/options injected
- **DHL Parcel DE**: `create_return_shipment` calls the dedicated `/returns/v1/orders` API
- **Canada Post**: `create_return_shipment` calls the dedicated `/authorizedreturn` endpoint
- **USPS**: `create_return_shipment` calls the dedicated Returns Label API

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| ShipmentRequest model | `modules/sdk/karrio/core/models.py:124-142` | Reuse as-is — `is_return` passed via `options` dict |
| ShipmentDetails model | `modules/sdk/karrio/core/models.py:462-475` | Reuse as-is — return IS a shipment |
| ReturnShipment model | `modules/sdk/karrio/core/models.py:450-459` | Not used here (that's for bundled returns) |
| Mapper base class | `modules/sdk/karrio/api/mapper.py` | Extend with `create_return_shipment_request` / `parse_return_shipment_response` |
| Proxy base class | `modules/sdk/karrio/api/proxy.py` | Extend with `create_return_shipment` |
| Fluent interface | `modules/sdk/karrio/api/interface.py:437-472` | Follow `Shipment.create` pattern |
| Server gateway | `modules/core/karrio/server/core/gateway.py:267-327` | Follow `Shipments.create` pattern |
| Capability detection | `modules/sdk/karrio/core/units.py` | Auto-detects "shipping" from method name containing "shipment" |
| UPS return options | `modules/connectors/ups/karrio/providers/ups/units.py` | `ReturnServiceCode` enum already exists |
| FedEx return schema | `modules/connectors/fedex/schemas/shipping_request.json` | `returnShipmentDetail` already defined |
| DHL Parcel DE retoure | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` | Reference for DHL return patterns |
| Canada Post return schemas | `modules/connectors/canadapost/karrio/schemas/canadapost/authreturn.py` | `AuthorizedReturnType`, `ReturnerType` already generated |
| MyDHL return VAS codes | `modules/connectors/mydhl/karrio/providers/mydhl/units.py:166-168` | `PH` (Return to Seller), `PR` (Return to Origin) |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RETURN SHIPMENT CREATION FLOW                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐│
│  │   Client      │────>│   Gateway    │────>│   Carrier API               ││
│  │   Request     │     │              │     │                             ││
│  │               │     │  Detects     │     │   UPS/FedEx/DHL Express:    ││
│  │ is_return:    │     │  is_return   │     │   Same shipment API +       ││
│  │   true        │     │  flag        │     │   return flags              ││
│  │               │     │              │     │                             ││
│  │ shipper:      │     │  Auto-swaps  │     │   DHL Parcel DE:            ││
│  │  (merchant)   │     │  addresses   │     │   /returns/v1/orders        ││
│  │ recipient:    │     │              │     │                             ││
│  │  (customer)   │     │  Routes to   │     │   Canada Post:              ││
│  │               │     │  create_     │     │   /authorizedreturn         ││
│  │               │     │  return_     │     │                             ││
│  │               │     │  shipment    │     │   USPS:                     ││
│  │               │     │              │     │   Returns Label API         ││
│  └──────────────┘     └──────────────┘     └──────────────────────────────┘│
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┤
│  │                        RESPONSE (same as shipment)                       │
│  ├──────────────────────────────────────────────────────────────────────────┤
│  │                                                                          │
│  │  ShipmentDetails(                                                        │
│  │      carrier_name="dhl_parcel_de",                                       │
│  │      tracking_number="340434310428091700",                               │
│  │      docs=Documents(label="base64..."),                                  │
│  │      meta={                                                              │
│  │          "is_return": True,                                              │
│  │          "qr_code_url": "https://...",           ← P1                   │
│  │          "outbound_tracking_number": "123...",                           │
│  │      },                                                                  │
│  │  )                                                                       │
│  │                                                                          │
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│ Client │     │   API    │     │ Gateway  │     │  Mapper  │     │ Carrier │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬────┘
    │               │                │                │                 │
    │  1. POST      │                │                │                 │
    │  /shipments   │                │                │                 │
    │  is_return:   │                │                │                 │
    │    true       │                │                │                 │
    │──────────────>│                │                │                 │
    │               │  2. Detect     │                │                 │
    │               │  is_return     │                │                 │
    │               │───────────────>│                │                 │
    │               │                │  3. Auto-swap  │                 │
    │               │                │  addresses     │                 │
    │               │                │  (shipper ↔    │                 │
    │               │                │   recipient)   │                 │
    │               │                │                │                 │
    │               │                │  4. Route to   │                 │
    │               │                │  create_return │                 │
    │               │                │  _shipment     │                 │
    │               │                │───────────────>│                 │
    │               │                │                │  5. Carrier-    │
    │               │                │                │  specific call  │
    │               │                │                │  (may be same   │
    │               │                │                │  or dedicated   │
    │               │                │                │  return API)    │
    │               │                │                │────────────────>│
    │               │                │                │                 │
    │               │                │                │  6. Response    │
    │               │                │                │<────────────────│
    │               │                │  7. Parse      │                 │
    │               │                │  response      │                 │
    │               │                │<───────────────│                 │
    │               │  8. Return     │                │                 │
    │               │  ShipmentDetails                │                 │
    │               │<───────────────│                │                 │
    │  9. Response  │                │                │                 │
    │  (standard    │                │                │                 │
    │   shipment)   │                │                │                 │
    │<──────────────│                │                │                 │
    │               │                │                │                 │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           REQUEST FLOW                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ ShipmentRequest│    │   Gateway /     │    │  Carrier Request            │ │
│  │               │    │   Interface     │    │                             │ │
│  │ shipper:      │    │                 │    │  UPS: ShipmentRequest +     │ │
│  │   merchant    │    │  1. Check       │    │    ReturnService element    │ │
│  │ recipient:    │───>│     is_return   │───>│                             │ │
│  │   customer    │    │  2. Swap addrs  │    │  FedEx: ShipmentRequest +   │ │
│  │ options:      │    │  3. Route to    │    │    returnShipmentDetail     │ │
│  │   is_return:  │    │     create_     │    │                             │ │
│  │     true      │    │     return_     │    │  DHL Parcel DE: Return      │ │
│  │   outbound_   │    │     shipment    │    │    Order (different API)    │ │
│  │   tracking_   │    │                 │    │                             │ │
│  │   number: ... │    │                 │    │  Canada Post: Authorized    │ │
│  │               │    │                 │    │    Return (different API)   │ │
│  └───────────────┘    └─────────────────┘    └─────────────────────────────┘ │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                           RESPONSE FLOW                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ShipmentDetails│    │   Provider      │    │  Carrier Response           │ │
│  │               │    │   (parse)       │    │                             │ │
│  │ tracking_     │    │                 │    │  UPS: Standard shipment     │ │
│  │   number      │<───│  Parse carrier  │<───│    response                 │ │
│  │ docs.label    │    │  response into  │    │                             │ │
│  │ meta:         │    │  standard       │    │  DHL Parcel DE: Return      │ │
│  │   is_return:  │    │  ShipmentDetails│    │    order response +         │ │
│  │     true      │    │                 │    │    QR code URL              │ │
│  │   qr_code_url │    │                 │    │                             │ │
│  └───────────────┘    └─────────────────┘    └─────────────────────────────┘ │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### ShipmentRequest Model (`modules/sdk/karrio/core/models.py`)

```python
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
    label_type: str = None
    is_return: bool = False                          # NEW
    outbound_tracking_number: str = None             # NEW — optional link to outbound

    metadata: Dict = {}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `is_return` | `bool` | No | When `True`, creates a return shipment. Gateway auto-swaps addresses and routes to `create_return_shipment` |
| `outbound_tracking_number` | `str` | No | Tracking number of the original outbound shipment. Passed to carriers that support return association (FedEx, Canada Post) |

### SDK Layer Changes

#### 1. Mapper Base Class (`modules/sdk/karrio/api/mapper.py`)

```python
# NEW methods to add

def create_return_shipment_request(
    self, payload: models.ShipmentRequest
) -> lib.Serializable:
    """Create a carrier specific return shipment request data from the payload.

    Args:
        payload (ShipmentRequest): the return shipment request payload
            (addresses already swapped by gateway)

    Returns:
        Serializable: a carrier specific serializable request data type

    Raises:
        MethodNotSupportedError: Is raised when the carrier integration
            does not implement this method
    """
    raise errors.MethodNotSupportedError(
        self.__class__.create_return_shipment_request.__name__,
        self.settings.carrier_name,
    )

def parse_return_shipment_response(
    self, response: lib.Deserializable
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    """Parse a return shipment response from a carrier into ShipmentDetails.

    Args:
        response (Deserializable): the carrier return shipment response

    Returns:
        Tuple: (ShipmentDetails, List[Message])

    Raises:
        MethodNotSupportedError: Is raised when the carrier integration
            does not implement this method
    """
    raise errors.MethodNotSupportedError(
        self.__class__.parse_return_shipment_response.__name__,
        self.settings.carrier_name,
    )
```

#### 2. Proxy Base Class (`modules/sdk/karrio/api/proxy.py`)

```python
# NEW method to add

def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable:
    """Send request(s) to create a return shipment label from a carrier webservice.

    Args:
        request (Serializable): a carrier specific serializable request data type

    Returns:
        Deserializable: a carrier specific deserializable response data type

    Raises:
        MethodNotSupportedError: Is raised when the carrier integration
            does not implement this method
    """
    raise errors.MethodNotSupportedError(
        self.__class__.create_return_shipment.__name__,
        self.settings.carrier_name,
    )
```

#### 3. Fluent Interface (`modules/sdk/karrio/api/interface.py`)

The `Shipment.create` method will be updated to detect `is_return` and route accordingly:

```python
class Shipment:
    @staticmethod
    def create(args: typing.Union[models.ShipmentRequest, dict]) -> IRequestFrom:
        logger.debug("Creating shipment", payload=lib.to_dict(args))
        payload = lib.to_object(models.ShipmentRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            if payload.is_return:
                # Auto-swap addresses: user provides outbound orientation
                swapped_payload = lib.to_object(
                    models.ShipmentRequest,
                    {
                        **lib.to_dict(payload),
                        "shipper": lib.to_dict(payload.recipient),
                        "recipient": lib.to_dict(payload.shipper),
                        "return_address": lib.to_dict(
                            payload.return_address or payload.shipper
                        ),
                    },
                )

                is_valid, abortion = check_operation(
                    gateway,
                    "create_return_shipment",
                    origin_country_code=swapped_payload.shipper.country_code,
                )
                if not is_valid:
                    return abortion

                request = gateway.mapper.create_return_shipment_request(swapped_payload)
                response = gateway.proxy.create_return_shipment(request)

                @fail_safe(gateway)
                def deserialize():
                    return gateway.mapper.parse_return_shipment_response(response)

                return IDeserialize(deserialize)

            # Existing shipment flow (unchanged)
            is_valid, abortion = check_operation(
                gateway,
                "create_shipment",
                origin_country_code=payload.shipper.country_code,
            )
            if not is_valid:
                return abortion

            request = gateway.mapper.create_shipment_request(payload)
            response = gateway.proxy.create_shipment(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
```

### Carrier Implementation Patterns

#### Pattern A: Carriers Reusing Shipment API (UPS, FedEx, DHL Express)

These carriers add return-specific flags to the existing shipment creation request.

```python
# Example: UPS Mapper
class Mapper(mapper.Mapper):
    settings: Settings

    def create_return_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        # Delegate to shipment request builder with return context
        return provider.return_shipment_request(payload, self.settings)

    def parse_return_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        # Reuse standard shipment response parser
        return provider.parse_shipment_response(response, self.settings)
```

```python
# Example: UPS Provider — return_shipment_request
def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.to_shipping_options(payload.options, ...)

    # Determine return service code from options or default
    return_service_code = options.get("ups_return_service_code", "9")  # Default: Print Return Label

    # Build standard shipment request with ReturnService element
    request = {
        # ... standard shipment fields ...
        "ReturnService": {"Code": return_service_code},
    }

    return lib.Serializable(request, ...)
```

#### Pattern B: Carriers with Dedicated Return API (DHL Parcel DE)

These carriers have a completely different API endpoint and request structure.

```python
# Example: DHL Parcel DE Mapper
class Mapper(mapper.Mapper):
    settings: Settings

    def create_return_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        # Build dedicated return API request (different from shipment)
        return provider.return_shipment_request(payload, self.settings)

    def parse_return_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_return_shipment_response(response, self.settings)
```

```python
# Example: DHL Parcel DE Provider — return_shipment_request
def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.to_shipping_options(payload.options, ...)
    shipper = lib.to_address(payload.shipper)  # Already swapped: customer
    receiver_id = options.get("dhl_parcel_de_receiver_id", "deu")

    request = {
        "receiverId": receiver_id,
        "customerReference": payload.reference or None,
        "shipper": {
            "name1": shipper.person_name or shipper.company_name,
            "addressStreet": shipper.street_name,
            "addressHouse": shipper.street_number,
            "postalCode": shipper.postal_code,
            "city": shipper.city,
            "country": lib.to_country_name(shipper.country_code, "iso3"),
        },
        "itemWeight": {
            "uom": "g",
            "value": lib.to_int(packages[0].weight.G),
        },
    }

    return lib.Serializable(request, lib.to_json)
```

```python
# Example: DHL Parcel DE Proxy — create_return_shipment
class Proxy(proxy.Proxy):
    settings: Settings

    def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/parcel/de/shipping/returns/v1/orders",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "dhl-api-key": self.settings.dhl_api_key,
                "Authorization": settings.authorization,
            },
        )
        return lib.Deserializable(response, lib.to_dict)
```

### Carrier-Specific Options Reference

**Note:** `is_return` and `outbound_tracking_number` are **explicit fields on ShipmentRequest**, not carrier options. The carrier-specific options below go in `options`:

| Option Key | Carrier | Type | Description |
|------------|---------|------|-------------|
| `ups_return_service_code` | UPS | `str` | Return type: `2`=Print&Mail, `3`=1-attempt, `5`=3-attempt, `8`=Electronic, `9`=Print |
| `fedex_return_type` | FedEx | `str` | `PRINT_RETURN_LABEL`, `EMAIL_RETURN_LABEL`, `PENDING`, `FEDEX_TAG` |
| `fedex_rma_reason` | FedEx | `str` | Return merchandise authorization reason |
| `dhl_parcel_de_receiver_id` | DHL Parcel DE | `str` | Return destination identifier (e.g., `"deu"`) |
| `dhl_parcel_de_label_type` | DHL Parcel DE | `str` | `BOTH` to get PDF + QR code |
| `mydhl_return_type` | DHL Express | `str` | `PH` (Return to Seller) or `PR` (Return to Origin) |
| `canadapost_return_type` | Canada Post | `str` | `authorized` (default) or `open` |

### Response Meta Fields

When `is_return` is true, the `ShipmentDetails.meta` dict will include:

| Meta Key | Type | Description |
|----------|------|-------------|
| `is_return` | `bool` | Always `True` for return shipments |
| `qr_code_url` | `str` | QR code URL for label-less returns (DHL Parcel DE, FedEx) |
| `outbound_tracking_number` | `str` | Original outbound tracking number (if provided) |
| `return_type` | `str` | Carrier-specific return type used |

### API Changes

**Endpoints affected:**

| Method | Endpoint | Change |
|--------|----------|--------|
| POST | `/v1/shipments` | Detects `is_return` field, routes to return flow |
| POST | `/v1/proxy/shipping` | Detects `is_return` field, routes to return flow |
| GET | `/v1/shipments` | Returns included by default; add `?is_return=true` or `?is_return=false` filter |
| GET | `/v1/shipments/{id}` | Response includes `is_return` field |

**Request example (return shipment):**

```json
{
  "service": "dhl_parcel_de_paket",
  "shipper": {
    "person_name": "Merchant Store",
    "address_line1": "Sträßchensweg 10",
    "city": "Bonn",
    "postal_code": "53113",
    "country_code": "DE"
  },
  "recipient": {
    "person_name": "Customer Name",
    "address_line1": "Hauptstrasse 1",
    "city": "Berlin",
    "postal_code": "10115",
    "country_code": "DE"
  },
  "parcels": [
    {"weight": 1.5, "weight_unit": "KG"}
  ],
  "is_return": true,
  "outbound_tracking_number": "123456789012",
  "options": {
    "dhl_parcel_de_receiver_id": "deu"
  }
}
```

**Response example:**

```json
{
  "id": "shp_return_abc123",
  "status": "purchased",
  "tracking_number": "340434310428091700",
  "shipment_identifier": "340434310428091700",
  "carrier_name": "dhl_parcel_de",
  "carrier_id": "dhl_parcel_de_account",
  "label_type": "PDF",
  "shipping_documents": [
    {
      "category": "label",
      "format": "PDF",
      "base64": "JVBERi0xLjQK..."
    }
  ],
  "meta": {
    "is_return": true,
    "qr_code_url": "https://www.dhl.de/retoure/qr/340434310428091700",
    "outbound_tracking_number": "123456789012",
    "return_type": "dhl_parcel_de_retoure"
  },
  "selected_rate": {
    "service": "dhl_parcel_de_paket",
    "carrier_name": "dhl_parcel_de",
    "total_charge": 4.99,
    "currency": "EUR"
  }
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| `is_return` with carrier that doesn't support returns | `MethodNotSupportedError` | Gateway raises error with carrier name |
| Return request without parcels | Validation error | ShipmentRequest validation (existing) |
| International return (customs required) | Customs data passed through | Carrier handles customs for returns; some restrict international returns |
| Return with same shipper and recipient address | Allowed (self-returns exist) | No special handling |
| DHL Parcel DE return without `receiver_id` | Use default `"deu"` | Fallback to country-based default |
| FedEx EMAIL_RETURN_LABEL without customer email | Error from carrier | Validate email presence for email return types |
| `outbound_tracking_number` for carrier that doesn't support linking | Ignored, stored in meta | Pass through to meta; don't error |
| Canada Post Open Return (batch labels) | Different flow from Authorized Return | Support via `canadapost_return_type: "open"` option |
| Auto-swap when `return_address` is explicitly set | Use `return_address` as return destination instead of swapped `shipper` | Check for explicit `return_address` before defaulting |
| USPS Scan-Based Return (pay on use) | Label generated, no upfront charge | Carrier handles billing; reflected in meta |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Carrier return API endpoint unreachable | Label not generated | Standard retry + error message with carrier context |
| DHL Parcel DE receiver_id invalid | 400 error from carrier | Validate against known receiver IDs; clear error message |
| Address swap creates invalid addresses | Carrier rejects request | Validate swapped addresses before API call |
| Carrier doesn't return QR code URL | Missing QR code in response | `qr_code_url` is optional in meta; graceful fallback |
| `create_return_shipment` not implemented for a carrier | `MethodNotSupportedError` | Clear error message indicating carrier doesn't support returns |
| USPS account not onboarded for returns | Carrier auth error | Document onboarding requirement; clear error message |
| Canada Post RAN validation fails | Return label not generated | Return error from Canada Post's validation |

---

## Implementation Plan

### Phase 1: SDK Foundation

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `is_return` and `outbound_tracking_number` to `ShipmentRequest` | `modules/sdk/karrio/core/models.py` | Pending | S |
| Add `create_return_shipment_request` to Mapper base | `modules/sdk/karrio/api/mapper.py` | Pending | S |
| Add `parse_return_shipment_response` to Mapper base | `modules/sdk/karrio/api/mapper.py` | Pending | S |
| Add `create_return_shipment` to Proxy base | `modules/sdk/karrio/api/proxy.py` | Pending | S |
| Update `Shipment.create` for `is_return` routing + address swap | `modules/sdk/karrio/api/interface.py` | Pending | M |

### Phase 2: Carrier Implementations

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| UPS return shipment (Pattern A — reuse shipment API) | `modules/connectors/ups/karrio/providers/ups/shipment/` | Pending | M |
| UPS return shipment tests | `modules/connectors/ups/tests/ups/test_shipment.py` | Pending | M |
| FedEx return shipment (Pattern A — reuse shipment API) | `modules/connectors/fedex/karrio/providers/fedex/shipment/` | Pending | M |
| FedEx return shipment tests | `modules/connectors/fedex/tests/fedex/test_shipment.py` | Pending | M |
| DHL Parcel DE return shipment (Pattern B — dedicated API) | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/` | Pending | L |
| DHL Parcel DE return tests | `modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/test_shipment.py` | Pending | M |
| DHL Express return shipment (Pattern A — VAS codes) | `modules/connectors/mydhl/karrio/providers/mydhl/shipment/` | Pending | M |
| DHL Express return tests | `modules/connectors/mydhl/tests/mydhl/test_shipment.py` | Pending | M |
| Canada Post authorized return (Pattern B — dedicated API) | `modules/connectors/canadapost/karrio/providers/canadapost/shipment/` | Pending | L |
| Canada Post return tests | `modules/connectors/canadapost/tests/canadapost/test_shipment.py` | Pending | M |
| USPS return label (Pattern B — dedicated API) | `modules/connectors/usps/karrio/providers/usps/shipment/` | Pending | L |
| USPS return tests | `modules/connectors/usps/tests/usps/test_shipment.py` | Pending | M |

### Phase 3: Server & API Layer

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update server gateway `Shipments.create` for `is_return` routing | `modules/core/karrio/server/core/gateway.py` | Pending | M |
| Add `is_return` and `outbound_tracking_number` to DRF serializers | `modules/core/karrio/server/core/serializers.py` | Pending | M |
| Add `is_return` field to Django Shipment model | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Add `outbound_tracking_number` to Shipment model (or meta) | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Create Django migration | `modules/manager/karrio/server/manager/migrations/` | Pending | S |
| Update shipment serializers for `is_return` / `outbound_tracking_number` | `modules/manager/karrio/server/manager/serializers/shipment.py` | Pending | M |
| Add `is_return` to Shipment `DIRECT_PROPS` | `modules/manager/karrio/server/manager/models.py` | Pending | S |
| Update GraphQL types with `is_return` field | `modules/graph/karrio/server/graph/schemas/base/types.py` | Pending | S |
| Django API tests | `modules/manager/karrio/server/manager/tests/` | Pending | M |

### Phase 4: Frontend & Types

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update TypeScript types for `is_return` option | `packages/types/rest/api.ts` | Pending | S |
| Update GraphQL types (if applicable) | `modules/graph/karrio/server/graph/schemas/` | Pending | M |

**Dependencies:** Phase 2 depends on Phase 1. Phase 3 depends on Phase 1. Phase 4 depends on Phase 3.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests (per carrier) | `modules/connectors/<carrier>/tests/` | Return request building + response parsing |
| Integration Tests | `modules/manager/karrio/server/manager/tests/` | API endpoint with `is_return` flag |

### Test Cases

#### Unit Tests — Carrier Return Shipment

```python
"""Test return shipment creation for DHL Parcel DE (dedicated API)."""

import unittest
from unittest.mock import ANY

class TestDHLParcelDEReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_create_return_shipment_request(self):
        """Verify return shipment request is built for DHL Parcel DE Returns API."""
        from karrio.providers.dhl_parcel_de.shipment.return_shipment import (
            return_shipment_request,
        )

        request = return_shipment_request(payload, settings)
        serialized = request.serialize()

        # print(serialized)  # Debug
        self.assertDictEqual(
            serialized,
            {
                "receiverId": "deu",
                "customerReference": "ORDER-123",
                "shipper": {
                    "name1": "Customer Name",
                    "addressStreet": "Hauptstrasse",
                    "addressHouse": "1",
                    "postalCode": "10115",
                    "city": "Berlin",
                    "country": "DEU",
                },
                "itemWeight": {"uom": "g", "value": 1500},
            },
        )

    def test_parse_return_shipment_response(self):
        """Verify return shipment response parsing from DHL Returns API."""
        from karrio.providers.dhl_parcel_de.shipment.return_shipment import (
            parse_return_shipment_response,
        )

        shipment, messages = parse_return_shipment_response(response, settings)

        # print(shipment)  # Debug
        self.assertIsNotNone(shipment)
        self.assertEqual(shipment.tracking_number, "340434310428091700")
        self.assertTrue(shipment.meta.get("is_return"))
        self.assertIsNotNone(shipment.meta.get("qr_code_url"))
```

#### Unit Tests — Address Auto-Swap

```python
"""Test address auto-swap for return shipments."""

import unittest

class TestReturnAddressSwap(unittest.TestCase):
    def test_addresses_swapped_for_return(self):
        """Verify shipper/recipient are swapped when is_return is True."""
        payload = {
            "service": "ups_ground",
            "shipper": {"person_name": "Merchant", "country_code": "US"},
            "recipient": {"person_name": "Customer", "country_code": "US"},
            "parcels": [{"weight": 1.0}],
            "is_return": True,
        }

        # After swap: customer becomes shipper, merchant becomes recipient
        # (because in the return flow, the customer is sending TO the merchant)
        # This is handled in the fluent interface's Shipment.create
```

#### Integration Tests — Django API

```python
"""Test shipment API with is_return flag."""

from unittest import mock

class TestReturnShipmentAPI(APITestCase):
    def test_create_return_shipment(self):
        """Verify API creates return shipment when is_return is True."""
        response = self.client.post(
            "/api/shipments",
            data={
                "service": "dhl_parcel_de_paket",
                "shipper": {... },  # Merchant address
                "recipient": {...},  # Customer address
                "parcels": [{...}],
                "is_return": True,
                "options": {
                    "dhl_parcel_de_receiver_id": "deu",
                },
            },
        )

        # print(response.data)  # Debug
        self.assertResponseNoErrors(response)
        self.assertTrue(response.data["meta"]["is_return"])
        self.assertIsNotNone(response.data["tracking_number"])
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run carrier-specific tests
python -m unittest discover -v -f modules/connectors/dhl_parcel_de/tests
python -m unittest discover -v -f modules/connectors/ups/tests
python -m unittest discover -v -f modules/connectors/fedex/tests
python -m unittest discover -v -f modules/connectors/canadapost/tests
python -m unittest discover -v -f modules/connectors/mydhl/tests
python -m unittest discover -v -f modules/connectors/usps/tests

# Run server tests
karrio test --failfast karrio.server.manager.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Address swap logic introduces bugs | High | Medium | Comprehensive unit tests; clear documentation of swap behavior |
| Carrier return APIs have authentication differences | Medium | Medium | DHL Parcel DE returns API has different auth — handle in proxy settings |
| USPS requires separate merchant onboarding for returns | High | High | Document requirement; fail with clear error message |
| Breaking change to `Shipment.create` fluent interface | High | Low | `is_return` check is additive; default path unchanged |
| Canada Post RAN web service requirement | Medium | Low | Out of scope for initial implementation; document as limitation |
| Multi-piece return shipments | Medium | Low | Use `to_multi_piece_shipment` for combining; test explicitly |
| QR code URL format varies by carrier | Low | Medium | Store as-is in meta; no URL normalization |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: `is_return` is a new option — existing requests without it are completely unaffected
- **SDK compatibility**: New Mapper/Proxy methods raise `MethodNotSupportedError` by default — no carrier breaks
- **Data compatibility**: If using existing Shipment model with `is_return` flag, existing shipments default to `False`
- **Feature flags**: Not needed — additive change with graceful degradation

### Data Migration

```python
# If adding is_return to existing Shipment model:
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("manager", "previous_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipment",
            name="is_return",
            field=models.BooleanField(default=False),
        ),
    ]
```

### Rollback Procedure

1. **Identify issue**: Monitor for API errors or unexpected address swaps
2. **Stop rollout**: Revert `Shipment.create` `is_return` routing (single file change)
3. **Revert carrier changes**: Each carrier's `create_return_shipment` is isolated
4. **Verify recovery**: Confirm standard shipment creation works correctly

---

## Appendices

### Appendix A: Carrier Return API Comparison

| Feature | UPS | FedEx | DHL Parcel DE | DHL Express | Canada Post | USPS |
|---------|-----|-------|--------------|-------------|-------------|------|
| **Separate Return API** | No | No | **Yes** | No | **Yes** | **Yes** |
| **Implementation Pattern** | A (reuse) | A (reuse) | B (dedicated) | A (reuse) | B (dedicated) | B (dedicated) |
| **How returns differ** | `ReturnService` element | `returnShipmentDetail` | Different endpoint + request | VAS codes `PH`/`PR` | `/authorizedreturn` | Returns Label API |
| **Address handling** | UPS swaps internally | User swaps | `receiverId` + `shipper` | User swaps | Receiver pre-configured | Pre-configured or in request |
| **RMA support** | Via reference fields | Native (`rma.reason`) | Via `customerReference` | Via reference fields | Native (RAN validation) | Via reference fields |
| **QR code / label-less** | No | Yes (email link) | **Yes** (`qrLink`) | Yes (QR validity) | No | No |
| **Pay-on-use** | No | No | No | No | **Yes** (bill on scan) | **Yes** (Scan-Based) |
| **Email return label** | Yes (ERL, code 8) | Yes (`EMAIL_RETURN_LABEL`) | No | No | No | No |

### Appendix B: Competitor API Comparison

| Feature | Karrio (proposed) | EasyPost | Shippo | ShipEngine/ShipStation |
|---------|-------------------|----------|--------|------------------------|
| **API approach** | `is_return` field on ShipmentRequest | `is_return` on shipment | `is_return` in `extra` | `is_return_label` on label |
| **Address swap** | Auto-swap | Auto-swap | Auto-swap (USPS/FedEx/UPS) | User provides correct direction |
| **Endpoint** | `POST /v1/shipments` | `POST /v1/shipments` | `POST /shipments` | `POST /v1/labels` |
| **Link to outbound** | Optional `outbound_tracking_number` | No native support | No native support | `POST /v1/labels/:id/return` |
| **Charge event** | Carrier-specific option | N/A | N/A | `charge_event` field |
| **QR code** | In meta (P1) | No | No | `paperless_download` |

### Appendix C: DHL Parcel DE Returns API Response Sample

```json
{
  "shipmentNo": "340434310428091700",
  "labelData": "JVBERi0xLjQK...",
  "qrLabelData": "iVBORw0KGgoAAAANSUhE...",
  "routingCode": "O/D53113+O1234/56789"
}
```

### Appendix D: UPS Return Service Codes

| Code | Service | Description |
|------|---------|-------------|
| `2` | Print and Mail | UPS prints label, mails to customer |
| `3` | Return 1-Attempt | UPS driver makes 1 pickup attempt |
| `5` | Return 3-Attempt | UPS driver makes 3 pickup attempts |
| `8` | Electronic Return Label | Label emailed to customer |
| `9` | Print Return Label | Merchant prints and includes with outbound |

### Appendix E: FedEx returnType Values

| Value | Description |
|-------|-------------|
| `PRINT_RETURN_LABEL` | Merchant prints return label |
| `EMAIL_RETURN_LABEL` | FedEx emails return label link + QR to customer |
| `PENDING` | Return label emailed, expires if unused |
| `FEDEX_TAG` | FedEx picks up return from customer |

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [x] All pending questions in "Open Questions & Decisions" have been asked
- [ ] All user decisions documented with rationale and date
- [ ] Edge cases requiring input have been resolved
- [ ] "Open Questions & Decisions" section cleaned up (all resolved)

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
