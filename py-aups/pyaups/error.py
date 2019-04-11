"""Australia Post Errors Datatype definition module."""

import attr
from typing import List, Optional
from jstruct import JList


@attr.s(auto_attribs=True)
class PostageError:
    errorMessage: Optional[str] = None


@attr.s(auto_attribs=True)
class APIError:
    code: Optional[str] = None
    message: Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    status: Optional[str] = None
    errors: List[APIError] = JList[APIError]
    error: List[PostageError] = JList[PostageError]
