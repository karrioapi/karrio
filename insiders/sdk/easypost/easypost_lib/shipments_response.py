from attr import s
from typing import Optional, List, Any
from jstruct import JList, JStruct


@s(auto_attribs=True)
class CustomsItem:
    id: Optional[str] = None
    object: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None
    hs_tariff_number: Optional[int] = None
    origin_country: Optional[str] = None
    quantity: Optional[int] = None
    value: Optional[float] = None
    weight: Optional[float] = None
    code: Optional[str] = None
    mode: Optional[str] = None
    manufacturer: Optional[str] = None
    currency: Optional[str] = None
    eccn: Optional[str] = None
    printed_commodity_identifier: Optional[str] = None


@s(auto_attribs=True)
class CustomsInfo:
    id: Optional[str] = None
    object: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    contents_explanation: Optional[str] = None
    contents_type: Optional[str] = None
    customs_certify: Optional[bool] = None
    customs_signer: Optional[str] = None
    eel_pfc: Optional[str] = None
    non_delivery_option: Optional[str] = None
    restriction_comments: Optional[str] = None
    restriction_type: Optional[str] = None
    mode: Optional[str] = None
    declaration: Optional[str] = None
    customs_items: List[CustomsItem] = JList[CustomsItem]


@s(auto_attribs=True)
class Fee:
    amount: Optional[str] = None
    charged: Optional[bool] = None
    object: Optional[str] = None
    refunded: Optional[bool] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class Form:
    object: Optional[str] = None
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    mode: Optional[str] = None
    form_type: Optional[str] = None
    form_url: Optional[str] = None
    submitted_electronically: Optional[bool] = None


@s(auto_attribs=True)
class Details:
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    time_zone: Optional[str] = None


@s(auto_attribs=True)
class Error:
    suggestion: Optional[str] = None
    code: Optional[str] = None
    field: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class Delivery:
    success: Optional[bool] = None
    errors: List[Error] = JList[Error]
    details: Optional[Details] = JStruct[Details]


@s(auto_attribs=True)
class Verifications:
    delivery: Optional[Delivery] = JStruct[Delivery]


@s(auto_attribs=True)
class Address:
    id: Optional[str] = None
    object: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    mode: Optional[str] = None
    carrier_facility: Optional[str] = None
    residential: Optional[bool] = None
    federal_tax_id: Optional[str] = None
    state_tax_id: Optional[str] = None
    verifications: Optional[Verifications] = JStruct[Verifications]


@s(auto_attribs=True)
class Parcel:
    id: Optional[str] = None
    object: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    predefined_package: Optional[str] = None
    weight: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@s(auto_attribs=True)
class PostageLabel:
    created_at: Optional[str] = None
    id: Optional[str] = None
    integrated_form: Optional[str] = None
    label_date: Optional[str] = None
    label_epl2_url: Optional[str] = None
    label_file_type: Optional[str] = None
    label_pdf_url: Optional[str] = None
    label_resolution: Optional[int] = None
    label_size: Optional[str] = None
    label_type: Optional[str] = None
    label_url: Optional[str] = None
    label_zpl_url: Optional[str] = None
    object: Optional[str] = None
    updated_at: Optional[str] = None


@s(auto_attribs=True)
class Rate:
    id: Optional[str] = None
    object: Optional[str] = None
    carrier_account_id: Optional[str] = None
    currency: Optional[str] = None
    service: Optional[str] = None
    rate: Optional[str] = None
    carrier: Optional[str] = None
    shipment_id: Optional[str] = None
    delivery_days: Optional[int] = None
    delivery_date: Optional[str] = None
    delivery_date_guaranteed: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@s(auto_attribs=True)
class SelectedRate:
    carrier: Optional[str] = None
    created_at: Optional[str] = None
    currency: Optional[str] = None
    id: Optional[str] = None
    object: Optional[str] = None
    rate: Optional[str] = None
    service: Optional[str] = None
    shipment_id: Optional[str] = None
    updated_at: Optional[str] = None


@s(auto_attribs=True)
class TrackingLocation:
    object: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[int] = None


@s(auto_attribs=True)
class TrackingDetail:
    object: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    datetime: Optional[str] = None
    source: Optional[str] = None
    tracking_location: Optional[TrackingLocation] = JStruct[TrackingLocation]


@s(auto_attribs=True)
class Tracker:
    created_at: Optional[str] = None
    id: Optional[str] = None
    mode: Optional[str] = None
    object: Optional[str] = None
    shipment_id: Optional[str] = None
    status: Optional[str] = None
    tracking_code: Optional[str] = None
    tracking_details: List[TrackingDetail] = JList[TrackingDetail]
    updated_at: Optional[str] = None
    public_url: Optional[str] = None


@s(auto_attribs=True)
class Shipment:
    id: Optional[str] = None
    object: Optional[str] = None
    mode: Optional[str] = None
    is_return: Optional[bool] = None
    batch_id: Optional[str] = None
    batch_message: Optional[str] = None
    batch_status: Optional[str] = None
    to_address: Optional[Address] = JStruct[Address]
    from_address: Optional[Address] = JStruct[Address]
    parcel: Optional[Parcel] = JStruct[Parcel]
    customs_info: Optional[CustomsInfo] = JStruct[CustomsInfo]
    fees: List[Fee] = JList[Fee]
    forms: List[Form] = JList[Form]
    options: Any = None
    rates: List[Rate] = JList[Rate]
    reference: Optional[str] = None
    scan_form: Optional[str] = None
    refund_status: Optional[str] = None
    selected_rate: Optional[SelectedRate] = JStruct[SelectedRate]
    status: Optional[str] = None
    postage_label: Optional[PostageLabel] = JStruct[PostageLabel]
    tracking_code: Optional[str] = None
    usps_zone: Optional[int] = None
    tracker: Optional[Tracker] = JStruct[Tracker]
    messages: List[Any] = []
    insurance: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@s(auto_attribs=True)
class ShipmentsResponse:
    has_more: Optional[bool] = None
    shipments: List[Shipment] = JList[Shipment]
