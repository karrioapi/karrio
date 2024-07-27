from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class FromAddressType:
    ignoreBadAddress: Optional[bool] = None
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


@s(auto_attribs=True)
class ShipmentType:
    pass


@s(auto_attribs=True)
class SCANFormMetadataType:
    form: Optional[int] = None
    imageType: Optional[str] = None
    labelType: Optional[str] = None
    mailingDate: Optional[str] = None
    overwriteMailingDate: Optional[bool] = None
    entryFacilityZIPCode: Optional[int] = None
    destinationEntryFacilityType: Optional[str] = None
    shipment: Optional[ShipmentType] = JStruct[ShipmentType]
    manifestNumber: Optional[str] = None
    trackingNumbers: List[str] = []
    fromAddress: Optional[FromAddressType] = JStruct[FromAddressType]


@s(auto_attribs=True)
class ScanFormResponseType:
    SCANFormMetadata: Optional[SCANFormMetadataType] = JStruct[SCANFormMetadataType]
    SCANFormImage: Optional[str] = None
