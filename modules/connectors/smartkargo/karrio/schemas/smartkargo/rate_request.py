import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DimensionType:
    pieces: typing.Optional[int] = None
    height: typing.Optional[float] = None
    width: typing.Optional[float] = None
    length: typing.Optional[float] = None
    grossWeight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class TaxIdentificationNumberType:
    type: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParticipantType:
    type: typing.Optional[str] = None
    primaryId: typing.Optional[str] = None
    additionalId: typing.Optional[str] = None
    account: typing.Optional[str] = None
    name: typing.Optional[str] = None
    postCode: typing.Optional[str] = None
    street: typing.Optional[str] = None
    street2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    countryId: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    email: typing.Optional[str] = None
    taxIdentificationNumbers: typing.Optional[typing.List[TaxIdentificationNumberType]] = jstruct.JList[TaxIdentificationNumberType]


@attr.s(auto_attribs=True)
class PackageType:
    reference: typing.Optional[str] = None
    commodityType: typing.Optional[str] = None
    serviceType: typing.Optional[str] = None
    paymentMode: typing.Optional[str] = None
    packageDescription: typing.Optional[str] = None
    totalPackages: typing.Optional[int] = None
    totalPieces: typing.Optional[int] = None
    grossVolumeUnitMeasure: typing.Optional[str] = None
    totalGrossWeight: typing.Optional[float] = None
    grossWeightUnitMeasure: typing.Optional[str] = None
    insuranceRequired: typing.Optional[bool] = None
    declaredValue: typing.Optional[float] = None
    specialHandlingType: typing.Any = None
    additionalInfo01: typing.Any = None
    additionalInfo02: typing.Any = None
    additionalInfo03: typing.Any = None
    additionalInfo04: typing.Any = None
    deliveryType: typing.Optional[str] = None
    channel: typing.Optional[str] = None
    labelRef2: typing.Any = None
    dimensions: typing.Optional[typing.List[DimensionType]] = jstruct.JList[DimensionType]
    participants: typing.Optional[typing.List[ParticipantType]] = jstruct.JList[ParticipantType]


@attr.s(auto_attribs=True)
class RateRequestType:
    reference: typing.Optional[str] = None
    issueDate: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
