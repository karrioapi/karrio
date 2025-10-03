import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class SuccessConsignmentType:
    success: typing.Optional[bool] = None
    referencenumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCancelResponseType:
    status: typing.Optional[str] = None
    success: typing.Optional[bool] = None
    successConsignments: typing.Optional[typing.List[SuccessConsignmentType]] = jstruct.JList[SuccessConsignmentType]
