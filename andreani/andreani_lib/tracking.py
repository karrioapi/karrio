from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
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


@dataclass
class EnviosTrazas:
    eventos: Optional[List[Evento]] = None
