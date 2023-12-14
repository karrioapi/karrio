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
class MetadataType:
    pass


@s(auto_attribs=True)
class ParcelContentType:
    description: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    quantity: Optional[int] = None
    countryoforigin: Optional[str] = None
    hscode: Optional[int] = None


@s(auto_attribs=True)
class AddressType:
    country: Optional[str] = None
    addressline1: Optional[str] = None
    addressline2: Optional[str] = None
    suburb: Optional[str] = None
    postcode: Optional[int] = None
    statename: Optional[str] = None


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
    taxids: Optional[TaxIDSType] = JStruct[TaxIDSType]


@s(auto_attribs=True)
class VolumeType:
    units: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class OrderRequestType:
    sender: Optional[ReceiverType] = JStruct[ReceiverType]
    receiver: Optional[ReceiverType] = JStruct[ReceiverType]
    description: Optional[str] = None
    customerreference: Optional[str] = None
    productcode: Optional[str] = None
    firstmileoption: Optional[str] = None
    pickupdate: Optional[str] = None
    weight: Optional[VolumeType] = JStruct[VolumeType]
    volume: Optional[VolumeType] = JStruct[VolumeType]
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    metadata: Optional[dict] = {}
    hidepickupaddress: Optional[bool] = None
    parcelcontents: List[ParcelContentType] = JList[ParcelContentType]
    contentstype: Optional[str] = None
