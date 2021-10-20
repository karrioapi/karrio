import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Linking:
    meta: Optional[str] = None
    contenido: Optional[str] = None


@attr.s(auto_attribs=True)
class Bulto:
    numeroDeBulto: Optional[int] = None
    numeroDeEnvio: Optional[str] = None
    totalizador: Optional[str] = None
    linking: Optional[List[Linking]] = JList[Linking]


@attr.s(auto_attribs=True)
class Sucursal:
    nomenclatura: Optional[str] = None
    descripcion: Optional[str] = None
    id: Optional[str] = None


@attr.s(auto_attribs=True)
class Ordenes:
    estado: Optional[str] = None
    tipo: Optional[str] = None
    sucursalDeDistribucion: Optional[Sucursal] = JStruct[Sucursal]
    sucursalDeRendicion: Optional[Sucursal] = JStruct[Sucursal]
    sucursalDeImposicion: Optional[Sucursal] = JStruct[Sucursal]
    fechaCreacion: Optional[str] = None
    zonaDeReparto: Optional[str] = None
    numeroDePermisionaria: Optional[str] = None
    descripcionServicio: Optional[str] = None
    etiquetaRemito: Optional[str] = None
    bultos: Optional[List[Bulto]] = JList[Bulto]
    fechaEstimadaDeEntrega: Optional[str] = None
    huellaDeCarbono: Optional[str] = None
    gastoEnergetico: Optional[str] = None
