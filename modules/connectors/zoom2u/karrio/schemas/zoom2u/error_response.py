import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ModelStateType:
    getQuoteRequestPickupSuburb: typing.Optional[typing.List[str]] = None
    getQuoteRequestPickupPostcode: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    errorcode: typing.Optional[str] = None
    message: typing.Optional[str] = None
    modelState: typing.Optional[ModelStateType] = jstruct.JStruct[ModelStateType]
