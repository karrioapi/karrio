import re
from karrio.core.utils import Enum, Flag, Spec


class FreightPackagingType(Flag):
    freightcom_pallet = "Pallet"
    freightcom_drum = "Drum"
    freightcom_boxes = "Boxes"
    freightcom_rolls = "Rolls"
    freightcom_pipes_tubes = "Pipes/Tubes"
    freightcom_bales = "Bales"
    freightcom_bags = "Bags"
    freightcom_cylinder = "Cylinder"
    freightcom_pails = "Pails"
    freightcom_reels = "Reels"

    freightcom_envelope = "Envelope"
    freightcom_courier = "Courier"
    freightcom_pak = "Pak"
    freightcom_package = "Package"

    """ Unified Packaging type mapping """
    envelope = freightcom_envelope
    pak = freightcom_pak
    tube = freightcom_pipes_tubes
    pallet = freightcom_pallet
    small_box = freightcom_boxes
    medium_box = freightcom_boxes
    large_box = freightcom_boxes
    your_packaging = freightcom_package


class PaymentType(Flag):  # TODO:: retrieve the complete list of payment types
    check = "Check"

    sender = "Sender"
    recipient = "Recipient"
    third_party = "Third Party"
    credit_card = "Card"


class Service(Enum):
    freightcom_all = "0"
    freightcom_usf_holland = "1911"
    freightcom_central_transport = "2029"
    freightcom_estes = "2107"
    freightcom_canpar_ground = "3400"
    freightcom_canpar_select = "3404"
    freightcom_canpar_overnight = "3407"
    freightcom_dicom_ground = "3700"
    freightcom_purolator_ground = "4000"
    freightcom_purolator_express = "4003"
    freightcom_purolator_express_9_am = "4004"
    freightcom_purolator_express_10_30_am = "4005"
    freightcom_purolator_ground_us = "4016"
    freightcom_purolator_express_us = "4015"
    freightcom_purolator_express_us_9_am = "4013"
    freightcom_purolator_express_us_10_30_am = "4014"
    freightcom_fedex_express_saver = "4100"
    freightcom_fedex_ground = "4101"
    freightcom_fedex_2day = "4102"
    freightcom_fedex_priority_overnight = "4104"
    freightcom_fedex_standard_overnight = "4105"
    freightcom_fedex_first_overnight = "4106"
    freightcom_fedex_international_priority = "4108"
    freightcom_fedex_international_economy = "4109"
    freightcom_ups_standard = "4600"
    freightcom_ups_expedited = "4601"
    freightcom_ups_express_saver = "4602"
    freightcom_ups_express = "4603"
    freightcom_ups_express_early = "4604"
    freightcom_ups_3day_select = "4605"
    freightcom_ups_worldwide_expedited = "4606"
    freightcom_ups_worldwide_express = "4607"
    freightcom_ups_worldwide_express_plus = "4608"
    freightcom_ups_worldwide_express_saver = "4609"
    freightcom_dhl_express_easy = "5202"
    freightcom_dhl_express_10_30 = "5208"
    freightcom_dhl_express_worldwide = "5211"
    freightcom_dhl_express_12_00 = "5215"
    freightcom_dhl_economy_select = "5216"
    freightcom_dhl_ecommerce_am_service = "5706"
    freightcom_dhl_ecommerce_ground_service = "5707"
    freightcom_canadapost_regular_parcel = "6301"
    freightcom_canadapost_expedited_parcel = "6300"
    freightcom_canadapost_xpresspost = "6303"
    freightcom_canadapost_priority = "6302"

    @staticmethod
    def info(serviceId, carrierId, serviceName, carrierName):
        carrier_name = CARRIER_IDS.get(str(carrierId)) or carrierName
        service = Service.map(str(serviceId))
        formatted_name = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', serviceName)
        service_name = (service.name or formatted_name).replace('freightcom_', '')

        return carrier_name, service.name_or_key, service_name


CARRIER_IDS = {
    "34": "canpar",
    "37": "dicom",
    "40": "purolator",
    "41": "fedex",
    "52": "dhl",
    "57": "dhl_ecommerce",
    "63": "canadapost",
    "46": "ups",
}


class Option(Flag):
    freightcom_saturday_pickup_required = Spec.asFlag("saturdayPickupRequired")
    freightcom_homeland_security = Spec.asFlag("homelandSecurity")
    freightcom_exhibition_convention_site = Spec.asFlag("exhibitionConventionSite")
    freightcom_military_base_delivery = Spec.asFlag("militaryBaseDelivery")
    freightcom_customs_in_bond_freight = Spec.asFlag("customsIn_bondFreight")
    freightcom_limited_access = Spec.asFlag("limitedAccess")
    freightcom_excess_length = Spec.asFlag("excessLength")
    freightcom_tailgate_pickup = Spec.asFlag("tailgatePickup")
    freightcom_residential_pickup = Spec.asFlag("residentialPickup")
    freightcom_cross_border_fee = Spec.asFlag("crossBorderFee")
    freightcom_notify_recipient = Spec.asFlag("notifyRecipient")
    freightcom_single_shipment = Spec.asFlag("singleShipment")
    freightcom_tailgate_delivery = Spec.asFlag("tailgateDelivery")
    freightcom_residential_delivery = Spec.asFlag("residentialDelivery")
    freightcom_insurance_type = Spec.asValue("insuranceType", float)
    freightcom_inside_delivery = Spec.asFlag("insideDelivery")
    freightcom_is_saturday_service = Spec.asFlag("isSaturdayService")
    freightcom_dangerous_goods_type = Spec.asFlag("dangerousGoodsType")
    freightcom_stackable = Spec.asFlag("stackable")


class FreightClass(Enum):
    freightcom_freight_class_50 = 50
    freightcom_freight_class_55 = 55
    freightcom_freight_class_60 = 60
    freightcom_freight_class_65 = 65
    freightcom_freight_class_70 = 70
    freightcom_freight_class_77 = 77
    freightcom_freight_class_77_5 = 77.5
    freightcom_freight_class_85 = 85
    freightcom_freight_class_92_5 = 92.5
    freightcom_freight_class_100 = 100
    freightcom_freight_class_110 = 110
    freightcom_freight_class_125 = 125
    freightcom_freight_class_150 = 150
    freightcom_freight_class_175 = 175
    freightcom_freight_class_200 = 200
    freightcom_freight_class_250 = 250
    freightcom_freight_class_300 = 300
    freightcom_freight_class_400 = 400
