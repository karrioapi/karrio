"""Australia Post Errors Datatype definition module."""

import attr
from typing import Optional, List
from jstruct import JList


@attr.s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    name: Optional[str] = None
    error_code: Optional[str] = None
    error_name: Optional[str] = None
    message: Optional[str] = None
    field: Optional[str] = None
    context: Optional[dict] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    errors: Optional[List[Error]] = None
