"""Example: Units Configuration Pattern

This example demonstrates how to define carrier-specific units (services, options,
packaging types, tracking status) in a Karrio carrier integration.
"""

# === FILE: karrio/providers/[carrier]/units.py ===

import karrio.lib as lib
import karrio.core.units as units


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options.
    
    These options can be set at the carrier connection level
    in the Karrio dashboard or API.
    """
    # Currency preference for rates
    currency = lib.OptionEnum("currency", str, "USD")
    
    # Label format preference
    label_type = lib.OptionEnum("label_type", str, "PDF")
    
    # Carrier-specific account options
    cost_centre_id = lib.OptionEnum("cost_centre_id", str)
    cost_centre_name = lib.OptionEnum("cost_centre_name", str)
    
    # Custom service/option lists (for hub carriers)
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class WeightUnit(lib.StrEnum):
    """Carrier weight unit mapping."""
    KG = "KG"
    LB = "LBS"
    OZ = "OZ"


class DimensionUnit(lib.StrEnum):
    """Carrier dimension unit mapping."""
    CM = "CM"
    IN = "IN"


class PackagingType(lib.StrEnum):
    """Carrier-specific packaging types.
    
    First section: Carrier's actual packaging codes
    Second section: Karrio unified types mapped to carrier codes
    """
    # Carrier-specific packaging types (actual API values)
    carrier_envelope = "ENVELOPE"
    carrier_pak = "PAK"
    carrier_small_box = "SMALL_BOX"
    carrier_medium_box = "MEDIUM_BOX"
    carrier_large_box = "LARGE_BOX"
    carrier_tube = "TUBE"
    carrier_pallet = "PALLET"
    carrier_custom = "YOUR_PACKAGING"
    
    # Unified Karrio packaging type mapping
    # Maps Karrio's standard types to carrier-specific values
    envelope = carrier_envelope
    pak = carrier_pak
    tube = carrier_tube
    pallet = carrier_pallet
    small_box = carrier_small_box
    medium_box = carrier_medium_box
    large_box = carrier_large_box
    your_packaging = carrier_custom


class ShippingService(lib.StrEnum):
    """Carrier-specific shipping services.
    
    Format: carrier_service_name = "Carrier API Code"
    
    The enum name (left side) becomes the Karrio service identifier.
    The value (right side) is what gets sent to the carrier API.
    """
    # Domestic services
    carrier_ground = "GROUND"
    carrier_express = "EXPRESS"
    carrier_express_saver = "EXPRESS_SAVER"
    carrier_overnight = "NEXT_DAY"
    carrier_two_day = "2_DAY"
    
    # International services
    carrier_international_priority = "INTL_PRIORITY"
    carrier_international_economy = "INTL_ECONOMY"
    carrier_international_express = "INTL_EXPRESS"
    
    # Special services
    carrier_freight = "FREIGHT_LTL"
    carrier_same_day = "SAME_DAY"


class ShippingOption(lib.Enum):
    """Carrier-specific shipping options.
    
    Format: option_name = lib.OptionEnum("carrier_code", type)
    
    Use lib.OptionEnum to define the carrier's option code and expected type.
    """
    # Carrier-specific options with their API codes
    carrier_signature_required = lib.OptionEnum("SIGNATURE", bool)
    carrier_adult_signature = lib.OptionEnum("ADULT_SIGNATURE", bool)
    carrier_saturday_delivery = lib.OptionEnum("SATURDAY_DELIVERY", bool)
    carrier_hold_for_pickup = lib.OptionEnum("HOLD_FOR_PICKUP", bool)
    carrier_insurance = lib.OptionEnum("INSURANCE", float)
    carrier_declared_value = lib.OptionEnum("DECLARED_VALUE", float)
    carrier_cod = lib.OptionEnum("COD", float)
    carrier_dry_ice = lib.OptionEnum("DRY_ICE", float)
    carrier_dangerous_goods = lib.OptionEnum("DANGEROUS_GOODS", bool)
    carrier_reference_1 = lib.OptionEnum("REFERENCE_1", str)
    carrier_reference_2 = lib.OptionEnum("REFERENCE_2", str)
    
    # Unified Karrio option mapping
    # Maps Karrio's standard options to carrier-specific options
    signature_required = carrier_signature_required
    saturday_delivery = carrier_saturday_delivery
    insurance = carrier_insurance
    cash_on_delivery = carrier_cod
    hold_at_location = carrier_hold_for_pickup


class CustomsOption(lib.Enum):
    """Carrier-specific customs options for international shipments."""
    carrier_eori_number = lib.OptionEnum("EORI", str)
    carrier_vat_number = lib.OptionEnum("VAT", str)
    carrier_tax_id = lib.OptionEnum("TAX_ID", str)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Initialize and merge shipping options.
    
    This function is called by lib.to_shipping_options() to process
    and validate options before they're used in requests.
    """
    # Merge package-level options if provided
    if package_options is not None:
        options.update(package_options.content)
    
    # Filter function to validate options
    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore
    
    return units.ShippingOptions(
        options,
        ShippingOption,
        items_filter=items_filter,
    )


class TrackingStatus(lib.Enum):
    """Carrier tracking status mapping to Karrio unified statuses.
    
    Each Karrio status maps to a list of carrier-specific status codes.
    This allows mapping multiple carrier codes to a single unified status.
    """
    # Pending/Pre-transit
    pending = ["PENDING", "LABEL_CREATED", "PRE_TRANSIT", "MANIFESTED"]
    
    # In Transit
    in_transit = [
        "IN_TRANSIT",
        "TRANSIT",
        "DEPARTED",
        "ARRIVED",
        "PROCESSING",
        "CUSTOMS_CLEARANCE",
        "IN_CUSTOMS",
        "EXPORT_CUSTOMS",
        "IMPORT_CUSTOMS",
    ]
    
    # Out for Delivery
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
        "ON_VEHICLE",
        "WITH_DRIVER",
        "DELIVERY_SCHEDULED",
    ]
    
    # Delivered
    delivered = [
        "DELIVERED",
        "DELIVERY_CONFIRMED",
        "SIGNED",
        "POD_RECEIVED",
    ]
    
    # Ready for Pickup
    ready_for_pickup = [
        "READY_FOR_PICKUP",
        "AT_PICKUP_POINT",
        "AWAITING_COLLECTION",
        "AVAILABLE_FOR_PICKUP",
    ]
    
    # Delivery Failed
    delivery_failed = [
        "DELIVERY_FAILED",
        "FAILED_DELIVERY",
        "DELIVERY_EXCEPTION",
        "UNDELIVERABLE",
        "REFUSED",
        "NOT_HOME",
    ]
    
    # Delivery Delayed
    delivery_delayed = [
        "DELAYED",
        "WEATHER_DELAY",
        "MECHANICAL_DELAY",
        "CUSTOMS_DELAY",
    ]
    
    # On Hold
    on_hold = [
        "ON_HOLD",
        "HELD",
        "HOLD",
        "AWAITING_INSTRUCTIONS",
        "ADDRESS_ISSUE",
    ]
    
    # Return
    return_to_sender = [
        "RETURNING",
        "RETURN_TO_SENDER",
        "RTS",
        "RETURNED",
    ]


class LabelType(lib.StrEnum):
    """Carrier-supported label formats."""
    PDF = "PDF"
    PNG = "PNG"
    ZPL = "ZPL"
    EPL = "EPL"


# === Usage Examples ===

"""
# In rate.py or shipment/create.py:

def rate_request(payload, settings):
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    # Access options with type safety
    signature = options.signature_required.state  # bool or None
    insurance = options.insurance.state  # float or None
    
    # Map services
    services = lib.to_services(payload.services, provider_units.ShippingService)
    for service in services:
        service_code = service.value_or_key  # Gets carrier API code
        service_name = service.name_or_key   # Gets Karrio service name

# In tracking.py:

def _extract_details(data, settings):
    # Map carrier status to Karrio unified status
    carrier_status = data.get("status", "UNKNOWN")
    status = provider_units.TrackingStatus.map(carrier_status)
    
    return models.TrackingDetails(
        status=status.value,  # Unified status enum value
        # ...
    )
"""
