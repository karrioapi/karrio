import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CommercialInvoiceType:
    termsOfSale: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomItemType:
    exportHsCode: typing.Optional[int] = None
    description: typing.Optional[str] = None
    importHsCode: typing.Optional[int] = None
    quantity: typing.Optional[int] = None
    quantityUnit: typing.Optional[str] = None
    weight: typing.Optional[int] = None
    commercialValue: typing.Optional[int] = None
    commercialValueCurrency: typing.Optional[str] = None
    manufactureCountryCode: typing.Optional[str] = None
    sku: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionType:
    pieceReference: typing.Optional[int] = None
    pieces: typing.Optional[int] = None
    height: typing.Optional[float] = None
    width: typing.Optional[float] = None
    length: typing.Optional[float] = None
    grossWeight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class PackageType:
    reference: typing.Optional[str] = None
    commodityType: typing.Optional[str] = None
    serviceType: typing.Optional[str] = None
    paymentMode: typing.Optional[str] = None
    origin: typing.Optional[str] = None
    destination: typing.Optional[str] = None
    packageDescription: typing.Optional[str] = None
    totalPackages: typing.Optional[int] = None
    totalPieces: typing.Optional[int] = None
    grossVolumeUnityMeasure: typing.Optional[str] = None
    totalGrossWeight: typing.Optional[float] = None
    grossWeightUnityMeasure: typing.Optional[str] = None
    hasInsurance: typing.Optional[bool] = None
    insuranceAmmount: typing.Optional[float] = None
    specialHandlingType: typing.Any = None
    additionalInfo01: typing.Any = None
    additionalInfo02: typing.Any = None
    additionalInfo03: typing.Any = None
    additionalInfo04: typing.Any = None
    deliveryType: typing.Optional[str] = None
    channel: typing.Optional[str] = None
    labelRef2: typing.Any = None
    incoterm: typing.Optional[str] = None
    dimensions: typing.Optional[typing.List[DimensionType]] = jstruct.JList[DimensionType]
    participants: typing.Optional[typing.List[typing.Dict[str, typing.Optional[str]]]] = None
    customItems: typing.Optional[typing.List[CustomItemType]] = jstruct.JList[CustomItemType]
    commercialInvoice: typing.Optional[CommercialInvoiceType] = jstruct.JStruct[CommercialInvoiceType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    reference: typing.Optional[str] = None
    issueDate: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
