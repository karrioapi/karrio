import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ContentsType:
    description: typing.Optional[str] = None
    country_of_origin: typing.Optional[str] = None
    value: typing.Optional[str] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class GrossType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PriceType:
    gross: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    net: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    tax: typing.Optional[GrossType] = jstruct.JStruct[GrossType]


@attr.s(auto_attribs=True)
class CoverType:
    price: typing.Optional[PriceType] = jstruct.JStruct[PriceType]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[str] = None
    width: typing.Optional[str] = None
    height: typing.Optional[str] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelType:
    format: typing.Optional[str] = None
    size: typing.Optional[str] = None
    url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MetadataType:
    pass


@attr.s(auto_attribs=True)
class ParcelContentType:
    description: typing.Optional[str] = None
    country_of_origin: typing.Optional[str] = None
    value: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    hs_code: typing.Optional[str] = None
    quantity: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PriceBreakdownType:
    base: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    discount: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    cover: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    fuel_surcharge: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    base_tax: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    discount_tax: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    cover_tax: typing.Optional[GrossType] = jstruct.JStruct[GrossType]
    fuel_surcharge_tax: typing.Optional[GrossType] = jstruct.JStruct[GrossType]


@attr.s(auto_attribs=True)
class ProductType:
    atl_only: typing.Optional[bool] = None
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None
    first_mile_option: typing.Optional[str] = None
    service: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    address_line1: typing.Optional[str] = None
    address_line2: typing.Optional[str] = None
    suburb: typing.Optional[str] = None
    state_name: typing.Optional[str] = None
    postcode: typing.Optional[int] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    company: typing.Optional[str] = None
    sendle_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverType:
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    instructions: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RouteType:
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None
    delivery_guarantee_status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SchedulingType:
    is_cancellable: typing.Optional[bool] = None
    pickup_date: typing.Optional[str] = None
    picked_up_on: typing.Optional[str] = None
    delivered_on: typing.Optional[str] = None
    estimated_delivery_date_minimum: typing.Optional[str] = None
    estimated_delivery_date_maximum: typing.Optional[str] = None
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class GstType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    rate: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class TaxBreakdownType:
    gst: typing.Optional[GstType] = jstruct.JStruct[GstType]
    qst: typing.Optional[GstType] = jstruct.JStruct[GstType]


@attr.s(auto_attribs=True)
class VolumeType:
    units: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderResponseType:
    order_id: typing.Optional[str] = None
    state: typing.Optional[str] = None
    order_url: typing.Optional[str] = None
    sendle_reference: typing.Optional[str] = None
    tracking_url: typing.Optional[str] = None
    labels: typing.Optional[typing.List[LabelType]] = jstruct.JList[LabelType]
    scheduling: typing.Optional[SchedulingType] = jstruct.JStruct[SchedulingType]
    hide_pickup_address: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    weight: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    volume: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    customer_reference: typing.Optional[str] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    sender: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    route: typing.Optional[RouteType] = jstruct.JStruct[RouteType]
    price: typing.Optional[PriceType] = jstruct.JStruct[PriceType]
    price_breakdown: typing.Optional[PriceBreakdownType] = jstruct.JStruct[PriceBreakdownType]
    tax_breakdown: typing.Optional[TaxBreakdownType] = jstruct.JStruct[TaxBreakdownType]
    cover: typing.Optional[CoverType] = jstruct.JStruct[CoverType]
    packaging_type: typing.Optional[str] = None
    contents: typing.Optional[ContentsType] = jstruct.JStruct[ContentsType]
    parcel_contents: typing.Optional[typing.List[ParcelContentType]] = jstruct.JList[ParcelContentType]
    contents_type: typing.Optional[str] = None
    label_provider: typing.Optional[str] = None
    product: typing.Optional[ProductType] = jstruct.JStruct[ProductType]
