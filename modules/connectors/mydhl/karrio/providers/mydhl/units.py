import karrio.lib as lib
import karrio.core.units as units


class LabelFormat(lib.StrEnum):
    PDF = "pdf"
    ZPL = "zpl"
    EPL = "epl"
    LP2 = "lp2"

    """ Unified Label format mapping """
    PNG = PDF


class UploadDocumentType(lib.StrEnum):
    """Carrier specific document image type"""

    invoice = "INV"
    proforma = "PNV"
    certificate_of_origin = "COO"
    nafta_certificate_of_origin = "NAF"
    commercial_invoice = "CIN"
    custom_declaration = "DCL"
    air_waybill = "AWB"

    """ Unified Document type mapping """
    pro_forma_invoice = proforma


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

    mydhl_standard_service = "DHL Express Standard Service"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # mydhl_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = mydhl_coverage  #  maps unified karrio option to carrier specific

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
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
