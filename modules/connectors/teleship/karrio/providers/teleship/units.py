import csv
import pathlib

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


# System config schema for runtime settings (e.g., OAuth credentials)
# Format: Dict[str, Tuple[default_value, description, type]]
# Note: The actual env values are read by the server (constance.py) using decouple
SYSTEM_CONFIG = {
    "TELESHIP_OAUTH_CLIENT_ID": (
        "",
        "The Teleship OAuth client ID",
        str,
    ),
    "TELESHIP_OAUTH_CLIENT_SECRET": (
        "",
        "The Teleship OAuth client secret",
        str,
    ),
    "TELESHIP_SANDBOX_OAUTH_CLIENT_ID": (
        "",
        "The Teleship sandbox OAuth client ID",
        str,
    ),
    "TELESHIP_SANDBOX_OAUTH_CLIENT_SECRET": (
        "",
        "The Teleship sandbox OAuth client secret",
        str,
    ),
}


class LabelType(lib.StrEnum):
    """Carrier specific label type"""

    PDF = "PDF"
    ZPL = "ZPL"
    PNG = "PNG"


class ConnectionConfig(lib.Enum):
    """Teleship connection configuration."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_format = lib.OptionEnum(
        "label_format",
        lib.units.create_enum("LabelType", [_.name for _ in list(LabelType)]),
        "PDF",
    )


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    envelope = "envelope"
    tube = "tube"
    parcel = "parcel"

    """ Unified Packaging type mapping """
    pak = envelope
    small_box = parcel
    medium_box = parcel
    your_packaging = parcel


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    teleship_expedited_pickup = "TELESHIP-EXPEDITED-PICKUP"
    teleship_expedited_dropoff = "TELESHIP-EXPEDITED-DROPOFF"
    teleship_standard_dropoff = "TELESHIP-STANDARD-DROPOFF"
    teleship_standard_pickup = "TELESHIP-STANDARD-PICKUP"
    teleship_postal_dropoff = "TELESHIP-POSTAL-DROPOFF"
    teleship_postal_pickup = "TELESHIP-POSTAL-PICKUP"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    teleship_signature_required = lib.OptionEnum("signatureRequired", bool, meta=dict(category="SIGNATURE"))
    teleship_delivery_warranty = lib.OptionEnum("deliveryWarranty", bool, meta=dict(category="INSURANCE"))
    teleship_delivery_PUDO = lib.OptionEnum("deliveryPUDO", bool, meta=dict(category="PUDO"))
    teleship_low_carbon = lib.OptionEnum("lowCarbon", bool)
    teleship_duty_tax_calculation = lib.OptionEnum("dutyTaxCalculation", bool)
    teleship_customer_reference = lib.OptionEnum("customerReference")
    teleship_order_tracking_reference = lib.OptionEnum("orderTrackingReference")
    teleship_commercial_invoice_reference = lib.OptionEnum("commercialInvoiceReference", meta=dict(category="INVOICE"))


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


class CustomsContentType(lib.StrEnum):
    """Teleship customs content types"""

    # Teleship-specific values (PascalCase)
    documents = "Documents"
    gift = "Gift"
    sample = "Sample"
    other = "Other"
    commercial_goods = "CommercialGoods"
    return_of_goods = "ReturnOfGoods"

    """ Unified content type mapping """
    merchandise = commercial_goods


class CustomsOption(lib.Enum):
    """Teleship customs identifiers"""

    EORI = lib.OptionEnum("EORI")
    IOSS = lib.OptionEnum("IOSS")
    VAT = lib.OptionEnum("VAT")
    EIN = lib.OptionEnum("EIN")
    VOECNUMBER = lib.OptionEnum("VOECNUMBER")

    """ Unified Customs Identifier type mapping """

    ioss = IOSS
    eori_number = EORI
    vat = VAT
    ein = EIN
    voec_number = VOECNUMBER
    vat_registration_number = VAT


class TrackingStatus(lib.Enum):
    """Teleship tracking statuses"""

    delivered = ["delivered"]
    in_transit = [
        "in_transit",
        "collected",
        "in_hub",
        "out_for_delivery",
        "customs_cleared",
    ]
    out_for_delivery = ["out_for_delivery"]
    delivery_failed = ["delivery_failed", "returned", "cancelled"]
    pending = ["pending", "created", "label_created"]


def load_services_from_csv() -> list:
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"
    if not csv_path.exists():
        return []
    services_dict: dict[str, dict] = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            karrio_service_code = ShippingService.map(service_code).name_or_key
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": row["service_name"],
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "USD"),
                    "min_weight": float(row["min_weight"]) if row.get("min_weight") else None,
                    "max_weight": float(row["max_weight"]) if row.get("max_weight") else None,
                    "max_length": float(row["max_length"]) if row.get("max_length") else None,
                    "max_width": float(row["max_width"]) if row.get("max_width") else None,
                    "max_height": float(row["max_height"]) if row.get("max_height") else None,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": (row.get("domicile") or "").lower() == "true",
                    "international": True if (row.get("international") or "").lower() == "true" else None,
                    "zones": [],
                }
            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=int(row["transit_days"].split("-")[0]) if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit() else None,
                country_codes=country_codes if country_codes else None,
            )
            services_dict[karrio_service_code]["zones"].append(zone)
    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
