import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class GroupType:
    group: typing.Optional[str] = None
    layout: typing.Optional[str] = None
    branded: typing.Optional[bool] = None
    left_offset: typing.Optional[int] = None
    top_offset: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PreferenceType:
    type: typing.Optional[str] = None
    format: typing.Optional[str] = None
    groups: typing.Optional[typing.List[GroupType]] = jstruct.JList[GroupType]


@attr.s(auto_attribs=True)
class ItemType:
    item_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipment_id: typing.Optional[str] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class LabelRequestType:
    wait_for_label_url: typing.Optional[bool] = None
    preferences: typing.Optional[typing.List[PreferenceType]] = jstruct.JList[PreferenceType]
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
