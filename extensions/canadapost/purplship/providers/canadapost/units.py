from purplship.core.utils import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "CM"
    weight_unit: str = "KG"


class PackagePresets(Flag):
    """
    Note that dimensions are in CM and weight in KG
    """
    canadapost_mailing_box = PackagePreset(width=10.2, height=15.2, length=1.0)
    canadapost_extra_small_mailing_box = PackagePreset(
        width=14.0, height=14.0, length=14.0
    )
    canadapost_small_mailing_box = PackagePreset(width=28.6, height=22.9, length=6.4)
    canadapost_medium_mailing_box = PackagePreset(width=31.0, height=23.5, length=13.3)
    canadapost_large_mailing_box = PackagePreset(width=38.1, height=30.5, length=9.5)
    canadapost_extra_large_mailing_box = PackagePreset(
        width=40.0, height=30.5, length=21.6
    )
    canadapost_corrugated_small_box = PackagePreset(
        width=42.0, height=32.0, length=32.0
    )
    canadapost_corrugated_medium_box = PackagePreset(
        width=46.0, height=38.0, length=32.0
    )
    canadapost_corrugated_large_box = PackagePreset(
        width=46.0, height=46.0, length=40.6
    )
    canadapost_xexpresspost_certified_envelope = PackagePreset(
        width=26.0, height=15.9, weight=0.5, length=1.5
    )
    canadapost_xexpresspost_national_large_envelope = PackagePreset(
        width=40.0, height=29.2, weight=1.36, length=1.5
    )
    canadapost_xexpresspost_regional_small_envelope = PackagePreset(
        width=26.0, height=15.9, weight=0.5, length=1.5
    )
    canadapost_xexpresspost_regional_large_envelope = PackagePreset(
        width=40.0, height=29.2, weight=1.36, length=1.5
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


INTERNATIONAL_NON_DELIVERY_OPTION = [
    'canadapost_return_at_senders_expense',
    'canadapost_return_to_sender',
    'canadapost_abandon'
]


class OptionCode(Flag):
    canadapost_signature = "SO"
    canadapost_coverage = "COV"
    canadapost_collect_on_delivery = "COD"
    canadapost_proof_of_age_required_18 = "PA18"
    canadapost_proof_of_age_required_19 = "PA19"
    canadapost_card_for_pickup = "HFP"
    canadapost_do_not_safe_drop = "DNS"
    canadapost_leave_at_door = "LAD"
    canadapost_deliver_to_post_office = "D2PO"
    canadapost_return_at_senders_expense = "RASE"
    canadapost_return_to_sender = "RTS"
    canadapost_abandon = "ABAN"

    """ Unified Option type mapping """
    insurance = canadapost_coverage
    cash_on_delivery = canadapost_collect_on_delivery
    signature_confirmation = canadapost_signature
