import typing
from karrio.core.utils import Enum, Flag
from karrio.core.units import Options
from karrio.core.utils.enum import OptionEnum


class WeightUnit(Flag):
    LB = "L"
    KG = "K"


class DimensionUnit(Enum):
    IN = "I"
    CM = "C"


class Charges(Flag):
    cod_charge = "Cash On Delivery"
    cos_charge = "Chain of Signature"
    dg_charge = "Dangerous Goods"
    dv_charge = "Declared Value"
    ea_charge = "Extended Area"
    freight_charge = "Freight Charge"
    fuel_surcharge = "Fuel Surcharge"
    handling = "Handling Charge"
    premium_charge = "Premium Service Charge"
    ra_charge = "Residential Address Surcharge"
    rural_charge = "Rural Address Surcharge"
    xc_charge = "Extra Care Charge"


class Service(Enum):
    canpar_ground = "1"
    canpar_usa = "2"
    canpar_select_letter = "3"
    canpar_select_pak = "4"
    canpar_select = "5"
    canpar_overnight_letter = "C"
    canpar_overnight_pak = "D"
    canpar_overnight = "E"
    canpar_usa_letter = "F"
    canpar_usa_pak = "G"
    canpar_select_usa = "H"
    canpar_international = "I"


class ShippingOption(Flag):
    canpar_cash_on_delivery = OptionEnum("Y")
    canpar_dangerous_goods = OptionEnum("dg", bool)
    canpar_extra_care = OptionEnum("xc", bool)
    canpar_ten_am = OptionEnum("A", bool)
    canpar_noon = OptionEnum("B", bool)
    canpar_no_signature_required = OptionEnum("2", bool)
    canpar_not_no_signature_required = OptionEnum("0", bool)
    canpar_saturday = OptionEnum("S", bool)

    """ Unified Option type mapping """
    cash_on_delivery = canpar_cash_on_delivery

    @classmethod
    def is_premium(cls, options: Options) -> typing.Optional[bool]:
        return next(
            (
                True
                for option, _ in options
                if option
                in [
                    cls.canpar_ten_am.name,
                    cls.canpar_noon.name,
                    cls.canpar_saturday.name,
                ]
            ),
            None,
        )

    @classmethod
    def is_nsr(cls, options: Options) -> typing.Optional[typing.Any]:
        return next(
            (
                options[o]
                for o in [
                    "canpar_no_signature_required",
                    "canpar_not_no_signature_required",
                ]
                if o in options
            ),
            None,
        )


def shipping_options_initializer(
    options: dict,
    package_options: Options = None,
) -> Options:
    _options = options.copy()

    # Apply package options if specified.
    if package_options is not None:
        _options.update(package_options.content)

    return Options(_options, ShippingOption)
