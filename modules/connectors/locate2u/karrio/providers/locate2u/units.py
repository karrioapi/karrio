import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


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

    locate2u_local_delivery = "Locate2u Local Delivery"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    appointment_time = lib.OptionEnum("appointment_time")
    time_window_start = lib.OptionEnum("time_window_start")
    time_window_end = lib.OptionEnum("time_window_end")
    brand_id = lib.OptionEnum("brand_id")
    duration_minutes = lib.OptionEnum("duration_minutes", lib.to_int)
    assigned_team_member_id = lib.OptionEnum("assigned_team_member_id")
    source = lib.OptionEnum("source")
    customer_id = lib.OptionEnum("customer_id")
    run_number = lib.OptionEnum("run_number")
    team_region_id = lib.OptionEnum("team_region_id")
    driver_instructions = lib.OptionEnum("driver_instructions")
    notes = lib.OptionEnum("notes")
    latitude = lib.OptionEnum("latitude", float)
    longitude = lib.OptionEnum("longitude", float)


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
    on_hold = ["On Hold"]
    delivered = ["Complete"]
    in_transit = ["Pending", "Enroute"]
    delivery_failed = ["Failed", "Cancelled"]
    delivery_delayed = ["Delayed"]
    out_for_delivery = ["Arrived"]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="Locate2u Local Delivery",
        service_code="locate2u_local_delivery",
        currency="AUD",
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
]
