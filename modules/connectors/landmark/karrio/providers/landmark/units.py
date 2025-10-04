
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class WeightUnit(lib.StrEnum):
    LB = "LB"
    KG = "KG"
    G = "G"


class DimensionUnit(lib.StrEnum):
    IN = "IN"
    CM = "CM"


class LabelFormat(lib.StrEnum):
    PDF = "PDF"
    JPG = "JPG"
    GIF = "GIF"
    BMP = "BMP"
    ZPL = "ZPL"
    PNG = "PNG"


class LabelEncoding(lib.StrEnum):
    LINKS = "LINKS"
    BASE64 = "BASE64"
    BASE64COMPRESSED = "BASE64COMPRESSED"


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


class ConnectionConfig(lib.Enum):
    """ Landmark connection configuration options """
    label_type = lib.OptionEnum("label_type", LabelFormat, default="PDF")
    account_currency = lib.OptionEnum("account_currency", str, default="EUR")
    import_request_by_default = lib.OptionEnum("import_request_by_default", bool, default=False)
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingService(lib.StrEnum):
    """ Carrier specific services """
    # MaxiPak Scan DDP shipments
    landmark_maxipak_ddp = "LGINTSTD"
    # MaxiPak Scan DDU shipments
    landmark_maxipak_ddu = "LGINTSTDU"
    # MiniPak Scan DDP shipments (EU ONLY)
    landmark_minipak_ddp = "LGINTBPIP"
    # MiniPak Scan DDU shipments (EU & ROW)
    landmark_minipak_ddu = "LGINTBPIU"


class ShippingOption(lib.Enum):
    """ Carrier specific options """

    landmark_shipment_insurance_freight = lib.OptionEnum("ShipmentInsuranceFreight", float)
    landmark_order_insurance_freight_total = lib.OptionEnum("OrderInsuranceFreightTotal", float)

    """ Unified Option type mapping """
    landmark_produce_label = lib.OptionEnum("ProduceLabel", bool)
    landmark_import_request = lib.OptionEnum("InportRequest", bool)
    fulfilled_by_landmark = lib.OptionEnum("FulfilledByLandmark", bool)
    landmark_freight_pro_number = lib.OptionEnum("FreightProNumber", str)
    landmark_freight_piece_unit = lib.OptionEnum("FreightPieceUnit", str)
    landmark_return_address_code = lib.OptionEnum("ReturnAddressCode", str)

    """ unified option type mapping """
    insurance = landmark_shipment_insurance_freight


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
    """Carrier tracking status mapping"""
    delivered = [
        "500",  # Item successfully delivered
        "510",  # Proof Of Delivery
    ]
    in_transit = [
        "50",   # Shipment Data Uploaded
        "60",   # Shipment inventory allocated
        "75",   # Shipment Processed
        "80",   # Shipment Fulfilled
        "100",  # Shipment information transmitted to carrier
        "125",  # Customs Cleared
        "150",  # Crossing Border
        "155",  # Crossing Received
        "200",  # Item scanned at postal facility
        "225",  # Item grouped at Landmark or partner facility
        "250",  # Item scanned for crossing
        "275",  # Item in transit with carrier
    ]
    on_hold = [
        "90",   # Shipment held for payment
        "135",  # Customs Issue
    ]
    delivery_failed = [
        "900",  # Delivery failed
    ]
    delivery_delayed = [
        "400",  # Attempted delivery
        "450",  # Item re-directed to new address
    ]
    out_for_delivery = [
        "300",  # Item out for delivery
    ]
    ready_for_pickup = [
        "410",  # Item available for pickup
    ]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name=f"Landmark {service.value}",
        service_code=service.name,
        currency=ConnectionConfig.account_currency.value,
        zones=[models.ServiceZone(label="Flat Rate", rate=0.0)],
    )
    for service in ShippingService
]
