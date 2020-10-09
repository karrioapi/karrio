from enum import Enum, Flag
from purplship.core.units import PackagePreset as BasePackagePreset
from dataclasses import dataclass


@dataclass
class PackagePreset(BasePackagePreset):
    dimension_unit: str = "IN"
    weight_unit: str = "LB"


class WeightUnit(Flag):
    LB = 'L'
    KG = 'K'


class DimensionUnit(Enum):
    IN = 'I'
    CM = 'C'


class Service(Enum):
    canpar_ground = '1'
    canpar_usa = '2'
    canpar_select_letter = '3'
    canpar_select_pak = '4'
    canpar_select = '5'
    canpar_overnight_letter = 'C'
    canpar_overnight_pak = 'D'
    canpar_overnight = 'E'
    canpar_usa_letter = 'F'
    canpar_usa_pak = 'G'
    canpar_select_usa = 'H'
    canpar_international = 'I'


class Option(Enum):
    canpar_cash_on_delivery = 'N'
    canpar_dangerous_goods = True
    canpar_extra_care = True
    canpar_ten_am = 'A'
    canpar_noon = 'B'
    canpar_no_signature_required = '2'
    canpar_not_no_signature_required = '0'
    canpar_saturday = 'S'

    """ Unified Option type mapping """
    cash_on_delivery = canpar_cash_on_delivery
