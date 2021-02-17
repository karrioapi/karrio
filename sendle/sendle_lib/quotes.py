import attr
from jstruct import JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class DomesticQuoteRequest:
    pickup_postcode: Optional[int] = None
    delivery_postcode: Optional[int] = None
    pickup_suburb: Optional[str] = None
    pickup_country: Optional[str] = None
    delivery_suburb: Optional[str] = None
    delivery_country: Optional[str] = None
    weight_value: Optional[int] = None
    weight_units: Optional[str] = None
    volume_value: Optional[float] = None
    volume_units: Optional[str] = None
    first_mile_option: Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalQuoteRequest:
    pickup_postcode: Optional[int] = None
    pickup_suburb: Optional[str] = None
    delivery_country: Optional[str] = None
    weight_value: Optional[int] = None
    weight_units: Optional[str] = None
    volume_value: Optional[float] = None
    volume_units: Optional[str] = None


@attr.s(auto_attribs=True)
class Eta:
    days_range: Optional[List[int]] = None
    date_range: Optional[List[str]] = None
    for_pickup_date: Optional[str] = None


@attr.s(auto_attribs=True)
class Price:
    amount: Optional[float] = None
    currency: Optional[str] = None


@attr.s(auto_attribs=True)
class QuotePrice:
    gross: Optional[Price] = JStruct[Price]
    net: Optional[Price] = JStruct[Price]
    tax: Optional[Price] = JStruct[Price]


@attr.s(auto_attribs=True)
class Quote:
    quote: Optional[QuotePrice] = JStruct[QuotePrice]
    plan_name: Optional[str] = None
    eta: Optional[Eta] = JStruct[Eta]
