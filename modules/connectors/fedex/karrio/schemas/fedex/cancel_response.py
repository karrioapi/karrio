import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AlertType:
    code: typing.Optional[str] = None
    alertType: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OutputType:
    cancelledShipment: typing.Optional[bool] = None
    cancelledHistory: typing.Optional[bool] = None
    successMessage: typing.Optional[str] = None
    alerts: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]


@attr.s(auto_attribs=True)
class CancelResponseType:
    transactionId: typing.Optional[str] = None
    customerTransactionId: typing.Optional[str] = None
    output: typing.Optional[OutputType] = jstruct.JStruct[OutputType]
