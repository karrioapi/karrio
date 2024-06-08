import typing
import karrio.lib as lib
from karrio.core.units import Options


class WeightUnit(lib.StrEnum):
    LB = "L"
    KG = "K"


class DimensionUnit(lib.StrEnum):
    IN = "I"
    CM = "C"


class Charges(lib.StrEnum):
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


class Service(lib.StrEnum):
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


class ShippingOption(lib.Enum):
    canpar_cash_on_delivery = lib.OptionEnum("Y")
    canpar_dangerous_goods = lib.OptionEnum("dg", bool)
    canpar_extra_care = lib.OptionEnum("xc", bool)
    canpar_ten_am = lib.OptionEnum("A", bool)
    canpar_noon = lib.OptionEnum("B", bool)
    canpar_no_signature_required = lib.OptionEnum("2", bool)
    canpar_not_no_signature_required = lib.OptionEnum("0", bool)
    canpar_saturday = lib.OptionEnum("S", bool)

    """ Unified Option type mapping """
    cash_on_delivery = canpar_cash_on_delivery
    saturday_delivery = canpar_saturday

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
