import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ParcelType:
    weight: typing.Optional[float] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ErAddressType:
    postalCode: typing.Optional[int] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequestType:
    shipperAddress: typing.Optional[ErAddressType] = jstruct.JStruct[ErAddressType]
    receiverAddress: typing.Optional[ErAddressType] = jstruct.JStruct[ErAddressType]
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    productCodes: typing.Optional[typing.List[str]] = None
