from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class PaginationType:
    count: Optional[int] = None
    next: Optional[str] = None
    page: Optional[int] = None


@s(auto_attribs=True)
class MetaType:
    pagination: Optional[PaginationType] = JStruct[PaginationType]
    requestid: Optional[str] = None


@s(auto_attribs=True)
class DiscountType:
    amount: Optional[int] = None
    originamount: Optional[int] = None


@s(auto_attribs=True)
class DetailType:
    fee: Optional[int] = None
    name: Optional[str] = None
    originfee: Optional[int] = None


@s(auto_attribs=True)
class OtherSurchargesType:
    details: List[DetailType] = JList[DetailType]
    totalfee: Optional[int] = None


@s(auto_attribs=True)
class RatesInOriginCurrencyType:
    additionalservicessurcharge: Optional[int] = None
    currency: Optional[str] = None
    ddphandlingfee: Optional[int] = None
    estimatedimportduty: Optional[int] = None
    estimatedimporttax: Optional[float] = None
    fuelsurcharge: Optional[int] = None
    importdutycharge: Optional[int] = None
    importtaxcharge: Optional[int] = None
    importtaxnonchargeable: Optional[int] = None
    insurancefee: Optional[int] = None
    minimumpickupfee: Optional[int] = None
    oversizedsurcharge: Optional[int] = None
    provincialsalestax: Optional[int] = None
    remoteareasurcharge: Optional[int] = None
    residentialdiscountedfee: Optional[int] = None
    residentialfullfee: Optional[int] = None
    salestax: Optional[int] = None
    shipmentcharge: Optional[int] = None
    shipmentchargetotal: Optional[int] = None
    totalcharge: Optional[int] = None
    warehousehandlingfee: Optional[int] = None


@s(auto_attribs=True)
class DestinationType:
    base: Optional[int] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class RemoteAreaSurchargesType:
    destination: Optional[DestinationType] = JStruct[DestinationType]
    origin: Optional[DestinationType] = JStruct[DestinationType]


@s(auto_attribs=True)
class RateType:
    additionalservicessurcharge: Optional[int] = None
    availablehandoveroptions: List[Any] = []
    costrank: Optional[int] = None
    courierid: Optional[str] = None
    courierlogourl: Optional[str] = None
    couriername: Optional[str] = None
    courierremarks: Optional[str] = None
    currency: Optional[str] = None
    ddphandlingfee: Optional[int] = None
    deliverytimerank: Optional[int] = None
    description: Optional[str] = None
    discount: Optional[DiscountType] = JStruct[DiscountType]
    easyshiprating: Optional[int] = None
    estimatedimportduty: Optional[int] = None
    estimatedimporttax: Optional[float] = None
    fuelsurcharge: Optional[int] = None
    fulldescription: Optional[str] = None
    importdutycharge: Optional[int] = None
    importtaxcharge: Optional[int] = None
    importtaxnonchargeable: Optional[int] = None
    incoterms: Optional[str] = None
    insurancefee: Optional[int] = None
    isabovethreshold: Optional[bool] = None
    maxdeliverytime: Optional[int] = None
    mindeliverytime: Optional[int] = None
    minimumpickupfee: Optional[int] = None
    othersurcharges: Optional[OtherSurchargesType] = JStruct[OtherSurchargesType]
    oversizedsurcharge: Optional[int] = None
    paymentrecipient: Optional[str] = None
    provincialsalestax: Optional[int] = None
    ratesinorigincurrency: Optional[RatesInOriginCurrencyType] = JStruct[RatesInOriginCurrencyType]
    remoteareasurcharge: Optional[int] = None
    remoteareasurcharges: Optional[RemoteAreaSurchargesType] = JStruct[RemoteAreaSurchargesType]
    residentialdiscountedfee: Optional[int] = None
    residentialfullfee: Optional[int] = None
    salestax: Optional[int] = None
    shipmentcharge: Optional[int] = None
    shipmentchargetotal: Optional[int] = None
    totalcharge: Optional[int] = None
    trackingrating: Optional[int] = None
    valueformoneyrank: Optional[int] = None
    warehousehandlingfee: Optional[int] = None


@s(auto_attribs=True)
class RateResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    rates: List[RateType] = JList[RateType]
