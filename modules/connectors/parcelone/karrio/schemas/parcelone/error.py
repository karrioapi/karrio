"""ParcelOne REST API v1 - Error Types."""

import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorDetailType:
    """Error detail information."""

    ErrorNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    """API error response."""

    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    errors: typing.Optional[typing.List[ErrorDetailType]] = jstruct.JList[ErrorDetailType]
    UniqId: typing.Optional[str] = None
