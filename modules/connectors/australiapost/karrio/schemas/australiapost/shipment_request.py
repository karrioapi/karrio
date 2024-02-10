from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


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
class COMMERCIALCLEARANCEAttributesType:
    incoterms: Optional[str] = None
    currency_code: Optional[str] = None
    declared_shipping_cost: Optional[str] = None
    buyer_code: Optional[int] = None
    buyer: Optional[FromType] = JStruct[FromType]
    offshore_return: Optional[FromType] = JStruct[FromType]


@s(auto_attribs=True)
class CommercialClearanceType:
    attributes: Optional[COMMERCIALCLEARANCEAttributesType] = JStruct[
        COMMERCIALCLEARANCEAttributesType
    ]


@s(auto_attribs=True)
class DELIVERYDATEAttributesType:
    date: Optional[str] = None


@s(auto_attribs=True)
class DateType:
    attributes: Optional[DELIVERYDATEAttributesType] = JStruct[
        DELIVERYDATEAttributesType
    ]


@s(auto_attribs=True)
class WindowType:
    start: Optional[str] = None
    end: Optional[str] = None


@s(auto_attribs=True)
class DELIVERYTIMESAttributesType:
    windows: List[WindowType] = JList[WindowType]


@s(auto_attribs=True)
class DeliveryTimesType:
    attributes: Optional[DELIVERYTIMESAttributesType] = JStruct[
        DELIVERYTIMESAttributesType
    ]


@s(auto_attribs=True)
class IDENTITYONDELIVERYAttributesType:
    id_capture_type: Optional[str] = None
    redirection_enabled: Optional[bool] = None


@s(auto_attribs=True)
class IdentityOnDeliveryType:
    attributes: Optional[IDENTITYONDELIVERYAttributesType] = JStruct[
        IDENTITYONDELIVERYAttributesType
    ]


@s(auto_attribs=True)
class PICKUPTIMEAttributesType:
    time: Optional[str] = None


@s(auto_attribs=True)
class PickupTimeType:
    attributes: Optional[PICKUPTIMEAttributesType] = JStruct[PICKUPTIMEAttributesType]


@s(auto_attribs=True)
class PRINTATDEPOTAttributesType:
    enabled: Optional[bool] = None


@s(auto_attribs=True)
class PrintAtDepotType:
    attributes: Optional[PRINTATDEPOTAttributesType] = JStruct[
        PRINTATDEPOTAttributesType
    ]


@s(auto_attribs=True)
class SAMEDAYIDENTITYONDELIVERYAttributesType:
    id_option: Optional[str] = None


@s(auto_attribs=True)
class SamedayIdentityOnDeliveryType:
    attributes: Optional[SAMEDAYIDENTITYONDELIVERYAttributesType] = JStruct[
        SAMEDAYIDENTITYONDELIVERYAttributesType
    ]


@s(auto_attribs=True)
class FeaturesType:
    DELIVERY_DATE: Optional[DateType] = JStruct[DateType]
    DELIVERY_TIMES: Optional[DeliveryTimesType] = JStruct[DeliveryTimesType]
    PICKUP_DATE: Optional[DateType] = JStruct[DateType]
    PICKUP_TIME: Optional[PickupTimeType] = JStruct[PickupTimeType]
    COMMERCIAL_CLEARANCE: Optional[CommercialClearanceType] = JStruct[
        CommercialClearanceType
    ]
    IDENTITY_ON_DELIVERY: Optional[IdentityOnDeliveryType] = JStruct[
        IdentityOnDeliveryType
    ]
    PRINT_AT_DEPOT: Optional[PrintAtDepotType] = JStruct[PrintAtDepotType]
    SAMEDAY_IDENTITY_ON_DELIVERY: Optional[SamedayIdentityOnDeliveryType] = JStruct[
        SamedayIdentityOnDeliveryType
    ]


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
    contains_dangerous_goods: Optional[bool] = None
    transportable_by_air: Optional[bool] = None
    item_description: Optional[str] = None
    features: Optional[FeaturesType] = JStruct[FeaturesType]
    classification_type: Optional[str] = None
    commercial_value: Optional[bool] = None
    description_of_other: Optional[str] = None
    export_declaration_number: Optional[int] = None
    import_reference_number: Optional[int] = None
    item_contents: List[ItemContentType] = JList[ItemContentType]


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
