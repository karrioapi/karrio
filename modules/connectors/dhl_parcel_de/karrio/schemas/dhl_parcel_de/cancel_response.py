import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelType:
    url: typing.Optional[str] = None
    format: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SstatusType:
    title: typing.Optional[str] = None
    status: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ItemType:
    shipmentNo: typing.Optional[int] = None
    sstatus: typing.Optional[SstatusType] = jstruct.JStruct[SstatusType]
    label: typing.Optional[LabelType] = jstruct.JStruct[LabelType]


@attr.s(auto_attribs=True)
class StatusType:
    title: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    instance: typing.Optional[str] = None
    detail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CancelResponseType:
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
