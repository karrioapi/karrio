from attr import s
from typing import List, Optional
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountAddressOfRecordType:
    streetLines: List[str] = []
    city: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    residential: Optional[bool] = None
    addressClassification: Optional[str] = None
    urbanizationCode: Optional[str] = None


@s(auto_attribs=True)
class AccountNumberType:
    value: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class ExpressFreightDetailType:
    truckType: Optional[str] = None
    service: Optional[str] = None
    trailerLength: Optional[str] = None
    bookingNumber: Optional[str] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class ContactType:
    companyName: Optional[str] = None
    personName: Optional[str] = None
    phoneNumber: Optional[str] = None
    phoneExtension: Optional[str] = None


@s(auto_attribs=True)
class PickupLocationType:
    contact: Optional[ContactType] = JStruct[ContactType]
    address: Optional[AccountAddressOfRecordType] = JStruct[AccountAddressOfRecordType]
    accountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    deliveryInstructions: Optional[str] = None


@s(auto_attribs=True)
class OriginDetailType:
    pickupAddressType: Optional[str] = None
    pickupLocation: Optional[PickupLocationType] = JStruct[PickupLocationType]
    readyDateTimestamp: Optional[str] = None
    customerCloseTime: Optional[str] = None
    pickupDateType: Optional[str] = None
    packageLocation: Optional[str] = None
    buildingPart: Optional[str] = None
    buildingPartDescription: Optional[int] = None
    earlyPickup: Optional[bool] = None
    suppliesRequested: Optional[str] = None
    geographicalPostalCode: Optional[str] = None


@s(auto_attribs=True)
class EmailDetailType:
    address: Optional[str] = None
    locale: Optional[str] = None


@s(auto_attribs=True)
class PickupNotificationDetailType:
    emailDetails: List[EmailDetailType] = JList[EmailDetailType]
    format: Optional[str] = None
    userMessage: Optional[str] = None


@s(auto_attribs=True)
class TotalWeightType:
    units: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class PickupRequestType:
    associatedAccountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    originDetail: Optional[OriginDetailType] = JStruct[OriginDetailType]
    associatedAccountNumberType: Optional[str] = None
    totalWeight: Optional[TotalWeightType] = JStruct[TotalWeightType]
    packageCount: Optional[int] = None
    carrierCode: Optional[str] = None
    accountAddressOfRecord: Optional[AccountAddressOfRecordType] = JStruct[AccountAddressOfRecordType]
    remarks: Optional[str] = None
    countryRelationships: Optional[str] = None
    pickupType: Optional[str] = None
    trackingNumber: Optional[str] = None
    commodityDescription: Optional[str] = None
    expressFreightDetail: Optional[ExpressFreightDetailType] = JStruct[ExpressFreightDetailType]
    oversizePackageCount: Optional[int] = None
    pickupNotificationDetail: Optional[PickupNotificationDetailType] = JStruct[PickupNotificationDetailType]
