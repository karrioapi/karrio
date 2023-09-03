from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Dimensions:
    length: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class Label:
    format: Optional[str] = None
    size: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class Metadata:
    pass


@s(auto_attribs=True)
class ParcelContent:
    description: Optional[str] = None
    country_of_origin: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None
    hs_code: Optional[str] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class Gross:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class Price:
    gross: Optional[Gross] = JStruct[Gross]
    net: Optional[Gross] = JStruct[Gross]
    tax: Optional[Gross] = JStruct[Gross]


@s(auto_attribs=True)
class PriceBreakdown:
    base: Optional[Gross] = JStruct[Gross]
    discount: Optional[Gross] = JStruct[Gross]
    cover: Optional[Gross] = JStruct[Gross]
    fuel_surcharge: Optional[Gross] = JStruct[Gross]
    base_tax: Optional[Gross] = JStruct[Gross]
    discount_tax: Optional[Gross] = JStruct[Gross]
    cover_tax: Optional[Gross] = JStruct[Gross]
    fuel_surcharge_tax: Optional[Gross] = JStruct[Gross]


@s(auto_attribs=True)
class Product:
    atl_only: Optional[bool] = None
    code: Optional[str] = None
    name: Optional[str] = None
    first_mile_option: Optional[str] = None
    service: Optional[str] = None


@s(auto_attribs=True)
class Address:
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    suburb: Optional[str] = None
    state_name: Optional[str] = None
    postcode: Optional[int] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class Contact:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    sendle_id: Optional[str] = None


@s(auto_attribs=True)
class Receiver:
    contact: Optional[Contact] = JStruct[Contact]
    address: Optional[Address] = JStruct[Address]
    instructions: Optional[str] = None


@s(auto_attribs=True)
class Route:
    description: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class Scheduling:
    is_cancellable: Optional[bool] = None
    pickup_date: Optional[str] = None
    picked_up_on: Optional[str] = None
    delivered_on: Optional[str] = None
    estimated_delivery_date_minimum: Optional[str] = None
    estimated_delivery_date_maximum: Optional[str] = None
    status: Any = None


@s(auto_attribs=True)
class Status:
    description: Optional[str] = None
    last_changed_at: Optional[str] = None


@s(auto_attribs=True)
class Gst:
    amount: Optional[int] = None
    currency: Optional[str] = None
    rate: Optional[float] = None


@s(auto_attribs=True)
class TaxBreakdown:
    gst: Optional[Gst] = JStruct[Gst]
    hst: Optional[Gst] = JStruct[Gst]
    qst: Optional[Gst] = JStruct[Gst]


@s(auto_attribs=True)
class Volume:
    value: Optional[str] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class OrderResponse:
    order_id: Optional[str] = None
    state: Optional[str] = None
    status: Optional[Status] = JStruct[Status]
    order_url: Optional[str] = None
    sendle_reference: Optional[str] = None
    tracking_url: Optional[str] = None
    metadata: Optional[Metadata] = JStruct[Metadata]
    labels: List[Label] = JList[Label]
    scheduling: Optional[Scheduling] = JStruct[Scheduling]
    hide_pickup_address: Optional[bool] = None
    description: Optional[str] = None
    weight: Optional[Volume] = JStruct[Volume]
    volume: Optional[Volume] = JStruct[Volume]
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    customer_reference: Optional[str] = None
    sender: Optional[Receiver] = JStruct[Receiver]
    receiver: Optional[Receiver] = JStruct[Receiver]
    route: Optional[Route] = JStruct[Route]
    price: Optional[Price] = JStruct[Price]
    price_breakdown: Optional[PriceBreakdown] = JStruct[PriceBreakdown]
    tax_breakdown: Optional[TaxBreakdown] = JStruct[TaxBreakdown]
    parcel_contents: List[ParcelContent] = JList[ParcelContent]
    product: Optional[Product] = JStruct[Product]
