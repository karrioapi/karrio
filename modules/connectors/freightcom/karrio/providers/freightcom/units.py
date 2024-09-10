import re
import karrio.lib as lib
import karrio.core.units as units


class FreightPackagingType(lib.StrEnum):
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


class PaymentType(lib.StrEnum):  # TODO:: retrieve the complete list of payment types
    check = "Check"

    sender = "Sender"
    recipient = "Recipient"
    third_party = "Third Party"
    credit_card = "Card"


class ShippingService(lib.StrEnum):
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

    @classmethod
    def info(cls, serviceId, carrierId, serviceName, carrierName):
        carrier_name = CARRIER_IDS.get(str(carrierId)) or carrierName
        service = cls.map(str(serviceId))
        formatted_name = re.sub(
            r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", serviceName
        )
        service_name = (service.name or formatted_name).replace("freightcom_", "")

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


class ShippingOption(lib.Enum):
    freightcom_saturday_pickup_required = lib.OptionEnum("saturdayPickupRequired", bool)
    freightcom_homeland_security = lib.OptionEnum("homelandSecurity", bool)
    freightcom_exhibition_convention_site = lib.OptionEnum(
        "exhibitionConventionSite", bool
    )
    freightcom_military_base_delivery = lib.OptionEnum("militaryBaseDelivery", bool)
    freightcom_customs_in_bond_freight = lib.OptionEnum("customsIn_bondFreight", bool)
    freightcom_limited_access = lib.OptionEnum("limitedAccess", bool)
    freightcom_excess_length = lib.OptionEnum("excessLength", bool)
    freightcom_tailgate_pickup = lib.OptionEnum("tailgatePickup", bool)
    freightcom_residential_pickup = lib.OptionEnum("residentialPickup", bool)
    freightcom_cross_border_fee = lib.OptionEnum("crossBorderFee", bool)
    freightcom_notify_recipient = lib.OptionEnum("notifyRecipient", bool)
    freightcom_single_shipment = lib.OptionEnum("singleShipment", bool)
    freightcom_tailgate_delivery = lib.OptionEnum("tailgateDelivery", bool)
    freightcom_residential_delivery = lib.OptionEnum("residentialDelivery", bool)
    freightcom_insurance_type = lib.OptionEnum("insuranceType", float)
    freightcom_inside_delivery = lib.OptionEnum("insideDelivery", bool)
    freightcom_is_saturday_service = lib.OptionEnum("isSaturdayService", bool)
    freightcom_dangerous_goods_type = lib.OptionEnum("dangerousGoodsType", bool)
    freightcom_stackable = lib.OptionEnum("stackable", bool)

    """ Unified Option type mapping """
    saturday_delivery = freightcom_saturday_pickup_required


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    return units.ShippingOptions(_options, ShippingOption)
