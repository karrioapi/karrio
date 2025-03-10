import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class UnavailableCourierType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MetaType:
    request_id: typing.Optional[str] = None
    status: typing.Optional[str] = None
    unavailable_couriers: typing.Optional[typing.List[UnavailableCourierType]] = jstruct.JList[UnavailableCourierType]
    errors: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class BuyerRegulatoryIdentifiersType:
    ein: typing.Optional[str] = None
    vat_number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CourierType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


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
    insured_amount: typing.Optional[int] = None
    insured_currency: typing.Optional[str] = None
    is_insured: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class LastFailureHTTPResponseMessageType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderDataType:
    buyer_notes: typing.Optional[str] = None
    buyer_selected_courier_name: typing.Optional[str] = None
    order_created_at: typing.Optional[str] = None
    order_tag_list: typing.Optional[typing.List[str]] = None
    platform_name: typing.Optional[str] = None
    platform_order_number: typing.Optional[str] = None
    seller_notes: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BoxType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None
    outer_dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    slug: typing.Optional[str] = None
    type: typing.Optional[str] = None
    weight: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ItemType:
    actual_weight: typing.Optional[int] = None
    category: typing.Optional[str] = None
    contains_battery_pi966: typing.Optional[bool] = None
    contains_battery_pi967: typing.Optional[bool] = None
    contains_liquids: typing.Optional[bool] = None
    declared_currency: typing.Optional[str] = None
    declared_customs_value: typing.Optional[int] = None
    description: typing.Optional[str] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    hs_code: typing.Optional[int] = None
    id: typing.Optional[str] = None
    origin_country_alpha2: typing.Optional[str] = None
    origin_currency: typing.Optional[str] = None
    origin_customs_value: typing.Optional[int] = None
    quantity: typing.Optional[int] = None
    sku: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    box: typing.Optional[BoxType] = jstruct.JStruct[BoxType]
    id: typing.Optional[str] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    total_actual_weight: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DetailType:
    fee: typing.Optional[int] = None
    name: typing.Optional[str] = None
    origin_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class OtherSurchargesType:
    details: typing.Optional[typing.List[DetailType]] = jstruct.JList[DetailType]
    total_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RatesInOriginCurrencyType:
    additional_services_surcharge: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    ddp_handling_fee: typing.Optional[str] = None
    estimated_import_duty: typing.Optional[str] = None
    estimated_import_tax: typing.Optional[str] = None
    fuel_surcharge: typing.Optional[int] = None
    import_duty_charge: typing.Optional[str] = None
    import_tax_charge: typing.Optional[str] = None
    import_tax_non_chargeable: typing.Optional[str] = None
    insurance_fee: typing.Optional[int] = None
    minimum_pickup_fee: typing.Optional[int] = None
    oversized_surcharge: typing.Optional[int] = None
    provincial_sales_tax: typing.Optional[int] = None
    remote_area_surcharge: typing.Optional[int] = None
    residential_discounted_fee: typing.Optional[int] = None
    residential_full_fee: typing.Optional[int] = None
    sales_tax: typing.Optional[int] = None
    shipment_charge: typing.Optional[int] = None
    shipment_charge_total: typing.Optional[int] = None
    total_charge: typing.Optional[int] = None
    warehouse_handling_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RateType:
    additional_services_surcharge: typing.Optional[int] = None
    available_handover_options: typing.Optional[typing.List[str]] = None
    cost_rank: typing.Optional[int] = None
    courier_id: typing.Optional[str] = None
    courier_logo_url: typing.Optional[str] = None
    courier_name: typing.Optional[str] = None
    courier_remarks: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    ddp_handling_fee: typing.Optional[str] = None
    delivery_time_rank: typing.Optional[int] = None
    description: typing.Optional[str] = None
    discount: typing.Optional[str] = None
    easyship_rating: typing.Optional[int] = None
    estimated_import_duty: typing.Optional[str] = None
    estimated_import_tax: typing.Optional[str] = None
    fuel_surcharge: typing.Optional[int] = None
    full_description: typing.Optional[str] = None
    import_duty_charge: typing.Optional[str] = None
    import_tax_charge: typing.Optional[str] = None
    import_tax_non_chargeable: typing.Optional[str] = None
    incoterms: typing.Optional[str] = None
    insurance_fee: typing.Optional[int] = None
    is_above_threshold: typing.Optional[bool] = None
    max_delivery_time: typing.Optional[int] = None
    min_delivery_time: typing.Optional[int] = None
    minimum_pickup_fee: typing.Optional[int] = None
    other_surcharges: typing.Optional[OtherSurchargesType] = jstruct.JStruct[OtherSurchargesType]
    oversized_surcharge: typing.Optional[int] = None
    payment_recipient: typing.Optional[str] = None
    provincial_sales_tax: typing.Optional[int] = None
    rates_in_origin_currency: typing.Optional[RatesInOriginCurrencyType] = jstruct.JStruct[RatesInOriginCurrencyType]
    remote_area_surcharge: typing.Optional[int] = None
    remote_area_surcharges: typing.Optional[str] = None
    residential_discounted_fee: typing.Optional[int] = None
    residential_full_fee: typing.Optional[int] = None
    sales_tax: typing.Optional[int] = None
    shipment_charge: typing.Optional[int] = None
    shipment_charge_total: typing.Optional[int] = None
    total_charge: typing.Optional[int] = None
    tracking_rating: typing.Optional[int] = None
    value_for_money_rank: typing.Optional[int] = None
    warehouse_handling_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RegulatoryIdentifiersType:
    eori: typing.Optional[str] = None
    ioss: typing.Optional[str] = None
    vat_number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingDocumentType:
    base64_encoded_strings: typing.Optional[typing.List[str]] = None
    category: typing.Optional[str] = None
    format: typing.Optional[str] = None
    page_size: typing.Optional[str] = None
    required: typing.Optional[bool] = None
    url: typing.Any = None


@attr.s(auto_attribs=True)
class ShippingSettingsType:
    b13_a_filing: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingType:
    alternate_tracking_number: typing.Optional[str] = None
    handler: typing.Optional[str] = None
    leg_number: typing.Optional[int] = None
    local_tracking_number: typing.Optional[str] = None
    tracking_number: typing.Optional[str] = None
    tracking_state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    buyer_regulatory_identifiers: typing.Optional[BuyerRegulatoryIdentifiersType] = jstruct.JStruct[BuyerRegulatoryIdentifiersType]
    consignee_tax_id: typing.Optional[str] = None
    courier: typing.Optional[CourierType] = jstruct.JStruct[CourierType]
    created_at: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    delivery_state: typing.Optional[str] = None
    destination_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    easyship_shipment_id: typing.Optional[str] = None
    eei_reference: typing.Optional[str] = None
    incoterms: typing.Optional[str] = None
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    label_generated_at: typing.Optional[str] = None
    label_paid_at: typing.Optional[str] = None
    label_state: typing.Optional[str] = None
    last_failure_http_response_messages: typing.Optional[typing.List[LastFailureHTTPResponseMessageType]] = jstruct.JList[LastFailureHTTPResponseMessageType]
    metadata: typing.Optional[typing.List[typing.Any]] = None
    order_created_at: typing.Optional[str] = None
    order_data: typing.Optional[OrderDataType] = jstruct.JStruct[OrderDataType]
    origin_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    pickup_state: typing.Optional[str] = None
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
    regulatory_identifiers: typing.Optional[RegulatoryIdentifiersType] = jstruct.JStruct[RegulatoryIdentifiersType]
    shipment_return: typing.Optional[bool] = None
    return_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    sender_address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    set_as_residential: typing.Optional[bool] = None
    shipment_state: typing.Optional[str] = None
    shipping_documents: typing.Optional[typing.List[ShippingDocumentType]] = jstruct.JList[ShippingDocumentType]
    shipping_settings: typing.Optional[ShippingSettingsType] = jstruct.JStruct[ShippingSettingsType]
    tracking_page_url: typing.Optional[str] = None
    trackings: typing.Optional[typing.List[TrackingType]] = jstruct.JList[TrackingType]
    updated_at: typing.Optional[str] = None
    warehouse_state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
