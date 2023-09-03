from attr import s
from typing import Optional, List, Any
from jstruct import JList, JStruct


@s(auto_attribs=True)
class CustomsItem:
    description: Optional[str] = None
    hs_tariff_number: Optional[int] = None
    origin_country: Optional[str] = None
    quantity: Optional[int] = None
    value: Optional[float] = None
    weight: Optional[float] = None
    code: Optional[str] = None
    manufacturer: Optional[str] = None
    currency: Optional[str] = None
    eccn: Optional[str] = None
    printed_commodity_identifier: Optional[str] = None


@s(auto_attribs=True)
class CustomsInfo:
    contents_explanation: Optional[str] = None
    contents_type: Optional[str] = None
    customs_certify: Optional[bool] = None
    customs_signer: Optional[str] = None
    eel_pfc: Optional[str] = None
    non_delivery_option: Optional[str] = None
    restriction_comments: Optional[str] = None
    restriction_type: Optional[str] = None
    declaration: Optional[str] = None
    customs_items: List[CustomsItem] = JList[CustomsItem]


@s(auto_attribs=True)
class Address:
    mode: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None
    country: Optional[str] = None
    residential: Optional[bool] = None
    carrier_facility: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    federal_tax_id: Optional[str] = None
    state_tax_id: Optional[str] = None


@s(auto_attribs=True)
class Parcel:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    predefined_package: Optional[str] = None
    weight: Optional[float] = None


@s(auto_attribs=True)
class Shipment:
    reference: Optional[str] = None
    is_return: Optional[bool] = None
    to_address: Optional[Address] = JStruct[Address]
    from_address: Optional[Address] = JStruct[Address]
    parcel: Optional[Parcel] = JStruct[Parcel]
    customs_info: Optional[CustomsInfo] = JStruct[CustomsInfo]
    options: Any = None
    carrier_accounts: List[str] = []


@s(auto_attribs=True)
class ShipmentRequest:
    shipment: Optional[Shipment] = JStruct[Shipment]
