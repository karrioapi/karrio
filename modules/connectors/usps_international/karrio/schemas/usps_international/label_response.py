import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CommitmentType:
    name: typing.Optional[str] = None
    scheduleDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExtraServiceType:
    serviceID: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    name: typing.Optional[str] = None
    price: typing.Optional[float] = None
    SKU: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelAddressType:
    streetAddress: typing.Optional[str] = None
    streetAddressAbbreviation: typing.Optional[str] = None
    secondaryAddress: typing.Optional[str] = None
    cityAbbreviation: typing.Optional[str] = None
    city: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    countryISOAlpha2Code: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    firm: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    ignoreBadAddress: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class LabelMetadataType:
    labelAddress: typing.Optional[LabelAddressType] = jstruct.JStruct[LabelAddressType]
    routingInformation: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None
    constructCode: typing.Optional[str] = None
    SKU: typing.Optional[str] = None
    postage: typing.Optional[float] = None
    extraServices: typing.Optional[typing.List[ExtraServiceType]] = jstruct.JList[ExtraServiceType]
    internationalPriceGroup: typing.Optional[str] = None
    zone: typing.Optional[str] = None
    commitment: typing.Optional[CommitmentType] = jstruct.JStruct[CommitmentType]
    weightUOM: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensionalWeight: typing.Optional[float] = None
    fees: typing.Optional[typing.List[typing.Any]] = None
    labelBrokerID: typing.Optional[str] = None
    bannerText: typing.Optional[str] = None
    retailDistributionCode: typing.Optional[str] = None
    serviceTypeCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class LabelResponseType:
    labelMetadata: typing.Optional[LabelMetadataType] = jstruct.JStruct[LabelMetadataType]
    labelImage: typing.Optional[str] = None
