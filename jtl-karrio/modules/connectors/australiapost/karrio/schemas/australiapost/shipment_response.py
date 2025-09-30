import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ItemSummaryType:
    total_cost: typing.Optional[int] = None
    total_cost_ex_gst: typing.Optional[float] = None
    total_gst: typing.Optional[float] = None
    manual_handling_surcharge: typing.Optional[float] = None
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDetailsType:
    article_id: typing.Optional[str] = None
    consignment_id: typing.Optional[str] = None
    barcode_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    item_id: typing.Optional[str] = None
    item_reference: typing.Optional[str] = None
    tracking_details: typing.Optional[TrackingDetailsType] = jstruct.JStruct[TrackingDetailsType]
    product_id: typing.Optional[str] = None
    item_summary: typing.Optional[ItemSummaryType] = jstruct.JStruct[ItemSummaryType]


@attr.s(auto_attribs=True)
class ShipmentSummaryType:
    total_cost: typing.Optional[int] = None
    total_cost_ex_gst: typing.Optional[float] = None
    fuel_surcharge: typing.Optional[float] = None
    total_gst: typing.Optional[float] = None
    manual_handling_surcharge: typing.Optional[float] = None
    status: typing.Optional[str] = None
    number_of_items: typing.Optional[int] = None
    tracking_summary: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipment_id: typing.Optional[str] = None
    shipment_reference: typing.Optional[str] = None
    shipment_creation_date: typing.Optional[str] = None
    shipment_modified_date: typing.Optional[str] = None
    customer_reference_1: typing.Optional[str] = None
    customer_reference_2: typing.Optional[str] = None
    sender_references: typing.Optional[typing.List[str]] = None
    email_tracking_enabled: typing.Optional[bool] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    shipment_summary: typing.Optional[ShipmentSummaryType] = jstruct.JStruct[ShipmentSummaryType]


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
