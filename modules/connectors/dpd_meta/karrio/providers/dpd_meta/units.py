import csv
import pathlib

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib


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
    """Carrier connection configuration options.

    configurable=False  → hidden from the carrier-connection UI (server-managed or
                          method-level; set via API or admin only).
    configurable=True   → visible and editable in the carrier-connection dialog.
    category            → groups fields into labelled sections in the UI.
    """

    shipping_options = lib.OptionEnum("shipping_options", list, meta=dict(category="GENERAL", configurable=False))
    shipping_services = lib.OptionEnum("shipping_services", list, meta=dict(category="GENERAL", configurable=False))
    # configurable=False: label fields are configured per shipping-method, not per connection
    label_type = lib.OptionEnum(
        "label_type",
        LabelPaperFormat,
        "A4",
        meta=dict(category="LABEL", configurable=False),
    )
    label_format = lib.OptionEnum(
        "label_format",
        LabelFormat,
        "PDF",
        meta=dict(category="LABEL", configurable=False),
    )
    label_paper_format = lib.OptionEnum(
        "label_paper_format",
        LabelPaperFormat,
        meta=dict(category="LABEL", configurable=False),
    )
    label_printer_position = lib.OptionEnum(
        "label_printer_position",
        LabelPrinterPosition,
        meta=dict(category="LABEL", configurable=False),
    )
    # configurable=False: dropoff_type is a method-level option, not a connection-level one
    dropoff_type = lib.OptionEnum("dropoff_type", DropOffType, meta=dict(category="PICKUP", configurable=False))
    sending_depot = lib.OptionEnum(
        "sending_depot",
        help="Pickup Sending Depot — depot identifier used as the pickup origin for this connection.",
        meta=dict(category="PICKUP", configurable=True),
    )
    # configurable=False: simulate is a developer/debug flag, not user-configurable
    simulate = lib.OptionEnum("simulate", bool, meta=dict(category="GENERAL", configurable=False))
    # configurable=False: extra_barcode and with_document are method-level, not connection-level
    extra_barcode = lib.OptionEnum("extra_barcode", bool, meta=dict(category="GENERAL", configurable=False))
    with_document = lib.OptionEnum("with_document", bool, meta=dict(category="GENERAL", configurable=False))
    cod_bank_code = lib.OptionEnum("cod_bank_code", meta=dict(category="COD", configurable=True))
    cod_bank_name = lib.OptionEnum("cod_bank_name", meta=dict(category="COD", configurable=True))
    cod_bank_account_number = lib.OptionEnum("cod_bank_account_number", meta=dict(category="COD", configurable=True))
    cod_bank_account_name = lib.OptionEnum("cod_bank_account_name", meta=dict(category="COD", configurable=True))
    cod_iban = lib.OptionEnum("cod_iban", meta=dict(category="COD", configurable=True))
    cod_bic = lib.OptionEnum("cod_bic", meta=dict(category="COD", configurable=True))


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
    # DPD Meta Group Product Codes (SoCodes). Source of truth: DPD Product &
    # Service List, April 2026 issue. Naming below uses the PDF's official
    # EDI prefix (CL/E12/E18/E830/IE2/MAIL/PL/B2C) where applicable.
    # Previous DE-SOAP short codes (AM2/PM2/AM0/...) are legacy and not
    # supported by the Meta API.
    dpd_meta_classic = "101"  # CL — DPD Classic
    dpd_meta_small = "136"  # CL — DPD Classic small parcel (Kleinpaket)
    dpd_meta_b2c_classic = "327"  # B2C — B2C DPD Classic (CL + predict)
    dpd_meta_b2c_small = "328"  # B2C — B2C DPD Classic small parcel
    dpd_meta_express_830 = "350"  # E830 — DPD 8:30
    dpd_meta_express_12 = "225"  # E12 — DPD 12:00
    dpd_meta_express_18 = "155"  # E18 — DPD GUARANTEE
    dpd_meta_international_express = "302"  # IE2 — DPD EXPRESS International
    dpd_meta_parcel_letter = "154"  # PL — DPD PARCELLetter
    dpd_meta_mail = "294"  # MAIL — DPD Mail
    # --- Non-Bronze services — hidden from Bronze certification demo (SHIP2-1194) ---
    # These services require special DPD agreements or are out of scope for Bronze.
    # Kept in source for reference; confirm final cut/keep list with Dan before GA.
    # dpd_meta_classic_exchange_inbound = "118"  # CL — DPD Classic exchange (inbound)
    # dpd_meta_classic_tyres = "365"  # MPS — DPD Tyre (CL + tyres)
    # dpd_meta_classic_tyres_b2c = "366"  # B2C — B2C DPD Tyre (CL + tyres + predict)
    # dpd_meta_food = "383"  # B2C — DPD Food Mo-Sa (CL + food + predict, special agreement)
    # dpd_meta_food_1200 = "379"  # EXP — DPD Food 12:00 (E12 + food + predict, special agreement)
    # dpd_meta_food_1800 = "378"  # EXP — DPD Food Express (E18 + food + predict, special agreement)
    # Parcel-to-Shop delivery (Paketshop Direktzustellung) — SoCode 337
    # (B2C: CL + parcelShopDelivery). Booking requires a `parcel_shop_id`
    # option; the recipient is the shop's address. SoCode 337 is also
    # reachable via 327 + parcel_shop_id at the request layer
    # (PUDO_PRODUCT_CODE_MAP) — both pathways resolve identically.
    dpd_meta_parcelshop = "337"  # B2C — Parcelshop direct delivery
    dpd_meta_shop_return = "332"  # B2C — DPD Return (labelless is a per-shipment option)
    dpd_meta_shop2shop_domestic = "345"  # B2C — Shop2Shop (AsCode A15, special agreement)
    dpd_meta_shop2home = "404"  # B2C — Shop2Home (AsCode A15, special agreement)

    # Variant differentiation lives in rate-sheet feature columns, not in
    # alias names. Mappings:
    #   • size XS/S → small_parcel option (327→328 via SMALL_PARCEL_PRODUCT_CODE_MAP)
    #   • saturday → saturday_delivery=True (101→103 via SATURDAY_PRODUCT_CODE_MAP)
    #   • shop drop-off → first_mile=dropoff (same SoCode 327, commercial label)
    #   • EU vs intl → zone_label distinguishes (single SoCode 302)
    #   • B2B vs B2C tyres → dpd_meta_classic_tyres (365) vs _tyres_b2c (366)
    #   • Limited Quantity hazmat → hazardous_limited_quantities option
    #     (LIMITED_QUANTITY_PRODUCT_CODE_MAP routes to 447/704/793/794/797/799)
    #
    # Codes 103, 109, 329, 330, 358 referenced in resolver maps are NOT in
    # the April 2026 PDF. They survive on legacy/special-agreement accounts
    # (Saturday Classic 103: NL/BE/PL/CZ/FR; Saturday B2C 358: NL/BE/BG;
    # COD codes 109/329/330: pre-DPD-DE-COD-deprecation). COUNTRY_ALLOWLIST
    # guards these against ROUTING_15 rejections in unsupported destinations.


class CustomsTerms(lib.StrEnum):
    """DPD customs terms (Incoterms)."""

    DAP_NOT_CLEARED = "s01"  # DAP, not cleared
    DDP_DUTIES_EXCL_TAXES = "s02"  # DDP, delivered duty paid (incl. duties, excl. taxes)
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

    # --- Delivery Options (Zustelloptionen) ---
    dpd_meta_saturday_delivery = lib.OptionEnum(
        "saturday_delivery",
        bool,
        help="Enable Saturday delivery service",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True),
    )
    # configurable=False: these routing options are hidden from the shipping-method editor
    # (non-Bronze / internal use) but remain functional so existing API integrations
    # and the resolver maps (SMALL_PARCEL_, EX_WORKS_, EXCHANGE_, FOOD_PRODUCT_CODE_MAP)
    # continue to route correctly.
    dpd_meta_small_parcel = lib.OptionEnum(
        "small_parcel",
        bool,
        help="Mark shipment as small package (Kleinpaket) — routes to 136 (B2B) or 328 (B2C)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=False, service_level=False),
    )
    dpd_meta_exchange_service = lib.OptionEnum(
        "exchange_service",
        bool,
        help="Enable exchange service — routes to 113 (outbound swap)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=False, service_level=False),
    )
    dpd_meta_ex_works = lib.OptionEnum(
        "ex_works",
        bool,
        help="Enable EX Works delivery mode — routes to 105/158/231/351",
        meta=dict(category="DELIVERY_OPTIONS", configurable=False, service_level=False),
    )
    dpd_meta_food = lib.OptionEnum(
        "food",
        bool,
        help="DPD Food service — routes to 383/378/379 (requires special agreement)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=False, service_level=False),
    )
    dpd_meta_id_check = lib.OptionEnum(
        "id_check",
        bool,
        help="Require recipient identity verification (DPD `PersonalDeliveryType=s2`). "
        "Recipient legal name must already be present in the address. "
        "ID number / date of birth / authorized name (DPD types s5/s6) are out of scope of this option.",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True),
    )
    dpd_meta_resolve_shipper_depot = lib.OptionEnum(
        "resolve_shipper_depot",
        bool,
        help="Resolve the shipper's DPD depot from the sender / pickup postal code "
        "(via the German DepotDataService) and inject it as sendingDepot. Enabled "
        "by default — required for reseller accounts that have no own DPD contract.",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False),
    )
    dpd_meta_delivery_date_from = lib.OptionEnum(
        "delivery_date_from",
        str,
        help="Earliest delivery date (YYYY-MM-DD)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False),
    )
    dpd_meta_delivery_date_to = lib.OptionEnum(
        "delivery_date_to",
        str,
        help="Latest delivery date (YYYY-MM-DD)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False),
    )
    dpd_meta_delivery_time_from = lib.OptionEnum(
        "delivery_time_from",
        str,
        help="Earliest delivery time (HH:MM)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False),
    )
    dpd_meta_delivery_time_to = lib.OptionEnum(
        "delivery_time_to",
        str,
        help="Latest delivery time (HH:MM)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False),
    )

    # --- PUDO (Parcel Shop) Options ---
    dpd_meta_dropoff_type = lib.OptionEnum(
        "dropoff_type",
        str,
        help="Drop-off type for parcel shop delivery (FULL_LABEL, QR_CODE, BOTH)",
        meta=dict(category="PUDO", configurable=False, service_level=False),
    )
    dpd_meta_parcel_shop_id = lib.OptionEnum(
        "parcel_shop_id",
        str,
        help="DPD ParcelShop ID for shop delivery",
        meta=dict(category="PUDO", configurable=True, service_level=False),
    )

    # --- Notification Options (Predict) ---
    dpd_meta_notification_email = lib.OptionEnum(
        "notification_email",
        str,
        help="Email for delivery notifications (Predict service)",
        meta=dict(category="NOTIFICATION", configurable=True, service_level=False),
    )
    dpd_meta_notification_sms = lib.OptionEnum(
        "notification_sms",
        str,
        help="SMS number for delivery notifications",
        meta=dict(category="NOTIFICATION", configurable=True, service_level=False),
    )

    # --- Insurance Options (Zusatzversicherung) ---
    dpd_meta_insurance_description = lib.OptionEnum(
        "insurance_description",
        str,
        help="Free text description for additional insurance purpose",
        meta=dict(category="INSURANCE", configurable=False, service_level=False, toggle=True),
    )

    # --- COD Options (Nachnahme) ---
    dpd_meta_cod_collect_type = lib.OptionEnum(
        "cod_collect_type",
        str,
        help="COD collection type (cash, cheque, etc.)",
        meta=dict(category="COD", configurable=True, service_level=False, toggle=True),
    )
    dpd_meta_cod_bank_code = lib.OptionEnum(
        "cod_bank_code",
        str,
        help="Bank code for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )
    dpd_meta_cod_bank_name = lib.OptionEnum(
        "cod_bank_name",
        str,
        help="Bank name for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )
    dpd_meta_cod_bank_account_number = lib.OptionEnum(
        "cod_bank_account_number",
        str,
        help="Bank account number for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )
    dpd_meta_cod_bank_account_name = lib.OptionEnum(
        "cod_bank_account_name",
        str,
        help="Account holder name for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )
    dpd_meta_cod_iban = lib.OptionEnum(
        "cod_iban",
        str,
        help="IBAN for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )
    dpd_meta_cod_bic = lib.OptionEnum(
        "cod_bic",
        str,
        help="BIC/SWIFT code for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )
    dpd_meta_cod_purpose = lib.OptionEnum(
        "cod_purpose",
        str,
        help="Purpose text for COD payment. Configure once on the carrier connection — overridable per-shipment.",
        meta=dict(category="COD", configurable=False, service_level=False),
    )

    # --- Dangerous Goods Options (Gefahrgut Versand) ---
    # configurable=False: Dangerous goods are out of scope for Bronze certification (SHIP2-1194).
    # These options remain functional at the API level for existing integrations but are
    # hidden from the shipping-method editor and carrier-connection UI.
    dpd_meta_dangerous_goods = lib.OptionEnum(
        "dangerous_goods",
        bool,
        help="Enable shipment of dangerous goods (Gefahrgut)",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=True),
    )
    dpd_meta_dg_identification_class = lib.OptionEnum(
        "dg_identification_class",
        str,
        help="Hazard identification number (Identifikationsklasse)",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_un_number = lib.OptionEnum(
        "dg_un_number",
        str,
        help="UN number for the hazardous material",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_weight = lib.OptionEnum(
        "dg_weight",
        float,
        help="Weight of dangerous goods package in kg",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_description = lib.OptionEnum(
        "dg_description",
        str,
        help="Detailed description of the dangerous goods",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_hazard_factor = lib.OptionEnum(
        "dg_hazard_factor",
        int,
        help="Factor defining the risk level of the hazardous goods (META-API requires integer)",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_hazard_class = lib.OptionEnum(
        "dg_hazard_class",
        str,
        help="Official hazard classification (e.g. 3 for flammable liquids)",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_nag_entry = lib.OptionEnum(
        "dg_nag_entry",
        str,
        help="Not otherwise specified (N.A.G.) entry for hazardous goods",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_packing_group = lib.OptionEnum(
        "dg_packing_group",
        str,
        help="Packing group (I, II, III) indicating packaging strength",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_packing_code = lib.OptionEnum(
        "dg_packing_code",
        str,
        help="DPD-specific packaging code for dangerous goods",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_subsidiary_risks = lib.OptionEnum(
        "dg_subsidiary_risks",
        str,
        help="Additional hazard classifications (subsidiary risks)",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )
    dpd_meta_dg_tunnel_restriction_code = lib.OptionEnum(
        "dg_tunnel_restriction_code",
        str,
        help="Code defining tunnel access restrictions for hazardous goods",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=False),
    )

    # --- Limited Quantity (ADR-LQ exemption for limited-quantity hazmat) ---
    # Routes to dedicated LQ SoCodes (447/704/793/794/797/799 per the
    # April 2026 Product & Service List) via LIMITED_QUANTITY_PRODUCT_CODE_MAP.
    # Mutually exclusive with full hazardous shipping; full hazardous wins
    # if both flags are set on the same parcel.
    # configurable=False: also hidden for Bronze (same as dangerous_goods above).
    dpd_meta_hazardous_limited_quantities = lib.OptionEnum(
        "hazardous_limited_quantities",
        bool,
        help="Ship as ADR Limited Quantity (LQ) — reduced hazardous documentation regime",
        meta=dict(category="DANGEROUS_GOOD", configurable=False, service_level=True),
    )

    # --- Label Options (internal — not configurable in shipping method editor) ---
    dpd_meta_label_format = lib.OptionEnum("label_format", str, meta=dict(configurable=False, service_level=False))
    dpd_meta_label_paper_format = lib.OptionEnum(
        "label_paper_format", str, meta=dict(configurable=False, service_level=False)
    )
    dpd_meta_label_printer_position = lib.OptionEnum(
        "label_printer_position",
        str,
        meta=dict(configurable=False, service_level=False),
    )

    # --- Internal/Debug Options (not configurable) ---
    dpd_meta_simulate = lib.OptionEnum("simulate", bool, meta=dict(configurable=False, service_level=False))
    dpd_meta_extra_barcode = lib.OptionEnum("extra_barcode", bool, meta=dict(configurable=False, service_level=False))
    dpd_meta_with_document = lib.OptionEnum("with_document", bool, meta=dict(configurable=False, service_level=False))

    """Unified Option type mapping"""
    saturday_delivery = dpd_meta_saturday_delivery
    dangerous_good = dpd_meta_dangerous_goods
    cash_on_delivery = lib.OptionEnum(
        "cash_on_delivery",
        float,
        help="Cash on delivery amount",
        meta=dict(category="COD", configurable=True, service_level=False),
    )
    insurance = lib.OptionEnum(
        "insurance",
        float,
        help="Additional insurance value",
        meta=dict(category="INSURANCE", configurable=True, service_level=False),
    )
    # configurable=False: declared value is out of scope for Bronze (SHIP2-1194)
    declared_value = lib.OptionEnum(
        "declared_value",
        str,
        help="Declared value for customs",
        meta=dict(category="INVOICE", configurable=False, service_level=False),
    )
    currency = lib.OptionEnum(
        "currency",
        str,
        help="Currency code for values",
        meta=dict(configurable=False, service_level=False),
    )


COD_PRODUCT_CODE_MAP: dict = {
    "101": "109",  # D,COD
    "327": "329",  # D,2C,COD
    "328": "330",  # D,2C,COD,XD
}

SATURDAY_PRODUCT_CODE_MAP: dict = {
    "101": "103",  # D,6 (NL/BE/PL/CZ/FR only per PDF p.31)
    "327": "358",  # D,6,2C (NL/BE/BG only per PDF p.31)
    "225": "228",  # AM2,6 — Express 12:00 Saturday
}

SMALL_PARCEL_PRODUCT_CODE_MAP: dict = {
    "101": "136",  # XD
    "327": "328",  # D,2C,XD
}

EX_WORKS_PRODUCT_CODE_MAP: dict = {
    "101": "105",  # D,EXW (DE/BE only per PDF p.31)
    "155": "158",  # PM2,EXW — Express 18:00 EX Works
    "225": "231",  # AM2,EXW — Express 12:00 EX Works
    "350": "351",  # AM0,EXW — Express 08:30 EX Works
}

PUDO_PRODUCT_CODE_MAP: dict = {
    "327": "337",  # D,2C,PSD
    "328": "338",  # D,2C,PSD,XD
}

ADDITIONAL_SERVICE_CODES: dict = {
    "345": "A15",
    "404": "A15",
}

# Country allowlist for SoCodes that DPD only accepts in specific destinations.
# Source: master PDF "Group Product Code" table per code.
# When a resolved code is in this map and the recipient country is not in its
# allowed set, the resolver falls back to the un-resolved base service code to
# avoid `ROUTING_15` ("service combination not possible") rejections.
COUNTRY_ALLOWLIST: dict = {
    "103": {"NL", "BE", "PL", "CZ", "FR"},  # D,SAT — Saturday Classic
    "358": {"NL", "BE", "BG"},  # D,2C,SAT — Saturday B2C
}

HAZARDOUS_PRODUCT_CODE_MAP: dict = {
    "101": "102",  # D + HAZ
}

EXCHANGE_PRODUCT_CODE_MAP: dict = {
    "101": "113",  # D + SWAP outbound
}

ID_CHECK_PRODUCT_CODE_MAP: dict = {
    "155": "168",  # E18 + ID-Check
    "225": "249",  # E12 + ID-Check
}

FOOD_PRODUCT_CODE_MAP: dict = {
    "101": "383",  # CL + food
    "155": "378",  # E18 + food
    "225": "379",  # E12 + food
}

# Limited-Quantity (ADR-LQ) variants — added per April 2026 Product & Service
# List. Each base SoCode has a dedicated LQ-prefix code so DPD can apply the
# reduced hazardous documentation regime end-to-end.
LIMITED_QUANTITY_PRODUCT_CODE_MAP: dict = {
    "101": "793",  # D + LQ
    "105": "704",  # D,EXW + LQ (also reachable from 101 via exw+LQ dual)
    "155": "799",  # E18 + LQ
    "225": "797",  # E12 + LQ
    "327": "794",  # D,2C + LQ
    "332": "447",  # D,2C,RET + LQ
}

# PDF-documented triples (p.31 + April 2026 LQ pairs):
# 330 = 2C,COD,XD; 338 = 2C,PSD,XD; 704 = D,EXW,LQ.
DUAL_OPTION_MAP: dict = {
    ("327", "cod", "small"): "330",
    ("327", "pudo", "small"): "338",
    ("101", "exw", "hazardous"): "106",
    ("101", "exw", "small"): "138",
    ("101", "exchange", "small"): "142",
    ("225", "exw", "saturday"): "234",
    ("155", "exw", "id_check"): "171",
    ("225", "exw", "id_check"): "255",
    ("101", "exw", "limited_quantity"): "704",
}


# B2C product family per Meta API spec (PDF pages 31-32 + April 2026 LQ):
# all "D,2C,..." codes — DPD BU-API requires predict.value for every 2C code.
B2C_PRODUCT_CODES = frozenset(
    {
        "327",
        "328",
        "329",
        "330",
        "332",
        "337",
        "338",
        "345",
        "358",
        "366",
        "378",
        "379",
        "383",
        "404",
        "447",
        "794",
    }
)

# Placeholder stamped as `sendingDepot` at mapping time; the proxy substitutes
# it with the shipper's resolved depot once it holds a public-WS session.
DEPOT_PLACEHOLDER = "[DEPOT]"

# EU member states (ISO-2, post-Brexit). Cross-border shipments where BOTH
# shipper and recipient are in this set don't require customs data per DPD.
EU_MEMBER_STATES = frozenset(
    {
        "AT",
        "BE",
        "BG",
        "HR",
        "CY",
        "CZ",
        "DK",
        "EE",
        "FI",
        "FR",
        "DE",
        "GR",
        "HU",
        "IE",
        "IT",
        "LV",
        "LT",
        "LU",
        "MT",
        "NL",
        "PL",
        "PT",
        "RO",
        "SK",
        "SI",
        "ES",
        "SE",
    }
)


def resolve_product_code(service: str, options, recipient_country: str | None = None) -> str:
    """Resolve the final DPD Group Code from service + options.

    Per DPD Meta API Item 4b: productCode MUST be a single pre-bundled SoCode;
    product + parameter combos are not supported. See PDF pages 31-32.

    Resolution is two-tier:
      1. DUAL_OPTION_MAP — option triples (e.g. (327, cod, small) -> 330) match first.
      2. Single-option precedence — food > hazardous > limited_quantity > exchange
         > id_check > cod > pudo > saturday > small > exw.

    Country guard (Phase 5): if the resolved code is in `COUNTRY_ALLOWLIST` and
    `recipient_country` is provided but not in the allowed set, fall back to the
    un-resolved base `service` to avoid DPD `ROUTING_15` rejections. When
    `recipient_country` is None (back-compat), no guard is applied.
    """
    code = _resolve_product_code_unguarded(service, options)
    allowed = COUNTRY_ALLOWLIST.get(code)
    if allowed is not None and recipient_country and recipient_country not in allowed:
        return service
    return code


def _resolve_product_code_unguarded(service: str, options) -> str:
    """Inner resolver — applies dual-triple + single-option precedence with no
    country guard. Public callers should use `resolve_product_code`."""
    cod = bool(options.cash_on_delivery.state)
    pudo = bool(options.dpd_meta_parcel_shop_id.state)
    saturday = bool(options.dpd_meta_saturday_delivery.state)
    small = bool(options.dpd_meta_small_parcel.state)
    exw = bool(options.dpd_meta_ex_works.state)
    exchange = bool(options.dpd_meta_exchange_service.state)
    food = bool(options.dpd_meta_food.state)
    hazardous = bool(options.dpd_meta_dangerous_goods.state)
    id_check = bool(options.dpd_meta_id_check.state)
    limited_quantity = bool(options.dpd_meta_hazardous_limited_quantities.state)

    # 1. Dual-option triples documented in master PDF.
    # Skipped when `food` is set — food has highest single-option precedence
    # and there is no documented (food, *) triple.
    if not food:
        if cod and small and (service, "cod", "small") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "cod", "small")]
        if pudo and small and (service, "pudo", "small") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "pudo", "small")]
        if exw and small and (service, "exw", "small") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "exw", "small")]
        if exchange and small and (service, "exchange", "small") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "exchange", "small")]
        if exw and saturday and (service, "exw", "saturday") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "exw", "saturday")]
        if exw and hazardous and (service, "exw", "hazardous") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "exw", "hazardous")]
        if exw and id_check and (service, "exw", "id_check") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "exw", "id_check")]
        if exw and limited_quantity and (service, "exw", "limited_quantity") in DUAL_OPTION_MAP:
            return DUAL_OPTION_MAP[(service, "exw", "limited_quantity")]

    # 2. Single-option precedence. limited_quantity sits between hazardous
    # and exchange — they are mutually exclusive in practice (full hazmat vs
    # the LQ exemption), so hazardous wins if both are erroneously set.
    if food:
        return FOOD_PRODUCT_CODE_MAP.get(service, service)
    if hazardous:
        return HAZARDOUS_PRODUCT_CODE_MAP.get(service, service)
    if limited_quantity:
        return LIMITED_QUANTITY_PRODUCT_CODE_MAP.get(service, service)
    if exchange:
        return EXCHANGE_PRODUCT_CODE_MAP.get(service, service)
    if id_check:
        return ID_CHECK_PRODUCT_CODE_MAP.get(service, service)
    if cod:
        return COD_PRODUCT_CODE_MAP.get(service, service)
    if pudo:
        return PUDO_PRODUCT_CODE_MAP.get(service, service)
    if saturday:
        return SATURDAY_PRODUCT_CODE_MAP.get(service, service)
    if small:
        return SMALL_PARCEL_PRODUCT_CODE_MAP.get(service, service)
    if exw:
        return EX_WORKS_PRODUCT_CODE_MAP.get(service, service)
    return service


def resolve_pudo_id(options, product_code: str) -> str | None:
    """Return pudoId only when the resolved productCode is a Parcel-to-Shop SoCode."""
    if product_code in {"337", "338", "345"}:
        return options.dpd_meta_parcel_shop_id.state or None
    return None


def should_resolve_shipper_depot(options, origin_country: str) -> bool:
    """Whether the shipper's depot must be resolved for this request.

    DPD reseller customers (no own contract) have no known `sendingDepot` — it
    must be derived per request from the sender / pickup postal code via the
    German DepotDataService. Controlled by the `resolve_shipper_depot` option
    (on by default) and limited to German origins, which the service covers.
    """
    return bool(options.dpd_meta_resolve_shipper_depot.state) and (origin_country or "").upper() == "DE"


def inject_sending_depot(payload: list, locations: list, *, settings, geo_routing: bool) -> list:
    """Substitute the `[DEPOT]` sendingDepot placeholder with the resolved depot.

    `locations` is the `parse_location_response` output; the first match's
    4-digit depot code is used. Shipments take the 7-digit GeoRouting code
    (business-unit code + depot); pickups take the bare 4-digit depot. When
    nothing resolves the placeholder is dropped so a bogus value is never sent.
    """
    depot = locations[0].location_id if locations else None
    if depot and geo_routing and settings.dpd_bucode:
        depot = f"{settings.dpd_bucode}{depot}"

    for item in payload if isinstance(payload, list) else [payload]:
        if item.get("sendingDepot") != DEPOT_PLACEHOLDER:
            continue
        if depot:
            item["sendingDepot"] = depot
        else:
            item.pop("sendingDepot", None)
    return payload


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options.

    `resolve_shipper_depot` defaults on so Shop2Shop / Shop2Home shipments
    resolve the shipper's depot unless a caller explicitly opts out.
    """

    if package_options is not None:
        options.update(package_options.content)

    options.setdefault("dpd_meta_resolve_shipper_depot", True)

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

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]

            # Map carrier service code to karrio service code
            karrio_service_code = ShippingService.map(service_code).name_or_key

            row_min_weight = float(row["min_weight"]) if row.get("min_weight") else None
            row_max_weight = float(row["max_weight"]) if row.get("max_weight") else None

            # Initialize service if not exists
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": row_min_weight,
                    "max_weight": row_max_weight,
                    "max_length": (float(row["max_length"]) if row.get("max_length") else None),
                    "max_width": (float(row["max_width"]) if row.get("max_width") else None),
                    "max_height": (float(row["max_height"]) if row.get("max_height") else None),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": row.get("domicile", "").lower() == "true",
                    "international": (True if row.get("international", "").lower() == "true" else None),
                    "zones": [],
                }
            else:
                # Update service-level weight bounds to cover all zones
                current = services_dict[karrio_service_code]
                if row_min_weight is not None and (
                    current["min_weight"] is None or row_min_weight < current["min_weight"]
                ):
                    current["min_weight"] = row_min_weight
                if row_max_weight is not None and (
                    current["max_weight"] is None or row_max_weight > current["max_weight"]
                ):
                    current["max_weight"] = row_max_weight
                # Merge domicile/international flags from subsequent rows
                if row.get("domicile", "").lower() == "true":
                    current["domicile"] = True
                if row.get("international", "").lower() == "true":
                    current["international"] = True

            # Parse country codes
            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=row_min_weight,
                max_weight=row_max_weight,
                transit_days=(int(row["transit_days"].split("-")[0]) if row.get("transit_days") else None),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()


class PushTrackingStatus(lib.Enum):
    """DPD Tracking Push `status` → unified status. See SPECS.md › Tracking Push."""

    pending = ["start_order"]
    picked_up = ["pickup_driver"]
    in_transit = ["pickup_depot", "delivery_depot", "delivery_nab"]
    out_for_delivery = ["delivery_carload"]
    on_hold = ["delivery_notification"]
    delivered = ["delivery_customer", "pickup_by_consignee"]
    ready_for_pickup = ["delivery_shop"]
    delivery_failed = ["error_pickup"]
    return_to_sender = ["error_return", "no_pickup_by_consignee"]


# Human-readable label per push `status` code (the payload carries only the code).
PUSH_STATUS_DESCRIPTIONS = {
    "start_order": "Order data captured",
    "pickup_driver": "Picked up by driver",
    "pickup_depot": "Arrived at incoming depot",
    "delivery_depot": "Arrived at outgoing depot",
    "delivery_carload": "Out for delivery",
    "delivery_nab": "Neighbour delivery scan",
    "delivery_notification": "Delivery obstacle (e.g. address clarification)",
    "delivery_customer": "Delivered to customer",
    "delivery_shop": "Delivered to pickup parcelshop",
    "error_pickup": "Problem at pickup",
    "error_return": "System return to sender",
    "pickup_by_consignee": "Picked up at parcelshop by recipient",
    "no_pickup_by_consignee": "Not picked up at parcelshop",
}
