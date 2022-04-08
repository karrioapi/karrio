from attr import s
from typing import Optional, List, Any
from jstruct import JList, JStruct


@s(auto_attribs=True)
class CustomsItem:
    id: Optional[str] = None
    object: Optional[str] = None
    description: Optional[str] = None
    hstariffnumber: Optional[int] = None
    origincountry: Optional[str] = None
    quantity: Optional[int] = None
    value: Optional[int] = None
    weight: Optional[int] = None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None


@s(auto_attribs=True)
class CustomsInfo:
    id: Optional[str] = None
    object: Optional[str] = None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None
    contentsexplanation: None
    contentstype: Optional[str] = None
    customscertify: Optional[bool] = None
    customssigner: None
    eelpfc: None
    nondeliveryoption: Optional[str] = None
    restrictioncomments: None
    restrictiontype: Optional[str] = None
    customsitems: List[CustomsItem] = JList[CustomsItem]


@s(auto_attribs=True)
class Options:
    pass


@s(auto_attribs=True)
class Error:
    suggestion: None
    code: Optional[str] = None
    field: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class Delivery:
    success: Optional[bool] = None
    errors: List[Error] = JList[Error]
    details: Optional[Options] = JStruct[Options]


@s(auto_attribs=True)
class Verifications:
    delivery: Optional[Delivery] = JStruct[Delivery]


@s(auto_attribs=True)
class Address:
    id: Optional[str] = None
    object: Optional[str] = None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None
    name: None
    company: Optional[str] = None
    street1: Optional[str] = None
    street2: None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: None
    mode: Optional[str] = None
    carrierfacility: None
    residential: Optional[bool] = None
    federaltaxid: None
    statetaxid: None
    verifications: Optional[Verifications] = JStruct[Verifications]


@s(auto_attribs=True)
class Parcel:
    id: Optional[str] = None
    object: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    predefinedpackage: None
    weight: Optional[float] = None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None


@s(auto_attribs=True)
class PostageLabel:
    createdat: Optional[str] = None
    id: Optional[str] = None
    integratedform: Optional[str] = None
    labeldate: Optional[str] = None
    labelepl2url: None
    labelfiletype: Optional[str] = None
    labelpdfurl: Optional[str] = None
    labelresolution: Optional[int] = None
    labelsize: Optional[str] = None
    labeltype: Optional[str] = None
    labelurl: Optional[str] = None
    labelzplurl: None
    object: Optional[str] = None
    updatedat: Optional[str] = None


@s(auto_attribs=True)
class Rate:
    id: Optional[str] = None
    object: Optional[str] = None
    carrieraccountid: Optional[str] = None
    service: Optional[str] = None
    rate: Optional[str] = None
    carrier: Optional[str] = None
    shipmentid: Optional[str] = None
    deliverydays: Optional[int] = None
    deliverydate: Optional[str] = None
    deliverydateguaranteed: Optional[bool] = None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None


@s(auto_attribs=True)
class SelectedRate:
    carrier: Optional[str] = None
    createdat: Optional[str] = None
    currency: Optional[str] = None
    id: Optional[str] = None
    object: Optional[str] = None
    rate: Optional[str] = None
    service: Optional[str] = None
    shipmentid: Optional[str] = None
    updatedat: Optional[str] = None


@s(auto_attribs=True)
class Tracker:
    createdat: Optional[str] = None
    id: Optional[str] = None
    mode: Optional[str] = None
    object: Optional[str] = None
    shipmentid: Optional[str] = None
    status: Optional[str] = None
    trackingcode: Optional[str] = None
    trackingdetails: List[Any] = JList[Any]
    updatedat: Optional[str] = None
    publicurl: Optional[str] = None


@s(auto_attribs=True)
class Shipment:
    id: Optional[str] = None
    object: Optional[str] = None
    mode: Optional[str] = None
    isreturn: Optional[bool] = None
    batchmessage: None
    batchstatus: None
    toaddress: Optional[Address] = JStruct[Address]
    fromaddress: Optional[Address] = JStruct[Address]
    parcel: Optional[Parcel] = JStruct[Parcel]
    customsinfo: Optional[CustomsInfo] = JStruct[CustomsInfo]
    options: Optional[Options] = JStruct[Options]
    rates: List[Rate] = JList[Rate]
    reference: None
    scanform: None
    refundstatus: None
    selectedrate: Optional[SelectedRate] = JStruct[SelectedRate]
    status: Optional[str] = None
    postagelabel: Optional[PostageLabel] = JStruct[PostageLabel]
    trackingcode: Optional[str] = None
    tracker: Optional[Tracker] = JStruct[Tracker]
    insurance: None
    createdat: Optional[str] = None
    updatedat: Optional[str] = None
