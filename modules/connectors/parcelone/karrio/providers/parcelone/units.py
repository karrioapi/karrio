"""ParcelOne units and enums. See SPECS.md for integration details."""

import csv
import pathlib

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib


class LabelFormat(lib.StrEnum):
    """Supported label formats. Vendor accepts: PDF, ZPL203, ZPL300, GIF."""

    PDF = "PDF"
    ZPL203 = "ZPL203"
    ZPL300 = "ZPL300"
    GIF = "GIF"
    # generic ZPL alias → 200 dpi default
    ZPL = ZPL203


class LabelSize(lib.StrEnum):
    """Supported label sizes."""

    A6 = "A6"
    A4 = "A4"


class WeightUnit(lib.StrEnum):
    """Supported weight units."""

    kg = "kg"
    g = "g"


class CEP(lib.StrEnum):
    """Available carriers (CEP = Courier, Express, Parcel) through ParcelOne."""

    DFR = "DFR"  # DPAG-FR
    DHL = "DHL"  # Deutsche Post - DHL
    DPD = "DPD"
    MFR = "MFR"  # Mondial Relay
    PA1 = "PA1"  # Parcel.One
    PAT = "PAT"  # Post AT
    PIT = "PIT"  # Poste Italiane
    PNL = "PNL"  # Post NL
    PNO = "PNO"  # PostNord
    PPL = "PPL"  # InPost
    UPS = "UPS"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type."""

    PACKAGE = "PACKAGE"
    PALLET = "PALLET"

    # Unified Packaging type mapping
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PALLET
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class CustomsContentType(lib.Enum):
    """Maps karrio content_type to ParcelOne ItemCategory int (vendor spec §1548)."""

    gift = 1
    documents = 2
    sample = 3
    return_merchandise = 4
    merchandise = 5
    other = 5  # alias — same vendor bucket as merchandise


class ConnectionConfig(lib.Enum):
    """ParcelOne connection configuration options."""

    cep_id = lib.OptionEnum("cep_id", str, "PA1")
    product_id = lib.OptionEnum("product_id", str, "eco")
    label_format = lib.OptionEnum("label_format", LabelFormat)
    label_size = lib.OptionEnum("label_size", LabelSize)
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)
    force_carrier_label = lib.OptionEnum("force_carrier_label", bool, True)
    app_identifier = lib.OptionEnum(
        "app_identifier",
        str,
        meta=dict(configurable=False),
    )


SYSTEM_CONFIG = {
    "PARCELONE_APP_IDENTIFIER": (
        "JTL-Shipping",
        "Source-software marker ParcelOne sees in their portal (ShippingData.Software)",
        str,
    ),
}


class ShippingService(lib.StrEnum):
    """ParcelOne shipping services.

    Format: ``parcelone_{cep_lower}_{product_lower}`` → vendor value
    ``"{CEPID}_{ProductID}"`` parsed by :func:`parse_service_code`.
    """

    # --- DFR (DPAG-FR) ---
    parcelone_dfr_gmp = "DFR_GMP"  # Packet
    parcelone_dfr_gpp = "DFR_GPP"  # Packet Plus
    parcelone_dfr_gpt = "DFR_GPT"  # Packet Tracked

    # --- DHL (Deutsche Post - DHL) ---
    parcelone_dhl_101 = "DHL_101"  # National
    parcelone_dhl_5301 = "DHL_5301"  # Weltpaket Premium
    parcelone_dhl_5302 = "DHL_5302"  # Weltpaket

    # --- MFR (Mondial Relay) ---
    parcelone_mfr_24r = "MFR_24R"  # Point Relais

    # --- PA1 (Parcel.One) ---
    parcelone_pa1_basic = "PA1_basic"  # Parcel Basic
    parcelone_pa1_basicL = "PA1_basicL"  # Letter Basic
    parcelone_pa1_eco = "PA1_eco"  # Parcel Eco
    parcelone_pa1_ecoL = "PA1_ecoL"  # Letter Eco
    parcelone_pa1_plus = "PA1_plus"  # Parcel Plus
    parcelone_pa1_plusL = "PA1_plusL"  # Letter Plus
    parcelone_pa1_plusZ = "PA1_plusZ"  # Parcel Plus Z

    # --- PAT (Post AT) ---
    parcelone_pat_klepa = "PAT_KLEPA"  # Kleinpaket 2000
    parcelone_pat_norna = "PAT_NORNA"  # Paket Standard
    parcelone_pat_selna = "PAT_SELNA"  # Premium Select

    # --- PIT (Poste Italiane) ---
    parcelone_pit_cbe = "PIT_CBE"  # Express Home COD
    parcelone_pit_cbs = "PIT_CBS"  # Standard Home COD
    parcelone_pit_pbe = "PIT_PBE"  # Express Home
    parcelone_pit_pbs = "PIT_PBS"  # Standard Home

    # --- PNL (Post NL) ---
    parcelone_pnl_2928 = "PNL_2928"  # Brievenbuspakje
    parcelone_pnl_3085 = "PNL_3085"  # Pakketen

    # --- PNO (PostNord) ---
    parcelone_pno_17 = "PNO_17"  # MyPack Home
    parcelone_pno_19 = "PNO_19"  # MyPack Collect

    # --- PPL (InPost) ---
    parcelone_ppl_courier_standard = "PPL_courier_standard"
    parcelone_ppl_locker_standard = "PPL_locker_standard"

    # --- UPS ---
    parcelone_ups_07 = "UPS_07"  # Express
    parcelone_ups_08 = "UPS_08"  # Expedited
    parcelone_ups_11 = "UPS_11"  # Standard
    parcelone_ups_54 = "UPS_54"  # Express Plus
    parcelone_ups_65 = "UPS_65"  # Express Saver

    # --- Legacy aliases (kept so existing connections do not break) ---
    parcelone_dhl_paket = parcelone_dhl_101
    parcelone_dhl_paket_international = parcelone_dhl_5302
    parcelone_dhl_express = parcelone_dhl_5301


def parse_service_code(service_code: str) -> tuple[str, str]:
    """Resolve a service code to ``(CEPID, ProductID)`` in canonical wire case.

    Accepts both ``parcelone_<cep>_<product>`` (any casing) and the wire
    form ``<CEPID>_<ProductID>``.
    """
    needle = (service_code or "").lower()
    for member in ShippingService:
        if member.name.lower() == needle or member.value.lower() == needle:
            cep, _, product = member.value.partition("_")
            return cep, product
    code = service_code
    if code.lower().startswith("parcelone_"):
        code = code[len("parcelone_") :]
    if "_" in code:
        cep, _, product = code.partition("_")
        return cep, product
    return code, ""


def compact_phone(value: str | None) -> str | None:
    """Return a space-free phone number capped at ParcelOne's 15-char limit.

    ParcelOne rejects ShipmentContact.Phone longer than 15 characters
    (error 1014, "fieldlength … Max:15"). karrio renders phone numbers in
    spaced international format (e.g. "+33 1 42 00 00 00", 17 chars), which
    overflows for most non-DE destinations on the UPS CEP. Sending the
    compact form ("+33142000000") keeps every digit and fits the limit.
    """
    if not value:
        return value
    return value.replace(" ", "")[:15]


EAN_METADATA_KEYS = ("EAN", "ean", "gtin", "GTIN")


def additional_info_for_commodity(item: models.Commodity) -> list[tuple[str, str]]:
    """Build the ParcelOne ``AdditionalInfo`` Key/Value pairs. See SPECS.md."""
    metadata = getattr(item, "metadata", None) or {}

    ean = next((metadata[key] for key in EAN_METADATA_KEYS if metadata.get(key)), None)
    pairs = [("EAN", str(ean))] if ean else []

    pairs.extend(
        (str(key), str(value))
        for key, value in metadata.items()
        if key not in EAN_METADATA_KEYS and value not in (None, "")
    )

    url_path = getattr(item, "product_url", None)
    if url_path and "urlPath" not in metadata:
        pairs.append(("urlPath", str(url_path)))

    return pairs


class ShippingOption(lib.Enum):
    """Carrier specific shipping options. See SPECS.md for behaviour."""

    # --- Return services ---
    parcelone_return_label = lib.OptionEnum(
        "SRL", bool, meta=dict(category="RETURN", configurable=True, service_level=True)
    )  # Retourelabel — return label attached to outbound shipment
    parcelone_return_only = lib.OptionEnum(
        "SRO", bool, meta=dict(category="RETURN", configurable=True, service_level=True)
    )  # Return Only — no outbound label, return label only
    parcelone_return_label_md = lib.OptionEnum(
        "SRLMD", bool, meta=dict(category="RETURN", configurable=True, service_level=True)
    )  # Retourelabel (alternate CEPs)
    parcelone_return_only_md = lib.OptionEnum(
        "SROMD", bool, meta=dict(category="RETURN", configurable=True, service_level=True)
    )  # Return Only (alternate CEPs)
    parcelone_return_no_label = lib.OptionEnum(
        "SRN", bool, meta=dict(category="RETURN", configurable=True, service_level=True)
    )  # Return Only Without Label
    # ReturnShipmentIndicator is UPS-exclusive (Mark Friebus, 2026-06). Non-UPS
    # returns use the SRO service; for UPS it selects the return type:
    # 2=Print+Mail by UPS, 3=Return Service 1-Attempt, 5=Return Service 3-Attempt,
    # 8=Electronic Return Label by URL, 9=Print Return Label. Defaults to 9.
    parcelone_return_indicator = lib.OptionEnum(
        "ReturnShipmentIndicator", int, meta=dict(category="RETURN", configurable=True, service_level=True)
    )
    parcelone_registered_mail = lib.OptionEnum(
        "SRM", bool, meta=dict(category="RETURN", configurable=True, service_level=True)
    )  # Registered Mail (return)

    # --- Tracking / last-mile ---
    parcelone_last_mile_tracking = lib.OptionEnum(
        "LMC", bool, meta=dict(category="TRACKING", configurable=True, service_level=True)
    )  # Last-Mile-Carrier Track Return

    # --- Label flavor ---
    parcelone_label_at_source = lib.OptionEnum(
        "LBL", bool, meta=dict(category="LABEL", configurable=True, service_level=True)
    )  # Carrier-branded label at source
    parcelone_label_no_logo = lib.OptionEnum(
        "LBNL", bool, meta=dict(category="LABEL", configurable=True, service_level=True)
    )  # Label without logo
    parcelone_label_qr = lib.OptionEnum(
        "LBQR", bool, meta=dict(category="LABEL", configurable=True, service_level=True)
    )  # QR-code label

    # --- Delivery options ---
    parcelone_saturday_delivery = lib.OptionEnum(
        "SDO", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True)
    )  # Saturday Delivery Only (PA1)
    parcelone_saturday_delivery_ups = lib.OptionEnum(
        "SA", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True)
    )  # Saturday Delivery (UPS)
    parcelone_saturday_delivery_pa1 = lib.OptionEnum(
        "SAD", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True)
    )  # Saturday Delivery (PA1 Eco)
    parcelone_evening_delivery = lib.OptionEnum(
        "SED", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True)
    )
    parcelone_neighbor_delivery = lib.OptionEnum(
        "SND", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False)
    )
    parcelone_no_neighbor = lib.OptionEnum(
        "NACHBAR", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False)
    )  # DHL: No delivery to neighbours
    parcelone_post_outlet_routing = lib.OptionEnum(
        "FILIALROUT", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False)
    )  # DHL Parcel Outlet Routing
    parcelone_post_office_delivery = lib.OptionEnum(
        "POO", bool, meta=dict(category="PUDO", configurable=True, service_level=False)
    )
    parcelone_post_delivery_point = lib.OptionEnum(
        "PDP", bool, meta=dict(category="PUDO", configurable=True, service_level=False)
    )
    parcelone_locker_delivery = lib.OptionEnum(
        "LOK", bool, meta=dict(category="PUDO", configurable=True, service_level=False)
    )
    parcelone_drop_off_point = lib.OptionEnum(
        "DROP", meta=dict(category="PUDO", configurable=True, service_level=False)
    )  # Parcel shop delivery (PUDO ID)
    # Locker / parcel-shop / post-office identifier. Sent as ShipToData.BranchID
    # — the field ParcelOne uses to route a shipment to a PUDO point (Mark
    # Friebus, 2026-06: locker shipments on PPL / MFR).
    parcelone_branch_id = lib.OptionEnum(
        "BranchID", str, meta=dict(category="PUDO", configurable=True, service_level=True)
    )
    parcelone_bulk_recipients = lib.OptionEnum(
        "SBR", bool, meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False)
    )

    # --- Signature / age verification ---
    parcelone_signature = lib.OptionEnum(
        "SIG", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )  # Receiver Signature (PA1, DHL)
    parcelone_signature_required = lib.OptionEnum(
        "SIGREQ", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )  # UPS: Signature Required
    parcelone_adult_signature = lib.OptionEnum(
        "ADULTSIG", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )  # UPS: Adult Signature
    parcelone_ident_check = lib.OptionEnum(
        "IDENT", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )
    parcelone_age_check = lib.OptionEnum(
        "AGE", int, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )
    parcelone_age_check_16 = lib.OptionEnum(
        "VISAGE16", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )  # DHL: Visual Age Check 16
    parcelone_age_check_18 = lib.OptionEnum(
        "VISAGE18", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )  # DHL: Visual Age Check 18
    parcelone_personally = lib.OptionEnum(
        "PERSON", bool, meta=dict(category="SIGNATURE", configurable=True, service_level=True)
    )  # DHL: Named person only

    # --- Insurance / declared value ---
    parcelone_insurance = lib.OptionEnum(
        "EI", float, meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )  # Extended Insurance 255 EUR
    parcelone_insurance_5 = lib.OptionEnum(
        "EI5", float, meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )  # Extended Insurance 555 EUR
    parcelone_insurance_currency = lib.OptionEnum(
        "INS_CURRENCY", meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )
    parcelone_insurance_ups = lib.OptionEnum(
        "WERT", float, meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )  # UPS: Insured Package
    parcelone_insurance_dhl_2500 = lib.OptionEnum(
        "WERT2500", float, meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )  # DHL: Insured 2500 EUR
    parcelone_insurance_dhl_25000 = lib.OptionEnum(
        "WERT25000", float, meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )  # DHL: Insured 25000 EUR
    parcelone_full_coverage = lib.OptionEnum(
        "COV", bool, meta=dict(category="INSURANCE", configurable=True, service_level=False)
    )

    # --- COD ---
    parcelone_cod = lib.OptionEnum(
        "COD", float, meta=dict(category="COD", configurable=True, service_level=False)
    )  # Cash on Delivery (PA1)
    parcelone_cod_currency = lib.OptionEnum(
        "COD_CURRENCY", meta=dict(category="COD", configurable=True, service_level=False)
    )
    parcelone_cod_dhl = lib.OptionEnum(
        "NN", float, meta=dict(category="COD", configurable=True, service_level=False)
    )  # DHL/UPS: Cash on Delivery

    # --- Customs / DDP ---
    parcelone_ddp_single = lib.OptionEnum(
        "DDPEV", bool, meta=dict(category="CUSTOMS", configurable=True, service_level=False)
    )  # DDP single shipment customs clearance
    parcelone_ddp_fiscal = lib.OptionEnum(
        "DDPFF", bool, meta=dict(category="CUSTOMS", configurable=True, service_level=False)
    )  # DDP fiscal-agency full customs

    # --- Notification services ---
    parcelone_notification_email = lib.OptionEnum(
        "MAIL", meta=dict(category="NOTIFICATION", configurable=True, service_level=False)
    )
    parcelone_notification_sms = lib.OptionEnum(
        "SMS", meta=dict(category="NOTIFICATION", configurable=True, service_level=False)
    )

    # --- Handling / premium ---
    parcelone_bulky_goods = lib.OptionEnum(
        "BSC", bool, meta=dict(configurable=True, service_level=True)
    )  # Bulky Shipment
    parcelone_bulky_goods_dhl = lib.OptionEnum(
        "GROSS", bool, meta=dict(configurable=True, service_level=True)
    )  # DHL: Surcharge Bulky Goods
    parcelone_priority = lib.OptionEnum("PRIO", bool, meta=dict(configurable=True, service_level=True))
    parcelone_express = lib.OptionEnum("SXP", bool, meta=dict(configurable=True, service_level=True))  # Express
    parcelone_additional_handling = lib.OptionEnum(
        "ZUSHAND", bool, meta=dict(configurable=True, service_level=True)
    )  # UPS: Additional Handling
    parcelone_carbon_neutral = lib.OptionEnum(
        "CARBON", bool, meta=dict(configurable=True, service_level=True)
    )  # UPS: Carbon-Neutral
    parcelone_premium = lib.OptionEnum("PREMIUM", bool, meta=dict(configurable=True, service_level=True))

    # --- Verification / scans ---
    parcelone_parcel_check = lib.OptionEnum(
        "BCP", bool, meta=dict(configurable=True, service_level=True)
    )  # Parcel Check
    parcelone_letter_check = lib.OptionEnum(
        "BCL", bool, meta=dict(configurable=True, service_level=True)
    )  # Letter Check
    parcelone_pickup_service = lib.OptionEnum(
        "SPU", bool, meta=dict(configurable=True, service_level=True)
    )  # Service Pickup
    parcelone_scan_at_hub = lib.OptionEnum("SSH", bool, meta=dict(configurable=True, service_level=True))
    parcelone_small_and_light = lib.OptionEnum("SNL", bool, meta=dict(configurable=True, service_level=True))
    parcelone_shipment_destruction = lib.OptionEnum(
        "SDO_DESTROY", bool, meta=dict(configurable=True, service_level=True)
    )  # SDO on non-PA1 CEPs — see SPECS.md "SDO ambiguity"

    # --- Surcharges (UPS / Post AT) ---
    parcelone_fuel_surcharge = lib.OptionEnum(
        "FUEL", bool, meta=dict(category="SURCHARGE", configurable=True, service_level=False)
    )
    parcelone_toll = lib.OptionEnum(
        "MAUT", bool, meta=dict(category="SURCHARGE", configurable=True, service_level=False)
    )
    parcelone_injection = lib.OptionEnum(
        "INJECT", bool, meta=dict(category="SURCHARGE", configurable=True, service_level=False)
    )

    # --- Letter products (PA1 basicL / plusL / ecoL) ---
    parcelone_big_letter = lib.OptionEnum("DGR", bool, meta=dict(configurable=True))
    parcelone_maxi_letter = lib.OptionEnum("DWS", bool, meta=dict(configurable=True))
    parcelone_packet_tracked = lib.OptionEnum("STP", bool, meta=dict(configurable=True))
    parcelone_letter_tracked = lib.OptionEnum("STM", bool, meta=dict(configurable=True))
    parcelone_packet_tracked_35 = lib.OptionEnum("P35", bool, meta=dict(configurable=True))
    parcelone_packet_tracked_75 = lib.OptionEnum("P75", bool, meta=dict(configurable=True))
    parcelone_registered_25 = lib.OptionEnum("R25", bool, meta=dict(configurable=True))
    parcelone_registered_55 = lib.OptionEnum("R55", bool, meta=dict(configurable=True))
    parcelone_tracked_mail_20 = lib.OptionEnum("T20", bool, meta=dict(configurable=True))
    parcelone_tracked_mail_25 = lib.OptionEnum("T25", bool, meta=dict(configurable=True))
    parcelone_tracked_mail_45 = lib.OptionEnum("T45", bool, meta=dict(configurable=True))
    parcelone_tracked_mail_50 = lib.OptionEnum("T50", bool, meta=dict(configurable=True))

    # --- Per-shipment overrides for routing identity ---
    parcelone_consigner_id = lib.OptionEnum(
        "CONSIGNER_ID",
        str,
        meta=dict(category="ROUTING", configurable=True, service_level=True),
    )
    parcelone_mandator_id = lib.OptionEnum(
        "MANDATOR_ID",
        str,
        meta=dict(category="ROUTING", configurable=True, service_level=True),
    )

    # Unified option mappings
    cash_on_delivery = parcelone_cod
    insurance = parcelone_insurance
    signature_required = parcelone_signature
    saturday_delivery = parcelone_saturday_delivery
    email_notification = parcelone_notification_email


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """Carrier tracking status mapping.

    Maps ParcelOne / last-mile-carrier tracking status codes to the unified status enum.
    """

    pending = [
        "CREATED",
        "REGISTERED",
        "DATA_RECEIVED",
        "LABEL_PRINTED",
        "0",
        "1",
        # PA1 numeric: "prepared for transportation by sender" (Tracking + TrackLMC)
        "100",
        "P100",
    ]
    delivered = [
        "DELIVERED",
        "POD",
        "DELIVERED_NEIGHBOR",
        "DELIVERED_SAFE_PLACE",
        "DELIVERED_PARCELSHOP",
        "90",
        # PA1 numeric: delivered (Tracking spec)
        "900",
    ]
    in_transit = [
        "IN_TRANSIT",
        "DEPARTED",
        "ARRIVED",
        "PROCESSED",
        "SORTING",
        "IN_DELIVERY_VEHICLE",
        "EXPORTED",
        "IMPORTED",
        "SHIPPED",
        "10",
        "20",
        "30",
        # PA1 numeric: handed over to carrier / at P1 HUB / left P1 HUB (Tracking + TrackLMC)
        "200",
        "300",
        "392",
        "394",
        "430",
        "P101",
    ]
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
        "ON_DELIVERY_VEHICLE",
        "DELIVERY_IN_PROGRESS",
        "80",
        # PA1 numeric: out for delivery (Tracking spec)
        "495",
    ]
    on_hold = [
        "HELD",
        "CUSTOMS",
        "CUSTOMS_CLEARANCE",
        "PAYMENT_REQUIRED",
        "AWAITING_PICKUP",
        "40",
    ]
    delivery_failed = [
        "FAILED",
        "EXCEPTION",
        "NOT_DELIVERED",
        "REFUSED",
        "ADDRESSEE_NOT_FOUND",
        "WRONG_ADDRESS",
        "99",
    ]
    delivery_delayed = [
        "DELAYED",
        "RESCHEDULED",
        "REDIRECTED",
    ]
    ready_for_pickup = [
        "READY_FOR_PICKUP",
        "AT_PARCELSHOP",
        "AVAILABLE_FOR_COLLECTION",
        "70",
    ]


class TrackingIncidentReason(lib.Enum):
    """Maps carrier exception codes to normalized incident reasons.

    IMPORTANT: This enum is required for tracking implementations.
    It maps carrier-specific exception/status codes to standardized
    incident reasons for tracking events. The reason field helps
    identify why a delivery exception occurred.

    Categories of reasons:
    - carrier_*: Issues caused by the carrier
    - consignee_*: Issues caused by the recipient
    - customs_*: Customs-related delays
    - weather_*: Weather/force majeure events
    """

    # Carrier-caused issues
    carrier_damaged_parcel = ["DAMAGED", "DMG"]
    carrier_sorting_error = ["MISROUTED", "MSR"]
    carrier_address_not_found = ["ADDRESS_NOT_FOUND", "ANF"]
    carrier_parcel_lost = ["LOST", "LP"]
    carrier_not_enough_time = ["LATE", "NO_TIME"]
    carrier_vehicle_issue = ["VEHICLE_BREAKDOWN", "VB"]

    # Consignee-caused issues
    consignee_refused = ["REFUSED", "RJ"]
    consignee_business_closed = ["BUSINESS_CLOSED", "BC"]
    consignee_not_available = ["NOT_AVAILABLE", "NA"]
    consignee_not_home = ["NOT_HOME", "NH", "ADDRESSEE_NOT_FOUND"]
    consignee_incorrect_address = ["WRONG_ADDRESS", "IA"]
    consignee_access_restricted = ["ACCESS_RESTRICTED", "AR"]

    # Customs-related issues
    customs_delay = ["CUSTOMS", "CUSTOMS_CLEARANCE", "CD"]
    customs_documentation = ["CUSTOMS_DOCS", "CM"]
    customs_duties_unpaid = ["PAYMENT_REQUIRED", "DU"]

    # Weather/force majeure
    weather_delay = ["WEATHER", "WE"]
    natural_disaster = ["NATURAL_DISASTER", "ND"]

    # Unknown/unmapped
    unknown = []


# Offline fallback for `services_for_product`. See SPECS.md "Architecture".
STATIC_PROFILE: dict = {
    "mandator": "1",
    "consigners": ["1"],
    "ceps": {
        "DFR": {
            "name": "DPAG-FR",
            "products": {
                "GMP": {"name": "Packet", "services": ["LBL"]},
                "GPP": {"name": "Packet Plus", "services": ["LBL"]},
                "GPT": {"name": "Packet Tracked", "services": ["LBL"]},
            },
        },
        "DHL": {
            "name": "Deutsche Post - DHL",
            "products": {
                "101": {
                    "name": "National",
                    "services": [
                        "FILIALROUT",
                        "GROSS",
                        "NACHBAR",
                        "NN",
                        "PERSON",
                        "SIG",
                        "VISAGE16",
                        "VISAGE18",
                        "WERT2500",
                        "WERT25000",
                    ],
                },
                "5301": {
                    "name": "Weltpaket Premium",
                    "services": ["GROSS", "NN", "WERT2500", "WERT25000"],
                },
                "5302": {
                    "name": "Weltpaket",
                    "services": ["GROSS", "NN", "WERT2500", "WERT25000"],
                },
            },
        },
        "DPD": {"name": "DPD", "products": {}},
        "MFR": {
            "name": "Mondial Relay",
            "products": {
                "24R": {
                    "name": "Point Relais",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
            },
        },
        "PA1": {
            "name": "PARCEL.ONE",
            "products": {
                "basic": {
                    "name": "Parcel Basic",
                    "services": [
                        "BCL",
                        "BCP",
                        "COD",
                        "DDPEV",
                        "DDPFF",
                        "EI",
                        "EI5",
                        "LBNL",
                        "LBQR",
                        "PDP",
                        "PRIO",
                        "SDO",
                        "SIG",
                        "SPU",
                        "SRL",
                        "SRLMD",
                        "SRO",
                        "SROMD",
                        "SXP",
                    ],
                },
                "basicL": {
                    "name": "Letter Basic",
                    "services": [
                        "BCL",
                        "LBNL",
                        "LBQR",
                        "P35",
                        "P75",
                        "R25",
                        "R55",
                        "SDO",
                        "SPU",
                        "SRM",
                        "SSH",
                        "STM",
                        "STP",
                        "T20",
                        "T25",
                        "T45",
                        "T50",
                    ],
                },
                "eco": {
                    "name": "Parcel Eco",
                    "services": [
                        "BCL",
                        "BCP",
                        "COD",
                        "COV",
                        "DDPEV",
                        "DDPFF",
                        "LBNL",
                        "LBQR",
                        "LOK",
                        "PDP",
                        "POO",
                        "PRIO",
                        "SAD",
                        "SDO",
                        "SED",
                        "SND",
                        "SNL",
                        "SPU",
                        "SRL",
                        "SRLMD",
                        "SRN",
                        "SRO",
                        "SROMD",
                        "SXP",
                    ],
                },
                "ecoL": {
                    "name": "Letter Eco",
                    "services": ["DGR", "DWS", "LBNL", "LBQR", "SDO", "SPU", "SSH"],
                },
                "plus": {
                    "name": "Parcel Plus",
                    "services": [
                        "BCL",
                        "BCP",
                        "BSC",
                        "COD",
                        "DDPEV",
                        "DDPFF",
                        "EI",
                        "EI5",
                        "LBNL",
                        "LBQR",
                        "PDP",
                        "PRIO",
                        "SBR",
                        "SDO",
                        "SIG",
                        "SPU",
                        "SRL",
                        "SRLMD",
                        "SRO",
                        "SROMD",
                        "SXP",
                    ],
                },
                "plusL": {
                    "name": "Letter Plus",
                    "services": [
                        "BCL",
                        "LBNL",
                        "LBQR",
                        "P35",
                        "P75",
                        "R25",
                        "R55",
                        "SDO",
                        "SPU",
                        "SRM",
                        "SSH",
                        "STM",
                        "STP",
                        "T20",
                        "T25",
                        "T45",
                        "T50",
                    ],
                },
                "plusZ": {
                    "name": "Parcel Plus Z",
                    "services": [
                        "BCL",
                        "BCP",
                        "BSC",
                        "COD",
                        "DDPEV",
                        "DDPFF",
                        "EI",
                        "EI5",
                        "LBNL",
                        "LBQR",
                        "LMC",
                        "PRIO",
                        "SDO",
                        "SPU",
                        "SRL",
                        "SRLMD",
                        "SRO",
                        "SROMD",
                    ],
                },
            },
        },
        "PAT": {
            "name": "Post AT",
            "products": {
                "KLEPA": {
                    "name": "Kleinpaket 2000",
                    "services": ["BCP", "BSC", "EI", "FUEL", "INJECT", "LBL", "MAUT", "SDO"],
                },
                "NORNA": {
                    "name": "Paket Standard",
                    "services": [
                        "BCP",
                        "BSC",
                        "EI",
                        "FUEL",
                        "INJECT",
                        "LBL",
                        "MAUT",
                        "SDO",
                        "SRL",
                        "SRO",
                    ],
                },
                "SELNA": {
                    "name": "Premium Select",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
            },
        },
        "PIT": {
            "name": "Poste Italiane",
            "products": {
                "CBE": {
                    "name": "Express Home COD",
                    "services": ["BCP", "BSC", "COD", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
                "CBS": {
                    "name": "Standard Home COD",
                    "services": ["BCP", "BSC", "COD", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
                "PBE": {
                    "name": "Express Home",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
                "PBS": {
                    "name": "Standard Home",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
            },
        },
        "PNL": {
            "name": "Post NL",
            "products": {
                "2928": {"name": "Brievenbuspakje", "services": []},
                "3085": {
                    "name": "Pakketen",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
            },
        },
        "PNO": {
            "name": "PostNord",
            "products": {
                "17": {
                    "name": "MyPack Home",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
                "19": {
                    "name": "MyPack Collect",
                    "services": ["BCP", "BSC", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
            },
        },
        "PPL": {
            "name": "InPost",
            "products": {
                "courier_standard": {
                    "name": "Courier Standard",
                    "services": ["BCP", "BSC", "COD", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
                "locker_standard": {
                    "name": "Locker Standard",
                    "services": ["BCP", "BSC", "COD", "EI", "LBL", "SDO", "SRL", "SRO"],
                },
            },
        },
        "UPS": {
            "name": "United Parcel Service",
            "products": {
                "07": {
                    "name": "Express",
                    "services": ["ADULTSIG", "CARBON", "GROSS", "NN", "SA", "SIGREQ", "WERT", "ZUSHAND"],
                },
                "08": {"name": "Expedited", "services": []},
                "11": {
                    "name": "Standard",
                    "services": ["ADULTSIG", "CARBON", "GROSS", "NN", "SIGREQ", "WERT", "ZUSHAND"],
                },
                "54": {"name": "Express Plus", "services": []},
                "65": {
                    "name": "Express Saver",
                    "services": ["ADULTSIG", "CARBON", "GROSS", "NN", "SIGREQ", "WERT", "ZUSHAND"],
                },
            },
        },
    },
}


def services_for_product(
    cep_id: str,
    product_id: str,
    profile: dict | None = None,
) -> list[str]:
    """Return the list of vendor ServiceID values valid on a (CEP, Product).

    Live ``profile`` first, falling back to :data:`STATIC_PROFILE`.
    """
    for source in (profile, STATIC_PROFILE):
        if not source:
            continue
        product = (source.get("ceps", {}).get(cep_id, {}).get("products", {}) or {}).get(product_id)
        if product:
            return list(product.get("services", []))
    return []


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
                service_name="Parcel.One Eco",
                service_code="parcelone_pa1_eco",
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

            # Parse transit days (handle "1-3" format)
            transit_days = None
            if row.get("transit_days"):
                transit_str = row["transit_days"].split("-")[0]
                if transit_str.isdigit():
                    transit_days = int(transit_str)

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=transit_days,
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
