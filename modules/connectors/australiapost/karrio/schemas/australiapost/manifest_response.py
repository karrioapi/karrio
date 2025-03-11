import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShippingMethodsType:
    the_3_h03: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TrackingSummaryType:
    sealed: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class OrderSummaryType:
    total_cost: typing.Optional[float] = None
    total_cost_ex_gst: typing.Optional[float] = None
    total_gst: typing.Optional[float] = None
    status: typing.Optional[str] = None
    tracking_summary: typing.Optional[TrackingSummaryType] = jstruct.JStruct[TrackingSummaryType]
    number_of_shipments: typing.Optional[int] = None
    number_of_items: typing.Optional[int] = None
    dangerous_goods_included: typing.Optional[bool] = None
    total_weight: typing.Optional[float] = None
    shipping_methods: typing.Optional[ShippingMethodsType] = jstruct.JStruct[ShippingMethodsType]


@attr.s(auto_attribs=True)
class ItemSummaryType:
    total_cost: typing.Optional[float] = None
    total_cost_ex_gst: typing.Optional[float] = None
    total_gst: typing.Optional[float] = None
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDetailsType:
    article_id: typing.Optional[str] = None
    consignment_id: typing.Optional[str] = None
    barcode_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    weight: typing.Optional[float] = None
    authority_to_leave: typing.Optional[bool] = None
    safe_drop_enabled: typing.Optional[bool] = None
    allow_partial_delivery: typing.Optional[bool] = None
    item_id: typing.Optional[str] = None
    item_reference: typing.Optional[str] = None
    tracking_details: typing.Optional[TrackingDetailsType] = jstruct.JStruct[TrackingDetailsType]
    product_id: typing.Optional[str] = None
    item_summary: typing.Optional[ItemSummaryType] = jstruct.JStruct[ItemSummaryType]


@attr.s(auto_attribs=True)
class ShipmentSummaryType:
    total_cost: typing.Optional[float] = None
    total_cost_ex_gst: typing.Optional[float] = None
    fuel_surcharge: typing.Optional[float] = None
    total_gst: typing.Optional[float] = None
    status: typing.Optional[str] = None
    tracking_summary: typing.Optional[TrackingSummaryType] = jstruct.JStruct[TrackingSummaryType]
    number_of_items: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipment_id: typing.Optional[str] = None
    shipment_reference: typing.Optional[str] = None
    shipment_creation_date: typing.Optional[str] = None
    email_tracking_enabled: typing.Optional[bool] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    shipment_summary: typing.Optional[ShipmentSummaryType] = jstruct.JStruct[ShipmentSummaryType]
    movement_type: typing.Optional[str] = None
    charge_to_account: typing.Optional[str] = None
    shipment_modified_date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderType:
    order_id: typing.Optional[str] = None
    order_reference: typing.Optional[str] = None
    order_creation_date: typing.Optional[str] = None
    order_summary: typing.Optional[OrderSummaryType] = jstruct.JStruct[OrderSummaryType]
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
    payment_method: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManifestResponseType:
    order: typing.Optional[OrderType] = jstruct.JStruct[OrderType]
