# Plan: FedEx Configurable `fedex_pickup_type` Option

FedEx's `pickupType` field (which describes how a shipper tenders a package — drop off, scheduled, or on-call) is hardcoded to `DROPOFF_AT_FEDEX_LOCATION` in both the rate and shipment request builders. This adds it as a standard FedEx `ShippingOption` so API consumers can send any of the three valid Ship API values. Default behaviour is unchanged (backward-compatible).

## Context

`pickupType` is hardcoded as `"DROPOFF_AT_FEDEX_LOCATION"` in both:

- `modules/connectors/fedex/karrio/providers/fedex/shipment/create.py` (line 293)
- `modules/connectors/fedex/karrio/providers/fedex/rate.py` (line 214)

Valid FedEx Ship API values (from `ship-api.json`, `rate-api.json`, and the API Reference Guide `#pickuptypes` table):

| Enumeration                 | Description                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| `DROPOFF_AT_FEDEX_LOCATION` | Shipment will be dropped off at a FedEx Location (current default) |
| `CONTACT_FEDEX_TO_SCHEDULE` | FedEx will be contacted to request a pickup                        |
| `USE_SCHEDULED_PICKUP`      | Shipment will be picked up as part of a regular scheduled pickup   |

Note: `ON_CALL`, `PACKAGE_RETURN_PROGRAM`, `REGULAR_STOP` are Pickup API values only — they do not belong in the shipment/rate request and should not be included in this option.

## Design Decisions

- **FedEx-only `ShippingOption`** — no SDK `ShipmentRequest` model changes
- Unified `PickupRequest.pickup_type` (`one_time`/`daily`/`recurring`) is a _different_ concept (it schedules a carrier driver pickup event). The field we are adding answers "how does this shipment get to the carrier?" — set at shipment creation time.
- `dpd_meta_dropoff_type` is a false cognate (controls label format at drop-off point, not tendering method) — not a reference pattern for this change
- `help` text exposure in the API endpoint is out of scope — separate PR
- Purolator (`PickupType`: `DropOff`/`PreScheduled`) and DHL Poland (`dropOffType`: `REGULAR_PICKUP`) also hardcode this concept — noted as future work, not in scope here
- Default remains `DROPOFF_AT_FEDEX_LOCATION` — zero behaviour change for existing integrations

## Implementation Steps

### Step 1 — `units.py`: add `FedExPickupType` StrEnum

File: `modules/connectors/fedex/karrio/providers/fedex/units.py`

Add before the `ConnectionConfig` class:

```python
class FedExPickupType(lib.StrEnum):
    """How the shipper will tender the package to FedEx (Ship API / Rate API)."""
    # Shipper brings the package to a FedEx drop-off location
    dropoff_at_fedex_location = "DROPOFF_AT_FEDEX_LOCATION"
    # FedEx will be contacted to schedule a one-time pickup
    contact_fedex_to_schedule = "CONTACT_FEDEX_TO_SCHEDULE"
    # Package will be collected as part of a regular standing pickup schedule
    use_scheduled_pickup = "USE_SCHEDULED_PICKUP"
```

### Step 2 — `units.py`: add `fedex_pickup_type` to `ShippingOption`

In the same file, add to the `ShippingOption` enum inside the delivery options group (near `fedex_saturday_delivery`):

```python
fedex_pickup_type = lib.OptionEnum(
    "fedex_pickup_type",
    str,
    help=(
        "How the shipper will tender the package to FedEx. "
        "Valid values: DROPOFF_AT_FEDEX_LOCATION, CONTACT_FEDEX_TO_SCHEDULE, USE_SCHEDULED_PICKUP. "
        "Defaults to DROPOFF_AT_FEDEX_LOCATION."
    ),
    meta=dict(category="DELIVERY_OPTIONS"),
)
```

### Step 3 — `shipment/create.py`: replace hardcoded `pickupType`

File: `modules/connectors/fedex/karrio/providers/fedex/shipment/create.py`, line 293

Replace:

```python
pickupType="DROPOFF_AT_FEDEX_LOCATION",
```

With:

```python
pickupType=(options.fedex_pickup_type.state or "DROPOFF_AT_FEDEX_LOCATION"),
```

### Step 4 — `rate.py`: replace hardcoded `pickupType`

File: `modules/connectors/fedex/karrio/providers/fedex/rate.py`, line 214

Replace:

```python
pickupType="DROPOFF_AT_FEDEX_LOCATION",
```

With:

```python
pickupType=(options.fedex_pickup_type.state or "DROPOFF_AT_FEDEX_LOCATION"),
```

### Step 5 — `i18n.py`: add translation entry

File: `modules/connectors/fedex/karrio/providers/fedex/i18n.py`

Add to `OPTION_NAME_TRANSLATIONS`:

```python
"fedex_pickup_type": _("FedEx Pickup Type"),
```

### Step 6 — `test_shipment.py`: add 2 new test methods + fixture constants

File: `modules/connectors/fedex/tests/fedex/test_shipment.py`

Add two fixture constants (minimal diffs of the existing `ShipmentRequest` fixture with only `pickupType` changed):

```python
ShipmentUseScheduledPickupRequest = {
    ...  # copy of ShipmentRequest with "pickupType": "USE_SCHEDULED_PICKUP"
}

ShipmentContactFedexPickupRequest = {
    ...  # copy of ShipmentRequest with "pickupType": "CONTACT_FEDEX_TO_SCHEDULE"
}
```

Add two new test methods to `TestFedExShipping`:

```python
def test_create_shipment_request_with_use_scheduled_pickup(self):
    request = gateway.mapper.create_shipment_request(
        models.ShipmentRequest(**{**ShipmentPayload, "options": {"fedex_pickup_type": "USE_SCHEDULED_PICKUP"}})
    )
    self.assertEqual(request.serialize(), ShipmentUseScheduledPickupRequest)

def test_create_shipment_request_with_contact_fedex_pickup(self):
    request = gateway.mapper.create_shipment_request(
        models.ShipmentRequest(**{**ShipmentPayload, "options": {"fedex_pickup_type": "CONTACT_FEDEX_TO_SCHEDULE"}})
    )
    self.assertEqual(request.serialize(), ShipmentContactFedexPickupRequest)
```

### Step 7 — `test_rate.py`: add 1 new test method + fixture constant

File: `modules/connectors/fedex/tests/fedex/test_rate.py`

Add one fixture constant (minimal diff of existing `RateRequest` with only `pickupType` changed):

```python
RateUseScheduledPickupRequest = {
    ...  # copy of RateRequest with "pickupType": "USE_SCHEDULED_PICKUP"
}
```

Add one new test method to `TestFedExRating`:

```python
def test_create_rate_request_with_use_scheduled_pickup(self):
    request = gateway.mapper.create_rate_request(
        models.RateRequest(**{**RatePayload, "options": {"fedex_pickup_type": "USE_SCHEDULED_PICKUP"}})
    )
    self.assertEqual(request.serialize(), RateUseScheduledPickupRequest)
```

## Files Changed

| File                                                                 | Change                                                          |
| -------------------------------------------------------------------- | --------------------------------------------------------------- |
| `modules/connectors/fedex/karrio/providers/fedex/units.py`           | Add `FedExPickupType` enum + `ShippingOption.fedex_pickup_type` |
| `modules/connectors/fedex/karrio/providers/fedex/shipment/create.py` | Replace hardcoded `pickupType` at line 293                      |
| `modules/connectors/fedex/karrio/providers/fedex/rate.py`            | Replace hardcoded `pickupType` at line 214                      |
| `modules/connectors/fedex/karrio/providers/fedex/i18n.py`            | Add `"fedex_pickup_type"` translation                           |
| `modules/connectors/fedex/tests/fedex/test_shipment.py`              | Add 2 tests + 2 fixture constants                               |
| `modules/connectors/fedex/tests/fedex/test_rate.py`                  | Add 1 test + 1 fixture constant                                 |

## Verification

```bash
source bin/activate-env
python -m unittest discover -v -f modules/connectors/fedex/tests
```

All 7 existing tests must pass unchanged — confirming `DROPOFF_AT_FEDEX_LOCATION` remains the default when no option is supplied.

The 3 new tests each call `request.serialize()` and directly assert `"pickupType"` in the resulting dict equals the option value passed.

## Future Work (out of scope)

- Expose `OptionEnum.help` through `GET /v1/carriers/fedex/options` API endpoint
- Add equivalent `purolator_pickup_type` option to Purolator connector (`DropOff`/`PreScheduled`)
- Add equivalent `dhl_poland_dropoff_type` option to DHL Poland connector
- Consider a unified `tendering_type` field on `ShipmentRequest` once all three carriers are done
- The 'create_label` core module for the Dashboard only renders boolean "CheckBoxField" options and skips other options so we can't see this option via the Dashboard atm
