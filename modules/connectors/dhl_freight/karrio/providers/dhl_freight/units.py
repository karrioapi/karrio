import csv
import pathlib

import karrio.core.models as models
import karrio.lib as lib

# System config schema for runtime settings (e.g., API credentials).
# Format: Dict[str, Tuple[default_value, description, type]]
SYSTEM_CONFIG = {
    "DHL_FREIGHT_CLIENT_ID": (
        "",
        "DHL Freight OAuth client ID for production",
        str,
    ),
    "DHL_FREIGHT_CLIENT_SECRET": (
        "",
        "DHL Freight OAuth client secret for production",
        str,
    ),
    "DHL_FREIGHT_SANDBOX_CLIENT_ID": (
        "",
        "DHL Freight OAuth client ID for sandbox/test mode",
        str,
    ),
    "DHL_FREIGHT_SANDBOX_CLIENT_SECRET": (
        "",
        "DHL Freight OAuth client secret for sandbox/test mode",
        str,
    ),
    "DHL_FREIGHT_ACCOUNT_NUMBER": (
        "",
        "DHL Freight consignor account number for production",
        str,
    ),
    "DHL_FREIGHT_SANDBOX_ACCOUNT_NUMBER": (
        "",
        "DHL Freight consignor account number for sandbox/test mode",
        str,
    ),
}


class PackagingType(lib.StrEnum):
    """DHL Freight package type qualifiers (piece-level)."""

    PAL = "PAL"  # Pallet (EUR / industrial)
    BOX = "BOX"
    CRT = "CRT"  # Crate
    PCS = "PCS"  # Loose pieces
    DRM = "DRM"  # Drum
    BAG = "BAG"
    ROL = "ROL"  # Roll
    UNT = "UNT"  # Generic Unit

    """ Unified Packaging type mapping """
    pallet = PAL
    small_box = BOX
    medium_box = BOX
    large_box = BOX
    your_packaging = PAL


class Incoterm(lib.StrEnum):
    """DHL Freight ``payerCode.code`` — incoterms 2020 + DHL conventions.

    The Product Manual restricts the set to the values DHL Freight will accept
    on the booking; unsupported terms (EXW, FCA, etc.) require manual handling
    by the DHL booking team.
    """

    DAP = "DAP"
    DDP = "DDP"
    CPT = "CPT"
    CIP = "CIP"
    DPU = "DPU"


class PieceReferenceQualifier(lib.StrEnum):
    """``references[].qualifier`` values supported by DHL Freight."""

    CNR = "CNR"  # Consignor reference
    CNZ = "CNZ"  # Consignee reference
    SHP = "SHP"  # Shipper reference
    ORD = "ORD"  # Order number
    INV = "INV"  # Invoice number


class PartyType(lib.StrEnum):
    """``parties[].type`` values — DHL Freight has FOUR distinct party roles."""

    Consignor = "Consignor"  # legal sender
    Consignee = "Consignee"  # legal receiver
    Pickup = "Pickup"  # physical pickup location (may equal Consignor)
    Delivery = "Delivery"  # physical delivery location (may equal Consignee)


class ShippingService(lib.Enum):
    """DHL Freight ``productCode`` values.

    Codes are taken from the 2026/R03 Product Manual. The enum value is the
    on-wire ``productCode`` sent on the booking; the enum name is the karrio
    service code surfaced to users.
    """

    # Eurapid / international groupage (express LTL across EU)
    dhl_freight_eurapid = "ECI"
    # Euroconnect — DHL's standard European groupage product
    dhl_freight_euroconnect = "ECX"
    # Euroconnect Plus — premium scheduled groupage
    dhl_freight_euroconnect_plus = "ECP"
    # Domestic groupage (national network of the origin country)
    dhl_freight_domestic = "DOM"
    # Full-truck-load / part-load (per quotation)
    dhl_freight_ftl = "FTL"


class ConnectionConfig(lib.Enum):
    language = lib.OptionEnum(
        "language",
        lib.units.create_enum("Language", ["de", "en", "fr", "es", "it", "nl"]),
        default="en",
    )
    default_payer_code = lib.OptionEnum(
        "default_payer_code",
        lib.units.create_enum("Incoterm", [_.name for _ in Incoterm]),  # type: ignore
        default="DAP",
    )
    default_payer_location = lib.OptionEnum("default_payer_location", str)
    cost_center = lib.OptionEnum("cost_center")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    # Print (Labelling) API follow-up (PRD §6.3). Opt-in: the Print request
    # schema is unpublished and unvalidated, so the booking → print chain is
    # off by default and fail-open (a print failure never fails the booking).
    auto_print_documents = lib.OptionEnum("auto_print_documents", bool, default=False)
    print_document_type = lib.OptionEnum(
        "print_document_type",
        lib.units.create_enum("PrintDocumentType", ["label", "shipmentList", "waybill"]),
        default="label",
    )


class ShippingOption(lib.Enum):
    """DHL Freight ``additionalServices`` — booking-time accessorials.

    Every flag here maps 1:1 to a field in the ``additionalServices`` object on
    the ``sendtransportinstruction`` payload. Categories match the categorisation
    karrio uses in the shipping-method editor.
    """

    # fmt: off
    # Delivery timing
    dhl_freight_after_12_delivery = lib.OptionEnum(
        "after12Delivery", bool,
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True,
                  help="Guaranteed delivery after 12:00 local time"),
    )
    dhl_freight_available_pickup_time = lib.OptionEnum(
        "availablePickupTime",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False,
                  help="Earliest pickup time (HH:MM, local time at origin)"),
    )
    dhl_freight_available_delivery_time = lib.OptionEnum(
        "availableDeliveryTime",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False,
                  help="Earliest delivery time (HH:MM, local time at destination)"),
    )
    dhl_freight_time_slot_booking_pickup = lib.OptionEnum(
        "timeSlotBookingPickup", bool,
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True,
                  help="Book a pickup time slot with the consignor"),
    )
    dhl_freight_time_slot_booking_delivery = lib.OptionEnum(
        "timeSlotBookingDelivery", bool,
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True,
                  help="Book a delivery time slot with the consignee"),
    )
    dhl_freight_pre_advice = lib.OptionEnum(
        "preAdvice", bool,
        default=True,
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True,
                  help="Pre-advise the consignee before delivery"),
    )
    # Loading services (DHL Freight-specific dock services)
    dhl_freight_tail_lift_loading = lib.OptionEnum(
        "tailLiftLoading", bool,
        meta=dict(category="LOADING", configurable=True, service_level=True,
                  help="Tail-lift truck required at pickup"),
    )
    dhl_freight_tail_lift_unloading = lib.OptionEnum(
        "tailLiftUnloading", bool,
        meta=dict(category="LOADING", configurable=True, service_level=True,
                  help="Tail-lift truck required at delivery"),
    )
    dhl_freight_side_loading_pickup = lib.OptionEnum(
        "sideLoadingPickup", bool,
        meta=dict(category="LOADING", configurable=True, service_level=True,
                  help="Side-loading vehicle required at pickup"),
    )
    dhl_freight_side_unloading_delivery = lib.OptionEnum(
        "sideUnloadingDelivery", bool,
        meta=dict(category="LOADING", configurable=True, service_level=True,
                  help="Side-unloading vehicle required at delivery"),
    )
    dhl_freight_drop_off_by_consignor = lib.OptionEnum(
        "dropOffByConsignor", bool,
        meta=dict(category="LOADING", configurable=True, service_level=True,
                  help="Consignor drops the freight at the DHL terminal (no pickup)"),
    )
    # Cargo conditioning
    dhl_freight_temperature_controlled = lib.OptionEnum(
        "temperatureControlled", dict,
        meta=dict(category="TEMPERATURE", configurable=True, service_level=False,
                  help="Temperature-controlled transport. Structure: "
                       "{type: 'Custom'|'Chilled'|'Frozen', min: float, max: float}"),
    )
    # Hazardous cargo (set true if any piece carries `dangerousGoods` ADR data)
    dhl_freight_dangerous_goods = lib.OptionEnum(
        "dangerousGoods", bool,
        meta=dict(category="HAZARDOUS", configurable=False, service_level=False,
                  help="Set automatically when a piece declares ADR dangerous goods"),
    )
    # Insurance (separate from declared goodsValue)
    dhl_freight_insurance = lib.OptionEnum(
        "insurance", dict,
        meta=dict(category="INSURANCE", configurable=True, service_level=False,
                  help="Additional cargo insurance. Structure: {value: float, currency: ISO}"),
    )
    # Cash on delivery
    dhl_freight_cash_on_delivery = lib.OptionEnum(
        "cashOnDelivery", dict,
        meta=dict(category="COD", configurable=True, service_level=False,
                  help="CoD amount. Structure: {amount: float, currency: ISO}"),
    )

    # Booking-level references / metadata
    dhl_freight_payer_code = lib.OptionEnum(
        "payerCode",
        lib.units.create_enum("PayerCode", [_.name for _ in Incoterm]),  # type: ignore
        meta=dict(category="INVOICE", configurable=True, service_level=False,
                  help="Incoterms payment term — payerCode.code (DAP/DDP/CPT/CIP/DPU)."),
    )
    dhl_freight_payer_code_location = lib.OptionEnum(
        "payerCodeLocation",
        meta=dict(category="INVOICE", configurable=True, service_level=False,
                  help="Optional payer location — payerCode.location."),
    )
    dhl_freight_consignor_account = lib.OptionEnum(
        "consignor_account",
        meta=dict(category="SHIPMENT", configurable=True, service_level=False,
                  help="Consignor DHL Freight account number (Parties[Consignor].Id). "
                       "Overrides the connection account_number; mandatory for booking."),
    )
    dhl_freight_consignee_account = lib.OptionEnum(
        "consignee_account",
        meta=dict(category="SHIPMENT", configurable=True, service_level=False,
                  help="Consignee DHL Freight account number (Parties[Consignee].Id), optional."),
    )
    dhl_freight_consignor_reference = lib.OptionEnum(
        "consignor_reference",
        meta=dict(category="SHIPMENT", configurable=True, service_level=False,
                  help="Consignor reference (writes a CNR entry under references[])"),
    )
    dhl_freight_consignee_reference = lib.OptionEnum(
        "consignee_reference",
        meta=dict(category="SHIPMENT", configurable=True, service_level=False,
                  help="Consignee reference (writes a CNZ entry under references[])"),
    )
    dhl_freight_order_reference = lib.OptionEnum(
        "order_reference",
        meta=dict(category="SHIPMENT", configurable=True, service_level=False,
                  help="Order reference (writes an ORD entry under references[])"),
    )
    dhl_freight_pickup_instruction = lib.OptionEnum(
        "pickupInstruction",
        meta=dict(category="INSTRUCTIONS", configurable=True, service_level=False,
                  help="Free-text pickup instruction (max 512 chars)"),
    )
    dhl_freight_delivery_instruction = lib.OptionEnum(
        "deliveryInstruction",
        meta=dict(category="INSTRUCTIONS", configurable=True, service_level=False,
                  help="Free-text delivery instruction (max 512 chars)"),
    )
    # Country-specific tax / customs references
    dhl_freight_uit_number = lib.OptionEnum(
        "uit_number",
        meta=dict(category="INVOICE", configurable=True, service_level=False,
                  help="Romania UIT_NUMBER (additional information record)"),
    )
    dhl_freight_ekaer_number = lib.OptionEnum(
        "ekaer_number",
        meta=dict(category="INVOICE", configurable=True, service_level=False,
                  help="Hungary EKAER_NUMBER (additional information record)"),
    )
    dhl_freight_sent_number = lib.OptionEnum(
        "sent_number",
        meta=dict(category="INVOICE", configurable=True, service_level=False,
                  help="Poland SENT_NUMBER (additional information record)"),
    )

    """ Unified Option type mapping """
    cash_on_delivery = dhl_freight_cash_on_delivery
    insurance = dhl_freight_insurance
    # fmt: on


class CustomsOption(lib.Enum):
    """DHL Freight customs-scoped options — read from ``customs.options``.

    These are the customs / freight-payment concepts the karrio ``Customs``
    model has no first-class slot for (PRD §6.6, §6.7). They take precedence
    over the same-named shipment-level ``ShippingOption`` fallbacks.
    """

    # fmt: off
    dhl_freight_payer_code = lib.OptionEnum("payerCode")                  # payerCode.code (incoterms)
    dhl_freight_payer_code_location = lib.OptionEnum("payerCodeLocation")  # payerCode.location
    dhl_freight_uit_number = lib.OptionEnum("UIT_NUMBER")                  # Romania
    dhl_freight_ekaer_number = lib.OptionEnum("EKAER_NUMBER")             # Hungary
    dhl_freight_sent_number = lib.OptionEnum("SENT_NUMBER")              # Poland
    # fmt: on


class PrintOption(lib.StrEnum):
    """DHL Freight Print (Labelling) API document types (PRD §6.3).

    ``label`` = barcode license-plate labels; ``shipmentList`` = shipment
    detail list; ``waybill`` = waybill / CMR.
    """

    label = "label"
    shipmentList = "shipmentList"
    waybill = "waybill"


# -----------------------------------------------------------------------------
# Tracking status mapping (DHL Group Unified Tracking API — UTAPI)
# -----------------------------------------------------------------------------
# DHL Freight tracking is served by the cross-BU UTAPI (/track/shipments),
# the same API dhl_universal uses. Its `statusCode` is one of a small
# normalized set; we map those, plus the verbose `status` text it sometimes
# returns instead.


class TrackingStatus(lib.Enum):
    pending = ["pre-transit"]
    in_transit = ["transit"]
    delivered = ["delivered"]
    delivery_failed = ["failure"]
    delivery_delayed = ["unknown"]


# -----------------------------------------------------------------------------
# Service levels (zone + weight-band rate sheet)
# -----------------------------------------------------------------------------


def load_services_from_csv() -> list[models.ServiceLevel]:
    """Load service definitions from the bundled CSV.

    CSV columns:
      service_code,service_name,zone_label,country_codes,
      min_weight,max_weight,max_length,max_width,max_height,
      rate,currency,transit_days,domicile,international
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        # Minimal fallback so the gateway can boot without a CSV present.
        return [
            models.ServiceLevel(
                service_name="DHL Freight Euroconnect",
                service_code="dhl_freight_euroconnect",
                currency="EUR",
                international=True,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    services_dict: dict[str, dict] = {}

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]
            karrio_service_code = ShippingService.map(service_code).name_or_key

            row_min_weight = float(row["min_weight"]) if row.get("min_weight") else None
            row_max_weight = float(row["max_weight"]) if row.get("max_weight") else None

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
                    "international": row.get("international", "").lower() == "true",
                    "zones": [],
                }
            else:
                current = services_dict[karrio_service_code]
                if row_min_weight is not None and (
                    current["min_weight"] is None or row_min_weight < current["min_weight"]
                ):
                    current["min_weight"] = row_min_weight
                if row_max_weight is not None and (
                    current["max_weight"] is None or row_max_weight > current["max_weight"]
                ):
                    current["max_weight"] = row_max_weight

            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]

            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=row_min_weight,
                max_weight=row_max_weight,
                transit_days=(int(row["transit_days"].split("-")[0]) if row.get("transit_days") else None),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()


def shipping_options_initializer(
    options: dict,
    package_options=None,
) -> "lib.units.ShippingOptions":
    """Apply default values to the given options."""
    import karrio.core.units as units

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption or key in units.ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)
