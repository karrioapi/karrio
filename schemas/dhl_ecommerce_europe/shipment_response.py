import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentDetail:
    shipmentTrackingNumber: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    serviceHandlingFeatureCodes: typing.List[str] = jstruct.JList[str]


@attr.s(auto_attribs=True)
class Document:
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OnDemandDelivery:
    deliveryOption: typing.Optional[str] = None
    location: typing.Optional[str] = None
    specialInstructions: typing.List[str] = jstruct.JList[str]
    gateCode: typing.Optional[str] = None
    whereIsTheKey: typing.Optional[str] = None
    neighborName: typing.Optional[str] = None
    neighborHouseNumber: typing.Optional[str] = None
    authorizerName: typing.Optional[str] = None
    servicePointId: typing.Optional[str] = None
    requestedDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCharge:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    price: typing.Optional[float] = None
    priceType: typing.Optional[str] = None
    serviceCodeMutuallyExclusive: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ShipmentResponse:
    shipmentTrackingNumber: typing.Optional[str] = None
    shipmentDetails: typing.List[ShipmentDetail] = jstruct.JList[ShipmentDetail]
    documents: typing.List[Document] = jstruct.JList[Document]
    onDemandDelivery: typing.Optional[OnDemandDelivery] = jstruct.JStruct[OnDemandDelivery]
    shipmentCharges: typing.List[ShipmentCharge] = jstruct.JList[ShipmentCharge] 