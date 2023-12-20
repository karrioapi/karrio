from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DimensionsType:
    units: Optional[str] = None
    height: Optional[float] = None
    width: Optional[float] = None
    length: Optional[float] = None


@s(auto_attribs=True)
class ParcelContentType:
    description: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    quantity: Optional[int] = None
    country_of_origin: Optional[str] = None
    hs_code: Optional[int] = None


@s(auto_attribs=True)
class AddressType:
    country: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    suburb: Optional[str] = None
    postcode: Optional[int] = None
    state_name: Optional[str] = None


@s(auto_attribs=True)
class ContactType:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None


@s(auto_attribs=True)
class TaxIDSType:
    ioss: Optional[str] = None


@s(auto_attribs=True)
class ReceiverType:
    address: Optional[AddressType] = JStruct[AddressType]
    contact: Optional[ContactType] = JStruct[ContactType]
    instructions: Optional[str] = None
    tax_ids: Optional[TaxIDSType] = JStruct[TaxIDSType]


@s(auto_attribs=True)
class VolumeType:
    units: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class OrderRequestType:
    sender: Optional[ReceiverType] = JStruct[ReceiverType]
    receiver: Optional[ReceiverType] = JStruct[ReceiverType]
    description: Optional[str] = None
    customer_reference: Optional[str] = None
    product_code: Optional[str] = None
    first_mile_option: Optional[str] = None
    pickup_date: Optional[str] = None
    weight: Optional[VolumeType] = JStruct[VolumeType]
    volume: Optional[VolumeType] = JStruct[VolumeType]
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    metadata: Optional[dict] = {}
    hide_pickup_address: Optional[bool] = None
    parcel_contents: List[ParcelContentType] = JList[ParcelContentType]
    contents_type: Optional[str] = None
