import typing
import karrio.lib as lib
import karrio.core.units as units

PRESET_DEFAULTS = dict(dimension_unit="IN", weight_unit="LB")


class PackagePresets(lib.Enum):
    """Purolator package presets
    Note that dimensions are in IN and weight in LB
    """

    purolator_express_envelope = units.PackagePreset(
        **dict(width=12.5, height=16, length=1.5, weight=1.0), **PRESET_DEFAULTS
    )
    purolator_express_pack = units.PackagePreset(
        **dict(width=12.5, height=16, length=1.0, weight=3.0), **PRESET_DEFAULTS
    )
    purolator_express_box = units.PackagePreset(
        **dict(width=18, height=12, length=3.5, weight=7.0), **PRESET_DEFAULTS
    )


class PackagingType(lib.StrEnum):
    purolator_express_envelope = "Envelope"
    purolator_express_pack = "Pack"
    purolator_express_box = "Box"
    purolator_customer_packaging = "Customer Packaging"

    """ Unified Packaging type mapping """
    envelope = purolator_express_envelope
    pak = purolator_express_pack
    tube = purolator_customer_packaging
    pallet = purolator_customer_packaging
    small_box = purolator_customer_packaging
    medium_box = purolator_customer_packaging
    large_box = purolator_customer_packaging
    your_packaging = purolator_customer_packaging


MeasurementOptions = units.MeasurementOptionsType(min_kg=0.45, min_lb=1)


class LabelType(lib.Enum):
    PDF = "Regular"
    ZPL = "Thermal"


class PrintType(lib.StrEnum):
    PDF = "Regular"
    ZPL = "Thermal"


class PaymentType(lib.StrEnum):
    sender = "Sender"
    recipient = "Receiver"
    third_party = "ThirdParty"
    credit_card = "CreditCard"


class DutyPaymentType(lib.StrEnum):
    sender = "Sender"
    recipient = "Receiver"
    third_party = "Buyer"


class CreditCardType(lib.StrEnum):
    visa = "Visa"
    mastercard = "Mastercard"
    american_express = "AmericanExpress"


class ShippingOption(lib.Enum):
    purolator_dangerous_goods = lib.OptionEnum("Dangerous Goods")
    purolator_chain_of_signature = lib.OptionEnum("Chain of Signature")
    purolator_express_cheque = lib.OptionEnum("ExpressCheque")
    purolator_hold_for_pickup = lib.OptionEnum("Hold For Pickup")
    purolator_return_services = lib.OptionEnum("Return Services")
    purolator_saturday_service = lib.OptionEnum("Saturday Service")
    purolator_origin_signature_not_required = lib.OptionEnum(
        "Origin Signature Not Required (OSNR)"
    )
    purolator_adult_signature_required = lib.OptionEnum(
        "Adult Signature Required (ASR)"
    )
    purolator_special_handling = lib.OptionEnum("Special Handling")

    """Karrio specific option"""
    purolator_show_alternative_services = lib.OptionEnum(
        "Show Alternate Services", bool
    )

    """ Unified Option type mapping """
    saturday_delivery = purolator_saturday_service


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
    service_is_defined: bool = False,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    # When no specific service is requested, set a default one.
    _options.update(
        {
            "purolator_show_alternative_services": _options.get(
                "purolator_show_alternative_services"
            )
            or (not service_is_defined)
        }
    )

    def items_filter(key: str) -> bool:
        return key in ShippingOption and key not in NON_OFFICIAL_SERVICES  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


NON_OFFICIAL_SERVICES = [ShippingOption.purolator_show_alternative_services.name]


class ShippingService(lib.StrEnum):
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
    purolator_ground_9_am = "PurolatorGround9AM"
    purolator_express_envelope_international = "PurolatorExpressEnvelopeInternational"
    purolator_ground_10_30_am = "PurolatorGround10:30AM"
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


def shipping_services_initializer(
    services: typing.List[str],
    is_international: bool = False,
    recipient_country: str = None,
) -> units.Services:
    """
    Apply default values to the given services.
    """

    # When no specific service is requested, set a default.
    if not any([svc in ShippingService for svc in services]):  # type: ignore
        if is_international is False:
            services.append(ShippingService.purolator_express.name)  # type: ignore
        elif recipient_country == "US":
            services.append(ShippingService.purolator_express_us.name)  # type: ignore
        else:
            services.append(ShippingService.purolator_express_international.name)  # type: ignore

    return units.Services(services, ShippingService)


class TrackingStatus(lib.Enum):
    in_transit = [""]
    delivered = ["Delivery"]
    delivery_failed = ["Undeliverable"]
    out_for_delivery = ["OnDelivery"]
