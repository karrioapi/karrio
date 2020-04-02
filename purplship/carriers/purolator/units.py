from enum import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "IN"
    weight_unit: str = "LB"


class PackagePresets(Flag):
    purolator_express_envelope = PackagePreset(weight=1)
    purolator_express_pack = PackagePreset(weight=3)
    purolator_express_box = PackagePreset(weight=7)


class PackagingType(Flag):
    purolator_express_envelope = "Envelop"
    purolator_express_pack = "Pack"
    purolator_express_box = "Box"
    purolator_customer_packaging = "Customer Packaging"

    """ Unified Packaging type mapping """
    envelope = purolator_express_envelope
    pak = purolator_express_pack
    tube = purolator_customer_packaging
    pallet = purolator_customer_packaging
    small_box = purolator_express_box
    medium_box = purolator_express_box
    large_box = purolator_express_box
    your_packaging = purolator_customer_packaging


class PaymentType(Flag):
    sender = "Sender"
    recipient = "Receiver"
    third_party = "ThirdParty"
    credit_card = "CreditCard"


class DutyPaymentType(Enum):
    sender = "Sender"
    recipient = "Receiver"
    third_party = "Buyer"


class CreditCardType(Flag):
    visa = "Visa"
    mastercard = "Mastercard"
    american_express = "AmericanExpress"


class Service(Enum):
    dangerous_goods = "Dangerous Goods"
    chain_of_signature = "Chain of Signature"
    express_cheque = "ExpressCheque"
    hold_for_pickup = "Hold For Pickup"
    return_services = "Return Services"
    saturday_service = "Saturday Service"
    origin_signature_not_required = "Origin Signature Not Required (OSNR)"
    adult_signature_required = "Adult Signature Required (ASR)"
    special_handling = "Special Handling"


class Product(Enum):
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
    purolator_ground9_am = "PurolatorGround9AM"
    purolator_express_envelope_international = "PurolatorExpressEnvelopeInternational"
    purolator_ground10_30_am = "PurolatorGround10:30AM"
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
