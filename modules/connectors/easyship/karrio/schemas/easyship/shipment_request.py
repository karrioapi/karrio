from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class BuyerRegulatoryIdentifiersType:
    ein: Optional[str] = None
    vatnumber: Optional[str] = None


@s(auto_attribs=True)
class CourierSelectionType:
    allowcourierfallback: Optional[bool] = None
    applyshippingrules: Optional[bool] = None
    listunavailablecouriers: Optional[bool] = None
    selectedcourierid: Optional[str] = None


@s(auto_attribs=True)
class ComparisonType:
    changes: Optional[str] = None
    post: Optional[str] = None
    pre: Optional[str] = None


@s(auto_attribs=True)
class ValidationType:
    detail: Optional[str] = None
    status: Optional[str] = None
    comparison: Optional[ComparisonType] = JStruct[ComparisonType]


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
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class InsuranceType:
    isinsured: Optional[bool] = None


@s(auto_attribs=True)
class OrderDataType:
    buyernotes: Optional[str] = None
    buyerselectedcouriername: Optional[str] = None
    ordercreatedat: Optional[str] = None
    platformname: Optional[str] = None
    platformordernumber: Optional[str] = None
    ordertaglist: List[str] = []
    sellernotes: Optional[str] = None


@s(auto_attribs=True)
class BoxType:
    height: Optional[int] = None
    length: Optional[int] = None
    weight: Optional[int] = None
    width: Optional[int] = None
    slug: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    actualweight: Optional[int] = None
    category: Any = None
    containsbatterypi966: Optional[bool] = None
    containsbatterypi967: Optional[bool] = None
    containsliquids: Optional[bool] = None
    declaredcurrency: Optional[str] = None
    declaredcustomsvalue: Optional[int] = None
    description: Optional[str] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    hscode: Optional[int] = None
    origincountryalpha2: Optional[str] = None
    quantity: Optional[int] = None
    sku: Optional[str] = None


@s(auto_attribs=True)
class ParcelType:
    box: Optional[BoxType] = JStruct[BoxType]
    items: List[ItemType] = JList[ItemType]
    totalactualweight: Optional[int] = None


@s(auto_attribs=True)
class RegulatoryIdentifiersType:
    eori: Optional[str] = None
    ioss: Optional[str] = None
    vatnumber: Optional[str] = None


@s(auto_attribs=True)
class AdditionalServicesType:
    deliveryconfirmation: Optional[str] = None
    qrcode: Optional[str] = None


@s(auto_attribs=True)
class B13AFilingType:
    option: Optional[str] = None
    optionexportcompliancestatement: Optional[str] = None
    permitnumber: Optional[str] = None


@s(auto_attribs=True)
class PrintingOptionsType:
    commercialinvoice: Optional[str] = None
    format: Optional[str] = None
    label: Optional[str] = None
    packingslip: Optional[str] = None
    remarks: Optional[str] = None


@s(auto_attribs=True)
class UnitsType:
    dimensions: Optional[str] = None
    weight: Optional[str] = None


@s(auto_attribs=True)
class ShippingSettingsType:
    additionalservices: Optional[AdditionalServicesType] = JStruct[AdditionalServicesType]
    b13afiling: Optional[B13AFilingType] = JStruct[B13AFilingType]
    buylabel: Optional[bool] = None
    buylabelsynchronous: Optional[bool] = None
    printingoptions: Optional[PrintingOptionsType] = JStruct[PrintingOptionsType]
    units: Optional[UnitsType] = JStruct[UnitsType]


@s(auto_attribs=True)
class ShipmentRequestType:
    buyerregulatoryidentifiers: Optional[BuyerRegulatoryIdentifiersType] = JStruct[BuyerRegulatoryIdentifiersType]
    courierselection: Optional[CourierSelectionType] = JStruct[CourierSelectionType]
    destinationaddress: Optional[AddressType] = JStruct[AddressType]
    consigneetaxid: Optional[int] = None
    eeireference: Optional[int] = None
    incoterms: Optional[str] = None
    metadata: List[Any] = []
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]
    orderdata: Optional[OrderDataType] = JStruct[OrderDataType]
    originaddress: Optional[AddressType] = JStruct[AddressType]
    regulatoryidentifiers: Optional[RegulatoryIdentifiersType] = JStruct[RegulatoryIdentifiersType]
    shipmentrequestreturn: Optional[bool] = None
    returnaddress: Optional[AddressType] = JStruct[AddressType]
    returnaddressid: Optional[str] = None
    senderaddress: Optional[AddressType] = JStruct[AddressType]
    senderaddressid: Optional[str] = None
    setasresidential: Optional[bool] = None
    shippingsettings: Optional[ShippingSettingsType] = JStruct[ShippingSettingsType]
    parcels: List[ParcelType] = JList[ParcelType]
