# Units Template

Template for `karrio/providers/[carrier]/units.py` — defines service enums, options, and mappings.

## Complete Template

```python
"""[Carrier] provider units and enums."""

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class PackagingType(lib.StrEnum):
    """Carrier packaging types mapped to Karrio packaging types."""
    carrier_your_packaging = "YOUR_PACKAGING"
    carrier_box = "BOX"
    carrier_envelope = "ENVELOPE"


class PackagePresets(lib.Enum):
    """Predefined package dimensions."""
    carrier_small_box = units.PackagePreset(
        weight=10.0, width=12.0, height=10.0, length=8.0,
        packaging_type="small_box",
        dimension_unit="IN", weight_unit="LB",
    )
    carrier_medium_box = units.PackagePreset(
        weight=25.0, width=18.0, height=14.0, length=12.0,
        packaging_type="medium_box",
        dimension_unit="IN", weight_unit="LB",
    )


class LabelType(lib.StrEnum):
    PDF = "PDF"
    ZPL = "ZPL"
    PNG = "PNG"


class WeightUnit(lib.StrEnum):
    LB = "LB"
    KG = "KG"


class DimensionUnit(lib.StrEnum):
    IN = "IN"
    CM = "CM"


class ShippingService(lib.StrEnum):
    """Map carrier service codes to Karrio service names.

    Usage:
        service = ShippingService.map("EXPRESS")  # Returns carrier_express
        code = ShippingService.carrier_express.value  # Returns "EXPRESS"
    """
    carrier_express = "EXPRESS"
    carrier_standard = "STANDARD"
    carrier_ground = "GROUND"
    carrier_overnight = "OVERNIGHT"
    carrier_economy = "ECONOMY"


class ShippingOption(lib.Enum):
    """Carrier-specific shipping options.

    Usage:
        options = lib.to_shipping_options(payload.options, ...)
        if options.carrier_signature_required.state:
            ...
    """
    carrier_signature_required = lib.OptionEnum("signatureRequired", bool)
    carrier_insurance = lib.OptionEnum("insurance", float)
    carrier_saturday_delivery = lib.OptionEnum("saturdayDelivery", bool)
    carrier_declared_value = lib.OptionEnum("declaredValue", float)

    # Standard Karrio options mapped to carrier options
    insurance = lib.OptionEnum("insurance", float)
    signature_confirmation = lib.OptionEnum("signatureRequired", bool)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Initialize shipping options with defaults."""
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    return units.ShippingOptions(_options, ShippingOption)


class TrackingStatus(lib.Enum):
    """Map carrier tracking status codes to normalized Karrio statuses.

    Normalized statuses:
        pending, in_transit, out_for_delivery, delivered,
        ready_for_pickup, delivery_failed, on_hold, unknown
    """
    on_hold = ["HOLD", "EXCEPTION"]
    delivered = ["DELIVERED", "COMPLETED"]
    in_transit = ["IN_TRANSIT", "SHIPPED", "DEPARTED"]
    delivery_failed = ["FAILED", "UNDELIVERABLE", "RETURNED"]
    out_for_delivery = ["OUT_FOR_DELIVERY"]
    ready_for_pickup = ["READY_FOR_PICKUP", "AVAILABLE"]


class ConnectionConfig(lib.Enum):
    """User-configurable connection settings."""
    label_type = lib.OptionEnum("label_type")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class CustomsOption(lib.Enum):
    """Customs-related options."""
    aes = lib.OptionEnum("aes")
    eel_pfc = lib.OptionEnum("eel_pfc")
    contents_type = lib.OptionEnum("contents_type")
    certificate_number = lib.OptionEnum("certificate_number")


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="Express Delivery",
        service_code="carrier_express",
        currency="USD",
        transit_days=1,
        max_weight=70,
        weight_unit="LB",
        zones=[models.ServiceZone(label="Domestic", rate=25.99)],
    ),
    models.ServiceLevel(
        service_name="Standard Delivery",
        service_code="carrier_standard",
        currency="USD",
        transit_days=5,
        max_weight=70,
        weight_unit="LB",
        zones=[models.ServiceZone(label="Domestic", rate=9.99)],
    ),
]
```

## Key Patterns

### Service Enum Bidirectional Mapping

```python
# Carrier code → Karrio name
service = ShippingService.map("EXPRESS")  # Returns ShippingService.carrier_express
karrio_name = service.name_or_key        # "carrier_express"

# Karrio name → Carrier code
carrier_code = ShippingService.carrier_express.value  # "EXPRESS"
```

### Options with Types

```python
# Boolean option
carrier_signature = lib.OptionEnum("signatureRequired", bool)

# Float option (monetary)
carrier_insurance = lib.OptionEnum("insurance", float)

# String option (default)
carrier_reference = lib.OptionEnum("reference")
```

### Tracking Status Mapping

```python
# Map carrier status to normalized status
status = next(
    (s.name for s in list(TrackingStatus) if carrier_status in s.value),
    "in_transit",  # Default fallback
)
```

### Hub Carrier Services (Dynamic)

For hub carriers like Easyship or ShipEngine, add static test services:

```python
class ShippingService(lib.StrEnum):
    hub_ups_ground = "UPS Ground via Hub"
    hub_fedex_express = "FedEx Express via Hub"
    # Dynamic services discovered at runtime
```
