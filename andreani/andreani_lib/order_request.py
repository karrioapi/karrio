from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
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


@dataclass
class Telefonos:
    tipo: Optional[int] = None
    numero: Optional[str] = None


@dataclass
class Contacto:
    nombreCompleto: Optional[str] = None
    eMail: Optional[str] = None
    documentoTipo: Optional[str] = None
    documentoNumero: Optional[str] = None
    telefonos: Optional[Telefonos] = None


@dataclass
class Postal:
    localidad: Optional[str] = None
    region: Optional[str] = None
    pais: Optional[str] = None
    codigoPostal: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    componentesDeDireccion: Optional[List[str]] = None


@dataclass
class Sucursal:
    id: Optional[str] = None


@dataclass
class Direccion:
    postal: Optional[Postal] = None
    sucursal: Optional[Sucursal] = None


@dataclass
class FechaDeEntrega:
    fecha: Optional[int] = None
    horaDesde: Optional[int] = None
    horaHasta: Optional[int] = None


@dataclass
class Remito:
    numeroRemito: Optional[str] = None
    complementarios: Optional[str] = None


@dataclass
class OrdenesDeEnvio:
    contrato: Optional[str] = None
    tipoServicio: Optional[str] = None
    sucursalClienteID: Optional[str] = None
    origen: Optional[Direccion] = None
    destino: Optional[Direccion] = None
    remitente: Optional[Contacto] = None
    destinatario: Optional[Contacto] = None
    remito: Optional[Remito] = None
    centroDeCostos: Optional[str] = None
    productoAEntregar: Optional[str] = None
    productoARetirar: Optional[str] = None
    tipoProducto: Optional[str] = None
    categoriaFacturacion: Optional[str] = None
    pagoDestino: Optional[int] = None
    valorACobrar: Optional[int] = None
    fechaDeEntrega: Optional[FechaDeEntrega] = None
    bultos: Optional[List[Bulto]] = None
