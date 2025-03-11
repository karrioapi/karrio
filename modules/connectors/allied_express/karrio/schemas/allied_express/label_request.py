import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ItemType:
    dangerous: typing.Optional[bool] = None
    height: typing.Optional[int] = None
    itemCount: typing.Optional[int] = None
    length: typing.Optional[int] = None
    volume: typing.Optional[float] = None
    weight: typing.Optional[int] = None
    width: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class GeographicAddressType:
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postCode: typing.Optional[int] = None
    state: typing.Optional[str] = None
    suburb: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class JobStopsType:
    companyName: typing.Optional[str] = None
    contact: typing.Optional[str] = None
    emailAddress: typing.Optional[str] = None
    geographicAddress: typing.Optional[GeographicAddressType] = jstruct.JStruct[GeographicAddressType]
    phoneNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelRequestType:
    bookedBy: typing.Optional[str] = None
    account: typing.Optional[str] = None
    instructions: typing.Optional[str] = None
    itemCount: typing.Optional[int] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    jobStopsP: typing.Optional[JobStopsType] = jstruct.JStruct[JobStopsType]
    jobStopsD: typing.Optional[JobStopsType] = jstruct.JStruct[JobStopsType]
    referenceNumbers: typing.Optional[typing.List[str]] = None
    serviceLevel: typing.Optional[str] = None
    volume: typing.Optional[float] = None
    weight: typing.Optional[int] = None
