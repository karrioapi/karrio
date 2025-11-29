import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AdditionalServicesType:
    signatureRequired: typing.Optional[bool] = None
    deliveryWarranty: typing.Optional[bool] = None
    deliveryPUDO: typing.Optional[bool] = None
    lowCarbon: typing.Optional[bool] = None
    dutyTaxCalculation: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class AddressType:
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postcode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillToType:
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    stateTaxId: typing.Optional[str] = None
    countryTaxId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ComplianceType:
    requiresLicensing: typing.Optional[bool] = None
    isHazardous: typing.Optional[bool] = None
    isRestricted: typing.Optional[bool] = None
    regulatoryInfo: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ValueType:
    amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    sku: typing.Optional[str] = None
    hsCode: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    category: typing.Optional[str] = None
    value: typing.Optional[ValueType] = jstruct.JStruct[ValueType]
    quantity: typing.Optional[int] = None
    unitWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    countryOfOrigin: typing.Optional[str] = None
    imageUrl: typing.Optional[str] = None
    productUrl: typing.Optional[str] = None
    compliance: typing.Optional[ComplianceType] = jstruct.JStruct[ComplianceType]


@attr.s(auto_attribs=True)
class CustomsType:
    EORI: typing.Optional[str] = None
    IOSS: typing.Optional[str] = None
    VAT: typing.Optional[str] = None
    EIN: typing.Optional[str] = None
    VOECNUMBER: typing.Optional[str] = None
    importerGST: typing.Optional[str] = None
    exporterGST: typing.Optional[str] = None
    consigneeGST: typing.Optional[str] = None
    contentType: typing.Optional[str] = None
    invoiceDate: typing.Optional[str] = None
    invoiceNumber: typing.Optional[str] = None
    GPSRContactInfo: typing.Optional[str] = None
    importerOfRecord: typing.Optional[BillToType] = jstruct.JStruct[BillToType]


@attr.s(auto_attribs=True)
class DimensionsType:
    unit: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ElectronicTradeDocumentType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    base64String: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MetadataType:
    fulfillmentOrderId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReturnToType:
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    serviceCode: typing.Optional[str] = None
    customerReference: typing.Optional[str] = None
    packageType: typing.Optional[str] = None
    description: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    orderTrackingReference: typing.Optional[str] = None
    commercialInvoiceReference: typing.Optional[str] = None
    shipTo: typing.Optional[ReturnToType] = jstruct.JStruct[ReturnToType]
    shipFrom: typing.Optional[ReturnToType] = jstruct.JStruct[ReturnToType]
    returnTo: typing.Optional[ReturnToType] = jstruct.JStruct[ReturnToType]
    billTo: typing.Optional[BillToType] = jstruct.JStruct[BillToType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    additionalServices: typing.Optional[AdditionalServicesType] = jstruct.JStruct[AdditionalServicesType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    electronicTradeDocuments: typing.Optional[typing.List[ElectronicTradeDocumentType]] = jstruct.JList[ElectronicTradeDocumentType]
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    customs: typing.Optional[CustomsType] = jstruct.JStruct[CustomsType]
