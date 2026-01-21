import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorMessageType:
    field: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    id: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    returnTrackingNumber: typing.Optional[str] = None
    errorMessages: typing.Optional[typing.List[ErrorMessageType]] = jstruct.JList[ErrorMessageType]
    labelLocation: typing.Optional[str] = None
    returnLabelLocation: typing.Optional[str] = None
    customsDocumentLocation: typing.Optional[str] = None
    manifestLocation: typing.Optional[str] = None
    commercialInvoiceLocation: typing.Optional[str] = None
