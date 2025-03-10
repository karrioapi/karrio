import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BaseType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class QuoteType:
    gross: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    net: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    tax: typing.Optional[BaseType] = jstruct.JStruct[BaseType]


@attr.s(auto_attribs=True)
class CoverType:
    price: typing.Optional[QuoteType] = jstruct.JStruct[QuoteType]


@attr.s(auto_attribs=True)
class EtaType:
    days_range: typing.Optional[typing.List[int]] = None
    date_range: typing.Optional[typing.List[str]] = None
    for_send_date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PriceBreakdownType:
    base: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    discount: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    cover: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    fuel_surcharge: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    base_tax: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    discount_tax: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    cover_tax: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    fuel_surcharge_tax: typing.Optional[BaseType] = jstruct.JStruct[BaseType]


@attr.s(auto_attribs=True)
class ProductType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None
    first_mile_option: typing.Optional[str] = None
    service: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RouteType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class GstType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    rate: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class TaxBreakdownType:
    gst: typing.Optional[GstType] = jstruct.JStruct[GstType]


@attr.s(auto_attribs=True)
class ProductResponseElementType:
    quote: typing.Optional[QuoteType] = jstruct.JStruct[QuoteType]
    price_breakdown: typing.Optional[PriceBreakdownType] = jstruct.JStruct[PriceBreakdownType]
    tax_breakdown: typing.Optional[TaxBreakdownType] = jstruct.JStruct[TaxBreakdownType]
    plan: typing.Optional[str] = None
    eta: typing.Optional[EtaType] = jstruct.JStruct[EtaType]
    route: typing.Optional[RouteType] = jstruct.JStruct[RouteType]
    allowed_packaging: typing.Optional[str] = None
    product: typing.Optional[ProductType] = jstruct.JStruct[ProductType]
    cover: typing.Optional[CoverType] = jstruct.JStruct[CoverType]
