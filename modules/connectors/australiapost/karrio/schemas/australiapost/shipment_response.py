from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ItemSummaryType:
    total_cost: Optional[int] = None
    total_cost_ex_gst: Optional[float] = None
    total_gst: Optional[float] = None
    manual_handling_surcharge: Optional[float] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class TrackingDetailsType:
    article_id: Optional[str] = None
    consignment_id: Optional[str] = None
    barcode_id: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    item_id: Optional[str] = None
    item_reference: Optional[str] = None
    tracking_details: Optional[TrackingDetailsType] = JStruct[TrackingDetailsType]
    product_id: Optional[str] = None
    item_summary: Optional[ItemSummaryType] = JStruct[ItemSummaryType]


@s(auto_attribs=True)
class ShipmentSummaryType:
    total_cost: Optional[int] = None
    total_cost_ex_gst: Optional[float] = None
    fuel_surcharge: Optional[float] = None
    total_gst: Optional[float] = None
    manual_handling_surcharge: Optional[float] = None
    status: Optional[str] = None
    number_of_items: Optional[int] = None
    tracking_summary: List[Any] = []


@s(auto_attribs=True)
class ShipmentType:
    shipment_id: Optional[str] = None
    shipment_reference: Optional[str] = None
    shipment_creation_date: Optional[str] = None
    shipment_modified_date: Optional[str] = None
    customer_reference_1: Optional[str] = None
    customer_reference_2: Optional[str] = None
    sender_references: List[str] = []
    email_tracking_enabled: Optional[bool] = None
    items: List[ItemType] = JList[ItemType]
    shipment_summary: Optional[ShipmentSummaryType] = JStruct[ShipmentSummaryType]


@s(auto_attribs=True)
class ShipmentResponseType:
    shipments: List[ShipmentType] = JList[ShipmentType]
