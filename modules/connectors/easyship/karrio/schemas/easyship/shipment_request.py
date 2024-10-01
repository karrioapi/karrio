from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class BuyerRegulatoryIdentifiersType:
    ein: Optional[str] = None
    vat_number: Optional[str] = None


@s(auto_attribs=True)
class CourierSelectionType:
    allow_courier_fallback: Optional[bool] = None
    apply_shipping_rules: Optional[bool] = None
    list_unavailable_couriers: Optional[bool] = None
    selected_courier_id: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    city: Optional[str] = None
    company_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    country_alpha2: Optional[str] = None
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None


@s(auto_attribs=True)
class InsuranceType:
    is_insured: Optional[bool] = None


@s(auto_attribs=True)
class OrderDataType:
    buyer_notes: Optional[str] = None
    buyer_selected_courier_name: Optional[str] = None
    order_created_at: Optional[str] = None
    platform_name: Optional[str] = None
    platform_order_number: Optional[str] = None
    order_tag_list: List[str] = []
    seller_notes: Optional[str] = None


@s(auto_attribs=True)
class BoxType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    slug: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    actual_weight: Optional[int] = None
    category: Any = None
    contains_battery_pi966: Optional[bool] = None
    contains_battery_pi967: Optional[bool] = None
    contains_liquids: Optional[bool] = None
    declared_currency: Optional[str] = None
    declared_customs_value: Optional[int] = None
    description: Optional[str] = None
    dimensions: Optional[BoxType] = JStruct[BoxType]
    hs_code: Optional[int] = None
    origin_country_alpha2: Optional[str] = None
    quantity: Optional[int] = None
    sku: Optional[str] = None


@s(auto_attribs=True)
class ParcelType:
    box: Optional[BoxType] = JStruct[BoxType]
    items: List[ItemType] = JList[ItemType]
    total_actual_weight: Optional[int] = None


@s(auto_attribs=True)
class RegulatoryIdentifiersType:
    eori: Optional[str] = None
    ioss: Optional[str] = None
    vat_number: Optional[str] = None


@s(auto_attribs=True)
class AdditionalServicesType:
    delivery_confirmation: Optional[str] = None
    qr_code: Optional[str] = None


@s(auto_attribs=True)
class B13AFilingType:
    option: Optional[str] = None
    option_export_compliance_statement: Optional[str] = None
    permit_number: Optional[str] = None


@s(auto_attribs=True)
class PrintingOptionsType:
    commercial_invoice: Optional[str] = None
    format: Optional[str] = None
    label: Optional[str] = None
    packing_slip: Optional[str] = None
    remarks: Optional[str] = None


@s(auto_attribs=True)
class UnitsType:
    dimensions: Optional[str] = None
    weight: Optional[str] = None


@s(auto_attribs=True)
class ShippingSettingsType:
    additional_services: Optional[AdditionalServicesType] = JStruct[AdditionalServicesType]
    b13_a_filing: Optional[B13AFilingType] = JStruct[B13AFilingType]
    buy_label: Optional[bool] = None
    buy_label_synchronous: Optional[bool] = None
    printing_options: Optional[PrintingOptionsType] = JStruct[PrintingOptionsType]
    units: Optional[UnitsType] = JStruct[UnitsType]


@s(auto_attribs=True)
class ShipmentRequestType:
    buyer_regulatory_identifiers: Optional[BuyerRegulatoryIdentifiersType] = JStruct[BuyerRegulatoryIdentifiersType]
    courier_selection: Optional[CourierSelectionType] = JStruct[CourierSelectionType]
    destination_address: Optional[AddressType] = JStruct[AddressType]
    consignee_tax_id: Optional[int] = None
    eei_reference: Optional[int] = None
    incoterms: Optional[str] = None
    metadata: List[Any] = []
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]
    order_data: Optional[OrderDataType] = JStruct[OrderDataType]
    origin_address: Optional[AddressType] = JStruct[AddressType]
    regulatory_identifiers: Optional[RegulatoryIdentifiersType] = JStruct[RegulatoryIdentifiersType]
    shipment_request_return: Optional[bool] = None
    return_address: Optional[AddressType] = JStruct[AddressType]
    return_address_id: Optional[str] = None
    sender_address: Optional[AddressType] = JStruct[AddressType]
    sender_address_id: Optional[str] = None
    set_as_residential: Optional[bool] = None
    shipping_settings: Optional[ShippingSettingsType] = JStruct[ShippingSettingsType]
    parcels: List[ParcelType] = JList[ParcelType]
