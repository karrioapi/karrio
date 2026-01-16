# Product Requirements Document: OptionEnum Meta Field

**Project**: OptionEnum Meta Field Enhancement
**Version**: 1.1
**Date**: 2026-01-15
**Status**: Completed

---

## Summary

Add a `meta` field (generic dict) to `OptionEnum` to allow metadata on options. Primary use cases:
1. Categorize options via `meta=dict(category="...")`
2. Define service compatibility via `meta=dict(compatible_services=[...])`

---

## Current State

```python
@attr.s(auto_attribs=True)
class OptionEnum:
    code: str
    type: typing.Union[typing.Callable, MetaEnum] = str
    state: typing.Any = None
    default: typing.Any = None
    help: typing.Optional[str] = None
```

## Enhanced State

```python
@attr.s(auto_attribs=True)
class OptionEnum:
    code: str
    type: typing.Union[typing.Callable, MetaEnum] = str
    state: typing.Any = None
    default: typing.Any = None
    help: typing.Optional[str] = None
    meta: typing.Optional[dict] = None  # NEW
```

---

## Meta Field Structure

The `meta` dict supports these keys:

| Key | Type | Description |
|-----|------|-------------|
| `category` | `str` | Option category (UPPERCASE) |
| `compatible_services` | `list[str]` | Service codes this option is available for |

### Example

```python
dhl_parcel_de_cash_on_delivery = lib.OptionEnum(
    "cashOnDelivery",
    float,
    meta=dict(
        category="COD",
        compatible_services=["V01PAK", "V62KP"]
    )
)
```

---

## Usage

### Core Generic Options (in `units.py`)

```python
class ShippingOption(utils.Enum):
    cash_on_delivery = utils.OptionEnum("COD", float, meta=dict(category="COD"))
    insurance = utils.OptionEnum("insurance", float, meta=dict(category="INSURANCE"))
    is_return = utils.OptionEnum("is_return", bool, meta=dict(category="RETURN"))
    signature_confirmation = utils.OptionEnum("signature_confirmation", bool, meta=dict(category="SIGNATURE"))
    hold_at_location = utils.OptionEnum("hold_at_location", bool, meta=dict(category="PUDO"))
```

### Carrier-Specific Options (in carrier `units.py`)

```python
class ShippingOption(lib.Enum):
    # Carrier-specific options with category and compatible_services
    dhl_parcel_de_cash_on_delivery = lib.OptionEnum(
        "cashOnDelivery", float,
        meta=dict(category="COD", compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_signed_for_by_recipient = lib.OptionEnum(
        "signedForByRecipient", bool,
        meta=dict(category="SIGNATURE", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_additional_insurance = lib.OptionEnum(
        "additionalInsurance", float,
        meta=dict(category="INSURANCE", compatible_services=["V01PAK", "V53WPAK", "V54EPAK", "V62KP"])
    )

    # Universal mappings
    cash_on_delivery = dhl_parcel_de_cash_on_delivery
    signature_confirmation = dhl_parcel_de_signed_for_by_recipient
    insurance = dhl_parcel_de_additional_insurance
```

---

## Category Conventions

Categories are **UPPERCASE strings**. Standard categories:

| Category | Description | Core Options |
|----------|-------------|--------------|
| `COD` | Cash/Collect on Delivery | `cash_on_delivery` |
| `INSURANCE` | Shipment insurance | `insurance`, `insured_by` |
| `RETURN` | Return shipment | `is_return` |
| `SIGNATURE` | Signature confirmation | `signature_confirmation` |
| `PUDO` | Pick Up / Drop Off | `hold_at_location`, `hold_at_location_address` |
| `LOCKER` | Locker delivery | `locker_id` |
| `DANGEROUS_GOOD` | Hazmat/DG | `dangerous_good` |
| `NOTIFICATION` | Notifications | `sms_notification`, `email_notification`, `email_notification_to` |
| `DELIVERY_OPTIONS` | Delivery scheduling | `sunday_delivery`, `saturday_delivery` |
| `INSTRUCTIONS` | Shipment instructions | `shipment_note`, `shipper_instructions`, `recipient_instructions` |
| `INVOICE` | Invoice details | `invoice_date`, `invoice_number` |
| `PAPERLESS` | Paperless trade | `paperless_trade`, `doc_files`, `doc_references` |

---

## DHL Parcel DE Service-Option Compatibility Matrix

Based on official DHL documentation (Verfügbare Services):

### Services

| Code | Karrio Service Code | Description |
|------|---------------------|-------------|
| `V01PAK` | `dhl_parcel_de_paket` | DHL Paket (domestic) |
| `V53WPAK` | `dhl_parcel_de_paket_international` | DHL Paket International |
| `V54EPAK` | `dhl_parcel_de_europaket` | DHL Europaket |
| `V62KP` | `dhl_parcel_de_kleinpaket` | DHL Kleinpaket |
| `V66WPI` | `dhl_parcel_de_warenpost_international` | Warenpost International |

### Options Compatibility

| Option | V01PAK | V53WPAK | V54EPAK | V62KP | V66WPI |
|--------|:------:|:-------:|:-------:|:-----:|:------:|
| `premium` | | x | | | x |
| `closestDropPoint` | x | x | | x | |
| `preferredNeighbour` | x | | | | |
| `preferredLocation` | x | | | | |
| `visualCheckOfAge` | x | | | | |
| `namedPersonOnly` | x | | | | |
| `identCheck` | x | | | | |
| `signedForByRecipient` | x | | | | |
| `noNeighbourDelivery` | x | | | | |
| `preferredDay` | x | | | | |
| `endorsement` | x | x | | x | x |
| `additionalInsurance` | x | x* | x* | x | |
| `bulkyGoods` | x | | | x | |
| `cashOnDelivery` | x | | | x | |
| `parcelOutletRouting` | x | x* | | x | |
| `postalDeliveryDutyPaid` | | x | | | |
| `dhlRetoure` | x | | | x | |

*Note: x* = availability depends on destination country*

---

## Implementation

### 1. Update `karrio/core/utils/enum.py`

Add `meta` field to `OptionEnum` and preserve it in `__call__`:

```python
@attr.s(auto_attribs=True)
class OptionEnum:
    code: str
    type: typing.Union[typing.Callable, MetaEnum] = str
    state: typing.Any = None
    default: typing.Any = None
    help: typing.Optional[str] = None
    meta: typing.Optional[dict] = None

    def __call__(self, value: typing.Any = None) -> "OptionEnum":
        _value = value if value is not None else self.default

        if self.type in (bool,):
            _state = _value is not False
        elif isinstance(self.type, MetaEnum):
            _state = self.type.map(_value).name
        elif callable(self.type):
            _state = self.type(_value)
        else:
            _state = _value

        return OptionEnum(
            code=self.code,
            type=self.type,
            state=_state,
            default=self.default,
            help=self.help,
            meta=self.meta,
        )
```

### 2. Update `karrio/core/units.py`

✅ Already done - core `ShippingOption` members have `meta=dict(category="...")`.

### 3. Update `karrio/references.py`

✅ Already done - `meta=c.value.meta` added to options collection (line ~521).

### 4. Update DHL Parcel DE Connector

Update `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py`:

```python
class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    dhl_parcel_de_preferred_neighbour = lib.OptionEnum(
        "preferredNeighbour",
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_preferred_location = lib.OptionEnum(
        "preferredLocation",
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_named_person_only = lib.OptionEnum(
        "namedPersonOnly", bool,
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_signed_for_by_recipient = lib.OptionEnum(
        "signedForByRecipient", bool,
        meta=dict(category="SIGNATURE", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_preferred_day = lib.OptionEnum(
        "preferredDay",
        meta=dict(category="DELIVERY_OPTIONS", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_no_neighbour_delivery = lib.OptionEnum(
        "noNeighbourDelivery", bool,
        meta=dict(category="DELIVERY_OPTIONS", compatible_services=["V01PAK"])
    )
    dhl_parcel_de_additional_insurance = lib.OptionEnum(
        "additionalInsurance", float,
        meta=dict(category="INSURANCE", compatible_services=["V01PAK", "V53WPAK", "V54EPAK", "V62KP"])
    )
    dhl_parcel_de_bulky_goods = lib.OptionEnum(
        "bulkyGoods", bool,
        meta=dict(compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_cash_on_delivery = lib.OptionEnum(
        "cashOnDelivery", float,
        meta=dict(category="COD", compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_premium = lib.OptionEnum(
        "premium", bool,
        meta=dict(compatible_services=["V53WPAK", "V66WPI"])
    )
    dhl_parcel_de_closest_drop_point = lib.OptionEnum(
        "closestDropPoint", bool,
        meta=dict(category="PUDO", compatible_services=["V01PAK", "V53WPAK", "V62KP"])
    )
    dhl_parcel_de_parcel_outlet_routing = lib.OptionEnum(
        "parcelOutletRouting",
        meta=dict(compatible_services=["V01PAK", "V53WPAK", "V62KP"])
    )
    dhl_parcel_de_postal_delivery_duty_paid = lib.OptionEnum(
        "postalDeliveryDutyPaid", bool,
        meta=dict(compatible_services=["V53WPAK"])
    )
    dhl_parcel_de_locker_id = lib.OptionEnum(
        "lockerID", lib.to_int,
        meta=dict(category="LOCKER", compatible_services=["V01PAK", "V62KP"])
    )
    dhl_parcel_de_ident_check = lib.OptionEnum(
        "identCheck", ship_req.IdentCheckType,
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_visual_check_of_age = lib.OptionEnum(
        "visualCheckOfAge",
        lib.units.create_enum("VisualCheckOfAge", ["A16", "A18"]),
        meta=dict(compatible_services=["V01PAK"])
    )
    dhl_parcel_de_endorsement = lib.OptionEnum(
        "endorsement",
        lib.units.create_enum("endorsement", ["RETURN", "SIGNATURE"]),
        default="RETURN",
        meta=dict(compatible_services=["V01PAK", "V53WPAK", "V62KP", "V66WPI"])
    )
    dhl_parcel_de_dhl_retoure = lib.OptionEnum(
        "dhlRetoure", ship_req.DhlRetoureType,
        meta=dict(category="RETURN", compatible_services=["V01PAK", "V62KP"])
    )
    # fmt: on

    """ Unified Option type mapping """
    signature_confirmation = dhl_parcel_de_signed_for_by_recipient
    hold_at_location = dhl_parcel_de_closest_drop_point
    cash_on_delivery = dhl_parcel_de_cash_on_delivery
    insurance = dhl_parcel_de_additional_insurance
    locker_id = dhl_parcel_de_locker_id
```

### 5. Update Other Carrier Connectors

Add `meta=dict(category="...", compatible_services=[...])` to other carrier options as documentation becomes available.

---

## Implementation Status

| Task | Status |
|------|--------|
| Update `OptionEnum` in `karrio/core/utils/enum.py` | ✅ Done |
| Update `karrio/references.py` | ✅ Done |
| Core `ShippingOption` categories | ✅ Done |
| DHL Parcel DE categories + compatible_services | ✅ Done |
| All other connectors (categories) | ✅ Done |

---

## Backward Compatibility

- `meta` field is optional, defaults to `None`
- Existing options continue to work unchanged
- No database migration required

---

*End of PRD*
