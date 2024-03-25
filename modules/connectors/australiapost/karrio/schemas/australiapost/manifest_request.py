from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class ShipmentType:
    shipment_id: Optional[str] = None


@s(auto_attribs=True)
class ManifestRequestType:
    order_reference: Optional[str] = None
    payment_method: Optional[str] = None
    consignor: Optional[str] = None
    shipments: List[ShipmentType] = JList[ShipmentType]
