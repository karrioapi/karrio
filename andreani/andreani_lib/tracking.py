import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Evento:
    Motivo: Optional[str] = None
    Submotivo: Optional[str] = None
    Fecha: Optional[str] = None
    Estado: Optional[str] = None
    EstadoId: Optional[int] = None
    MotivoId: Optional[int] = None
    SubmotivoId: Optional[int] = None
    Sucursal: Optional[str] = None
    SucursalId: Optional[int] = None
    Ciclo: Optional[str] = None


@attr.s(auto_attribs=True)
class EnviosTrazas:
    eventos: Optional[List[Evento]] = JList[Evento]
