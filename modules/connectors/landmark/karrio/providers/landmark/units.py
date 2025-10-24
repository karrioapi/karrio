import csv
import pathlib
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


class ConnectionConfig(lib.Enum):
    """Landmark connection configuration options"""

    label_type = lib.OptionEnum("label_type", LabelFormat, default="PDF")
    account_currency = lib.OptionEnum("account_currency", str, default="EUR")
    import_request_by_default = lib.OptionEnum(
        "import_request_by_default", bool, default=False
    )
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingServiceName(lib.StrEnum):
    """Carrier specific services"""

    # fmt: off
    landmark_maxipak_scan_ddp = "MaxiPak Scan DDP"
    landmark_maxipak_scan_ddu = "MaxiPak Scan DDU"
    landmark_minipak_scan_ddp = "MiniPak Scan DDP (EU Only)"
    landmark_minipak_scan_ddu = "MiniPak Scan DDU shipments (EU & ROW)"
    landmark_maxipak_scan_premium_ups_express_ddp = "MaxiPak Scan Premium UPS Express DDP"
    landmark_maxipak_scan_premium_ups_express_ddu = "MaxiPak Scan Premium UPS Express DDU"
    landmark_maxipak_scan_premium_ups_standard_ddp = "MaxiPak Scan Premium UPS Standard DDP"
    landmark_maxipak_scan_premium_ups_standard_ddu = "MaxiPak Scan Premium UPS Standard DDU"
    # fmt: on


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    # MaxiPak Scan DDP shipments
    landmark_maxipak_scan_ddp = "LGINTSTD"
    # MaxiPak Scan DDU shipments
    landmark_maxipak_scan_ddu = "LGINTSTDU"
    # MiniPak Scan DDP shipments (EU ONLY)
    landmark_minipak_scan_ddp = "LGINTBPIP"
    # MiniPak Scan DDU shipments (EU & ROW)
    landmark_minipak_scan_ddu = "LGINTBPIU"
    # MaxiPak Scan DDP PUDO shipments
    landmark_maxipak_scan_ddp_pudo = "LGINTPUDO"
    # MaxiPak Scan Premium UPS Express DDP shipments
    landmark_maxipak_scan_premium_ups_express_ddp = "LGINTUPSS"
    # MaxiPak Scan Premium UPS Express DDU shipments
    landmark_maxipak_scan_premium_ups_express_ddu = "LGINTUPSSU"
    # MaxiPak Scan Premium UPS Standard DDP shipments
    landmark_maxipak_scan_premium_ups_standard_ddp = "LGINTUPST"
    # MaxiPak Scan Premium UPS Standard DDU shipments
    landmark_maxipak_scan_premium_ups_standard_ddu = "LGINTUPSTU"

    landmark_maxipak_scan_premium = landmark_maxipak_scan_premium_ups_standard_ddp


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    landmark_shipment_insurance_freight = lib.OptionEnum(
        "ShipmentInsuranceFreight", float
    )
    landmark_order_insurance_freight_total = lib.OptionEnum(
        "OrderInsuranceFreightTotal", float
    )

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
        "50",  # Shipment Data Uploaded
        "60",  # Shipment inventory allocated
        "75",  # Shipment Processed
        "80",  # Shipment Fulfilled
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
        "90",  # Shipment held for payment
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


def load_services_from_csv() -> list:
    """
    Load service definitions from CSV file.
    CSV format: service_code, service_name, zone_label, country_codes, min_weight, max_weight, rate, currency, transit_days
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        # Fallback to simple default if CSV doesn't exist
        return [
            models.ServiceLevel(
                service_name=ShippingServiceName.map(
                    ShippingService.map(service.name).name_or_key
                ).value_or_key,
                service_code=service.name,
                currency="GBP",
                zones=[models.ServiceZone(label="Flat Rate", rate=0.0)],
            )
            for service in ShippingService  # type: ignore
        ]

    # Group zones by service
    services_dict: dict[str, dict] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]

            # Initialize service if not exists
            if service_code not in services_dict:
                services_dict[service_code] = {
                    "service_name": ShippingServiceName.map(
                        ShippingService.map(service_code).name_or_key
                    ).value_or_key,
                    "service_code": ShippingService.map(service_code).name_or_key,
                    "currency": row.get("currency", "GBP"),
                    "zones": [],
                }

            # Parse country codes
            country_codes = [
                c.strip() for c in row.get("country_codes", "").split(",") if c.strip()
            ]

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=(
                    int(row["transit_days"]) if row.get("transit_days") else None
                ),
                country_codes=country_codes,
            )

            services_dict[service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects and mark as international-only
    return [
        models.ServiceLevel(
            **service_data,
            international=True,  # All Landmark services are international-only
            domicile=False,
            weight_unit="KG",  # Weight unit for zone matching
        )
        for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
