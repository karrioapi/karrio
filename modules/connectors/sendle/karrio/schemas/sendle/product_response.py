from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class BaseType:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class QuoteType:
    gross: Optional[BaseType] = JStruct[BaseType]
    net: Optional[BaseType] = JStruct[BaseType]
    tax: Optional[BaseType] = JStruct[BaseType]


@s(auto_attribs=True)
class CoverType:
    price: Optional[QuoteType] = JStruct[QuoteType]


@s(auto_attribs=True)
class EtaType:
    days_range: List[int] = []
    date_range: List[str] = []
    for_send_date: Optional[str] = None


@s(auto_attribs=True)
class PriceBreakdownType:
    base: Optional[BaseType] = JStruct[BaseType]
    discount: Optional[BaseType] = JStruct[BaseType]
    cover: Optional[BaseType] = JStruct[BaseType]
    fuel_surcharge: Optional[BaseType] = JStruct[BaseType]
    base_tax: Optional[BaseType] = JStruct[BaseType]
    discount_tax: Optional[BaseType] = JStruct[BaseType]
    cover_tax: Optional[BaseType] = JStruct[BaseType]
    fuel_surcharge_tax: Optional[BaseType] = JStruct[BaseType]


@s(auto_attribs=True)
class ProductType:
    code: Optional[str] = None
    name: Optional[str] = None
    first_mile_option: Optional[str] = None
    service: Optional[str] = None


@s(auto_attribs=True)
class RouteType:
    type: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class GstType:
    amount: Optional[float] = None
    currency: Optional[str] = None
    rate: Optional[float] = None


@s(auto_attribs=True)
class TaxBreakdownType:
    gst: Optional[GstType] = JStruct[GstType]


@s(auto_attribs=True)
class ProductResponseElementType:
    quote: Optional[QuoteType] = JStruct[QuoteType]
    price_breakdown: Optional[PriceBreakdownType] = JStruct[PriceBreakdownType]
    tax_breakdown: Optional[TaxBreakdownType] = JStruct[TaxBreakdownType]
    plan: Optional[str] = None
    eta: Optional[EtaType] = JStruct[EtaType]
    route: Optional[RouteType] = JStruct[RouteType]
    allowed_packaging: Optional[str] = None
    product: Optional[ProductType] = JStruct[ProductType]
    cover: Optional[CoverType] = JStruct[CoverType]
