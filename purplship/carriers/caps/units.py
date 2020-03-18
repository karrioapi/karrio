from enum import Enum


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


class OptionCode(Enum):
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
