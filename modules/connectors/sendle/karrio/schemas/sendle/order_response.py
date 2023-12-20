from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ContentsType:
    description: Optional[str] = None
    country_of_origin: Optional[str] = None
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
class ParcelContentType:
    description: Optional[str] = None
    country_of_origin: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None
    hs_code: Optional[str] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class PriceBreakdownType:
    base: Optional[GrossType] = JStruct[GrossType]
    discount: Optional[GrossType] = JStruct[GrossType]
    cover: Optional[GrossType] = JStruct[GrossType]
    fuel_surcharge: Optional[GrossType] = JStruct[GrossType]
    base_tax: Optional[GrossType] = JStruct[GrossType]
    discount_tax: Optional[GrossType] = JStruct[GrossType]
    cover_tax: Optional[GrossType] = JStruct[GrossType]
    fuel_surcharge_tax: Optional[GrossType] = JStruct[GrossType]


@s(auto_attribs=True)
class ProductType:
    atl_only: Optional[bool] = None
    code: Optional[str] = None
    name: Optional[str] = None
    first_mile_option: Optional[str] = None
    service: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    suburb: Optional[str] = None
    state_name: Optional[str] = None
    postcode: Optional[int] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class ContactType:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    sendle_id: Optional[str] = None


@s(auto_attribs=True)
class ReceiverType:
    contact: Optional[ContactType] = JStruct[ContactType]
    address: Optional[AddressType] = JStruct[AddressType]
    instructions: Optional[str] = None


@s(auto_attribs=True)
class RouteType:
    description: Optional[str] = None
    type: Optional[str] = None
    delivery_guarantee_status: Optional[str] = None


@s(auto_attribs=True)
class SchedulingType:
    is_cancellable: Optional[bool] = None
    pickup_date: Optional[str] = None
    picked_up_on: Optional[str] = None
    delivered_on: Optional[str] = None
    estimated_delivery_date_minimum: Optional[str] = None
    estimated_delivery_date_maximum: Optional[str] = None
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
    order_id: Optional[str] = None
    state: Optional[str] = None
    order_url: Optional[str] = None
    sendle_reference: Optional[str] = None
    tracking_url: Optional[str] = None
    labels: List[LabelType] = JList[LabelType]
    scheduling: Optional[SchedulingType] = JStruct[SchedulingType]
    hide_pickup_address: Optional[bool] = None
    description: Optional[str] = None
    weight: Optional[VolumeType] = JStruct[VolumeType]
    volume: Optional[VolumeType] = JStruct[VolumeType]
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    customer_reference: Optional[str] = None
    metadata: Optional[dict] = {}
    sender: Optional[ReceiverType] = JStruct[ReceiverType]
    receiver: Optional[ReceiverType] = JStruct[ReceiverType]
    route: Optional[RouteType] = JStruct[RouteType]
    price: Optional[PriceType] = JStruct[PriceType]
    price_breakdown: Optional[PriceBreakdownType] = JStruct[PriceBreakdownType]
    tax_breakdown: Optional[TaxBreakdownType] = JStruct[TaxBreakdownType]
    cover: Optional[CoverType] = JStruct[CoverType]
    packaging_type: Optional[str] = None
    contents: Optional[ContentsType] = JStruct[ContentsType]
    parcel_contents: List[ParcelContentType] = JList[ParcelContentType]
    contents_type: Optional[str] = None
    label_provider: Optional[str] = None
    product: Optional[ProductType] = JStruct[ProductType]
