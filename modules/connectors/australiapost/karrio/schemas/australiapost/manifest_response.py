from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ShippingMethodsType:
    the_3_h03: Optional[int] = None


@s(auto_attribs=True)
class TrackingSummaryType:
    sealed: Optional[int] = None


@s(auto_attribs=True)
class OrderSummaryType:
    total_cost: Optional[float] = None
    total_cost_ex_gst: Optional[float] = None
    total_gst: Optional[float] = None
    status: Optional[str] = None
    tracking_summary: Optional[TrackingSummaryType] = JStruct[TrackingSummaryType]
    number_of_shipments: Optional[int] = None
    number_of_items: Optional[int] = None
    dangerous_goods_included: Optional[bool] = None
    total_weight: Optional[float] = None
    shipping_methods: Optional[ShippingMethodsType] = JStruct[ShippingMethodsType]


@s(auto_attribs=True)
class ItemSummaryType:
    total_cost: Optional[float] = None
    total_cost_ex_gst: Optional[float] = None
    total_gst: Optional[float] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class TrackingDetailsType:
    article_id: Optional[str] = None
    consignment_id: Optional[str] = None
    barcode_id: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    weight: Optional[float] = None
    authority_to_leave: Optional[bool] = None
    safe_drop_enabled: Optional[bool] = None
    allow_partial_delivery: Optional[bool] = None
    item_id: Optional[str] = None
    item_reference: Optional[str] = None
    tracking_details: Optional[TrackingDetailsType] = JStruct[TrackingDetailsType]
    product_id: Optional[str] = None
    item_summary: Optional[ItemSummaryType] = JStruct[ItemSummaryType]


@s(auto_attribs=True)
class ShipmentSummaryType:
    total_cost: Optional[float] = None
    total_cost_ex_gst: Optional[float] = None
    fuel_surcharge: Optional[float] = None
    total_gst: Optional[float] = None
    status: Optional[str] = None
    tracking_summary: Optional[TrackingSummaryType] = JStruct[TrackingSummaryType]
    number_of_items: Optional[int] = None


@s(auto_attribs=True)
class ShipmentType:
    shipment_id: Optional[str] = None
    shipment_reference: Optional[str] = None
    shipment_creation_date: Optional[str] = None
    email_tracking_enabled: Optional[bool] = None
    items: List[ItemType] = JList[ItemType]
    shipment_summary: Optional[ShipmentSummaryType] = JStruct[ShipmentSummaryType]
    movement_type: Optional[str] = None
    charge_to_account: Optional[str] = None
    shipment_modified_date: Optional[str] = None


@s(auto_attribs=True)
class OrderType:
    order_id: Optional[str] = None
    order_reference: Optional[str] = None
    order_creation_date: Optional[str] = None
    order_summary: Optional[OrderSummaryType] = JStruct[OrderSummaryType]
    shipments: List[ShipmentType] = JList[ShipmentType]
    payment_method: Optional[str] = None


@s(auto_attribs=True)
class ManifestResponseType:
    order: Optional[OrderType] = JStruct[OrderType]
