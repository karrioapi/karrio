""" TNT Native Types """

import karrio.lib as lib

PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")


class PackagePresets(lib.Flag):
    tnt_envelope_doc = lib.units.PackagePreset(
        **dict(width=35.0, height=1.0, length=27.5, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    tnt_satchel_bag1 = lib.units.PackagePreset(
        **dict(weight=2.0, width=40.0, height=1.0, length=30.0, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    tnt_satchel_bag2 = lib.units.PackagePreset(
        **dict(weight=4.0, width=47.5, height=1.0, length=38.0, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    tnt_box_B = lib.units.PackagePreset(
        **dict(
            weight=4.0,
            width=29.5,
            height=19.0,
            length=40.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    tnt_box_C = lib.units.PackagePreset(
        **dict(
            weight=6.0,
            width=29.5,
            height=29.0,
            length=40.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    tnt_box_D = lib.units.PackagePreset(
        **dict(
            weight=10.0,
            width=39.5,
            height=29.0,
            length=50.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    tnt_box_E = lib.units.PackagePreset(
        **dict(
            weight=15.0,
            width=39.5,
            height=49.5,
            length=44.0,
            packaging_type="medium_box",
        ),
        **PRESET_DEFAULTS
    )
    tnt_medpack_ambient = lib.units.PackagePreset(
        **dict(width=18.0, height=12.0, length=23.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    tnt_medpack_fronzen_10 = lib.units.PackagePreset(
        **dict(width=37.0, height=35.5, length=40.0, packaging_type="large_box"),
        **PRESET_DEFAULTS
    )


class PackageType(lib.Flag):
    tnt_envelope = "envelope"
    tnt_satchel = "satchel"
    tnt_box = "box"
    tnt_cylinder = "cylinder"
    tnt_pallet = "pallet"

    """ Unified Packaging type mapping """
    envelope = tnt_envelope
    pak = tnt_satchel
    tube = tnt_cylinder
    pallet = tnt_pallet
    small_box = tnt_box
    medium_box = tnt_box
    large_box = tnt_box
    your_packaging = "your_packaging"


class PaymentType(lib.Flag):
    sender = "S"
    recipient = "R"
    third_party = recipient


class ConnectionConfig(lib.Enum):
    label_type = lib.OptionEnum("label_type")


class ShipmentService(lib.Enum):
    tnt_special_express = "1N"
    tnt_9_00_express = "09N"
    tnt_10_00_express = "10N"
    tnt_12_00_express = "12N"
    tnt_express = "EX"
    tnt_economy_express = "48N"
    tnt_global_express = "15N"


class ShippingOption(lib.Flag):
    tnt_priority = lib.OptionEnum("PR")
    tnt_insurance = lib.OptionEnum("IN", float)
    tnt_enhanced_liability = lib.OptionEnum("EL")
    tnt_dangerous_goods_fully_regulated = lib.OptionEnum("HZ")
    tnt_dangerous_goods_in_limited_quantities = lib.OptionEnum("LQ")
    tnt_dry_ice_shipments = lib.OptionEnum("DI")
    tnt_biological_substances = lib.OptionEnum("BB")
    tnt_lithium_batteries = lib.OptionEnum("LB")
    tnt_dangerous_goods_in_excepted_quantities = lib.OptionEnum("EQ")
    tnt_radioactive_materials_in_excepted_packages = lib.OptionEnum("XP")
    tnt_pre_delivery_notification = lib.OptionEnum("SMS")

    tnt_division_international_shipments = lib.OptionEnum("G")
    tnt_division_global_link_domestic = lib.OptionEnum("D")
    tnt_division_german_domestic = lib.OptionEnum("H")
    tnt_division_uk_domestic = lib.OptionEnum("010")

    insurance = tnt_insurance


def shipping_options_initializer(
    options: dict,
    package_options: lib.units.Options = None,
) -> lib.units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption and "division" not in key  # type: ignore

    return lib.units.ShippingOptions(
        _options, ShippingOption, items_filter=items_filter
    )
