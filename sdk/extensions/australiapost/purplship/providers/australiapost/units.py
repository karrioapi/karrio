""" Australia Post Native Types """

# from purplship.core.utils import Enum, Flag
#
# PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")
#
#
# class PackagePresets(Flag):
#     # carrier_envelope = PackagePreset(
#     #     **dict(weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="envelope"),
#     #     **PRESET_DEFAULTS
#     # )
#     # carrier_box = PackagePreset(
#     #     **dict(weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="medium_box"),
#     #     **PRESET_DEFAULTS
#     # )
#     pass
#
#
# class PackageType(Flag):
#     carrier_envelope = "ENVELOPE CODE"
#     carrier_box = "BOX CODE"
#     carrier_your_packaging = "CUSTOM PACKAGING CODE"
#
#     """ Unified Packaging type mapping """
#     envelope = carrier_envelope
#     pak = carrier_envelope
#     tube = carrier_your_packaging
#     pallet = carrier_your_packaging
#     small_box = carrier_box
#     medium_box = carrier_box
#     large_box = carrier_box
#     your_packaging = carrier_your_packaging
#
#
# class Service(Enum):
#     carrier_standard = "STANDARD CODE"
#     carrier_premium = "PREMIUM CODE"
#     carrier_overnight = "OVERNIGHT CODE"
#
#
# class Option(Flag):
#     carrier_signature = "SIGNATURE CODE"
#     carrier_saturday_delivery = "SATURDAY DELIVERY CODE"
#     carrier_dry_ice = "DRY ICE CODE"
