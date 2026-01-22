import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

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
    """Carrier specific services"""

    sendle_standard_pickup = "STANDARD-PICKUP"
    sendle_standard_dropoff = "STANDARD-DROPOFF"
    sendle_express_pickup = "EXPRESS-PICKUP"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    sendle_hide_pickup_address = lib.OptionEnum("hide_pickup_address", bool, meta=dict(category="DELIVERY_OPTIONS"))
    sendle_first_mile_option = lib.OptionEnum("first_mile_option", bool, meta=dict(category="DELIVERY_OPTIONS"))


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
    on_hold = ["Pickup Attempted", "Delivery Attempted"]
    delivered = ["Delivered"]
    in_transit = ["Pickup", "Drop Off", "Dropped Off", "In Transit"]
    delivery_failed = ["Damaged", "Unable to Deliver"]
    delivery_delayed = ["Card Left"]
    out_for_delivery = ["Out for Delivery", "Local Delivery"]
    ready_for_pickup = ["Left with Agent"]


class TrackingIncidentReason(lib.Enum):
    """Maps Sendle exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["Damaged", "Package Damaged", "Parcel Damaged"]
    carrier_sorting_error = ["Sorting Error", "Misrouted"]
    carrier_address_not_found = ["Address Not Found", "Unable to Locate Address"]
    carrier_parcel_lost = ["Lost", "Missing"]
    carrier_not_enough_time = ["Insufficient Time", "Time Constraint"]
    carrier_vehicle_issue = ["Vehicle Issue", "Transport Issue"]

    # Consignee-caused issues
    consignee_refused = ["Refused", "Delivery Refused", "Recipient Refused"]
    consignee_business_closed = ["Business Closed", "Closed"]
    consignee_not_available = ["Not Available", "Recipient Not Available"]
    consignee_not_home = ["Not Home", "No One Home", "Card Left"]
    consignee_incorrect_address = ["Incorrect Address", "Wrong Address"]
    consignee_access_restricted = ["Access Restricted", "Unable to Access"]

    # Customs-related issues
    customs_delay = ["Customs Delay", "Customs Hold", "Customs Processing"]
    customs_documentation = ["Customs Documentation", "Missing Documents"]
    customs_duties_unpaid = ["Duties Unpaid", "Customs Fees Outstanding"]

    # Weather/Force majeure
    weather_delay = ["Weather Delay", "Weather", "Severe Weather"]
    natural_disaster = ["Natural Disaster", "Emergency Situation"]

    # Delivery exceptions
    delivery_exception_hold = ["Held at Agent", "Left with Agent", "Pickup Attempted", "Delivery Attempted"]
    delivery_exception_undeliverable = ["Unable to Deliver", "Undeliverable"]

    # Other issues
    unknown = []
