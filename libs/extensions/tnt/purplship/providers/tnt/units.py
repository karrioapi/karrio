""" TNT Native Types """

from purplship.core.utils import Enum, Flag, Spec
from purplship.core.units import PackagePreset

PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")


class PackagePresets(Flag):
    tnt_envelope_doc = PackagePreset(
        **dict(width=35.0, height=1.0, length=27.5, packaging_type="envelope"),
        **PRESET_DEFAULTS
    )
    tnt_satchel_bag1 = PackagePreset(
        **dict(weight=2.0, width=40.0, height=1.0, length=30.0, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    tnt_satchel_bag2 = PackagePreset(
        **dict(weight=4.0, width=47.5, height=1.0, length=38.0, packaging_type="pak"),
        **PRESET_DEFAULTS
    )
    tnt_box_B = PackagePreset(
        **dict(weight=4.0, width=29.5, height=19.0, length=40.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    tnt_box_C = PackagePreset(
        **dict(weight=6.0, width=29.5, height=29.0, length=40.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    tnt_box_D = PackagePreset(
        **dict(weight=10.0, width=39.5, height=29.0, length=50.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    tnt_box_E = PackagePreset(
        **dict(weight=15.0, width=39.5, height=49.5, length=44.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    tnt_medpack_ambient = PackagePreset(
        **dict(width=18.0, height=12.0, length=23.0, packaging_type="medium_box"),
        **PRESET_DEFAULTS
    )
    tnt_medpack_fronzen_10 = PackagePreset(
        **dict(width=37.0, height=35.5, length=40.0, packaging_type="large_box"),
        **PRESET_DEFAULTS
    )


class PackageType(Flag):
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


class PaymentType(Flag):
    sender = "S"
    recipient = "R"
    third_party = recipient


class ShipmentService(Enum):
    tnt_special_express = "1N"
    tnt_9_00_express = "09N"
    tnt_10_00_express = "10N"
    tnt_12_00_express = "12N"
    tnt_express = "EX"
    tnt_economy_express = "48N"
    tnt_global_express = "15N"


class ShipmentOption(Flag):
    tnt_priority = Spec.asKey('PR')
    tnt_insurance = Spec.asValue('IN', float)
    tnt_enhanced_liability = Spec.asKey('EL')
    tnt_dangerous_goods_fully_regulated = Spec.asKey('HZ')
    tnt_dangerous_goods_in_limited_quantities = Spec.asKey('LQ')
    tnt_dry_ice_shipments = Spec.asKey('DI')
    tnt_biological_substances = Spec.asKey('BB')
    tnt_lithium_batteries = Spec.asKey('LB')
    tnt_dangerous_goods_in_excepted_quantities = Spec.asKey('EQ')
    tnt_radioactive_materials_in_excepted_packages = Spec.asKey('XP')
    tnt_pre_delivery_notification = Spec.asKey('SMS')

    tnt_division_international_shipments = Spec.asKey('G')
    tnt_division_global_link_domestic = Spec.asKey('D')
    tnt_division_german_domestic = Spec.asKey('H')
    tnt_division_uk_domestic = Spec.asKey('010')

    insurance = tnt_insurance
