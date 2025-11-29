import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    level: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class WeightType:
    value: typing.Optional[int] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdditionalServicesType:
    signatureRequired: typing.Optional[bool] = None
    deliveryWarranty: typing.Optional[bool] = None
    deliveryPUDO: typing.Optional[bool] = None
    lowCarbon: typing.Optional[bool] = None
    dutyTaxCalculation: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    line1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None
    state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillToType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    stateTaxId: typing.Optional[str] = None
    countryTaxId: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class ComplianceType:
    isControlGood: typing.Optional[bool] = None
    controlType: typing.Optional[str] = None
    regulatoryAgency: typing.Optional[str] = None
    regulatoryProgram: typing.Optional[str] = None
    regulatoryCategoryCode: typing.Optional[str] = None
    EIN: typing.Optional[str] = None
    iossNumber: typing.Optional[str] = None
    importLicenseNumber: typing.Optional[str] = None
    certificationType: typing.Optional[str] = None
    certificationReference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MetadataType:
    pass


@attr.s(auto_attribs=True)
class ValueType:
    amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    hsCode: typing.Optional[str] = None
    predictedHsCode: typing.Optional[str] = None
    predictedTaxCode: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    value: typing.Optional[ValueType] = jstruct.JStruct[ValueType]
    unitWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    countryOfOrigin: typing.Optional[str] = None
    category: typing.Optional[str] = None
    imageUrl: typing.Optional[str] = None
    productUrl: typing.Optional[str] = None
    productId: typing.Optional[str] = None
    variantId: typing.Optional[str] = None
    compliance: typing.Optional[ComplianceType] = jstruct.JStruct[ComplianceType]
    dutiesAndTaxes: typing.Optional[typing.List[str]] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]


@attr.s(auto_attribs=True)
class CustomsType:
    contentType: typing.Optional[str] = None
    incoterms: typing.Optional[str] = None
    invoiceNumber: typing.Optional[str] = None
    invoiceDate: typing.Optional[str] = None
    orderId: typing.Optional[str] = None
    orderTotalValue: typing.Optional[ValueType] = jstruct.JStruct[ValueType]
    certified: typing.Optional[bool] = None
    signedBy: typing.Optional[str] = None
    EORI: typing.Optional[str] = None
    IOSS: typing.Optional[str] = None
    VAT: typing.Optional[str] = None
    EIN: typing.Optional[str] = None
    VOECNUMBER: typing.Optional[str] = None
    SWISSVAT: typing.Optional[str] = None
    KARVAT: typing.Optional[str] = None
    CAGST: typing.Optional[str] = None
    AUGST: typing.Optional[str] = None
    NZGST: typing.Optional[str] = None
    JPConsumptionTax: typing.Optional[str] = None
    GPSRContactInfo: typing.Optional[str] = None
    importerOfRecord: typing.Optional[BillToType] = jstruct.JStruct[BillToType]


@attr.s(auto_attribs=True)
class DocumentType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    url: typing.Optional[str] = None
    base64String: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EventType:
    timestamp: typing.Optional[str] = None
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StMileType:
    carrier: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ChargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceType:
    name: typing.Optional[str] = None
    checkoutName: typing.Optional[str] = None
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    transit: typing.Optional[int] = None
    dispatchDays: typing.Optional[int] = None
    includeFirstMile: typing.Optional[bool] = None
    isActive: typing.Optional[bool] = None
    id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateType:
    price: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    transit: typing.Optional[int] = None
    estimatedDelivery: typing.Optional[str] = None
    service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]


@attr.s(auto_attribs=True)
class ReturnToType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class SurchargeType:
    id: typing.Optional[str] = None
    type: typing.Optional[str] = None
    name: typing.Optional[str] = None
    amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    shipmentId: typing.Optional[str] = None
    updatedAt: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipmentId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    estimatedDelivery: typing.Optional[str] = None
    documents: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
    shipTo: typing.Optional[ReturnToType] = jstruct.JStruct[ReturnToType]
    shipFrom: typing.Optional[ReturnToType] = jstruct.JStruct[ReturnToType]
    returnTo: typing.Optional[ReturnToType] = jstruct.JStruct[ReturnToType]
    billTo: typing.Optional[BillToType] = jstruct.JStruct[BillToType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    packageType: typing.Optional[str] = None
    description: typing.Optional[str] = None
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    customs: typing.Optional[CustomsType] = jstruct.JStruct[CustomsType]
    additionalServices: typing.Optional[AdditionalServicesType] = jstruct.JStruct[AdditionalServicesType]
    rate: typing.Optional[RateType] = jstruct.JStruct[RateType]
    scaleWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    billWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    actualBillWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    actualScaleWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    actualDimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    customerReference: typing.Optional[str] = None
    commercialInvoiceReference: typing.Optional[str] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    firstMile: typing.Optional[StMileType] = jstruct.JStruct[StMileType]
    lastMile: typing.Optional[StMileType] = jstruct.JStruct[StMileType]
    dropOffLocation: typing.Optional[BillToType] = jstruct.JStruct[BillToType]
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    surcharges: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    trackingURL: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None
    updatedAt: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
