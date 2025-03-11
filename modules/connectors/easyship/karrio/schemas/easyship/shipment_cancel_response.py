import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetaType:
    request_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SuccessType:
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCancelResponseType:
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]
    success: typing.Optional[SuccessType] = jstruct.JStruct[SuccessType]
