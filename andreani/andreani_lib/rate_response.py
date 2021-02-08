import attr
from jstruct import JList, JStruct
from typing import Optional


@attr.s(auto_attribs=True)
class Tarifa:
    seguroDistribucion: Optional[str] = None
    distribucion: Optional[str] = None
    total: Optional[str] = None


@attr.s(auto_attribs=True)
class Tarifas:
    pesoAforado: Optional[str] = None
    tarifaSinIva: Optional[Tarifa] = JStruct[Tarifa]
    tarifaConIva: Optional[Tarifa] = JStruct[Tarifa]
