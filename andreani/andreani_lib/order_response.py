from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class Linking:
    meta: Optional[str] = None
    contenido: Optional[str] = None


@dataclass
class Bulto:
    numeroDeBulto: Optional[int] = None
    numeroDeEnvio: Optional[str] = None
    totalizador: Optional[str] = None
    linking: Optional[List[Linking]] = None


@dataclass
class Sucursal:
    nomenclatura: Optional[str] = None
    descripcion: Optional[str] = None
    id: Optional[str] = None


@dataclass
class Ordenes:
    estado: Optional[str] = None
    tipo: Optional[str] = None
    sucursalDeDistribucion: Optional[Sucursal] = None
    sucursalDeRendicion: Optional[Sucursal] = None
    sucursalDeImposicion: Optional[Sucursal] = None
    fechaCreacion: Optional[str] = None
    zonaDeReparto: Optional[str] = None
    numeroDePermisionaria: Optional[str] = None
    descripcionServicio: Optional[str] = None
    etiquetaRemito: Optional[str] = None
    bultos: Optional[List[Bulto]] = None
    fechaEstimadaDeEntrega: Optional[str] = None
    huellaDeCarbono: Optional[str] = None
    gastoEnergetico: Optional[str] = None
