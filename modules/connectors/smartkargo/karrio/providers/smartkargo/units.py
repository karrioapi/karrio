
import karrio.lib as lib
import karrio.core.units as units


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")  # Example of label type config with PDF default


class PackagingType(lib.StrEnum):
    """ Carrier specific packaging type """
    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """ Carrier specific services """
    smartkargo_standard_service = "SmartKargo Standard Service"


class ShippingOption(lib.Enum):
    """ Carrier specific options """
    # smartkargo_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = smartkargo_coverage  #  maps unified karrio option to carrier specific

    pass


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """Maps carrier tracking status codes to normalized Karrio statuses."""
    pending = ["PENDING", "CREATED", "LABEL_PRINTED"]
    picked_up = ["PICKED_UP", "COLLECTED"]
    on_hold = ["ON_HOLD", "HELD"]
    delivered = ["DELIVERED", "POD"]
    in_transit = ["IN_TRANSIT", "DEPARTED", "ARRIVED"]
    delivery_failed = ["FAILED", "NOT_DELIVERED", "REFUSED"]
    delivery_delayed = ["DELAYED", "RESCHEDULED"]
    out_for_delivery = ["OUT_FOR_DELIVERY"]
    ready_for_pickup = ["READY_FOR_PICKUP"]


class TrackingIncidentReason(lib.Enum):
    """Maps carrier exception codes to normalized incident reasons.

    These codes map carrier-specific exception/status codes to standardized
    incident reasons for tracking events. The reason field helps identify
    why a delivery exception occurred.

    Update this enum with actual carrier-specific exception codes.
    """
    # Carrier-caused issues
    carrier_damaged_parcel = ["DAMAGED", "DMG"]
    carrier_sorting_error = ["MISROUTED", "MSR"]
    carrier_address_not_found = ["ADDRESS_NOT_FOUND", "ANF"]
    carrier_parcel_lost = ["LOST", "LP"]
    carrier_not_enough_time = ["LATE", "NO_TIME"]
    carrier_vehicle_issue = ["VEHICLE_BREAKDOWN", "VB"]

    # Consignee-caused issues
    consignee_refused = ["REFUSED", "RJ"]
    consignee_business_closed = ["BUSINESS_CLOSED", "BC"]
    consignee_not_available = ["NOT_AVAILABLE", "NA"]
    consignee_not_home = ["NOT_HOME", "NH"]
    consignee_incorrect_address = ["WRONG_ADDRESS", "IA"]
    consignee_access_restricted = ["ACCESS_RESTRICTED", "AR"]

    # Customs-related issues
    customs_delay = ["CUSTOMS_DELAY", "CD"]
    customs_documentation = ["CUSTOMS_DOCS", "CM"]
    customs_duties_unpaid = ["DUTIES_UNPAID", "DU"]

    # Weather/Force majeure
    weather_delay = ["WEATHER", "WE"]
    natural_disaster = ["NATURAL_DISASTER", "ND"]

    # Unknown
    unknown = []
