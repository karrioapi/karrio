from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DomesticQuoteRequest:
    pickup_suburb: Optional[str] = None
    pickup_postcode: Optional[int] = None
    pickup_country: Optional[str] = None
    delivery_suburb: Optional[str] = None
    delivery_postcode: Optional[int] = None
    delivery_country: Optional[str] = None
    weight_value: Optional[float] = None
    weight_units: Optional[str] = None
    volume_value: Optional[float] = None
    volume_units: Optional[str] = None
    first_mile_option: Optional[str] = None


@s(auto_attribs=True)
class InternationalQuoteRequest:
    pickup_suburb: Optional[str] = None
    pickup_postcode: Optional[int] = None
    delivery_country: Optional[str] = None
    weight_value: Optional[float] = None
    weight_units: Optional[str] = None
    volume_value: Optional[float] = None
    volume_units: Optional[str] = None


@s(auto_attribs=True)
class Eta:
    days_range: List[int] = []
    date_range: List[str] = []
    for_pickup_date: Optional[str] = None


@s(auto_attribs=True)
class Gross:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class QuoteClass:
    gross: Optional[Gross] = JStruct[Gross]
    net: Optional[Gross] = JStruct[Gross]
    tax: Optional[Gross] = JStruct[Gross]


@s(auto_attribs=True)
class Quote:
    quote: Optional[QuoteClass] = JStruct[QuoteClass]
    plan_name: Optional[str] = None
    eta: Optional[Eta] = JStruct[Eta]


@s(auto_attribs=True)
class Rating:
    domestic_quote_request: Optional[DomesticQuoteRequest] = JStruct[DomesticQuoteRequest]
    international_quote_request: Optional[InternationalQuoteRequest] = JStruct[InternationalQuoteRequest]
    quotes: List[Quote] = JList[Quote]
