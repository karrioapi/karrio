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

    laposte_standard_service = "La Poste Standard Service"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # laposte_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = laposte_coverage  #  maps unified karrio option to carrier specific

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
    delivered = ["DI1"]
    in_transit = [""]
    out_for_delivery = ["MD2", "ET1"]


class TrackingIncidentReason(lib.Enum):
    """Maps La Poste exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = []
    carrier_sorting_error = []
    carrier_address_not_found = ["AN1"]
    carrier_parcel_lost = []
    carrier_vehicle_issue = []

    # Consignee-caused issues
    consignee_refused = ["RE1"]
    consignee_business_closed = []
    consignee_not_available = ["ND1", "AG1"]
    consignee_not_home = ["ND1"]
    consignee_incorrect_address = ["AN1"]
    consignee_access_restricted = []

    # Customs-related issues
    customs_delay = ["DO1"]
    customs_documentation = []
    customs_duties_unpaid = []

    # Weather/Force majeure
    weather_delay = []
    natural_disaster = []

    # Other issues
    unknown = []
