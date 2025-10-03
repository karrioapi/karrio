import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FromAddressType:
    ignoreBadAddress: typing.Optional[bool] = None
    streetAddress: typing.Optional[str] = None
    secondaryAddress: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    ZIPCode: typing.Optional[str] = None
    ZIPPlus4: typing.Optional[str] = None
    urbanization: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    firm: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    trackingNumbers: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ScanFormRequestType:
    form: typing.Optional[int] = None
    imageType: typing.Optional[str] = None
    labelType: typing.Optional[str] = None
    mailingDate: typing.Optional[str] = None
    overwriteMailingDate: typing.Optional[bool] = None
    entryFacilityZIPCode: typing.Optional[int] = None
    destinationEntryFacilityType: typing.Optional[str] = None
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    fromAddress: typing.Optional[FromAddressType] = jstruct.JStruct[FromAddressType]
