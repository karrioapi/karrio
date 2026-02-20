import csv
import pathlib
import re
import typing
import unicodedata
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models

PRESET_DEFAULTS = dict(dimension_unit="IN", weight_unit="LB")


class PackagePresets(lib.Enum):
    """Purolator package presets
    Note that dimensions are in IN and weight in LB
    """

    purolator_express_envelope = units.PackagePreset(
        **dict(width=12.5, height=16, length=1.5, weight=1.0), **PRESET_DEFAULTS
    )
    purolator_express_pack = units.PackagePreset(
        **dict(width=12.5, height=16, length=1.0, weight=3.0), **PRESET_DEFAULTS
    )
    purolator_express_box = units.PackagePreset(
        **dict(width=18, height=12, length=3.5, weight=7.0), **PRESET_DEFAULTS
    )


class PackagingType(lib.StrEnum):
    purolator_express_envelope = "Envelope"
    purolator_express_pack = "Pack"
    purolator_express_box = "Box"
    purolator_customer_packaging = "Customer Packaging"

    """ Unified Packaging type mapping """
    envelope = purolator_express_envelope
    pak = purolator_express_pack
    tube = purolator_customer_packaging
    pallet = purolator_customer_packaging
    small_box = purolator_customer_packaging
    medium_box = purolator_customer_packaging
    large_box = purolator_customer_packaging
    your_packaging = purolator_customer_packaging


MeasurementOptions = units.MeasurementOptionsType(min_kg=0.45, min_lb=1)


class LabelType(lib.Enum):
    PDF = "Regular"
    ZPL = "Thermal"


class PrintType(lib.StrEnum):
    PDF = "Regular"
    ZPL = "Thermal"


class PaymentType(lib.StrEnum):
    sender = "Sender"
    recipient = "Receiver"
    third_party = "ThirdParty"
    credit_card = "CreditCard"


class DutyPaymentType(lib.StrEnum):
    sender = "Sender"
    recipient = "Receiver"
    third_party = "Buyer"


class CreditCardType(lib.StrEnum):
    visa = "Visa"
    mastercard = "Mastercard"
    american_express = "AmericanExpress"


class ShippingOption(lib.Enum):
    purolator_dangerous_goods = lib.OptionEnum(
        "Dangerous Goods", meta=dict(category="DANGEROUS_GOOD")
    )
    purolator_chain_of_signature = lib.OptionEnum(
        "Chain of Signature", meta=dict(category="SIGNATURE")
    )
    purolator_express_cheque = lib.OptionEnum(
        "ExpressCheque", meta=dict(category="COD")
    )
    purolator_hold_for_pickup = lib.OptionEnum(
        "Hold For Pickup", meta=dict(category="PUDO")
    )
    purolator_return_services = lib.OptionEnum(
        "Return Services", meta=dict(category="RETURN")
    )
    purolator_saturday_service = lib.OptionEnum(
        "Saturday Service", meta=dict(category="DELIVERY_OPTIONS")
    )
    purolator_origin_signature_not_required = lib.OptionEnum(
        "Origin Signature Not Required (OSNR)", meta=dict(category="SIGNATURE")
    )
    purolator_adult_signature_required = lib.OptionEnum(
        "Adult Signature Required (ASR)", meta=dict(category="SIGNATURE")
    )
    purolator_special_handling = lib.OptionEnum("Special Handling")

    """Karrio specific option"""
    purolator_show_alternative_services = lib.OptionEnum(
        "Show Alternate Services", bool
    )

    """ Unified Option type mapping """
    saturday_delivery = purolator_saturday_service


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
    service_is_defined: bool = False,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    # When no specific service is requested, set a default one.
    _options.update(
        {
            "purolator_show_alternative_services": _options.get(
                "purolator_show_alternative_services"
            )
            or (not service_is_defined)
        }
    )

    def items_filter(key: str) -> bool:
        return key in ShippingOption and key not in NON_OFFICIAL_SERVICES  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


NON_OFFICIAL_SERVICES = [ShippingOption.purolator_show_alternative_services.name]


class ShippingService(lib.StrEnum):
    purolator_express_9_am = "PurolatorExpress9AM"
    purolator_express_us = "PurolatorExpressU.S."
    purolator_express_10_30_am = "PurolatorExpress10:30AM"
    purolator_express_us_9_am = "PurolatorExpressU.S.9AM"
    purolator_express_12_pm = "PurolatorExpress12PM"
    purolator_express_us_10_30_am = "PurolatorExpressU.S.10:30AM"
    purolator_express = "PurolatorExpress"
    purolator_express_us_12_00 = "PurolatorExpressU.S.12:00"
    purolator_express_evening = "PurolatorExpressEvening"
    purolator_express_envelope_us = "PurolatorExpressEnvelopeU.S."
    purolator_express_envelope_9_am = "PurolatorExpressEnvelope9AM"
    purolator_express_us_envelope_9_am = "PurolatorExpressU.S.Envelope9AM"
    purolator_express_envelope_10_30_am = "PurolatorExpressEnvelope10:30AM"
    purolator_express_us_envelope_10_30_am = "PurolatorExpressU.S.Envelope10:30AM"
    purolator_express_envelope_12_pm = "PurolatorExpressEnvelope12PM"
    purolator_express_us_envelope_12_00 = "PurolatorExpressU.S.Envelope12:00"
    purolator_express_envelope = "PurolatorExpressEnvelope"
    purolator_express_pack_us = "PurolatorExpressPackU.S."
    purolator_express_envelope_evening = "PurolatorExpressEnvelopeEvening"
    purolator_express_us_pack_9_am = "PurolatorExpressU.S.Pack9AM"
    purolator_express_pack_9_am = "PurolatorExpressPack9AM"
    purolator_express_us_pack_10_30_am = "PurolatorExpressU.S.Pack10:30AM"
    purolator_express_pack10_30_am = "PurolatorExpressPack10:30AM"
    purolator_express_us_pack_12_00 = "PurolatorExpressU.S.Pack12:00"
    purolator_express_pack_12_pm = "PurolatorExpressPack12PM"
    purolator_express_box_us = "PurolatorExpressBoxU.S."
    purolator_express_pack = "PurolatorExpressPack"
    purolator_express_us_box_9_am = "PurolatorExpressU.S.Box9AM"
    purolator_express_pack_evening = "PurolatorExpressPackEvening"
    purolator_express_us_box_10_30_am = "PurolatorExpressU.S.Box10:30AM"
    purolator_express_box_9_am = "PurolatorExpressBox9AM"
    purolator_express_us_box_12_00 = "PurolatorExpressU.S.Box12:00"
    purolator_express_box_10_30_am = "PurolatorExpressBox10:30AM"
    purolator_ground_us = "PurolatorGroundU.S."
    purolator_express_box_12_pm = "PurolatorExpressBox12PM"
    purolator_express_international = "PurolatorExpressInternational"
    purolator_express_box = "PurolatorExpressBox"
    purolator_express_international_9_am = "PurolatorExpressInternational9AM"
    purolator_express_box_evening = "PurolatorExpressBoxEvening"
    purolator_express_international_10_30_am = "PurolatorExpressInternational10:30AM"
    purolator_ground = "PurolatorGround"
    purolator_express_international_12_00 = "PurolatorExpressInternational12:00"
    purolator_ground_9_am = "PurolatorGround9AM"
    purolator_express_envelope_international = "PurolatorExpressEnvelopeInternational"
    purolator_ground_10_30_am = "PurolatorGround10:30AM"
    purolator_express_international_envelope_9_am = (
        "PurolatorExpressInternationalEnvelope9AM"
    )
    purolator_ground_evening = "PurolatorGroundEvening"
    purolator_express_international_envelope_10_30_am = (
        "PurolatorExpressInternationalEnvelope10:30AM"
    )
    purolator_quick_ship = "PurolatorQuickShip"
    purolator_express_international_envelope_12_00 = (
        "PurolatorExpressInternationalEnvelope12:00"
    )
    purolator_quick_ship_envelope = "PurolatorQuickShipEnvelope"
    purolator_express_pack_international = "PurolatorExpressPackInternational"
    purolator_quick_ship_pack = "PurolatorQuickShipPack"
    purolator_express_international_pack_9_am = "PurolatorExpressInternationalPack9AM"
    purolator_quick_ship_box = "PurolatorQuickShipBox"
    purolator_express_international_pack_10_30_am = (
        "PurolatorExpressInternationalPack10:30AM"
    )
    purolator_express_international_pack_12_00 = (
        "PurolatorExpressInternationalPack12:00"
    )
    purolator_express_box_international = "PurolatorExpressBoxInternational"
    purolator_express_international_box_9_am = "PurolatorExpressInternationalBox9AM"
    purolator_express_international_box_10_30_am = (
        "PurolatorExpressInternationalBox10:30AM"
    )
    purolator_express_international_box_12_00 = "PurolatorExpressInternationalBox12:00"


def shipping_services_initializer(
    services: typing.List[str],
    is_international: bool = False,
    recipient_country: str = None,
) -> units.Services:
    """
    Apply default values to the given services.
    """

    # When no specific service is requested, set a default.
    if not any([svc in ShippingService for svc in services]):  # type: ignore
        if is_international is False:
            services.append(ShippingService.purolator_express.name)  # type: ignore
        elif recipient_country == "US":
            services.append(ShippingService.purolator_express_us.name)  # type: ignore
        else:
            services.append(ShippingService.purolator_express_international.name)  # type: ignore

    return units.Services(services, ShippingService)


class TrackingStatus(lib.Enum):
    # Keep explicit status names we emit from `map_tracking_status`.
    pending = ["__pending__"]
    picked_up = ["ProofOfPickUp"]
    in_transit = ["Other"]
    out_for_delivery = ["OnDelivery"]
    delivered = ["Delivery"]
    on_hold = ["Undeliverable"]
    ready_for_pickup = ["__ready_for_pickup__"]
    return_to_sender = ["__return_to_sender__"]
    delivery_delayed = ["__delivery_delayed__"]
    delivery_failed = ["__delivery_failed__"]
    unknown = [""]


# Why this mapping exists:
# - Purolator ScanType values are too coarse, especially `Undeliverable`.
# - Real tracking payloads encode meaningful status in description text
#   (e.g. pickup-ready vs return-to-sender vs delay).
# - We keep exact mappings for known descriptions and keyword fallback for
#   wording drift.
PUROLATOR_TRACKING_STATUS_MAPPING: dict[str, dict[str, str]] = {
    "Other": {
        "__default__": TrackingStatus.in_transit.name,
        "Shipper created a label": TrackingStatus.pending.name,
        "Shipment created - interim manifest received": TrackingStatus.pending.name,
        "Shipment created - final manifest received": TrackingStatus.pending.name,
        "New tracking number assigned": TrackingStatus.pending.name,
        "Label information electronically submitted": TrackingStatus.pending.name,
    },
    "OnDelivery": {
        "__default__": TrackingStatus.out_for_delivery.name,
        "On vehicle for delivery": TrackingStatus.out_for_delivery.name,
    },
    "Delivery": {
        "__default__": TrackingStatus.delivered.name,
        "Shipment delivered": TrackingStatus.delivered.name,
        "Delivered to Customer by Locker": TrackingStatus.delivered.name,
        "Package removed from Locker": TrackingStatus.delivered.name,
        # Seen in production under ScanType=Delivery and not a final delivery.
        "Transferring to Shipping Centre - please wait for further instructions": TrackingStatus.in_transit.name,
    },
    "ProofOfPickUp": {
        "__default__": TrackingStatus.picked_up.name,
        "Picked up by Purolator at": TrackingStatus.picked_up.name,
        "Received by Purolator for processing at": TrackingStatus.picked_up.name,
    },
    "Undeliverable": {
        "__default__": TrackingStatus.on_hold.name,
        "Shipment created - interim manifest received": TrackingStatus.pending.name,
        "Shipment created - final manifest received": TrackingStatus.pending.name,
        "Shipment created": TrackingStatus.pending.name,
        "Shipper created a label": TrackingStatus.pending.name,
        "Arrived at sort facility": TrackingStatus.in_transit.name,
        "Departed sort facility": TrackingStatus.in_transit.name,
        "Shipment in transit": TrackingStatus.in_transit.name,
        "Shipment redirected": TrackingStatus.in_transit.name,
        "Resolution complete - shipment redirected": TrackingStatus.in_transit.name,
        "Available for pickup for 5 business days from arrival date at the counter": TrackingStatus.ready_for_pickup.name,
        "Item Held for Pickup at Locker": TrackingStatus.ready_for_pickup.name,
        "Item available for receiver to pick up at post office": TrackingStatus.ready_for_pickup.name,
        "Receiver advised they will pick up shipment": TrackingStatus.ready_for_pickup.name,
        "Shipment available for pickup. Unable to contact customer": TrackingStatus.ready_for_pickup.name,
        "Shipment available for pickup. Unable to contact customer.": TrackingStatus.ready_for_pickup.name,
        "Receiver contacted.  Shipment available for pickup": TrackingStatus.ready_for_pickup.name,
        "Receiver contacted, no answer.  Shipment available for pickup": TrackingStatus.ready_for_pickup.name,
        "Shipper contacted.  Shipment available for pickup": TrackingStatus.ready_for_pickup.name,
        "Shipment unclaimed - to be returned to sender": TrackingStatus.return_to_sender.name,
        "Shipment undeliverable - Returned to sender": TrackingStatus.return_to_sender.name,
        "Unable to deliver - item returned to sender": TrackingStatus.return_to_sender.name,
        "Unable to deliver - item returned to shipper": TrackingStatus.return_to_sender.name,
        "Returned to sender.  Shipment no longer available for pickup": TrackingStatus.return_to_sender.name,
    },
}


# Keep both layers:
# - exact matches for audited known descriptions.
# - keyword fallback for unseen wording variants in Undeliverable events.
UNDELIVERABLE_KEYWORD_RULES: list[tuple[tuple[str, ...], str]] = [
    (
        (
            "returned to sender",
            "returned to shipper",
            "to be returned to sender",
            "returned to the shipper",
            "retourne a l'expediteur",
            "retour a l'expediteur",
            "renvoye a l'expediteur",
            "retourne a l expediteur",
            "retour a l expediteur",
            "renvoye a l expediteur",
        ),
        TrackingStatus.return_to_sender.name,
    ),
    (
        (
            "available for pickup",
            "held for pickup",
            "pickup location",
            "disponible pour le ramassage",
            "disponible pour ramassage",
            "point de ramassage",
            "point de cueillette",
            "ramassage",
            "ramasser",
        ),
        TrackingStatus.ready_for_pickup.name,
    ),
    (
        (
            "delayed",
            "delay",
            "rescheduled",
            "redelivery",
            "new delivery date",
            "missed connection",
            "mechanical",
            "weather",
            "road closure",
            "natural disaster",
            "sorting error",
            "late tender",
            "special handling",
            "hold period extended",
            "re-attempt",
            "rail delay",
            "ferry delay",
            "service disruption",
            "retard",
            "retarde",
            "retardee",
            "retardes",
            "retardees",
            "reporte",
            "reportee",
            "reportes",
            "reportees",
            "replanifie",
            "replanifiee",
            "replanifies",
            "replanifiees",
            "meteo",
            "intemperies",
            "fermeture de route",
            "catastrophe naturelle",
            "perturbation de service",
        ),
        TrackingStatus.delivery_delayed.name,
    ),
]


def normalize_tracking_description(description: typing.Optional[str]) -> str:
    normalized = re.sub(r"\s+", " ", str(description or "").strip().lower())
    normalized = normalized.replace("’", "'")
    normalized = "".join(
        c
        for c in unicodedata.normalize("NFKD", normalized)
        if not unicodedata.combining(c)
    )
    return normalized.rstrip(".")


def _normalize_tracking_status_mapping(
    raw_mapping: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    normalized_mapping: dict[str, dict[str, str]] = {}
    for event_code, description_mapping in raw_mapping.items():
        normalized_mapping[event_code] = {}
        for description, mapped_status in description_mapping.items():
            if description == "__default__":
                normalized_mapping[event_code]["__default__"] = mapped_status
                continue

            normalized_mapping[event_code][
                normalize_tracking_description(description)
            ] = mapped_status

    return normalized_mapping


NORMALIZED_PUROLATOR_TRACKING_STATUS_MAPPING = _normalize_tracking_status_mapping(
    PUROLATOR_TRACKING_STATUS_MAPPING
)


def map_tracking_status(
    event_code: typing.Optional[str],
    event_description: typing.Optional[str],
) -> str:
    code = str(event_code or "").strip()
    normalized_description = normalize_tracking_description(event_description)
    mapped_descriptions = NORMALIZED_PUROLATOR_TRACKING_STATUS_MAPPING.get(code)

    if mapped_descriptions is None:
        return TrackingStatus.unknown.name

    if normalized_description in mapped_descriptions:
        return mapped_descriptions[normalized_description]

    if code == "Undeliverable":
        for needles, status_id in UNDELIVERABLE_KEYWORD_RULES:
            if any(needle in normalized_description for needle in needles):
                return status_id

    return mapped_descriptions.get("__default__", TrackingStatus.unknown.name)


class TrackingIncidentReason(lib.Enum):
    """Maps Purolator exception codes to normalized TrackingIncidentReason."""

    # Carrier-caused issues
    carrier_damaged_parcel = ["Damaged", "Package Damaged"]
    carrier_sorting_error = ["Misrouted", "Routing Error"]
    carrier_address_not_found = ["Address Not Found", "Invalid Address"]
    carrier_parcel_lost = ["Lost", "Missing Package"]
    carrier_not_enough_time = ["Insufficient Time"]
    carrier_vehicle_issue = ["Vehicle Breakdown", "Mechanical Issue"]

    # Consignee-caused issues
    consignee_refused = ["Refused", "Delivery Refused", "Recipient Refused"]
    consignee_business_closed = ["Business Closed", "Closed"]
    consignee_not_available = ["Not Available", "Recipient Not Available"]
    consignee_not_home = ["Not Home", "No One Home", "Recipient Not Home"]
    consignee_incorrect_address = ["Incorrect Address", "Wrong Address", "Bad Address"]
    consignee_access_restricted = [
        "Access Restricted",
        "Cannot Access",
        "Restricted Access",
    ]

    # Customs-related issues
    customs_delay = ["Customs Delay", "Customs Hold", "Customs Processing"]
    customs_documentation = [
        "Customs Documentation Required",
        "Missing Customs Documents",
    ]
    customs_duties_unpaid = ["Duties Unpaid", "Customs Fees Due"]

    # Weather/Force majeure
    weather_delay = ["Weather Delay", "Weather", "Severe Weather"]
    natural_disaster = ["Natural Disaster", "Emergency"]

    # Delivery exceptions
    delivery_exception_hold = ["Hold", "Customer Hold", "Held at Depot"]
    delivery_exception_undeliverable = ["Undeliverable", "Cannot Deliver"]

    # Other issues
    unknown = []


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
                    "currency": row.get("currency", "CAD"),
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
                    "domicile": (row.get("domicile") or "").lower() == "true",
                    "international": (
                        True
                        if (row.get("international") or "").lower() == "true"
                        else None
                    ),
                    "zones": [],
                }
            country_codes = [
                c.strip() for c in row.get("country_codes", "").split(",") if c.strip()
            ]
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=(
                    int(row["transit_days"].split("-")[0])
                    if row.get("transit_days")
                    and row["transit_days"].split("-")[0].isdigit()
                    else None
                ),
                country_codes=country_codes if country_codes else None,
            )
            services_dict[karrio_service_code]["zones"].append(zone)
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
