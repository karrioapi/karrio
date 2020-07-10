from enum import Enum, Flag


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
    check = 'Check'

    sender = "Sender"
    recipient = "Recipient"
    third_party = "Third Party"
    credit_card = "Card"


class Service(Enum):
    freightcom_central_transport = "2029"
    freigthcom_estes = "2107"
    freigthcom_usf_holland = "1911"
    freightcom_fedex_ground = "4101"
    freightcom_ups_standard = "4600"
    freightcom_fedex_2_day = "4102"
    freightcom_fedex_priority_overnight = "4104"
    freightcom_fedex_standard_overnight = "4105"
    freightcom_ground = "3400"
    freightcom_ups_expedited = "4601"
    freightcom_ups_express_saver = "4602"
    freightcom_ups_express = "4603"
    freightcom_fedex_express_saver = "4100"
    freightcom_ups_express_early = "4604"
    freightcom_select = "3404"
    freightcom_dayr_e_comm_ground_service = "5707"
    freightcom_overnight = "3407"
    freightcom_purolator_ground = "4000"
    freightcom_purolator_express = "4003"
    freightcom_purolator_express_10_30_am = "4005"
    freightcom_fedex_first_overnight = "4106"
    freightcom_purolator_express_9_am = "4004"
    freightcom_dayr_e_comm_am_service = "5706"


class Option(Flag):
    freightcom_saturday_pickup_required = "saturdayPickupRequired"
    freightcom_homeland_security = "homelandSecurity"
    freightcom_exhibition_convention_site = "exhibitionConventionSite"
    freightcom_military_base_delivery = "militaryBaseDelivery"
    freightcom_customs_in_bond_freight = "customsIn_bondFreight"
    freightcom_limited_access = "limitedAccess"
    freightcom_excess_length = "excessLength"
    freightcom_tailgate_pickup = "tailgatePickup"
    freightcom_residential_pickup = "residentialPickup"
    freightcom_cross_border_fee = "crossBorderFee"
    freightcom_notify_recipient = "notifyRecipient"
    freightcom_single_shipment = "singleShipment"
    freightcom_tailgate_delivery = "tailgateDelivery"
    freightcom_residential_delivery = "residentialDelivery"
    freightcom_insurance_type = "insuranceType"
    freightcom_inside_delivery = "insideDelivery"
    freightcom_is_saturday_service = "isSaturdayService"
    freightcom_dangerous_goods_type = "dangerousGoodsType"
    freightcom_stackable = "stackable"


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
