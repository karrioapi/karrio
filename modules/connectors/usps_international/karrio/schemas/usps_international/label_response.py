from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ExtraServiceType:
    serviceID: Optional[str] = None
    serviceName: Optional[str] = None
    price: Optional[int] = None


@s(auto_attribs=True)
class FeeType:
    name: Optional[str] = None
    SKU: Optional[str] = None
    price: Optional[int] = None


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


@s(auto_attribs=True)
class LabelMetadataType:
    labelAddress: Optional[LabelAddressType] = JStruct[LabelAddressType]
    internationalTrackingNumber: Optional[str] = None
    constructCode: Optional[str] = None
    SKU: Optional[str] = None
    postage: Optional[int] = None
    extraServices: List[ExtraServiceType] = JList[ExtraServiceType]
    internationalPriceGroup: Optional[str] = None
    weightUOM: Optional[str] = None
    weight: Optional[int] = None
    dimensionalWeight: Optional[str] = None
    fees: List[FeeType] = JList[FeeType]
    labelBrokerID: Optional[str] = None


@s(auto_attribs=True)
class LabelResponseType:
    labelMetadata: Optional[LabelMetadataType] = JStruct[LabelMetadataType]
    labelImage: Optional[str] = None
