"""
Veho Rate Response Schema based on OpenAPI spec
"""

import attr
import typing


@attr.s(auto_attribs=True)
class SimpleQuoteItem:
    """Veho Simple Quote Item - matches OpenAPI spec"""
    
    quoteId: typing.Optional[str] = None
    transitTime: typing.Optional[float] = None
    serviceClass: typing.Optional[str] = None
    currency: typing.Optional[str] = "USD"
    rate: typing.Optional[float] = None
    assumedInjectionZip: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    billableWeight: typing.Optional[float] = None
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    zone: typing.Optional[str] = None


# SimpleQuoteResponse is an array of SimpleQuoteItem objects
SimpleQuoteResponse = typing.List[SimpleQuoteItem] 
