import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class NDetailsType:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    alternate_phone: typing.Optional[str] = None
    address_line_1: typing.Optional[str] = None
    address_line_2: typing.Optional[str] = None
    pincode: typing.Optional[int] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    email: typing.Optional[str] = None
    city_name: typing.Optional[str] = None
    state_name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PiecesDetailType:
    description: typing.Optional[str] = None
    declared_value: typing.Optional[int] = None
    weight: typing.Optional[str] = None
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ConsignmentType:
    customer_code: typing.Optional[str] = None
    service_type_id: typing.Optional[str] = None
    load_type: typing.Optional[str] = None
    description: typing.Optional[str] = None
    dimension_unit: typing.Optional[str] = None
    length: typing.Optional[str] = None
    width: typing.Optional[str] = None
    height: typing.Optional[str] = None
    weight_unit: typing.Optional[str] = None
    weight: typing.Optional[str] = None
    declared_value: typing.Optional[str] = None
    num_pieces: typing.Optional[int] = None
    origin_details: typing.Optional[NDetailsType] = jstruct.JStruct[NDetailsType]
    destination_details: typing.Optional[NDetailsType] = jstruct.JStruct[NDetailsType]
    return_details: typing.Optional[NDetailsType] = jstruct.JStruct[NDetailsType]
    customer_reference_number: typing.Optional[str] = None
    cod_collection_mode: typing.Optional[str] = None
    cod_amount: typing.Optional[str] = None
    commodity_id: typing.Optional[int] = None
    eway_bill: typing.Optional[str] = None
    is_risk_surcharge_applicable: typing.Optional[bool] = None
    invoice_number: typing.Optional[str] = None
    invoice_date: typing.Optional[str] = None
    reference_number: typing.Optional[str] = None
    pieces_detail: typing.Optional[typing.List[PiecesDetailType]] = jstruct.JList[PiecesDetailType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    consignments: typing.Optional[typing.List[ConsignmentType]] = jstruct.JList[ConsignmentType]
