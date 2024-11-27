from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CommitmentType:
    name: Optional[str] = None
    scheduleDeliveryDate: Optional[str] = None


@s(auto_attribs=True)
class ExtraServiceType:
    serviceID: Optional[str] = None
    serviceName: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    SKU: Optional[str] = None


@s(auto_attribs=True)
class LabelAddressType:
    streetAddress: Optional[str] = None
    streetAddressAbbreviation: Optional[str] = None
    secondaryAddress: Optional[str] = None
    cityAbbreviation: Optional[str] = None
    city: Optional[str] = None
    postalCode: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    countryISOAlpha2Code: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    firm: Optional[str] = None
    phone: Optional[str] = None
    ignoreBadAddress: Optional[bool] = None


@s(auto_attribs=True)
class LabelMetadataType:
    labelAddress: Optional[LabelAddressType] = JStruct[LabelAddressType]
    routingInformation: Optional[int] = None
    trackingNumber: Optional[str] = None
    constructCode: Optional[str] = None
    SKU: Optional[str] = None
    postage: Optional[float] = None
    extraServices: List[ExtraServiceType] = JList[ExtraServiceType]
    internationalPriceGroup: Optional[str] = None
    zone: Optional[str] = None
    commitment: Optional[CommitmentType] = JStruct[CommitmentType]
    weightUOM: Optional[str] = None
    weight: Optional[float] = None
    dimensionalWeight: Optional[float] = None
    fees: List[Any] = []
    labelBrokerID: Optional[str] = None
    bannerText: Optional[str] = None
    retailDistributionCode: Optional[str] = None
    serviceTypeCode: Optional[int] = None


@s(auto_attribs=True)
class LabelResponseType:
    labelMetadata: Optional[LabelMetadataType] = JStruct[LabelMetadataType]
    labelImage: Optional[str] = None
