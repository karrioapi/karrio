"""Sendle Quotes Datatypes definition module."""

import attr
from typing import List
from jstruct import JStruct


@attr.s(auto_attribs=True)
class DomesticParcelQuote:
    pickup_suburb: str = None
    pickup_postcode: str = None
    delivery_suburb: str = None
    delivery_postcode: str = None
    kilogram_weight: str = None
    cubic_metre_volume: str = None
    plan_name: str = None


@attr.s(auto_attribs=True)
class InternationalParcelQuote:
    pickup_suburb: str = None
    pickup_postcode: str = None
    delivery_country: str = None
    kilogram_weight: str = None
    cubic_metre_volume: str = None
    plan_name: str = None


@attr.s(auto_attribs=True)
class Pricing:
    amount: float = None
    currency: str = None


@attr.s(auto_attribs=True)
class Quote:
    gross: Pricing = JStruct[Pricing]
    net: Pricing = JStruct[Pricing]
    tax: Pricing = JStruct[Pricing]


@attr.s(auto_attribs=True)
class Eta:
    days_range: List[int] = None
    date_range: List[str] = None
    for_pickup_date: str = None


@attr.s(auto_attribs=True)
class Route:
    type: str = None
    description: str = None


@attr.s(auto_attribs=True)
class ParcelQuoteResponse:
    quote: Quote = JStruct[Quote]
    plan_name: str = None
    eta: Eta = JStruct[Eta]
    route: Route = JStruct[Route]
