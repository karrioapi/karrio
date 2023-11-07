from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class SizeOptions:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class WeightOptions:
    weight: Optional[float] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class Package:
    refNumber: Optional[int] = None
    weightOptions: Optional[WeightOptions] = JStruct[WeightOptions]
    sizeOptions: Optional[SizeOptions] = JStruct[SizeOptions]


@s(auto_attribs=True)
class RateRequest:
    postalCode: Optional[str] = None
    originPostalCode: Optional[str] = None
    packages: List[Package] = JList[Package]
