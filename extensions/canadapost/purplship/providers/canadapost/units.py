from purplship.core.utils import Enum, Flag, Spec
from purplship.core.units import PackagePreset

PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")


class PackagePresets(Flag):
    """
    Note that dimensions are in CM and weight in KG
    """
    canadapost_mailing_box = PackagePreset(
        **dict(width=10.2, height=15.2, length=1.0),
        **PRESET_DEFAULTS
    )
    canadapost_extra_small_mailing_box = PackagePreset(
        **dict(width=14.0, height=14.0, length=14.0),
        **PRESET_DEFAULTS
    )
    canadapost_small_mailing_box = PackagePreset(
        **dict(width=28.6, height=22.9, length=6.4),
        **PRESET_DEFAULTS
    )
    canadapost_medium_mailing_box = PackagePreset(
        **dict(width=31.0, height=23.5, length=13.3),
        **PRESET_DEFAULTS
    )
    canadapost_large_mailing_box = PackagePreset(
        **dict(width=38.1, height=30.5, length=9.5),
        **PRESET_DEFAULTS
    )
    canadapost_extra_large_mailing_box = PackagePreset(
        **dict(width=40.0, height=30.5, length=21.6),
        **PRESET_DEFAULTS
    )
    canadapost_corrugated_small_box = PackagePreset(
        **dict(width=42.0, height=32.0, length=32.0),
        **PRESET_DEFAULTS
    )
    canadapost_corrugated_medium_box = PackagePreset(
        **dict(width=46.0, height=38.0, length=32.0),
        **PRESET_DEFAULTS
    )
    canadapost_corrugated_large_box = PackagePreset(
        **dict(width=46.0, height=46.0, length=40.6),
        **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_certified_envelope = PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5),
        **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_national_large_envelope = PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5),
        **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_small_envelope = PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5),
        **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_large_envelope = PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5),
        **PRESET_DEFAULTS
    )


class MeasurementOptions(Enum):
    quant = 0.1


class LabelType(Enum):
    PDF_4x6 = ("PDF", "4x6")
    PDF_8_5x11 = ("PDF", "8.5x11")
    ZPL_4x6 = ("ZPL", "4x6")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    ZPL = ZPL_4x6


class PaymentType(Flag):
    account = "Account"
    card = "CreditCard"
    supplier_account = "SupplierAccount"

    sender = account
    recipient = account
    third_party = supplier_account
    credit_card = card


class ServiceType(Enum):
    canadapost_regular_parcel = "DOM.RP"
    canadapost_expedited_parcel = "DOM.EP"
    canadapost_xpresspost = "DOM.XP"
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


class OptionCode(Enum):
    canadapost_signature = Spec.asKey("SO")
    canadapost_coverage = Spec.asKeyVal("COV", float)
    canadapost_collect_on_delivery = Spec.asKeyVal("COD", float)
    canadapost_proof_of_age_required_18 = Spec.asKey("PA18")
    canadapost_proof_of_age_required_19 = Spec.asKey("PA19")
    canadapost_card_for_pickup = Spec.asKey("HFP")
    canadapost_do_not_safe_drop = Spec.asKey("DNS")
    canadapost_leave_at_door = Spec.asKey("LAD")
    canadapost_deliver_to_post_office = Spec.asKey("D2PO")
    canadapost_return_at_senders_expense = Spec.asKey("RASE")
    canadapost_return_to_sender = Spec.asKey("RTS")
    canadapost_abandon = Spec.asKey("ABAN")

    """ Unified Option type mapping """
    insurance = canadapost_coverage
    cash_on_delivery = canadapost_collect_on_delivery
    signature_confirmation = canadapost_signature


INTERNATIONAL_NON_DELIVERY_OPTION = [
    OptionCode.canadapost_return_at_senders_expense.name,
    OptionCode.canadapost_return_to_sender.name,
    OptionCode.canadapost_abandon.name,
]
