from attr import s
from typing import List, Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Eta:
    days_range: List[int] = []
    date_range: List[str] = []
    for_send_date: Optional[str] = None


@s(auto_attribs=True)
class Base:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class PriceBreakdown:
    base: Optional[Base] = JStruct[Base]
    discount: Optional[Base] = JStruct[Base]
    cover: Optional[Base] = JStruct[Base]
    fuel_surcharge: Optional[Base] = JStruct[Base]
    base_tax: Optional[Base] = JStruct[Base]
    discount_tax: Optional[Base] = JStruct[Base]
    cover_tax: Optional[Base] = JStruct[Base]
    fuel_surcharge_tax: Optional[Base] = JStruct[Base]


@s(auto_attribs=True)
class Product:
    code: Optional[str] = None
    name: Optional[str] = None
    first_mile_option: Optional[str] = None
    service: Optional[str] = None


@s(auto_attribs=True)
class Quote:
    gross: Optional[Base] = JStruct[Base]
    net: Optional[Base] = JStruct[Base]
    tax: Optional[Base] = JStruct[Base]


@s(auto_attribs=True)
class Route:
    type: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class Gst:
    amount: Optional[float] = None
    currency: Optional[str] = None
    rate: Optional[float] = None


@s(auto_attribs=True)
class TaxBreakdown:
    gst: Optional[Gst] = JStruct[Gst]
    hst: Optional[Gst] = JStruct[Gst]
    qst: Optional[Gst] = JStruct[Gst]


@s(auto_attribs=True)
class ProductsResponseElement:
    quote: Optional[Quote] = JStruct[Quote]
    price_breakdown: Optional[PriceBreakdown] = JStruct[PriceBreakdown]
    tax_breakdown: Optional[TaxBreakdown] = JStruct[TaxBreakdown]
    plan: Optional[str] = None
    eta: Optional[Eta] = JStruct[Eta]
    route: Optional[Route] = JStruct[Route]
    allowed_packaging: Optional[str] = None
    product: Optional[Product] = JStruct[Product]
