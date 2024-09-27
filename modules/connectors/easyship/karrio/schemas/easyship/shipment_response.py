from attr import s
from typing import Optional, List, Any
from jstruct import JList, JStruct


@s(auto_attribs=True)
class UnavailableCourierType:
    id: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class MetaType:
    request_id: Optional[str] = None
    status: Optional[str] = None
    unavailable_couriers: List[UnavailableCourierType] = JList[UnavailableCourierType]
    errors: List[str] = []


@s(auto_attribs=True)
class BuyerRegulatoryIdentifiersType:
    ein: Optional[str] = None
    vat_number: Optional[str] = None


@s(auto_attribs=True)
class CourierType:
    id: Optional[str] = None
    name: Optional[str] = None


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
    insured_amount: Optional[int] = None
    insured_currency: Optional[str] = None
    is_insured: Optional[bool] = None


@s(auto_attribs=True)
class LastFailureHTTPResponseMessageType:
    code: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class OrderDataType:
    buyer_notes: Optional[str] = None
    buyer_selected_courier_name: Optional[str] = None
    order_created_at: Optional[str] = None
    order_tag_list: List[str] = []
    platform_name: Optional[str] = None
    platform_order_number: Optional[str] = None
    seller_notes: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None


@s(auto_attribs=True)
class BoxType:
    id: Optional[str] = None
    name: Optional[str] = None
    outer_dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    slug: Optional[str] = None
    type: Optional[str] = None
    weight: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    actual_weight: Optional[int] = None
    category: Optional[str] = None
    contains_battery_pi966: Optional[bool] = None
    contains_battery_pi967: Optional[bool] = None
    contains_liquids: Optional[bool] = None
    declared_currency: Optional[str] = None
    declared_customs_value: Optional[int] = None
    description: Optional[str] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    hs_code: Optional[int] = None
    id: Optional[str] = None
    origin_country_alpha2: Optional[str] = None
    origin_currency: Optional[str] = None
    origin_customs_value: Optional[int] = None
    quantity: Optional[int] = None
    sku: Optional[str] = None


@s(auto_attribs=True)
class ParcelType:
    box: Optional[BoxType] = JStruct[BoxType]
    id: Optional[str] = None
    items: List[ItemType] = JList[ItemType]
    total_actual_weight: Optional[int] = None


@s(auto_attribs=True)
class DetailType:
    fee: Optional[int] = None
    name: Optional[str] = None
    origin_fee: Optional[int] = None


@s(auto_attribs=True)
class OtherSurchargesType:
    details: List[DetailType] = JList[DetailType]
    total_fee: Optional[int] = None


@s(auto_attribs=True)
class RatesInOriginCurrencyType:
    additional_services_surcharge: Optional[int] = None
    currency: Optional[str] = None
    ddp_handling_fee: Optional[str] = None
    estimated_import_duty: Optional[str] = None
    estimated_import_tax: Optional[str] = None
    fuel_surcharge: Optional[int] = None
    import_duty_charge: Optional[str] = None
    import_tax_charge: Optional[str] = None
    import_tax_non_chargeable: Optional[str] = None
    insurance_fee: Optional[int] = None
    minimum_pickup_fee: Optional[int] = None
    oversized_surcharge: Optional[int] = None
    provincial_sales_tax: Optional[int] = None
    remote_area_surcharge: Optional[int] = None
    residential_discounted_fee: Optional[int] = None
    residential_full_fee: Optional[int] = None
    sales_tax: Optional[int] = None
    shipment_charge: Optional[int] = None
    shipment_charge_total: Optional[int] = None
    total_charge: Optional[int] = None
    warehouse_handling_fee: Optional[int] = None


@s(auto_attribs=True)
class RateType:
    additional_services_surcharge: Optional[int] = None
    available_handover_options: List[str] = []
    cost_rank: Optional[int] = None
    courier_id: Optional[str] = None
    courier_logo_url: Optional[str] = None
    courier_name: Optional[str] = None
    courier_remarks: Optional[str] = None
    currency: Optional[str] = None
    ddp_handling_fee: Optional[str] = None
    delivery_time_rank: Optional[int] = None
    description: Optional[str] = None
    discount: Optional[str] = None
    easyship_rating: Optional[int] = None
    estimated_import_duty: Optional[str] = None
    estimated_import_tax: Optional[str] = None
    fuel_surcharge: Optional[int] = None
    full_description: Optional[str] = None
    import_duty_charge: Optional[str] = None
    import_tax_charge: Optional[str] = None
    import_tax_non_chargeable: Optional[str] = None
    incoterms: Optional[str] = None
    insurance_fee: Optional[int] = None
    is_above_threshold: Optional[bool] = None
    max_delivery_time: Optional[int] = None
    min_delivery_time: Optional[int] = None
    minimum_pickup_fee: Optional[int] = None
    other_surcharges: Optional[OtherSurchargesType] = JStruct[OtherSurchargesType]
    oversized_surcharge: Optional[int] = None
    payment_recipient: Optional[str] = None
    provincial_sales_tax: Optional[int] = None
    rates_in_origin_currency: Optional[RatesInOriginCurrencyType] = JStruct[RatesInOriginCurrencyType]
    remote_area_surcharge: Optional[int] = None
    remote_area_surcharges: Optional[str] = None
    residential_discounted_fee: Optional[int] = None
    residential_full_fee: Optional[int] = None
    sales_tax: Optional[int] = None
    shipment_charge: Optional[int] = None
    shipment_charge_total: Optional[int] = None
    total_charge: Optional[int] = None
    tracking_rating: Optional[int] = None
    value_for_money_rank: Optional[int] = None
    warehouse_handling_fee: Optional[int] = None


@s(auto_attribs=True)
class RegulatoryIdentifiersType:
    eori: Optional[str] = None
    ioss: Optional[str] = None
    vat_number: Optional[str] = None


@s(auto_attribs=True)
class ShippingDocumentType:
    base64_encoded_strings: List[str] = []
    category: Optional[str] = None
    format: Optional[str] = None
    page_size: Optional[str] = None
    required: Optional[bool] = None
    url: Any = None


@s(auto_attribs=True)
class ShippingSettingsType:
    b13_a_filing: Optional[str] = None


@s(auto_attribs=True)
class TrackingType:
    alternate_tracking_number: Optional[str] = None
    handler: Optional[str] = None
    leg_number: Optional[int] = None
    local_tracking_number: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_state: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    buyer_regulatory_identifiers: Optional[BuyerRegulatoryIdentifiersType] = JStruct[BuyerRegulatoryIdentifiersType]
    consignee_tax_id: Optional[str] = None
    courier: Optional[CourierType] = JStruct[CourierType]
    created_at: Optional[str] = None
    currency: Optional[str] = None
    delivery_state: Optional[str] = None
    destination_address: Optional[AddressType] = JStruct[AddressType]
    easyship_shipment_id: Optional[str] = None
    eei_reference: Optional[str] = None
    incoterms: Optional[str] = None
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]
    label_generated_at: Optional[str] = None
    label_paid_at: Optional[str] = None
    label_state: Optional[str] = None
    last_failure_http_response_messages: List[LastFailureHTTPResponseMessageType] = JList[LastFailureHTTPResponseMessageType]
    metadata: List[Any] = []
    order_created_at: Optional[str] = None
    order_data: Optional[OrderDataType] = JStruct[OrderDataType]
    origin_address: Optional[AddressType] = JStruct[AddressType]
    parcels: List[ParcelType] = JList[ParcelType]
    pickup_state: Optional[str] = None
    rates: List[RateType] = JList[RateType]
    regulatory_identifiers: Optional[RegulatoryIdentifiersType] = JStruct[RegulatoryIdentifiersType]
    shipment_return: Optional[bool] = None
    return_address: Optional[AddressType] = JStruct[AddressType]
    sender_address: Optional[AddressType] = JStruct[AddressType]
    set_as_residential: Optional[bool] = None
    shipment_state: Optional[str] = None
    shipping_documents: List[ShippingDocumentType] = JList[ShippingDocumentType]
    shipping_settings: Optional[ShippingSettingsType] = JStruct[ShippingSettingsType]
    tracking_page_url: Optional[str] = None
    trackings: List[TrackingType] = JList[TrackingType]
    updated_at: Optional[str] = None
    warehouse_state: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    shipment: Optional[ShipmentType] = JStruct[ShipmentType]
