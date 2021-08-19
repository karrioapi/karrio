from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Contents:
    description: Optional[str] = None
    value: Optional[str] = None
    country_of_origin: Optional[str] = None


@s(auto_attribs=True)
class Metadata:
    pass


@s(auto_attribs=True)
class Address:
    address_line1: Optional[str] = None
    suburb: Optional[str] = None
    postcode: Optional[int] = None
    country: Optional[str] = None
    state_name: Optional[str] = None


@s(auto_attribs=True)
class ReceiverContact:
    name: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class Receiver:
    contact: Optional[ReceiverContact] = JStruct[ReceiverContact]
    address: Optional[Address] = JStruct[Address]
    instructions: Optional[str] = None


@s(auto_attribs=True)
class SenderContact:
    name: Optional[str] = None
    phone: Optional[str] = None


@s(auto_attribs=True)
class Sender:
    contact: Optional[SenderContact] = JStruct[SenderContact]
    address: Optional[Address] = JStruct[Address]
    instructions: Optional[str] = None


@s(auto_attribs=True)
class Volume:
    value: Optional[str] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class OrderRequest:
    pickup_date: Optional[str] = None
    first_mile_option: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[Volume] = JStruct[Volume]
    volume: Optional[Volume] = JStruct[Volume]
    customer_reference: Optional[str] = None
    metadata: Optional[Metadata] = JStruct[Metadata]
    sender: Optional[Sender] = JStruct[Sender]
    receiver: Optional[Receiver] = JStruct[Receiver]
    contents: Optional[Contents] = JStruct[Contents]
