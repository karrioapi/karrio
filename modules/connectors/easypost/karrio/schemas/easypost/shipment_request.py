import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Address:
    mode: typing.Optional[str] = None
    street1: typing.Optional[str] = None
    street2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zip: typing.Optional[int] = None
    country: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    carrier_facility: typing.Optional[str] = None
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    federal_tax_id: typing.Optional[str] = None
    state_tax_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsItem:
    description: typing.Optional[str] = None
    hs_tariff_number: typing.Optional[int] = None
    origin_country: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    value: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    code: typing.Optional[str] = None
    manufacturer: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    eccn: typing.Optional[str] = None
    printed_commodity_identifier: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsInfo:
    contents_explanation: typing.Optional[str] = None
    contents_type: typing.Optional[str] = None
    customs_certify: typing.Optional[bool] = None
    customs_signer: typing.Optional[str] = None
    eel_pfc: typing.Optional[str] = None
    non_delivery_option: typing.Optional[str] = None
    restriction_comments: typing.Optional[str] = None
    restriction_type: typing.Optional[str] = None
    declaration: typing.Optional[str] = None
    customs_items: typing.Optional[typing.List[CustomsItem]] = jstruct.JList[CustomsItem]


@attr.s(auto_attribs=True)
class Parcel:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    predefined_package: typing.Optional[str] = None
    weight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Shipment:
    reference: typing.Optional[str] = None
    is_return: typing.Optional[bool] = None
    to_address: typing.Optional[Address] = jstruct.JStruct[Address]
    from_address: typing.Optional[Address] = jstruct.JStruct[Address]
    return_address: typing.Optional[Address] = jstruct.JStruct[Address]
    buyer_address: typing.Optional[Address] = jstruct.JStruct[Address]
    parcel: typing.Optional[Parcel] = jstruct.JStruct[Parcel]
    customs_info: typing.Optional[CustomsInfo] = jstruct.JStruct[CustomsInfo]
    options: typing.Any = None
    carrier_accounts: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ShipmentRequest:
    shipment: typing.Optional[Shipment] = jstruct.JStruct[Shipment]
