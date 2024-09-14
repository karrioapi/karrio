from attr import s
from typing import Optional, List, Any
from jstruct import JList, JStruct


@s(auto_attribs=True)
class UnavailableCourierType:
    id: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class MetaType:
    requestid: Optional[str] = None
    status: Optional[str] = None
    unavailablecouriers: List[UnavailableCourierType] = JList[UnavailableCourierType]
    errors: List[str] = []


@s(auto_attribs=True)
class BuyerRegulatoryIdentifiersType:
    ein: Optional[str] = None
    vatnumber: Optional[str] = None


@s(auto_attribs=True)
class CourierType:
    id: Optional[str] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    city: Optional[str] = None
    companyname: Optional[str] = None
    contactemail: Optional[str] = None
    contactname: Optional[str] = None
    contactphone: Optional[str] = None
    countryalpha2: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    postalcode: Optional[str] = None
    state: Optional[str] = None


@s(auto_attribs=True)
class InsuranceType:
    insuredamount: Optional[int] = None
    insuredcurrency: Optional[str] = None
    isinsured: Optional[bool] = None


@s(auto_attribs=True)
class LastFailureHTTPResponseMessageType:
    code: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class OrderDataType:
    buyernotes: Optional[str] = None
    buyerselectedcouriername: Optional[str] = None
    ordercreatedat: Optional[str] = None
    ordertaglist: List[str] = []
    platformname: Optional[str] = None
    platformordernumber: Optional[str] = None
    sellernotes: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None


@s(auto_attribs=True)
class BoxType:
    id: Optional[str] = None
    name: Optional[str] = None
    outerdimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    slug: Optional[str] = None
    type: Optional[str] = None
    weight: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    actualweight: Optional[int] = None
    category: Optional[str] = None
    containsbatterypi966: Optional[bool] = None
    containsbatterypi967: Optional[bool] = None
    containsliquids: Optional[bool] = None
    declaredcurrency: Optional[str] = None
    declaredcustomsvalue: Optional[int] = None
    description: Optional[str] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    hscode: Optional[int] = None
    id: Optional[str] = None
    origincountryalpha2: Optional[str] = None
    origincurrency: Optional[str] = None
    origincustomsvalue: Optional[int] = None
    quantity: Optional[int] = None
    sku: Optional[str] = None


@s(auto_attribs=True)
class ParcelType:
    box: Optional[BoxType] = JStruct[BoxType]
    id: Optional[str] = None
    items: List[ItemType] = JList[ItemType]
    totalactualweight: Optional[int] = None


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
    ddphandlingfee: Optional[str] = None
    estimatedimportduty: Optional[str] = None
    estimatedimporttax: Optional[str] = None
    fuelsurcharge: Optional[int] = None
    importdutycharge: Optional[str] = None
    importtaxcharge: Optional[str] = None
    importtaxnonchargeable: Optional[str] = None
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
class RateType:
    additionalservicessurcharge: Optional[int] = None
    availablehandoveroptions: List[str] = []
    costrank: Optional[int] = None
    courierid: Optional[str] = None
    courierlogourl: Optional[str] = None
    couriername: Optional[str] = None
    courierremarks: Optional[str] = None
    currency: Optional[str] = None
    ddphandlingfee: Optional[str] = None
    deliverytimerank: Optional[int] = None
    description: Optional[str] = None
    discount: Optional[str] = None
    easyshiprating: Optional[int] = None
    estimatedimportduty: Optional[str] = None
    estimatedimporttax: Optional[str] = None
    fuelsurcharge: Optional[int] = None
    fulldescription: Optional[str] = None
    importdutycharge: Optional[str] = None
    importtaxcharge: Optional[str] = None
    importtaxnonchargeable: Optional[str] = None
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
    remoteareasurcharges: Optional[str] = None
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
class RegulatoryIdentifiersType:
    eori: Optional[str] = None
    ioss: Optional[str] = None
    vatnumber: Optional[str] = None


@s(auto_attribs=True)
class B13AFilingType:
    option: Optional[str] = None
    optionexportcompliancestatement: Optional[str] = None
    permitnumber: Optional[str] = None


@s(auto_attribs=True)
class ShippingDocumentType:
    b13afiling: Optional[B13AFilingType] = JStruct[B13AFilingType]


@s(auto_attribs=True)
class ShippingSettingsType:
    b13afiling: Optional[str] = None


@s(auto_attribs=True)
class TrackingType:
    alternatetrackingnumber: Optional[str] = None
    handler: Optional[str] = None
    legnumber: Optional[int] = None
    localtrackingnumber: Optional[str] = None
    trackingnumber: Optional[str] = None
    trackingstate: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    buyerregulatoryidentifiers: Optional[BuyerRegulatoryIdentifiersType] = JStruct[BuyerRegulatoryIdentifiersType]
    consigneetaxid: Optional[str] = None
    courier: Optional[CourierType] = JStruct[CourierType]
    createdat: Optional[str] = None
    currency: Optional[str] = None
    deliverystate: Optional[str] = None
    destinationaddress: Optional[AddressType] = JStruct[AddressType]
    easyshipshipmentid: Optional[str] = None
    eeireference: Optional[str] = None
    incoterms: Optional[str] = None
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]
    labelgeneratedat: Optional[str] = None
    labelpaidat: Optional[str] = None
    labelstate: Optional[str] = None
    lastfailurehttpresponsemessages: List[LastFailureHTTPResponseMessageType] = JList[LastFailureHTTPResponseMessageType]
    metadata: List[Any] = []
    ordercreatedat: Optional[str] = None
    orderdata: Optional[OrderDataType] = JStruct[OrderDataType]
    originaddress: Optional[AddressType] = JStruct[AddressType]
    parcels: List[ParcelType] = JList[ParcelType]
    pickupstate: Optional[str] = None
    rates: List[RateType] = JList[RateType]
    regulatoryidentifiers: Optional[RegulatoryIdentifiersType] = JStruct[RegulatoryIdentifiersType]
    shipmentreturn: Optional[bool] = None
    returnaddress: Optional[AddressType] = JStruct[AddressType]
    senderaddress: Optional[AddressType] = JStruct[AddressType]
    setasresidential: Optional[bool] = None
    shipmentstate: Optional[str] = None
    shippingdocuments: List[ShippingDocumentType] = JList[ShippingDocumentType]
    shippingsettings: Optional[ShippingSettingsType] = JStruct[ShippingSettingsType]
    trackingpageurl: Optional[str] = None
    trackings: List[TrackingType] = JList[TrackingType]
    updatedat: Optional[str] = None
    warehousestate: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    shipment: Optional[ShipmentType] = JStruct[ShipmentType]
