from attr import s
from typing import Optional, Any, List
from jstruct import JList


@s(auto_attribs=True)
class ItemType:
    item_id: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    shipment_id: Optional[str] = None
    options: List[Any] = []
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class LabelType:
    request_id: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    request_date: Optional[str] = None
    url_creation_date: Optional[str] = None
    shipments: List[ShipmentType] = JList[ShipmentType]
    shipment_ids: List[str] = []


@s(auto_attribs=True)
class LabelResponseType:
    labels: List[LabelType] = JList[LabelType]
