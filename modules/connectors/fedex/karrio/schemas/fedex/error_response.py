import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    transactionId: typing.Optional[str] = None
    customerTransactionId: typing.Optional[str] = None
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
