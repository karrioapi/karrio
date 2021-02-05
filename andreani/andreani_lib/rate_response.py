from pydantic.dataclasses import dataclass
from typing import Optional


@dataclass
class Tarifa:
    seguroDistribucion: Optional[str] = None
    distribucion: Optional[str] = None
    total: Optional[str] = None


@dataclass
class Tarifas:
    pesoAforado: Optional[str] = None
    tarifaSinIva: Optional[Tarifa] = None
    tarifaConIva: Optional[Tarifa] = None
