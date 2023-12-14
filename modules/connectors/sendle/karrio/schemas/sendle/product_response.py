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
    daysrange: List[int] = []
    daterange: List[str] = []
    forsenddate: Optional[str] = None


@s(auto_attribs=True)
class PriceBreakdownType:
    base: Optional[BaseType] = JStruct[BaseType]
    discount: Optional[BaseType] = JStruct[BaseType]
    cover: Optional[BaseType] = JStruct[BaseType]
    fuelsurcharge: Optional[BaseType] = JStruct[BaseType]
    basetax: Optional[BaseType] = JStruct[BaseType]
    discounttax: Optional[BaseType] = JStruct[BaseType]
    covertax: Optional[BaseType] = JStruct[BaseType]
    fuelsurchargetax: Optional[BaseType] = JStruct[BaseType]


@s(auto_attribs=True)
class ProductType:
    code: Optional[str] = None
    name: Optional[str] = None
    firstmileoption: Optional[str] = None
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
    pricebreakdown: Optional[PriceBreakdownType] = JStruct[PriceBreakdownType]
    taxbreakdown: Optional[TaxBreakdownType] = JStruct[TaxBreakdownType]
    plan: Optional[str] = None
    eta: Optional[EtaType] = JStruct[EtaType]
    route: Optional[RouteType] = JStruct[RouteType]
    allowedpackaging: Optional[str] = None
    product: Optional[ProductType] = JStruct[ProductType]
    cover: Optional[CoverType] = JStruct[CoverType]
