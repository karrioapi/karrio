"""Royal Mail Shipping Service Datatypes definition module."""

import attr
from typing import List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class Address:
    building_name: str = None
    building_number: str = None
    address_line1: str = None
    address_line2: str = None
    address_line3: str = None
    post_town: str = None
    county: str = None
    post_code: str = None
    country_code: str = None


@attr.s(auto_attribs=True)
class CancelOrUpdateShipmentResponse:
    shipment_number: str = None


@attr.s(auto_attribs=True)
class CompletedShipments:
    state: str = None


@attr.s(auto_attribs=True)
class Contact:
    name: str = None
    complementary_name: str = None
    telephone_number: str = None
    email: str = None


@attr.s(auto_attribs=True)
class Measurement:
    unit_of_measure: str = None
    value: float = None


@attr.s(auto_attribs=True)
class ContentDetail:
    country_of_manufacture_code: str = None
    manufacturers_name: str = None
    description: str = None
    unit_weight: Measurement = JStruct[Measurement]
    unit_quantity: int = None
    unit_value: float = None
    currency_code: str = None
    tariff_code: float = None
    tariff_description: str = None


@attr.s(auto_attribs=True)
class CreatedShipmentResponse:
    completed_shipments: CompletedShipments = JStruct[CompletedShipments]


@attr.s(auto_attribs=True)
class DocumentsRequest:
    document_name: str = None
    document_copies: float = None


@attr.s(auto_attribs=True)
class Error:
    state: str = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    error_code: str = None
    error_description: str = None
    error_cause: str = None
    error_resolution: str = None


@attr.s(auto_attribs=True)
class InlineResponse200:
    international_document: str = None


@attr.s(auto_attribs=True)
class LabelImages:
    image1_d_barcode: str = None
    image2_d_matrix: str = None


@attr.s(auto_attribs=True)
class LabelResponseLabelData:
    upu_code: str = None
    information_type_id: str = None
    version_id: str = None
    format: str = None
    mail_type: str = None
    item_id: str = None
    check_digit: str = None
    item_weight: str = None
    weight_type: str = None
    product: str = None
    tracking_number: str = None
    destination_postcode_dps: str = None
    return_to_sender_postcode: str = None
    required_at_delivery: str = None
    building_number: str = None
    building_name: str = None
    date_of_shipment: str = None


@attr.s(auto_attribs=True)
class ManifestRequest:
    service_occurence: str = None
    service_code: str = None
    your_description: str = None
    your_reference: str = None


@attr.s(auto_attribs=True)
class ManifestShipment:
    code: str = None
    shipment_number: str = None


@attr.s(auto_attribs=True)
class ManifestResponse:
    batch_number: int = None
    count: int = None
    manifest: str = None
    shipments: List[ManifestShipment] = JList[ManifestShipment]


@attr.s(auto_attribs=True)
class OfflineShipment:
    number: str = None
    item_id: str = None
    status: str = None


@attr.s(auto_attribs=True)
class Parcel:
    weight: Measurement = JStruct[Measurement]
    length: Measurement = JStruct[Measurement]
    height: Measurement = JStruct[Measurement]
    width: Measurement = JStruct[Measurement]
    purpose_of_shipment: str = None
    explanation: str = None
    invoice_number: str = None
    export_license_number: str = None
    certificate_number: str = None
    content_details: List[ContentDetail] = JList[ContentDetail]
    fees: fees = None


@attr.s(auto_attribs=True)
class PrintManifestResponse:
    manifest: str = None


@attr.s(auto_attribs=True)
class RecipientAddress:
    building_name: str = None
    building_number: str = None
    address_line1: str = None
    address_line2: str = None
    address_line3: str = None
    state_or_province: str = None
    post_town: str = None
    post_code: str = None
    country: str = None


@attr.s(auto_attribs=True)
class RecipientContact:
    name: str = None
    complementary_name: str = None
    telephone_number: str = None
    electronic_address: str = None


@attr.s(auto_attribs=True)
class LabelResponse:
    label: str = None
    label_images: LabelImages = JStruct[LabelImages]
    format: str = None
    label_data: LabelResponseLabelData = JStruct[LabelResponseLabelData]
    recipient_address: RecipientAddress = JStruct[RecipientAddress]
    recipient_contact: RecipientContact = JStruct[RecipientContact]


@attr.s(auto_attribs=True)
class Service:
    format: str = None
    occurrence: str = None
    offering: str = None
    type: str = None
    signature: str = None
    enhancements: dict = None


@attr.s(auto_attribs=True)
class ShipmentBarcodeItem:
    shipment_number: str = None
    item_id: str = None
    status: str = None
    valid_from: str = None
    label: str = None


@attr.s(auto_attribs=True)
class ShipmentRequestItem:
    offline_shipment: List[OfflineShipment] = JList[OfflineShipment]
    count: int = None
    weight: Measurement = JStruct[Measurement]


@attr.s(auto_attribs=True)
class Shipment:
    shipment_type: str = None
    service: Service = JStruct[Service]
    shipping_date: str = None
    items: List[ShipmentRequestItem] = JList[ShipmentRequestItem]
    recipient_contact: Contact = JStruct[Contact]
    recipient_address: Address = JStruct[Address]
    sender_reference: str = None
    department_reference: str = None
    customer_reference: str = None
    safe_place: str = None


@attr.s(auto_attribs=True)
class ShipmentRequestItemInternational:
    count: str = None
    weight: Measurement = JStruct[Measurement]


@attr.s(auto_attribs=True)
class ShipmentWithBarcodeAndWeight:
    shipment_items: List[ShipmentBarcodeItem] = JList[ShipmentBarcodeItem]
    weight: Measurement = JStruct[Measurement]


@attr.s(auto_attribs=True)
class ShipmentsRequestInternationalInfo:
    parcels: List[Parcel] = JList[Parcel]
    shipper_exporter_vat_no: str = None
    recipient_importers_vat_no: str = None
    original_export_shipment_no: str = None
    documents_only: bool = None
    shipment_description: str = None
    comments: str = None
    invoice_date: str = None
    terms_of_delivery: str = None
    purchase_order_ref: str = None


@attr.s(auto_attribs=True)
class ShipmentsRequest:
    shipment_type: str = None
    service: Service = JStruct[Service]
    bfpo_code: str = None
    items: List[ShipmentRequestItemInternational] = JList[ShipmentRequestItemInternational]
    recipient_contact: Contact = JStruct[Contact]
    recipient_address: Address = JStruct[Address]
    sender_reference: str = None
    department_reference: str = None
    customer_reference: str = None
    safe_place: str = None
    international_info: ShipmentsRequestInternationalInfo = JStruct[ShipmentsRequestInternationalInfo]


@attr.s(auto_attribs=True)
class Token:
    token: str = None
