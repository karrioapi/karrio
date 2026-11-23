import csv
import pathlib
import karrio.lib as lib
import karrio.core.models as models

PRESET_DEFAULTS = dict(
    dimension_unit="CM",
    weight_unit="KG",
)

MeasurementOptions = lib.units.MeasurementOptionsType(
    quant=0.1,
    min_kg=0.01,
    min_in=0.01,
)


class PackagePresets(lib.Enum):
    """
    Note that dimensions are in CM and weight in KG
    """

    canadapost_mailing_box = lib.units.PackagePreset(
        **dict(width=10.2, height=15.2, length=1.0), **PRESET_DEFAULTS
    )
    canadapost_extra_small_mailing_box = lib.units.PackagePreset(
        **dict(width=14.0, height=14.0, length=14.0), **PRESET_DEFAULTS
    )
    canadapost_small_mailing_box = lib.units.PackagePreset(
        **dict(width=28.6, height=22.9, length=6.4), **PRESET_DEFAULTS
    )
    canadapost_medium_mailing_box = lib.units.PackagePreset(
        **dict(width=31.0, height=23.5, length=13.3), **PRESET_DEFAULTS
    )
    canadapost_large_mailing_box = lib.units.PackagePreset(
        **dict(width=38.1, height=30.5, length=9.5), **PRESET_DEFAULTS
    )
    canadapost_extra_large_mailing_box = lib.units.PackagePreset(
        **dict(width=40.0, height=30.5, length=21.6), **PRESET_DEFAULTS
    )
    canadapost_corrugated_small_box = lib.units.PackagePreset(
        **dict(width=42.0, height=32.0, length=32.0), **PRESET_DEFAULTS
    )
    canadapost_corrugated_medium_box = lib.units.PackagePreset(
        **dict(width=46.0, height=38.0, length=32.0), **PRESET_DEFAULTS
    )
    canadapost_corrugated_large_box = lib.units.PackagePreset(
        **dict(width=46.0, height=46.0, length=40.6), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_certified_envelope = lib.units.PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_national_large_envelope = lib.units.PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_small_envelope = lib.units.PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_large_envelope = lib.units.PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5), **PRESET_DEFAULTS
    )


class LabelType(lib.Enum):
    PDF_4x6 = ("PDF", "4x6")
    PDF_8_5x11 = ("PDF", "8.5x11")
    ZPL_4x6 = ("ZPL", "4x6")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    ZPL = ZPL_4x6


class PaymentType(lib.StrEnum):
    account = "Account"
    card = "CreditCard"
    supplier_account = "SupplierAccount"

    sender = account
    recipient = account
    third_party = supplier_account
    credit_card = card


class ConnectionConfig(lib.Enum):
    cost_center = lib.OptionEnum("cost_center")
    label_type = lib.OptionEnum("label_type", LabelType)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    transmit_shipment_by_default = lib.OptionEnum("transmit_shipment_by_default", bool)


class ServiceType(lib.Enum):
    canadapost_regular_parcel = "DOM.RP"
    canadapost_expedited_parcel = "DOM.EP"
    canadapost_xpresspost = "DOM.XP"
    canadapost_xpresspost_certified = "DOM.XP.CERT"
    canadapost_priority = "DOM.PC"
    canadapost_library_books = "DOM.LIB"
    canadapost_expedited_parcel_usa = "USA.EP"
    canadapost_priority_worldwide_envelope_usa = "USA.PW.ENV"
    canadapost_priority_worldwide_pak_usa = "USA.PW.PAK"
    canadapost_priority_worldwide_parcel_usa = "USA.PW.PARCEL"
    canadapost_small_packet_usa_air = "USA.SP.AIR"
    canadapost_tracked_packet_usa = "USA.TP"
    canadapost_tracked_packet_usa_lvm = "USA.TP.LVM"
    canadapost_xpresspost_usa = "USA.XP"
    canadapost_xpresspost_international = "INT.XP"
    canadapost_international_parcel_air = "INT.IP.AIR"
    canadapost_international_parcel_surface = "INT.IP.SURF"
    canadapost_priority_worldwide_envelope_intl = "INT.PW.ENV"
    canadapost_priority_worldwide_pak_intl = "INT.PW.PAK"
    canadapost_priority_worldwide_parcel_intl = "INT.PW.PARCEL"
    canadapost_small_packet_international_air = "INT.SP.AIR"
    canadapost_small_packet_international_surface = "INT.SP.SURF"
    canadapost_tracked_packet_international = "INT.TP"


class ShippingOption(lib.Enum):
    canadapost_signature = lib.OptionEnum("SO", bool, meta=dict(category="SIGNATURE"))
    canadapost_coverage = lib.OptionEnum("COV", float, meta=dict(category="INSURANCE"))
    canadapost_collect_on_delivery = lib.OptionEnum("COD", float, meta=dict(category="COD"))
    canadapost_proof_of_age_required_18 = lib.OptionEnum("PA18", bool, meta=dict(category="SIGNATURE"))
    canadapost_proof_of_age_required_19 = lib.OptionEnum("PA19", bool, meta=dict(category="SIGNATURE"))
    canadapost_card_for_pickup = lib.OptionEnum("HFP", bool, meta=dict(category="PUDO"))
    canadapost_do_not_safe_drop = lib.OptionEnum("DNS", bool, meta=dict(category="DELIVERY_OPTIONS"))
    canadapost_leave_at_door = lib.OptionEnum("LAD", bool, meta=dict(category="DELIVERY_OPTIONS"))
    canadapost_deliver_to_post_office = lib.OptionEnum("D2PO", bool, meta=dict(category="PUDO"))
    canadapost_return_at_senders_expense = lib.OptionEnum("RASE", bool, meta=dict(category="RETURN"))
    canadapost_return_to_sender = lib.OptionEnum("RTS", bool, meta=dict(category="RETURN"))
    canadapost_abandon = lib.OptionEnum("ABAN", bool)

    """ Custom Option """
    canadapost_cost_center = lib.OptionEnum("cost-centre")
    canadapost_submit_shipment = lib.OptionEnum("transmit-shipment", bool)

    """ Unified Option type mapping """
    insurance = canadapost_coverage
    cash_on_delivery = canadapost_collect_on_delivery
    signature_confirmation = canadapost_signature


def shipping_options_initializer(
    options: dict,
    package_options: lib.units.ShippingOptions = None,
    is_international: bool = False,
) -> lib.units.ShippingOptions:
    _options = options.copy()

    # Apply default non delivery options for if international.
    no_international_option_specified: bool = not any(
        key in _options for key in INTERNATIONAL_NON_DELIVERY_OPTION
    )

    if is_international and no_international_option_specified:
        _options.update(
            {ShippingOption.canadapost_return_at_senders_expense.name: True}
        )

    # Apply package options if specified.
    if package_options is not None:
        _options.update(package_options.content)

    # Define carrier option filter.
    def items_filter(key: str) -> bool:
        return key in ShippingOption and key not in CUSTOM_OPTIONS  # type:ignore

    return lib.units.ShippingOptions(
        _options, ShippingOption, items_filter=items_filter
    )


# Canonical Canada Post event mapping used for tracker status normalization.
# Sources:
# - Official Canada Post message/event code table:
#   https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/messagescodetables.jsf
# - Live event payloads observed in production integrations, including padded IDs like `0100`.
#
# Canada Post event descriptions pass through on TrackingEvent.description.
# Status normalization stays deterministic by mapping only the event code.
TRACKING_STATUS_MAPPING = {
    "100": {"__default__": "picked_up"},
    "102": {"__default__": "in_transit"},
    "104": {"__default__": "picked_up"},
    "105": {"__default__": "picked_up"},
    "106": {"__default__": "in_transit"},
    "107": {"__default__": "picked_up"},
    "1100": {"__default__": "on_hold"},
    "113": {"__default__": "in_transit"},
    "114": {"__default__": "in_transit"},
    "115": {"__default__": "in_transit"},
    "116": {"__default__": "in_transit"},
    "117": {"__default__": "in_transit"},
    "118": {"__default__": "in_transit"},
    "120": {"__default__": "in_transit"},
    "1200": {"__default__": "on_hold"},
    "1203": {"__default__": "in_transit"},
    "121": {"__default__": "in_transit"},
    "1210": {"__default__": "in_transit"},
    "1214": {"__default__": "in_transit"},
    "1215": {"__default__": "in_transit"},
    "1216": {"__default__": "in_transit"},
    "1220": {"__default__": "in_transit"},
    "1221": {"__default__": "in_transit"},
    "1223": {"__default__": "in_transit"},
    "1224": {"__default__": "in_transit"},
    "1225": {"__default__": "in_transit"},
    "1230": {"__default__": "in_transit"},
    "1232": {"__default__": "in_transit"},
    "1234": {"__default__": "in_transit"},
    "1240": {"__default__": "picked_up"},
    "1241": {"__default__": "in_transit"},
    "1244": {"__default__": "picked_up"},
    "1245": {"__default__": "on_hold"},
    "127": {"__default__": "in_transit"},
    "130": {"__default__": "in_transit"},
    "1300": {"__default__": "pending"},
    "1301": {"__default__": "pending"},
    "1302": {"__default__": "pending"},
    "1303": {"__default__": "pending"},
    "1405": {"__default__": "delivered"},
    "1406": {"__default__": "delivered"},
    "1407": {"__default__": "ready_for_pickup"},
    "1408": {"__default__": "delivered"},
    "1409": {"__default__": "delivered"},
    "1410": {"__default__": "delivery_delayed"},
    "1411": {"__default__": "on_hold"},
    "1412": {"__default__": "on_hold"},
    "1414": {"__default__": "delivery_delayed"},
    "1415": {"__default__": "return_to_sender"},
    "1416": {"__default__": "return_to_sender"},
    "1417": {"__default__": "return_to_sender"},
    "1418": {"__default__": "return_to_sender"},
    "1419": {"__default__": "return_to_sender"},
    "1420": {"__default__": "return_to_sender"},
    "1421": {"__default__": "delivered"},
    "1422": {"__default__": "delivered"},
    "1423": {"__default__": "delivered"},
    "1424": {"__default__": "delivered"},
    "1425": {"__default__": "delivered"},
    "1426": {"__default__": "delivered"},
    "1427": {"__default__": "delivered"},
    "1428": {"__default__": "delivered"},
    "1429": {"__default__": "delivered"},
    "1430": {"__default__": "delivered"},
    "1431": {"__default__": "delivered"},
    "1432": {"__default__": "delivered"},
    "1433": {"__default__": "delivered"},
    "1434": {"__default__": "delivered"},
    "1435": {"__default__": "ready_for_pickup"},
    "1436": {"__default__": "ready_for_pickup"},
    "1437": {"__default__": "ready_for_pickup"},
    "1438": {"__default__": "ready_for_pickup"},
    "1441": {"__default__": "delivered"},
    "1442": {"__default__": "delivered"},
    "1443": {"__default__": "on_hold"},
    "1444": {"__default__": "on_hold"},
    "1450": {"__default__": "on_hold"},
    "1461": {"__default__": "delivered"},
    "1462": {"__default__": "delivered"},
    "1463": {"__default__": "delivered"},
    "1465": {"__default__": "delivered"},
    "1466": {"__default__": "delivered"},
    "1467": {"__default__": "delivered"},
    "1468": {"__default__": "delivered"},
    "1469": {"__default__": "delivered"},
    "1471": {"__default__": "delivered"},
    "1472": {"__default__": "delivered"},
    "1473": {"__default__": "delivered"},
    "1475": {"__default__": "delivered"},
    "1476": {"__default__": "delivered"},
    "1479": {"__default__": "ready_for_pickup"},
    "1480": {"__default__": "out_for_delivery"},
    "1481": {"__default__": "return_to_sender"},
    "1482": {"__default__": "return_to_sender"},
    "1483": {"__default__": "on_hold"},
    "1484": {"__default__": "on_hold"},
    "1487": {"__default__": "on_hold"},
    "1488": {"__default__": "ready_for_pickup"},
    "1490": {"__default__": "out_for_delivery"},
    "1491": {"__default__": "return_to_sender"},
    "1492": {"__default__": "return_to_sender"},
    "1493": {"__default__": "on_hold"},
    "1494": {"__default__": "on_hold"},
    "1495": {"__default__": "return_to_sender"},
    "1496": {"__default__": "delivered"},
    "1498": {"__default__": "delivered"},
    "150": {"__default__": "in_transit"},
    "152": {"__default__": "in_transit"},
    "156": {"__default__": "on_hold"},
    "159": {"__default__": "on_hold"},
    "160": {"__default__": "on_hold"},
    "161": {"__default__": "on_hold"},
    "162": {"__default__": "on_hold"},
    "163": {"__default__": "on_hold"},
    "167": {"__default__": "return_to_sender"},
    "168": {"__default__": "return_to_sender"},
    "169": {"__default__": "return_to_sender"},
    "170": {"__default__": "picked_up"},
    "1701": {"__default__": "ready_for_pickup"},
    "1703": {"__default__": "in_transit"},
    "1705": {"__default__": "ready_for_pickup"},
    "171": {"__default__": "in_transit"},
    "172": {"__default__": "on_hold"},
    "173": {"__default__": "on_hold"},
    "174": {"__default__": "out_for_delivery"},
    "175": {"__default__": "in_transit"},
    "179": {"__default__": "in_transit"},
    "181": {"__default__": "return_to_sender"},
    "182": {"__default__": "return_to_sender"},
    "183": {"__default__": "return_to_sender"},
    "184": {"__default__": "return_to_sender"},
    "190": {"__default__": "in_transit"},
    "198": {"__default__": "in_transit"},
    "20": {"__default__": "delivered"},
    "2001": {"__default__": "delivered"},
    "21": {"__default__": "delivered"},
    "2101": {"__default__": "in_transit"},
    "2300": {"__default__": "picked_up"},
    "2407": {"__default__": "ready_for_pickup"},
    "2410": {"__default__": "delivery_delayed"},
    "2411": {"__default__": "on_hold"},
    "2412": {"__default__": "on_hold"},
    "2414": {"__default__": "delivery_delayed"},
    "2500": {"__default__": "picked_up"},
    "2501": {"__default__": "picked_up"},
    "2600": {"__default__": "return_to_sender"},
    "2601": {"__default__": "return_to_sender"},
    "2802": {"__default__": "return_to_sender"},
    "3000": {"__default__": "pending"},
    "3001": {"__default__": "return_to_sender"},
    "3002": {"__default__": "pending"},
    "400": {"__default__": "in_transit"},
    "4000": {"__default__": "in_transit"},
    "405": {"__default__": "in_transit"},
    "410": {"__default__": "in_transit"},
    "4100": {"__default__": "in_transit"},
    "4202": {"__default__": "in_transit"},
    "4310": {"__default__": "in_transit"},
    "4311": {"__default__": "in_transit"},
    "4330": {"__default__": "in_transit"},
    "4400": {"__default__": "in_transit"},
    "4450": {"__default__": "in_transit"},
    "4500": {"__default__": "in_transit"},
    "4550": {"__default__": "in_transit"},
    "4600": {"__default__": "in_transit"},
    "4650": {"__default__": "return_to_sender"},
    "4700": {"__default__": "on_hold"},
    "4900": {"__default__": "in_transit"},
    "4950": {"__default__": "in_transit"},
    "500": {"__default__": "out_for_delivery"},
    "5201": {"__default__": "on_hold"},
    "610": {"__default__": "in_transit"},
    "611": {"__default__": "in_transit"},
    "612": {"__default__": "in_transit"},
    "613": {"__default__": "in_transit"},
    "614": {"__default__": "in_transit"},
    "615": {"__default__": "in_transit"},
    "616": {"__default__": "in_transit"},
    "617": {"__default__": "in_transit"},
    "618": {"__default__": "in_transit"},
    "619": {"__default__": "in_transit"},
    "620": {"__default__": "in_transit"},
    "621": {"__default__": "delivery_delayed"},
    "622": {"__default__": "delivery_delayed"},
    "623": {"__default__": "delivery_delayed"},
    "624": {"__default__": "on_hold"},
    "625": {"__default__": "delivery_delayed"},
    "626": {"__default__": "on_hold"},
    "627": {"__default__": "delivery_delayed"},
    "628": {"__default__": "delivery_delayed"},
    "629": {"__default__": "in_transit"},
    "630": {"__default__": "on_hold"},
    "700": {"__default__": "in_transit"},
    "701": {"__default__": "in_transit"},
    "710": {"__default__": "in_transit"},
    "800": {"__default__": "in_transit"},
    "804": {"__default__": "in_transit"},
    "810": {"__default__": "in_transit"},
    "815": {"__default__": "in_transit"},
    "8901": {"__default__": "in_transit"},
    "900": {"__default__": "in_transit"},
    "910": {"__default__": "in_transit"},
}


def normalize_tracking_event_identifier(event_identifier):
    raw = str(event_identifier or "").strip()
    if raw.isdigit():
        return str(int(raw))
    return raw


def map_tracking_status(event_identifier, event_description=None):
    normalized_event_id = normalize_tracking_event_identifier(event_identifier)
    description_mapping = TRACKING_STATUS_MAPPING.get(normalized_event_id)

    if not description_mapping:
        return "unknown"

    return description_mapping.get("__default__", "unknown")


def map_tracking_incident_reason(event_identifier):
    normalized_event_id = normalize_tracking_event_identifier(event_identifier)
    return next(
        (
            reason.name
            for reason in list(TrackingIncidentReason)
            if normalized_event_id in reason.value
        ),
        None,
    )


class TrackingIncidentReason(lib.Enum):
    """Maps Canada Post exception codes to normalized TrackingIncidentReason.

    Based on Canada Post tracking event codes.
    """
    # Carrier-caused issues
    carrier_damaged_parcel = ["119", "142", "143", "144", "145", "146", "147", "148", "149"]
    carrier_sorting_error = ["128", "129", "130", "131", "132", "133"]
    carrier_address_not_found = ["122", "123", "1413", "1440", "1485", "1486", "1489", "1490"]
    carrier_parcel_lost = ["124", "126", "151", "152", "153"]
    carrier_not_enough_time = ["155", "157", "158"]
    carrier_vehicle_issue = ["134", "135", "136", "137", "138"]

    # Consignee-caused issues
    consignee_refused = ["150", "1415", "1416"]
    consignee_business_closed = ["179", "181", "182"]
    consignee_not_available = ["183", "184", "190", "1418", "1419", "1420"]
    consignee_not_home = ["167", "168", "169", "1417"]
    consignee_incorrect_address = ["172", "173", "1482", "1483"]
    consignee_access_restricted = ["154", "180", "185", "186", "187", "188", "189"]

    # Customs-related issues
    customs_delay = ["810", "1443", "1484", "1487"]
    customs_documentation = ["117", "120", "121"]
    customs_duties_unpaid = ["125", "127", "1494"]

    # Weather/Force majeure
    weather_delay = ["159", "160", "161", "162", "163"]
    natural_disaster = ["164", "165", "166"]

    # Other issues
    unknown = []


INTERNATIONAL_NON_DELIVERY_OPTION = [
    ShippingOption.canadapost_return_at_senders_expense.name,
    ShippingOption.canadapost_return_to_sender.name,
    ShippingOption.canadapost_abandon.name,
]

CUSTOM_OPTIONS = [
    ShippingOption.canadapost_cost_center.name,
    ShippingOption.canadapost_submit_shipment.name,
]


def load_services_from_csv() -> list:
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"
    if not csv_path.exists():
        return []
    services_dict: dict[str, dict] = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            karrio_service_code = ServiceType.map(service_code).name_or_key
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": row["service_name"],
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "CAD"),
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
