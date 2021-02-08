import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Bulto:
    largoCm: Optional[int] = None
    anchoCm: Optional[int] = None
    altoCm: Optional[int] = None
    volumen: Optional[int] = None
    kilos: Optional[int] = None
    pesoAforado: Optional[int] = None
    valorDeclarado: Optional[int] = None
    categoria: Optional[str] = None


@attr.s(auto_attribs=True)
class Tarifas:
    pais: Optional[str] = None
    cpDestino: Optional[int] = None
    contrato: Optional[str] = None
    cliente: Optional[str] = None
    sucursalOrigen: Optional[str] = None
    bultos: Optional[List[Bulto]] = JList[Bulto]
