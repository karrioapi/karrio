import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ListOfResultCodeType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCancelResponseType:
    listOfResultCodes: typing.Optional[typing.List[ListOfResultCodeType]] = jstruct.JList[ListOfResultCodeType]
    shipmentOrderID: typing.Optional[str] = None
