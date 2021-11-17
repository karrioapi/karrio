from purplship.core.utils import Enum, Flag, Spec


class LabelType(Flag):
    BLP_LABEL = "BLP"
    LBLP_LABEL_A4_PDF = "LBLP"
    ZBLP_LABEL_ZPL = "ZBLP"

    """ Unified Label type mapping """
    PDF = LBLP_LABEL_A4_PDF
    ZPL = ZBLP_LABEL_ZPL


class PaymentType(Flag):
    shipper = "SHIPPER"
    receiver = "RECEIVER"
    user = "USER"

    """ Unified Payment type mapping """
    sender = shipper
    recipient = receiver
    third_party = user


class PackagingType(Flag):
    dhl_parcel_pl_envelope = "ENVELOPE"
    dhl_parcel_pl_package = "PACKAGE"
    dhl_parcel_pl_pallet = "PALLET"

    """ Unified Packaging type mapping """
    envelope = dhl_parcel_pl_envelope
    pak = dhl_parcel_pl_package
    tube = dhl_parcel_pl_package
    pallet = dhl_parcel_pl_pallet
    small_box = dhl_parcel_pl_package
    medium_box = dhl_parcel_pl_package
    large_box = dhl_parcel_pl_package
    your_packaging = dhl_parcel_pl_package


class Service(Enum):
    dhl_parcel_pl_premium = "PR"
    dhl_parcel_pl_polska = "AH"
    dhl_parcel_pl_09 = "09"
    dhl_parcel_pl_12 = "12"
    dhl_parcel_pl_connect = "EK"
    dhl_parcel_pl_international = "PI"


class Option(Flag):
    dhl_parcel_pl_delivery_in_18_22_hours = Spec.asKey("1722")
    dhl_parcel_pl_delivery_on_saturday = Spec.asKey("SATURDAY")
    dhl_parcel_pl_pickup_on_staturday = Spec.asKey("NAD_SOBOTA")
    dhl_parcel_pl_insuration = Spec.asKeyVal("UBEZP")
    dhl_parcel_pl_collect_on_delivery = Spec.asKeyVal("COD")
    dhl_parcel_pl_information_to_receiver = Spec.asKey("PDI")
    dhl_parcel_pl_return_of_document = Spec.asKey("ROD")
    dhl_parcel_pl_proof_of_delivery = Spec.asKey("POD")
    dhl_parcel_pl_delivery_to_neighbour = Spec.asKey("SAS")
    dhl_parcel_pl_self_collect = Spec.asKey("ODB")

    """ Unified Option type mapping """
    cash_on_delivery = dhl_parcel_pl_collect_on_delivery
    insurance = dhl_parcel_pl_insuration
