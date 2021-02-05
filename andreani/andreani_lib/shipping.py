from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class Bulto:
    kilos: Optional[float] = None
    valorDeclaradoConImpuestos: Optional[int] = None
    IdDeProducto: Optional[str] = None
    volumen: Optional[int] = None


@dataclass
class Contacto:
    tipoYNumeroDeDocumento: Optional[str] = None
    nombreYApellido: Optional[str] = None
    eMail: Optional[str] = None


@dataclass
class PostalDeDestino:
    codigoPostal: Optional[int] = None
    localidad: Optional[str] = None
    region: Optional[str] = None
    comment: Optional[str] = None
    pais: Optional[str] = None
    direccion: Optional[str] = None


@dataclass
class Destino:
    Postal: Optional[PostalDeDestino] = None


@dataclass
class SucursalDeDistribucion:
    nomenclatura: Optional[str] = None
    descripcion: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Envio:
    contrato: Optional[int] = None
    numeroDeTracking: Optional[str] = None
    estado: Optional[str] = None
    sucursalDeDistribucion: Optional[SucursalDeDistribucion] = None
    fechaCreacion: Optional[str] = None
    destino: Optional[Destino] = None
    remitente: Optional[Contacto] = None
    destinatario: Optional[Contacto] = None
    bultos: Optional[List[Bulto]] = None
    referencias: Optional[List[str]] = None


@dataclass
class FiltroDeEnvio:
    codigoCliente: Optional[str] = None
    idDeProducto: Optional[int] = None
    numeroDeDocumentoDestinatario: Optional[int] = None
    fechaCreacionDesde: Optional[str] = None
    fechaCreacionHasta: Optional[str] = None
    contrato: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class Envios:
    envios: Optional[List[Envio]] = None
    filtroDeEnvio: Optional[FiltroDeEnvio] = None
