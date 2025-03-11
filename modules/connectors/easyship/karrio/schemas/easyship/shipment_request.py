import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BuyerRegulatoryIdentifiersType:
    ein: typing.Optional[str] = None
    vat_number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CourierSelectionType:
    allow_courier_fallback: typing.Optional[bool] = None
    apply_shipping_rules: typing.Optional[bool] = None
    list_unavailable_couriers: typing.Optional[bool] = None
    selected_courier_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    city: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    contact_email: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    contact_phone: typing.Optional[str] = None
    country_alpha2: typing.Optional[str] = None
    line_1: typing.Optional[str] = None
    line_2: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InsuranceType:
    is_insured: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class OrderDataType:
    buyer_notes: typing.Optional[str] = None
    buyer_selected_courier_name: typing.Optional[str] = None
    order_created_at: typing.Optional[str] = None
    platform_name: typing.Optional[str] = None
    platform_order_number: typing.Optional[str] = None
    order_tag_list: typing.Optional[typing.List[str]] = None
    seller_notes: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BoxType:
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    slug: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    actual_weight: typing.Optional[int] = None
    category: typing.Any = None
    contains_battery_pi966: typing.Optional[bool] = None
    contains_battery_pi967: typing.Optional[bool] = None
    contains_liquids: typing.Optional[bool] = None
    declared_currency: typing.Optional[str] = None
    declared_customs_value: typing.Optional[int] = None
    description: typing.Optional[str] = None
    dimensions: typing.Optional[BoxType] = jstruct.JStruct[BoxType]
    hs_code: typing.Optional[int] = None
    origin_country_alpha2: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    sku: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    box: typing.Optional[BoxType] = jstruct.JStruct[BoxType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    total_actual_weight: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RegulatoryIdentifiersType:
    eori: typing.Optional[str] = None
    ioss: typing.Optional[str] = None
    vat_number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdditionalServicesType:
    delivery_confirmation: typing.Optional[str] = None
    qr_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class B13AFilingType:
    option: typing.Optional[str] = None
    option_export_compliance_statement: typing.Optional[str] = None
    permit_number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PrintingOptionsType:
    commercial_invoice: typing.Optional[str] = None
    format: typing.Optional[str] = None
    label: typing.Optional[str] = None
    packing_slip: typing.Optional[str] = None
    remarks: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UnitsType:
    dimensions: typing.Optional[str] = None
    weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingSettingsType:
    additional_services: typing.Optional[AdditionalServicesType] = jstruct.JStruct[AdditionalServicesType]
    b13_a_filing: typing.Optional[B13AFilingType] = jstruct.JStruct[B13AFilingType]
    buy_label: typing.Optional[bool] = None
    buy_label_synchronous: typing.Optional[bool] = None
    printing_options: typing.Optional[PrintingOptionsType] = jstruct.JStruct[PrintingOptionsType]
    units: typing.Optional[UnitsType] = jstruct.JStruct[UnitsType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    buyer_regulatory_identifiers: typing.Optional[BuyerRegulatoryIdentifiersType] = jstruct.JStruct[BuyerRegulatoryIdentifiersType]
    courier_selection: typing.Optional[CourierSelectionType] = jstruct.JStruct[CourierSelectionType]
    destination_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    consignee_tax_id: typing.Optional[int] = None
    eei_reference: typing.Optional[int] = None
    incoterms: typing.Optional[str] = None
    metadata: typing.Optional[typing.List[typing.Any]] = None
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    order_data: typing.Optional[OrderDataType] = jstruct.JStruct[OrderDataType]
    origin_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    regulatory_identifiers: typing.Optional[RegulatoryIdentifiersType] = jstruct.JStruct[RegulatoryIdentifiersType]
    shipment_request_return: typing.Optional[bool] = None
    return_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    return_address_id: typing.Optional[str] = None
    sender_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    sender_address_id: typing.Optional[str] = None
    set_as_residential: typing.Optional[bool] = None
    shipping_settings: typing.Optional[ShippingSettingsType] = jstruct.JStruct[ShippingSettingsType]
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
