import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DimensionsType:
    units: typing.Optional[str] = None
    height: typing.Optional[float] = None
    width: typing.Optional[float] = None
    length: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class MetadataType:
    pass


@attr.s(auto_attribs=True)
class ParcelContentType:
    description: typing.Optional[str] = None
    value: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    country_of_origin: typing.Optional[str] = None
    hs_code: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class AddressType:
    country: typing.Optional[str] = None
    address_line1: typing.Optional[str] = None
    address_line2: typing.Optional[str] = None
    suburb: typing.Optional[str] = None
    postcode: typing.Optional[int] = None
    state_name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxIDSType:
    ioss: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    instructions: typing.Optional[str] = None
    tax_ids: typing.Optional[TaxIDSType] = jstruct.JStruct[TaxIDSType]


@attr.s(auto_attribs=True)
class VolumeType:
    units: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class OrderRequestType:
    sender: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    description: typing.Optional[str] = None
    customer_reference: typing.Optional[str] = None
    product_code: typing.Optional[str] = None
    first_mile_option: typing.Optional[str] = None
    pickup_date: typing.Optional[str] = None
    weight: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    volume: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    hide_pickup_address: typing.Optional[bool] = None
    parcel_contents: typing.Optional[typing.List[ParcelContentType]] = jstruct.JList[ParcelContentType]
    contents_type: typing.Optional[str] = None
