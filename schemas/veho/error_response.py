"""
Veho Error Response Schema based on OpenAPI spec
"""

import attr
import typing


@attr.s(auto_attribs=True)
class ErrorDetail:
    """Error Detail - matches OpenAPI spec"""
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    path: typing.Optional[typing.List[typing.Union[str, int]]] = None
    expected: typing.Optional[str] = None
    received: typing.Optional[str] = None
    keys: typing.Optional[typing.List[str]] = None
    options: typing.Optional[typing.List[str]] = None
    minimum: typing.Optional[float] = None
    maximum: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    """Veho Error Response - matches OpenAPI spec"""
    
    message: str
    errors: typing.Optional[typing.List[ErrorDetail]] = None
    error: typing.Optional[typing.Union[dict, str]] = None  # Legacy error field (deprecated) 
