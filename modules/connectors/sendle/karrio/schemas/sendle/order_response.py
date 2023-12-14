from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ContentsType:
    description: Optional[str] = None
    countryoforigin: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class GrossType:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class PriceType:
    gross: Optional[GrossType] = JStruct[GrossType]
    net: Optional[GrossType] = JStruct[GrossType]
    tax: Optional[GrossType] = JStruct[GrossType]


@s(auto_attribs=True)
class CoverType:
    price: Optional[PriceType] = JStruct[PriceType]


@s(auto_attribs=True)
class DimensionsType:
    length: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class LabelType:
    format: Optional[str] = None
    size: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class MetadataType:
    pass


@s(auto_attribs=True)
class ParcelContentType:
    description: Optional[str] = None
    countryoforigin: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None
    hscode: Optional[str] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class PriceBreakdownType:
    base: Optional[GrossType] = JStruct[GrossType]
    discount: Optional[GrossType] = JStruct[GrossType]
    cover: Optional[GrossType] = JStruct[GrossType]
    fuelsurcharge: Optional[GrossType] = JStruct[GrossType]
    basetax: Optional[GrossType] = JStruct[GrossType]
    discounttax: Optional[GrossType] = JStruct[GrossType]
    covertax: Optional[GrossType] = JStruct[GrossType]
    fuelsurchargetax: Optional[GrossType] = JStruct[GrossType]


@s(auto_attribs=True)
class ProductType:
    atlonly: Optional[bool] = None
    code: Optional[str] = None
    name: Optional[str] = None
    firstmileoption: Optional[str] = None
    service: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    addressline1: Optional[str] = None
    addressline2: Optional[str] = None
    suburb: Optional[str] = None
    statename: Optional[str] = None
    postcode: Optional[int] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class ContactType:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    sendleid: Optional[str] = None


@s(auto_attribs=True)
class ReceiverType:
    contact: Optional[ContactType] = JStruct[ContactType]
    address: Optional[AddressType] = JStruct[AddressType]
    instructions: Optional[str] = None


@s(auto_attribs=True)
class RouteType:
    description: Optional[str] = None
    type: Optional[str] = None
    deliveryguaranteestatus: Optional[str] = None


@s(auto_attribs=True)
class SchedulingType:
    iscancellable: Optional[bool] = None
    pickupdate: Optional[str] = None
    pickedupon: Optional[str] = None
    deliveredon: Optional[str] = None
    estimateddeliverydateminimum: Optional[str] = None
    estimateddeliverydatemaximum: Optional[str] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class GstType:
    amount: Optional[float] = None
    currency: Optional[str] = None
    rate: Optional[float] = None


@s(auto_attribs=True)
class TaxBreakdownType:
    gst: Optional[GstType] = JStruct[GstType]
    qst: Optional[GstType] = JStruct[GstType]


@s(auto_attribs=True)
class VolumeType:
    units: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class OrderResponseType:
    orderid: Optional[str] = None
    state: Optional[str] = None
    orderurl: Optional[str] = None
    sendlereference: Optional[str] = None
    trackingurl: Optional[str] = None
    labels: List[LabelType] = JList[LabelType]
    scheduling: Optional[SchedulingType] = JStruct[SchedulingType]
    hidepickupaddress: Optional[bool] = None
    description: Optional[str] = None
    weight: Optional[VolumeType] = JStruct[VolumeType]
    volume: Optional[VolumeType] = JStruct[VolumeType]
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    customerreference: Optional[str] = None
    metadata: Optional[dict] = {}
    sender: Optional[ReceiverType] = JStruct[ReceiverType]
    receiver: Optional[ReceiverType] = JStruct[ReceiverType]
    route: Optional[RouteType] = JStruct[RouteType]
    price: Optional[PriceType] = JStruct[PriceType]
    pricebreakdown: Optional[PriceBreakdownType] = JStruct[PriceBreakdownType]
    taxbreakdown: Optional[TaxBreakdownType] = JStruct[TaxBreakdownType]
    cover: Optional[CoverType] = JStruct[CoverType]
    packagingtype: Optional[str] = None
    contents: Optional[ContentsType] = JStruct[ContentsType]
    parcelcontents: List[ParcelContentType] = JList[ParcelContentType]
    contentstype: Optional[str] = None
    labelprovider: Optional[str] = None
    product: Optional[ProductType] = JStruct[ProductType]
