import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FromType:
    name: typing.Optional[str] = None
    lines: typing.Optional[typing.List[str]] = None
    suburb: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[int] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    country: typing.Optional[str] = None
    business_name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class COMMERCIALCLEARANCEAttributesType:
    incoterms: typing.Optional[str] = None
    currency_code: typing.Optional[str] = None
    declared_shipping_cost: typing.Optional[str] = None
    buyer_code: typing.Optional[int] = None
    buyer: typing.Optional[FromType] = jstruct.JStruct[FromType]
    offshore_return: typing.Optional[FromType] = jstruct.JStruct[FromType]


@attr.s(auto_attribs=True)
class CommercialClearanceType:
    attributes: typing.Optional[COMMERCIALCLEARANCEAttributesType] = jstruct.JStruct[COMMERCIALCLEARANCEAttributesType]


@attr.s(auto_attribs=True)
class DELIVERYDATEAttributesType:
    date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DateType:
    attributes: typing.Optional[DELIVERYDATEAttributesType] = jstruct.JStruct[DELIVERYDATEAttributesType]


@attr.s(auto_attribs=True)
class WindowType:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DELIVERYTIMESAttributesType:
    windows: typing.Optional[typing.List[WindowType]] = jstruct.JList[WindowType]


@attr.s(auto_attribs=True)
class DeliveryTimesType:
    attributes: typing.Optional[DELIVERYTIMESAttributesType] = jstruct.JStruct[DELIVERYTIMESAttributesType]


@attr.s(auto_attribs=True)
class IDENTITYONDELIVERYAttributesType:
    id_capture_type: typing.Optional[str] = None
    redirection_enabled: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class IdentityOnDeliveryType:
    attributes: typing.Optional[IDENTITYONDELIVERYAttributesType] = jstruct.JStruct[IDENTITYONDELIVERYAttributesType]


@attr.s(auto_attribs=True)
class PICKUPTIMEAttributesType:
    time: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupTimeType:
    attributes: typing.Optional[PICKUPTIMEAttributesType] = jstruct.JStruct[PICKUPTIMEAttributesType]


@attr.s(auto_attribs=True)
class PRINTATDEPOTAttributesType:
    enabled: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PrintAtDepotType:
    attributes: typing.Optional[PRINTATDEPOTAttributesType] = jstruct.JStruct[PRINTATDEPOTAttributesType]


@attr.s(auto_attribs=True)
class SAMEDAYIDENTITYONDELIVERYAttributesType:
    id_option: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SamedayIdentityOnDeliveryType:
    attributes: typing.Optional[SAMEDAYIDENTITYONDELIVERYAttributesType] = jstruct.JStruct[SAMEDAYIDENTITYONDELIVERYAttributesType]


@attr.s(auto_attribs=True)
class FeaturesType:
    delivery_date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    delivery_times: typing.Optional[DeliveryTimesType] = jstruct.JStruct[DeliveryTimesType]
    pickup_date: typing.Optional[DateType] = jstruct.JStruct[DateType]
    pickup_time: typing.Optional[PickupTimeType] = jstruct.JStruct[PickupTimeType]
    commercial_clearance: typing.Optional[CommercialClearanceType] = jstruct.JStruct[CommercialClearanceType]
    identity_on_delivery: typing.Optional[IdentityOnDeliveryType] = jstruct.JStruct[IdentityOnDeliveryType]
    print_at_depot: typing.Optional[PrintAtDepotType] = jstruct.JStruct[PrintAtDepotType]
    sameday_identity_on_delivery: typing.Optional[SamedayIdentityOnDeliveryType] = jstruct.JStruct[SamedayIdentityOnDeliveryType]


@attr.s(auto_attribs=True)
class ItemContentType:
    country_of_origin: typing.Optional[str] = None
    description: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    tariff_code: typing.Optional[int] = None
    value: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    item_contents_reference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    item_reference: typing.Optional[str] = None
    product_id: typing.Optional[str] = None
    length: typing.Optional[float] = None
    height: typing.Optional[float] = None
    width: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    cubic_volume: typing.Optional[float] = None
    authority_to_leave: typing.Optional[bool] = None
    allow_partial_delivery: typing.Optional[bool] = None
    contains_dangerous_goods: typing.Optional[bool] = None
    transportable_by_air: typing.Optional[bool] = None
    item_description: typing.Optional[str] = None
    features: typing.Optional[FeaturesType] = jstruct.JStruct[FeaturesType]
    classification_type: typing.Optional[str] = None
    commercial_value: typing.Optional[bool] = None
    description_of_other: typing.Optional[str] = None
    export_declaration_number: typing.Optional[int] = None
    import_reference_number: typing.Optional[int] = None
    item_contents: typing.Optional[typing.List[ItemContentType]] = jstruct.JList[ItemContentType]


@attr.s(auto_attribs=True)
class ShipmentType:
    shipment_reference: typing.Optional[str] = None
    customer_reference_1: typing.Optional[str] = None
    customer_reference_2: typing.Optional[str] = None
    email_tracking_enabled: typing.Optional[bool] = None
    shipment_from: typing.Optional[FromType] = jstruct.JStruct[FromType]
    to: typing.Optional[FromType] = jstruct.JStruct[FromType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    movement_type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
