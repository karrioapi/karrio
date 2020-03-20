import attr
from enum import Enum, Flag


@attr.s(auto_attribs=True)
class Template:
    width: float  # CM
    height: float  # CM
    length: float = None  # CM
    weight: float = None  # KG
    thickness: float = None  # CM


class PackageTemplate(Flag):
    caps_mailing_box = Template(width=10.2, height=15.2)
    caps_extra_small_mailing_box = Template(width=14.0, height=14.0, length=14.0)
    caps_small_mailing_box = Template(width=28.6, height=22.9, length=6.4)
    caps_medium_mailing_box = Template(width=31.0, height=23.5, length=13.3)
    caps_large_mailing_box = Template(width=38.1, height=30.5, length=9.5)
    caps_extra_large_mailing_box = Template(width=40.0, height=30.5, length=21.6)
    caps_corrugated_small_box = Template(width=42.0, height=32.0, length=32.0)
    caps_corrugated_medium_box = Template(width=46.0, height=38.0, length=32.0)
    caps_corrugated_large_box = Template(width=46.0, height=46.0, length=40.6)
    caps_xexpresspost_certified_envelope = Template(width=26.0, height=15.9, weight=0.5, thickness=1.5)
    caps_xexpresspost_national_large_envelope = Template(width=40.0, height=29.2, weight=1.36, thickness=1.5)
    caps_xexpresspost_regional_small_envelope = Template(width=26.0, height=15.9, weight=0.5, thickness=1.5)
    caps_xexpresspost_regional_large_envelope = Template(width=40.0, height=29.2, weight=1.36, thickness=1.5)


class PrinterType(Enum):
    regular = '8.5x11'
    thermal = '4x6'


class LablelEncoding(Enum):
    pdf = 'PDF'
    zpl = 'ZPL'


class ServiceType(Enum):
    caps_regular_parcel = "DOM.RP"
    caps_expedited_parcel = "DOM.EP"
    caps_xpresspost = "DOM.XP"
    caps_priority = "DOM.PC"
    caps_library_books = "DOM.LIB"
    caps_expedited_parcel_usa = "USA.EP"
    caps_priority_worldwide_envelope_usa = "USA.PW.ENV"
    caps_priority_worldwide_pak_usa = "USA.PW.PAK"
    caps_priority_worldwide_parcel_usa = "USA.PW.PARCEL"
    caps_small_packet_usa_air = "USA.SP.AIR"
    caps_tracked_packet_usa = "USA.TP"
    caps_tracked_packet_usa_lvm = "USA.TP.LVM"
    caps_xpresspost_usa = "USA.XP"
    caps_xpresspost_international = "INT.XP"
    caps_international_parcel_air = "INT.IP.AIR"
    caps_international_parcel_surface = "INT.IP.SURF"
    caps_priority_worldwide_envelope_intl = "INT.PW.ENV"
    caps_priority_worldwide_pak_intl = "INT.PW.PAK"
    caps_priority_worldwide_parcel_intl = "INT.PW.PARCEL"
    caps_small_packet_international_air = "INT.SP.AIR"
    caps_small_packet_international_surface = "INT.SP.SURF"
    caps_tracked_packet_international = "INT.TP"


class OptionCode(Flag):
    caps_signature = "SO"
    caps_coverage = "COV"
    caps_collect_on_delivery = "COD"
    caps_proof_of_age_required_18 = "PA18"
    caps_proof_of_age_required_19 = "PA19"
    caps_card_for_pickup = "HFP"
    caps_do_not_safe_drop = "DNS"
    caps_leave_at_door = "LAD"
    caps_deliver_to_post_office = "D2PO"
    caps_return_at_senders_expense = "RASE"
    caps_return_to_sender = "RTS"
    caps_abandon = "ABAN"

    """ Unified Option type mapping """
    insurance = caps_coverage
    cash_on_delivery = caps_collect_on_delivery
