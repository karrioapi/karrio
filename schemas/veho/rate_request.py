"""
Veho Rate Request Schema based on OpenAPI spec
"""

import attr
import typing


@attr.s(auto_attribs=True)
class Package:
    """Package for quote request"""
    length: float
    width: float
    height: float
    weight: float


@attr.s(auto_attribs=True)
class SimpleQuoteRequest:
    """Veho Simple Quote Request - matches OpenAPI spec"""
    
    originationZip: str
    deliveryZip: str
    packages: typing.List[Package]
    shipDate: typing.Optional[str] = None
    serviceClass: typing.Optional[str] = "groundPlus" 
