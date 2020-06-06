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

    """ Unified Packaging type mapping """
    pallet = freightcom_pallet
    small_box = freightcom_boxes
    medium_box = freightcom_boxes
    large_box = freightcom_boxes


class PaymentType(Flag):  # TODO:: retrieve the complete list of payment types
    check = 'Check'

    sender = "Sender"
    recipient = "Recipient"
    third_party = "Third Party"
    credit_card = "Card"


class Service(Enum):  # TODO:: retrieve the complete list of services
    freightcom_central_transport = "2029"
    freightcom_2107 = "2107"
    freightcom_1911 = "1911"


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
