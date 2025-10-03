import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FromAddressType:
    ignoreBadAddress: typing.Optional[bool] = None
    streetAddress: typing.Optional[str] = None
    streetAddressAbbreviation: typing.Optional[str] = None
    secondaryAddress: typing.Optional[str] = None
    cityAbbreviation: typing.Optional[str] = None
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
    pass


@attr.s(auto_attribs=True)
class SCANFormMetadataType:
    form: typing.Optional[int] = None
    imageType: typing.Optional[str] = None
    labelType: typing.Optional[str] = None
    mailingDate: typing.Optional[str] = None
    overwriteMailingDate: typing.Optional[bool] = None
    entryFacilityZIPCode: typing.Optional[int] = None
    destinationEntryFacilityType: typing.Optional[str] = None
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    manifestNumber: typing.Optional[str] = None
    trackingNumbers: typing.Optional[typing.List[str]] = None
    fromAddress: typing.Optional[FromAddressType] = jstruct.JStruct[FromAddressType]


@attr.s(auto_attribs=True)
class ScanFormResponseType:
    SCANFormMetadata: typing.Optional[SCANFormMetadataType] = jstruct.JStruct[SCANFormMetadataType]
    SCANFormImage: typing.Optional[str] = None
