import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ItemType:
    item_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipment_id: typing.Optional[str] = None
    options: typing.Optional[typing.List[typing.Any]] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class LabelType:
    request_id: typing.Optional[str] = None
    url: typing.Optional[str] = None
    status: typing.Optional[str] = None
    request_date: typing.Optional[str] = None
    url_creation_date: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
    shipment_ids: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class LabelResponseType:
    labels: typing.Optional[typing.List[LabelType]] = jstruct.JList[LabelType]
