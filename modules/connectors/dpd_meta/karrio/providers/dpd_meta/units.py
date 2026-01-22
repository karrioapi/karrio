import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class BusinessUnit(lib.StrEnum):
    """DPD business unit codes."""

    DE = "001"
    FR = "002"
    NL = "010"
    GB = "011"
    AT = "014"
    CZ = "015"
    SK = "016"
    HU = "017"
    BG = "018"
    ES = "020"
    PL = "021"
    IT = "023"
    SI = "026"
    HR = "028"
    PT = "030"
    EE = "031"
    LT = "032"
    LV = "033"
    BE = "034"
    CH = "036"
    RO = "041"
    IE = "046"


class LabelFormat(lib.StrEnum):
    """DPD label format options - supports 18 formats from API."""

    PDF = "PDF"
    EPL = "EPL"
    ZPL = "ZPL"
    TIFF = "TIFF"
    PNG = "PNG"
    PPR = "PPR"
    SPD = "SPD"
    Z2D = "Z2D"
    THE = "THE"
    XML = "XML"
    XML2D = "XML2D"
    THEPSG = "THEPSG"
    ZPLPSG = "ZPLPSG"
    ZPL300 = "ZPL300"
    JSON = "JSON"
    PS = "PS"
    DATA = "DATA"
    CLP = "CLP"
    HTML = "HTML"


class LabelPaperFormat(lib.StrEnum):
    """DPD label paper size options."""

    A4 = "A4"
    A5 = "A5"
    A6 = "A6"
    A7 = "A7"


class LabelPrinterPosition(lib.StrEnum):
    """DPD label position on A4 paper."""

    UPPER_LEFT = "UPPER_LEFT"
    UPPER_RIGHT = "UPPER_RIGHT"
    LOWER_LEFT = "LOWER_LEFT"
    LOWER_RIGHT = "LOWER_RIGHT"


class DropOffType(lib.StrEnum):
    """DPD drop-off type options."""

    FULL_LABEL = "FULL_LABEL"
    QR_CODE = "QR_CODE"
    BOTH = "BOTH"


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", LabelPaperFormat, "A4")
    label_format = lib.OptionEnum("label_format", LabelFormat, "PDF")
    label_paper_format = lib.OptionEnum("label_paper_format", LabelPaperFormat)
    label_printer_position = lib.OptionEnum("label_printer_position", LabelPrinterPosition)
    dropoff_type = lib.OptionEnum("dropoff_type", DropOffType)
    simulate = lib.OptionEnum("simulate", bool)
    extra_barcode = lib.OptionEnum("extra_barcode", bool)
    with_document = lib.OptionEnum("with_document", bool)
    bucode = lib.OptionEnum("bucode", BusinessUnit)


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """Unified Packaging type mapping"""
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """DPD META-API product codes"""

    dpd_meta_classic = "101"
    dpd_meta_express_10 = "E10"
    dpd_meta_express_12 = "E12"
    dpd_meta_express_18 = "E18"
    dpd_meta_parcel_shop = "PS"


class CustomsTerms(lib.StrEnum):
    """DPD customs terms (Incoterms)."""

    DAP_NOT_CLEARED = "s01"  # DAP, not cleared
    DDP_DUTIES_EXCL_TAXES = (
        "s02"  # DDP, delivered duty paid (incl. duties, excl. taxes)
    )
    DDP_DUTIES_INCL_TAXES = "s03"  # DDP, delivered duty paid (incl. duties and taxes)
    EXW = "s05"  # Ex Works
    DAP = "s06"  # DAP
    DAP_DDP_ENHANCED = "s07"  # DAP & DDP enhanced, duty/taxes pre-paid by receiver


class CustomsPaper(lib.StrEnum):
    """DPD customs accompanying documents."""

    COMMERCIAL_INVOICE = "A"
    PRO_FORMA_INVOICE = "B"
    EXPORT_DECLARATION = "C"
    EUR1 = "D"
    EUR2 = "E"
    ATR = "F"
    DELIVERY_NOTE = "G"
    THIRD_PARTY_BILLING = "H"
    T1_DOCUMENT = "I"


class ClearanceStatus(lib.StrEnum):
    """DPD customs clearance status."""

    NO = "N"
    FREE = "F"
    EXPORT_CLEARED = "E"
    TRANSIT_CLEARED = "T"
    IMPORT_CLEARED = "I"
    HYBRID = "H"


class CustomsValueLevel(lib.StrEnum):
    """DPD customs value classification."""

    HIGH = "H"  # High value
    MEDIUM = "M"  # Mid (above 22€ and below 150€)
    LOW = "L"  # Low value


class ExportReason(lib.StrEnum):
    """DPD export reason codes."""

    SALE = "s01"
    RETURN_REPLACEMENT = "s02"
    GIFT = "s03"


class ParcelType(lib.StrEnum):
    """DPD international parcel type."""

    DOCUMENT = "D"
    NON_DOC = "P"


class CodCollectType(lib.StrEnum):
    """DPD COD collection type."""

    CASH = "s0"
    CROSSED_CHEQUE = "s1"
    CREDIT_CARD = "s2"
    DEFAULT = "s9"  # Default, depending on receiving BU


class BusinessType(lib.StrEnum):
    """DPD business type for legal entity."""

    PRIVATE = "P"
    BUSINESS = "B"


class Incoterm(lib.StrEnum):
    """Standard Incoterms mapping to DPD customs terms."""

    DAP = CustomsTerms.DAP
    DDP = CustomsTerms.DDP_DUTIES_INCL_TAXES
    DDU = CustomsTerms.DAP_NOT_CLEARED
    EXW = CustomsTerms.EXW

    # Standard mappings
    CFR = CustomsTerms.DAP
    CIF = CustomsTerms.DAP
    CIP = CustomsTerms.DAP
    CPT = CustomsTerms.DAP
    FCA = CustomsTerms.EXW
    FOB = CustomsTerms.EXW
    FAS = CustomsTerms.EXW


class CustomsContentType(lib.StrEnum):
    """Karrio unified customs content type to DPD export reason mapping."""

    sale = ExportReason.SALE
    merchandise = ExportReason.SALE
    gift = ExportReason.GIFT
    sample = ExportReason.SALE
    return_merchandise = ExportReason.RETURN_REPLACEMENT
    repair = ExportReason.RETURN_REPLACEMENT
    documents = ExportReason.SALE
    other = ExportReason.SALE


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    dpd_meta_saturday_delivery = lib.OptionEnum("saturday_delivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dpd_meta_label_format = lib.OptionEnum("label_format", str)
    dpd_meta_label_paper_format = lib.OptionEnum("label_paper_format", str)
    dpd_meta_label_printer_position = lib.OptionEnum("label_printer_position", str)
    dpd_meta_dropoff_type = lib.OptionEnum("dropoff_type", str, meta=dict(category="PUDO"))
    dpd_meta_simulate = lib.OptionEnum("simulate", bool)
    dpd_meta_extra_barcode = lib.OptionEnum("extra_barcode", bool)
    dpd_meta_with_document = lib.OptionEnum("with_document", bool)
    dpd_meta_notification_email = lib.OptionEnum("notification_email", str, meta=dict(category="NOTIFICATION"))
    dpd_meta_notification_sms = lib.OptionEnum("notification_sms", str, meta=dict(category="NOTIFICATION"))
    dpd_meta_delivery_date_from = lib.OptionEnum("delivery_date_from", str, meta=dict(category="DELIVERY_OPTIONS"))
    dpd_meta_delivery_date_to = lib.OptionEnum("delivery_date_to", str, meta=dict(category="DELIVERY_OPTIONS"))
    dpd_meta_delivery_time_from = lib.OptionEnum("delivery_time_from", str, meta=dict(category="DELIVERY_OPTIONS"))
    dpd_meta_delivery_time_to = lib.OptionEnum("delivery_time_to", str, meta=dict(category="DELIVERY_OPTIONS"))

    """COD options"""
    dpd_meta_cod_collect_type = lib.OptionEnum("cod_collect_type", str, meta=dict(category="COD"))
    dpd_meta_cod_bank_code = lib.OptionEnum("cod_bank_code", str, meta=dict(category="COD"))
    dpd_meta_cod_bank_name = lib.OptionEnum("cod_bank_name", str, meta=dict(category="COD"))
    dpd_meta_cod_bank_account_number = lib.OptionEnum("cod_bank_account_number", str, meta=dict(category="COD"))
    dpd_meta_cod_bank_account_name = lib.OptionEnum("cod_bank_account_name", str, meta=dict(category="COD"))
    dpd_meta_cod_iban = lib.OptionEnum("cod_iban", str, meta=dict(category="COD"))
    dpd_meta_cod_bic = lib.OptionEnum("cod_bic", str, meta=dict(category="COD"))
    dpd_meta_cod_purpose = lib.OptionEnum("cod_purpose", str, meta=dict(category="COD"))

    """Unified Option type mapping"""
    saturday_delivery = dpd_meta_saturday_delivery
    label_format = dpd_meta_label_format
    label_paper_format = dpd_meta_label_paper_format
    label_printer_position = dpd_meta_label_printer_position
    dropoff_type = dpd_meta_dropoff_type
    simulate = dpd_meta_simulate
    extra_barcode = dpd_meta_extra_barcode
    with_document = dpd_meta_with_document
    cash_on_delivery = lib.OptionEnum("cash_on_delivery", float, meta=dict(category="COD"))
    insurance = lib.OptionEnum("insurance", float, meta=dict(category="INSURANCE"))
    declared_value = lib.OptionEnum("declared_value", float)
    currency = lib.OptionEnum("currency", str)


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


class ShippingDocumentCategory(lib.StrEnum):
    """Carrier specific document category types.

    Maps DPD META document types to standard ShippingDocumentCategory.
    Values match the exact syntax used by DPD META API.
    """

    shipping_label = "shippingLabel"
    qr_code = "qrcode"


def load_services_from_csv() -> list:
    """
    Load service definitions from CSV file.
    CSV format: service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,currency,transit_days,domicile,international
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        # Fallback to simple default if CSV doesn't exist
        return [
            models.ServiceLevel(
                service_name="DPD Classic",
                service_code="dpd_meta_classic",
                currency="EUR",
                domicile=True,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    # Group zones by service
    services_dict: dict[str, dict] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]

            # Map carrier service code to karrio service code
            karrio_service_code = ShippingService.map(service_code).name_or_key

            # Initialize service if not exists
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": (
                        float(row["min_weight"]) if row.get("min_weight") else None
                    ),
                    "max_weight": (
                        float(row["max_weight"]) if row.get("max_weight") else None
                    ),
                    "max_length": (
                        float(row["max_length"]) if row.get("max_length") else None
                    ),
                    "max_width": (
                        float(row["max_width"]) if row.get("max_width") else None
                    ),
                    "max_height": (
                        float(row["max_height"]) if row.get("max_height") else None
                    ),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": row.get("domicile", "").lower() == "true",
                    "international": (
                        True if row.get("international", "").lower() == "true" else None
                    ),
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
                transit_days=(
                    int(row["transit_days"]) if row.get("transit_days") else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
