""" [carrier] Native Types """

from purplship.core.utils import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "IN"
    weight_unit: str = "LB"
    packaging_type: str = "medium_box"


class PackagePresets(Flag):
    # carrier_envelope = PackagePreset(weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="envelope")
    # carrier_box = PackagePreset(weight=1.0, width=33.7, height=18.2, length=10.0)
    pass


class PackageType(Flag):
    carrier_envelope = "ENVELOPE CODE"
    carrier_box = "BOX CODE"
    carrier_your_packaging = "CUSTOM PACKAGING CODE"

    """ Unified Packaging type mapping """
    envelope = carrier_envelope
    pak = carrier_envelope
    tube = carrier_your_packaging
    pallet = carrier_your_packaging
    small_box = carrier_box
    medium_box = carrier_box
    large_box = carrier_box
    your_packaging = carrier_your_packaging


class Service(Enum):
    carrier_standard = "STANDARD CODE"
    carrier_premium = "PREMIUM CODE"
    carrier_overnight = "OVERNIGHT CODE"


class Option(Flag):
    carrier_signature = "SIGNATURE CODE"
    carrier_saturday_delivery = "SATURDAY DELIVERY CODE"
    carrier_dry_ice = "DRY ICE CODE"
