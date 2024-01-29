from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AttributesType:
    cover_amount: Optional[float] = None
    rate: Optional[float] = None
    included_cover: Optional[float] = None
    maximum_cover: Optional[float] = None


@s(auto_attribs=True)
class FeatureType:
    attributes: Optional[AttributesType] = JStruct[AttributesType]


@s(auto_attribs=True)
class FeaturesType:
    feature: Optional[FeatureType] = JStruct[FeatureType]


@s(auto_attribs=True)
class ItemContentType:
    country_of_origin: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[int] = None
    tariff_code: Optional[int] = None
    value: Optional[float] = None
    weight: Optional[float] = None
    item_contents_reference: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    item_reference: Optional[str] = None
    product_id: Optional[str] = None
    length: Optional[float] = None
    height: Optional[float] = None
    width: Optional[float] = None
    weight: Optional[float] = None
    cubic_volume: Optional[float] = None
    authority_to_leave: Optional[bool] = None
    allow_partial_delivery: Optional[bool] = None
    item_description: Optional[str] = None
    features: Optional[dict] = {}
    classification_type: Optional[str] = None
    commercial_value: Optional[bool] = None
    description_of_other: Optional[str] = None
    export_declaration_number: Optional[int] = None
    import_reference_number: Optional[int] = None
    item_contents: List[ItemContentType] = JList[ItemContentType]
    contains_dangerous_goods: Optional[bool] = None


@s(auto_attribs=True)
class FromType:
    name: Optional[str] = None
    lines: List[str] = []
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    business_name: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    shipment_reference: Optional[str] = None
    customer_reference_1: Optional[str] = None
    customer_reference_2: Optional[str] = None
    email_tracking_enabled: Optional[bool] = None
    shipment_from: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    items: List[ItemType] = JList[ItemType]
    movement_type: Optional[str] = None


@s(auto_attribs=True)
class ShipmentRequestType:
    shipments: List[ShipmentType] = JList[ShipmentType]
