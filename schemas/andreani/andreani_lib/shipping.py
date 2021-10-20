import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Bulto:
    kilos: Optional[float] = None
    valorDeclaradoConImpuestos: Optional[int] = None
    IdDeProducto: Optional[str] = None
    volumen: Optional[int] = None


@attr.s(auto_attribs=True)
class Contacto:
    tipoYNumeroDeDocumento: Optional[str] = None
    nombreYApellido: Optional[str] = None
    eMail: Optional[str] = None


@attr.s(auto_attribs=True)
class PostalDeDestino:
    codigoPostal: Optional[int] = None
    localidad: Optional[str] = None
    region: Optional[str] = None
    comment: Optional[str] = None
    pais: Optional[str] = None
    direccion: Optional[str] = None


@attr.s(auto_attribs=True)
class Destino:
    Postal: Optional[PostalDeDestino] = JStruct[PostalDeDestino]


@attr.s(auto_attribs=True)
class SucursalDeDistribucion:
    nomenclatura: Optional[str] = None
    descripcion: Optional[str] = None
    id: Optional[int] = None


@attr.s(auto_attribs=True)
class Envio:
    contrato: Optional[int] = None
    numeroDeTracking: Optional[str] = None
    estado: Optional[str] = None
    sucursalDeDistribucion: Optional[SucursalDeDistribucion] = JStruct[SucursalDeDistribucion]
    fechaCreacion: Optional[str] = None
    destino: Optional[Destino] = JStruct[Destino]
    remitente: Optional[Contacto] = JStruct[Contacto]
    destinatario: Optional[Contacto] = JStruct[Contacto]
    bultos: Optional[List[Bulto]] = JList[Bulto]
    referencias: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class FiltroDeEnvio:
    codigoCliente: Optional[str] = None
    idDeProducto: Optional[int] = None
    numeroDeDocumentoDestinatario: Optional[int] = None
    fechaCreacionDesde: Optional[str] = None
    fechaCreacionHasta: Optional[str] = None
    contrato: Optional[int] = None
    limit: Optional[int] = None
