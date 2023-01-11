import karrio.core.units as units
import karrio.core.utils as utils

PRESET_DEFAULTS = dict(
    dimension_unit="CM",
    weight_unit="KG",
)

MeasurementOptions = units.MeasurementOptionsType(
    quant=0.1,
    min_kg=0.01,
    min_in=0.01,
)


class PackagePresets(utils.Flag):
    """
    Note that dimensions are in CM and weight in KG
    """

    canadapost_mailing_box = units.PackagePreset(
        **dict(width=10.2, height=15.2, length=1.0), **PRESET_DEFAULTS
    )
    canadapost_extra_small_mailing_box = units.PackagePreset(
        **dict(width=14.0, height=14.0, length=14.0), **PRESET_DEFAULTS
    )
    canadapost_small_mailing_box = units.PackagePreset(
        **dict(width=28.6, height=22.9, length=6.4), **PRESET_DEFAULTS
    )
    canadapost_medium_mailing_box = units.PackagePreset(
        **dict(width=31.0, height=23.5, length=13.3), **PRESET_DEFAULTS
    )
    canadapost_large_mailing_box = units.PackagePreset(
        **dict(width=38.1, height=30.5, length=9.5), **PRESET_DEFAULTS
    )
    canadapost_extra_large_mailing_box = units.PackagePreset(
        **dict(width=40.0, height=30.5, length=21.6), **PRESET_DEFAULTS
    )
    canadapost_corrugated_small_box = units.PackagePreset(
        **dict(width=42.0, height=32.0, length=32.0), **PRESET_DEFAULTS
    )
    canadapost_corrugated_medium_box = units.PackagePreset(
        **dict(width=46.0, height=38.0, length=32.0), **PRESET_DEFAULTS
    )
    canadapost_corrugated_large_box = units.PackagePreset(
        **dict(width=46.0, height=46.0, length=40.6), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_certified_envelope = units.PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_national_large_envelope = units.PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_small_envelope = units.PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_large_envelope = units.PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5), **PRESET_DEFAULTS
    )


class LabelType(utils.Enum):
    PDF_4x6 = ("PDF", "4x6")
    PDF_8_5x11 = ("PDF", "8.5x11")
    ZPL_4x6 = ("ZPL", "4x6")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    ZPL = ZPL_4x6


class PaymentType(utils.Flag):
    account = "Account"
    card = "CreditCard"
    supplier_account = "SupplierAccount"

    sender = account
    recipient = account
    third_party = supplier_account
    credit_card = card


class ServiceType(utils.Enum):
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


class ShippingOption(utils.Enum):
    canadapost_signature = utils.OptionEnum("SO", bool)
    canadapost_coverage = utils.OptionEnum("COV", float)
    canadapost_collect_on_delivery = utils.OptionEnum("COD", float)
    canadapost_proof_of_age_required_18 = utils.OptionEnum("PA18", bool)
    canadapost_proof_of_age_required_19 = utils.OptionEnum("PA19", bool)
    canadapost_card_for_pickup = utils.OptionEnum("HFP", bool)
    canadapost_do_not_safe_drop = utils.OptionEnum("DNS", bool)
    canadapost_leave_at_door = utils.OptionEnum("LAD", bool)
    canadapost_deliver_to_post_office = utils.OptionEnum("D2PO", bool)
    canadapost_return_at_senders_expense = utils.OptionEnum("RASE", bool)
    canadapost_return_to_sender = utils.OptionEnum("RTS", bool)
    canadapost_abandon = utils.OptionEnum("ABAN", bool)

    """ Custom Option """
    canadapost_cost_center = utils.OptionEnum("cost-centre")

    """ Unified Option type mapping """
    insurance = canadapost_coverage
    cash_on_delivery = canadapost_collect_on_delivery
    signature_confirmation = canadapost_signature


INTERNATIONAL_NON_DELIVERY_OPTION = [
    ShippingOption.canadapost_return_at_senders_expense.name,
    ShippingOption.canadapost_return_to_sender.name,
    ShippingOption.canadapost_abandon.name,
]

CUSTOM_OPTIONS = [
    ShippingOption.canadapost_cost_center.name,
]

TRACKING_DELIVERED_EVENT_CODES = [
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


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
    is_international: bool = False,
) -> units.ShippingOptions:
    _options = options.copy()

    # Apply default non delivery options for if international.
    no_international_option_specified: bool = not any(
        key in _options for key in INTERNATIONAL_NON_DELIVERY_OPTION
    )

    if is_international and no_international_option_specified:
        _options.update({ShippingOption.canadapost_return_at_senders_expense.name: True})

    # Apply package options if specified.
    if package_options is not None:
        _options.update(package_options.content)

    # Define carrier option filter.
    def items_filter(key: str) -> bool:
        return key in ShippingOption and key not in CUSTOM_OPTIONS  # type:ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)
