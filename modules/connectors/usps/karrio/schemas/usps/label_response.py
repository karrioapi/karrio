from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CommitmentType:
    name: Optional[str] = None
    scheduleDeliveryDate: Optional[str] = None


@s(auto_attribs=True)
class ExtraServiceType:
    name: Optional[str] = None
    SKU: Optional[str] = None
    price: Optional[int] = None


@s(auto_attribs=True)
class InductionTypeType:
    pass


@s(auto_attribs=True)
class LabelAddressType:
    streetAddress: Optional[str] = None
    streetAddressAbbreviation: Optional[str] = None
    secondaryAddress: Optional[str] = None
    cityAbbreviation: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    ZIPCode: Optional[str] = None
    ZIPPlus4: Optional[str] = None
    urbanization: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    firm: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    ignoreBadAddress: Optional[bool] = None


@s(auto_attribs=True)
class LinkType:
    rel: List[str] = []
    title: Optional[str] = None
    href: Optional[str] = None
    method: Optional[str] = None
    submissionMediaType: Optional[str] = None
    targetMediaType: Optional[str] = None


@s(auto_attribs=True)
class LabelMetadataType:
    labelAddress: Optional[LabelAddressType] = JStruct[LabelAddressType]
    routingInformation: Optional[str] = None
    trackingNumber: Optional[str] = None
    constructCode: Optional[str] = None
    SKU: Optional[str] = None
    postage: Optional[int] = None
    extraServices: List[ExtraServiceType] = JList[ExtraServiceType]
    zone: Optional[str] = None
    commitment: Optional[CommitmentType] = JStruct[CommitmentType]
    weightUOM: Optional[str] = None
    weight: Optional[int] = None
    dimensionalWeight: Optional[int] = None
    fees: List[ExtraServiceType] = JList[ExtraServiceType]
    permitHolderName: Optional[str] = None
    inductionType: Optional[InductionTypeType] = JStruct[InductionTypeType]
    labelBrokerID: Optional[str] = None
    links: List[LinkType] = JList[LinkType]


@s(auto_attribs=True)
class LabelResponseType:
    labelMetadata: Optional[LabelMetadataType] = JStruct[LabelMetadataType]
    returnLabelMetadata: Optional[LabelMetadataType] = JStruct[LabelMetadataType]
    labelImage: Optional[str] = None
    receiptImage: Optional[str] = None
    returnLabelImage: Optional[str] = None
    returnReceiptImage: Optional[str] = None
