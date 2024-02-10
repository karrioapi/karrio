from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class GroupType:
    group: Optional[str] = None
    layout: Optional[str] = None
    branded: Optional[bool] = None
    left_offset: Optional[int] = None
    top_offset: Optional[int] = None


@s(auto_attribs=True)
class PreferenceType:
    type: Optional[str] = None
    format: Optional[str] = None
    groups: List[GroupType] = JList[GroupType]


@s(auto_attribs=True)
class ItemType:
    item_id: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    shipment_id: Optional[str] = None
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class LabelRequestType:
    wait_for_label_url: Optional[bool] = None
    preferences: List[PreferenceType] = JList[PreferenceType]
    shipments: List[ShipmentType] = JList[ShipmentType]
