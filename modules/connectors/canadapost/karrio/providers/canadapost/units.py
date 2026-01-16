import karrio.lib as lib

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


class TrackingStatus(lib.Enum):
    """Carrier tracking status mapping"""

    delivered = [
        "1408",
        "1409",
        "1421",
        "1422",
        "1423",
        "1424",
        "1425",
        "1426",
        "1427",
        "1428",
        "1429",
        "1430",
        "1431",
        "1432",
        "1433",
        "1434",
        "1441",
        "1442",
        "1496",
        "1497",
        "1498",
        "1499",
    ]
    in_transit = [""]
    picked_up = [
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "1400",
        "1401",
        "1402",
        "1403",
        "1404",
        "1405",
    ]
    on_hold = [
        "117",
        "120",
        "121",
        "125",
        "127",
        "810",
        "1411",
        "1414",
        "1443",
        "1484",
        "1487",
        "1494",
        "2411",
        "2414",
        "4700",
    ]
    ready_for_pickup = [
        "118",
        "156",
        "1407",
        "1410",
        "1435",
        "1436",
        "1437",
        "1438",
        "1479",
        "1488",
        "1701",
        "2410",
    ]
    delivery_failed = [
        "150",
        "154",
        "167",
        "168",
        "169",
        "167",
        "168",
        "169",
        "179",
        "181",
        "182",
        "183",
        "184",
        "190",
        "1100",
        "1415",
        "1416",
        "1417",
        "1418",
        "1419",
        "1420",
        "1450",
        "1481",
        "1482",
        "1483",
        "1491",
        "1492",
        "1493",
        "2600",
        "2802",
        "3001",
        "4650",
    ]
    delivery_delayed = [
        "159",
        "160",
        "161",
        "162",
        "163",
        "172",
        "173",
        "2412",
    ]
    out_for_delivery = ["174", "500"]


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
