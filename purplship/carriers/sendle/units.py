"""PurplShip Sendle domain"""
from enum import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "IN"
    weight_unit: str = "LB"


class PackagePresets(Flag):
    sendle_satchel = PackagePreset(weight=0.5, volume=0.002)
    sendle_shoebox = PackagePreset(weight=2, volume=0.008)
    sendle_briefcase = PackagePreset(weight=5, volume=0.02)
    sendle_carry_on = PackagePreset(weight=10, volume=0.04)
    sendle_luggage = PackagePreset(weight=25, volume=0.1)


class Plan(Enum):
    sendle_easy = "Easy"
    sendle_premium = "Premium"
    sendle_pro = "Pro"
