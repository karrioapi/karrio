import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Bulto:
    kilos: Optional[int] = None
    largoCm: Optional[int] = None
    altoCm: Optional[int] = None
    anchoCm: Optional[int] = None
    volumenCm: Optional[int] = None
    valorDeclaradoSinImpuestos: Optional[int] = None
    valorDeclaradoConImpuestos: Optional[int] = None
    descripcion: Optional[str] = None
    referencias: Optional[List[str]] = None
    numeroDeEnvio: Optional[str] = None


@attr.s(auto_attribs=True)
class Telefonos:
    tipo: Optional[int] = None
    numero: Optional[str] = None


@attr.s(auto_attribs=True)
class Contacto:
    nombreCompleto: Optional[str] = None
    eMail: Optional[str] = None
    documentoTipo: Optional[str] = None
    documentoNumero: Optional[str] = None
    telefonos: Optional[Telefonos] = JStruct[Telefonos]


@attr.s(auto_attribs=True)
class Postal:
    localidad: Optional[str] = None
    region: Optional[str] = None
    pais: Optional[str] = None
    codigoPostal: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    componentesDeDireccion: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class Sucursal:
    id: Optional[str] = None


@attr.s(auto_attribs=True)
class Direccion:
    postal: Optional[Postal] = JStruct[Postal]
    sucursal: Optional[Sucursal] = JStruct[Sucursal]


@attr.s(auto_attribs=True)
class FechaDeEntrega:
    fecha: Optional[int] = None
    horaDesde: Optional[int] = None
    horaHasta: Optional[int] = None


@attr.s(auto_attribs=True)
class Remito:
    numeroRemito: Optional[str] = None
    complementarios: Optional[str] = None


@attr.s(auto_attribs=True)
class OrdenesDeEnvio:
    contrato: Optional[str] = None
    tipoServicio: Optional[str] = None
    sucursalClienteID: Optional[str] = None
    origen: Optional[Direccion] = JStruct[Direccion]
    destino: Optional[Direccion] = JStruct[Direccion]
    remitente: Optional[Contacto] = JStruct[Contacto]
    destinatario: Optional[Contacto] = JStruct[Contacto]
    remito: Optional[Remito] = JStruct[Remito]
    centroDeCostos: Optional[str] = None
    productoAEntregar: Optional[str] = None
    productoARetirar: Optional[str] = None
    tipoProducto: Optional[str] = None
    categoriaFacturacion: Optional[str] = None
    pagoDestino: Optional[int] = None
    valorACobrar: Optional[int] = None
    fechaDeEntrega: Optional[FechaDeEntrega] = JStruct[FechaDeEntrega]
    bultos: Optional[List[Bulto]] = JList[Remito]
