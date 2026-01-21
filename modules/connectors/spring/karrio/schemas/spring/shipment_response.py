import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CalculatedTotalType:
    sourceValue: typing.Optional[float] = None
    destinationValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ProductType:
    hs6code: typing.Optional[str] = None
    commodityCode: typing.Optional[str] = None
    value: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    description: typing.Optional[str] = None
    percentageDutyRate: typing.Optional[int] = None
    taxRate: typing.Optional[float] = None
    dutyValue: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    taxValue: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    productTotal: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    hs6codeDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LandedCostType:
    requestId: typing.Optional[str] = None
    sourceCountry: typing.Optional[str] = None
    sourceCurrency: typing.Optional[str] = None
    destinationCountry: typing.Optional[str] = None
    destinationCurrency: typing.Optional[str] = None
    convertCurrency: typing.Optional[bool] = None
    currencyExchange: typing.Optional[str] = None
    exchangeRate: typing.Optional[float] = None
    rateLastUpdated: typing.Optional[str] = None
    shippingValue: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]
    productRawTotal: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    calculatedTotal: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    totalTax: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    totalDuty: typing.Optional[CalculatedTotalType] = jstruct.JStruct[CalculatedTotalType]
    isError: typing.Optional[bool] = None
    errorCode: typing.Optional[int] = None
    notes: typing.Optional[str] = None
    generatedDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DdpInfoType:
    requestId: typing.Optional[str] = None
    landedCost: typing.Optional[LandedCostType] = jstruct.JStruct[LandedCostType]


@attr.s(auto_attribs=True)
class ShipmentType:
    TrackingNumber: typing.Optional[str] = None
    ShipperReference: typing.Optional[str] = None
    DisplayId: typing.Optional[str] = None
    Service: typing.Optional[str] = None
    Carrier: typing.Optional[str] = None
    CarrierTrackingNumber: typing.Optional[str] = None
    CarrierLocalTrackingNumber: typing.Optional[str] = None
    CarrierTrackingUrl: typing.Optional[str] = None
    LabelFormat: typing.Optional[str] = None
    LabelType: typing.Optional[str] = None
    LabelImage: typing.Optional[str] = None
    DdpInfo: typing.Optional[DdpInfoType] = jstruct.JStruct[DdpInfoType]


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    ErrorLevel: typing.Optional[int] = None
    Error: typing.Optional[str] = None
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
