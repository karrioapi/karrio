import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CommitmentType:
    name: typing.Optional[str] = None
    scheduleDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExtraServiceType:
    name: typing.Optional[str] = None
    SKU: typing.Optional[str] = None
    price: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class InductionTypeObjectType:
    pass


@attr.s(auto_attribs=True)
class LabelAddressType:
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
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    ignoreBadAddress: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class LinkType:
    rel: typing.Optional[typing.List[str]] = None
    title: typing.Optional[str] = None
    href: typing.Optional[str] = None
    method: typing.Optional[str] = None
    submissionMediaType: typing.Optional[str] = None
    targetMediaType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelMetadataType:
    labelAddress: typing.Optional[LabelAddressType] = jstruct.JStruct[LabelAddressType]
    routingInformation: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    constructCode: typing.Optional[str] = None
    SKU: typing.Optional[str] = None
    postage: typing.Optional[int] = None
    extraServices: typing.Optional[typing.List[ExtraServiceType]] = jstruct.JList[ExtraServiceType]
    zone: typing.Optional[str] = None
    commitment: typing.Optional[CommitmentType] = jstruct.JStruct[CommitmentType]
    weightUOM: typing.Optional[str] = None
    weight: typing.Optional[int] = None
    dimensionalWeight: typing.Optional[int] = None
    fees: typing.Optional[typing.List[ExtraServiceType]] = jstruct.JList[ExtraServiceType]
    permitHolderName: typing.Optional[str] = None
    inductionType: typing.Optional[InductionTypeObjectType] = jstruct.JStruct[InductionTypeObjectType]
    labelBrokerID: typing.Optional[str] = None
    links: typing.Optional[typing.List[LinkType]] = jstruct.JList[LinkType]
    bannerText: typing.Optional[str] = None
    retailDistributionCode: typing.Optional[str] = None
    serviceTypeCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class LabelResponseType:
    labelMetadata: typing.Optional[LabelMetadataType] = jstruct.JStruct[LabelMetadataType]
    returnLabelMetadata: typing.Optional[LabelMetadataType] = jstruct.JStruct[LabelMetadataType]
    labelImage: typing.Optional[str] = None
    receiptImage: typing.Optional[str] = None
    returnLabelImage: typing.Optional[str] = None
    returnReceiptImage: typing.Optional[str] = None
