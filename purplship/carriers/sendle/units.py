"""PurplShip Sendle domain"""
import attr
from enum import Enum, Flag


@attr.s(auto_attribs=True)
class Template:
    weight: float  # kg
    volume: float  # m3


class PackageTemplate(Flag):
    sendle_satchel = Template(weight=0.5, volume=0.002)
    sendle_shoebox = Template(weight=2, volume=0.008)
    sendle_briefcase = Template(weight=5, volume=0.02)
    sendle_carry_on = Template(weight=10, volume=0.04)
    sendle_luggage = Template(weight=25, volume=0.1)


class Plan(Enum):
    sendle_easy = "Easy"
    sendle_premium = "Premium"
    sendle_pro = "Pro"
