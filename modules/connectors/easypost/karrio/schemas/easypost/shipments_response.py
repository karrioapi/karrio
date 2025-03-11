import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Details:
    longitude: typing.Optional[float] = None
    latitude: typing.Optional[float] = None
    time_zone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Error:
    suggestion: typing.Optional[str] = None
    code: typing.Optional[str] = None
    field: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Delivery:
    success: typing.Optional[bool] = None
    errors: typing.Optional[typing.List[Error]] = jstruct.JList[Error]
    details: typing.Optional[Details] = jstruct.JStruct[Details]


@attr.s(auto_attribs=True)
class Verifications:
    delivery: typing.Optional[Delivery] = jstruct.JStruct[Delivery]


@attr.s(auto_attribs=True)
class Address:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    street1: typing.Optional[str] = None
    street2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zip: typing.Optional[int] = None
    country: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    carrier_facility: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    federal_tax_id: typing.Optional[str] = None
    state_tax_id: typing.Optional[str] = None
    verifications: typing.Optional[Verifications] = jstruct.JStruct[Verifications]


@attr.s(auto_attribs=True)
class CustomsItem:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
    description: typing.Optional[str] = None
    hs_tariff_number: typing.Optional[int] = None
    origin_country: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    value: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    code: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    manufacturer: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    eccn: typing.Optional[str] = None
    printed_commodity_identifier: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsInfo:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
    contents_explanation: typing.Optional[str] = None
    contents_type: typing.Optional[str] = None
    customs_certify: typing.Optional[bool] = None
    customs_signer: typing.Optional[str] = None
    eel_pfc: typing.Optional[str] = None
    non_delivery_option: typing.Optional[str] = None
    restriction_comments: typing.Optional[str] = None
    restriction_type: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    declaration: typing.Optional[str] = None
    customs_items: typing.Optional[typing.List[CustomsItem]] = jstruct.JList[CustomsItem]


@attr.s(auto_attribs=True)
class Fee:
    amount: typing.Optional[str] = None
    charged: typing.Optional[bool] = None
    object: typing.Optional[str] = None
    refunded: typing.Optional[bool] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Form:
    object: typing.Optional[str] = None
    id: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    form_type: typing.Optional[str] = None
    form_url: typing.Optional[str] = None
    submitted_electronically: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class Parcel:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    predefined_package: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostageLabel:
    created_at: typing.Optional[str] = None
    id: typing.Optional[str] = None
    integrated_form: typing.Optional[str] = None
    label_date: typing.Optional[str] = None
    label_epl2_url: typing.Optional[str] = None
    label_file_type: typing.Optional[str] = None
    label_pdf_url: typing.Optional[str] = None
    label_resolution: typing.Optional[int] = None
    label_size: typing.Optional[str] = None
    label_type: typing.Optional[str] = None
    label_url: typing.Optional[str] = None
    label_zpl_url: typing.Optional[str] = None
    object: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Rate:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    carrier_account_id: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    service: typing.Optional[str] = None
    rate: typing.Optional[str] = None
    carrier: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    delivery_days: typing.Optional[int] = None
    delivery_date: typing.Optional[str] = None
    delivery_date_guaranteed: typing.Optional[bool] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SelectedRate:
    carrier: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    rate: typing.Optional[str] = None
    service: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingLocation:
    object: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country: typing.Optional[str] = None
    zip: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TrackingDetail:
    object: typing.Optional[str] = None
    message: typing.Optional[str] = None
    status: typing.Optional[str] = None
    tracking_detail_datetime: typing.Optional[str] = None
    source: typing.Optional[str] = None
    tracking_location: typing.Optional[TrackingLocation] = jstruct.JStruct[TrackingLocation]


@attr.s(auto_attribs=True)
class Tracker:
    created_at: typing.Optional[str] = None
    id: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    object: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    status: typing.Optional[str] = None
    tracking_code: typing.Optional[str] = None
    tracking_details: typing.Optional[typing.List[TrackingDetail]] = jstruct.JList[TrackingDetail]
    updated_at: typing.Optional[str] = None
    public_url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Shipment:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    is_return: typing.Optional[bool] = None
    batch_id: typing.Optional[str] = None
    batch_message: typing.Optional[str] = None
    batch_status: typing.Optional[str] = None
    to_address: typing.Optional[Address] = jstruct.JStruct[Address]
    from_address: typing.Optional[Address] = jstruct.JStruct[Address]
    return_address: typing.Optional[Address] = jstruct.JStruct[Address]
    buyer_address: typing.Optional[Address] = jstruct.JStruct[Address]
    parcel: typing.Optional[Parcel] = jstruct.JStruct[Parcel]
    customs_info: typing.Optional[CustomsInfo] = jstruct.JStruct[CustomsInfo]
    fees: typing.Optional[typing.List[Fee]] = jstruct.JList[Fee]
    forms: typing.Optional[typing.List[Form]] = jstruct.JList[Form]
    options: typing.Any = None
    rates: typing.Optional[typing.List[Rate]] = jstruct.JList[Rate]
    reference: typing.Optional[str] = None
    scan_form: typing.Optional[str] = None
    refund_status: typing.Optional[str] = None
    selected_rate: typing.Optional[SelectedRate] = jstruct.JStruct[SelectedRate]
    status: typing.Optional[str] = None
    postage_label: typing.Optional[PostageLabel] = jstruct.JStruct[PostageLabel]
    tracking_code: typing.Optional[str] = None
    usps_zone: typing.Optional[int] = None
    tracker: typing.Optional[Tracker] = jstruct.JStruct[Tracker]
    messages: typing.Optional[typing.List[typing.Any]] = None
    insurance: typing.Optional[float] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentsResponse:
    has_more: typing.Optional[bool] = None
    shipments: typing.Optional[typing.List[Shipment]] = jstruct.JList[Shipment]
