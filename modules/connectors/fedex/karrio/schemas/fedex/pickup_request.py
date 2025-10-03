import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountAddressOfRecordType:
    streetLines: typing.Optional[typing.List[str]] = None
    city: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    addressClassification: typing.Optional[str] = None
    urbanizationCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AccountNumberType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExpressFreightDetailType:
    truckType: typing.Optional[str] = None
    service: typing.Optional[str] = None
    trailerLength: typing.Optional[str] = None
    bookingNumber: typing.Optional[str] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ContactType:
    companyName: typing.Optional[str] = None
    personName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    phoneExtension: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupLocationType:
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    address: typing.Optional[AccountAddressOfRecordType] = jstruct.JStruct[AccountAddressOfRecordType]
    accountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    deliveryInstructions: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OriginDetailType:
    pickupAddressType: typing.Optional[str] = None
    pickupLocation: typing.Optional[PickupLocationType] = jstruct.JStruct[PickupLocationType]
    readyDateTimestamp: typing.Optional[str] = None
    customerCloseTime: typing.Optional[str] = None
    pickupDateType: typing.Optional[str] = None
    packageLocation: typing.Optional[str] = None
    buildingPart: typing.Optional[str] = None
    buildingPartDescription: typing.Optional[int] = None
    earlyPickup: typing.Optional[bool] = None
    suppliesRequested: typing.Optional[str] = None
    geographicalPostalCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EmailDetailType:
    address: typing.Optional[str] = None
    locale: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupNotificationDetailType:
    emailDetails: typing.Optional[typing.List[EmailDetailType]] = jstruct.JList[EmailDetailType]
    format: typing.Optional[str] = None
    userMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TotalWeightType:
    units: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupRequestType:
    associatedAccountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    originDetail: typing.Optional[OriginDetailType] = jstruct.JStruct[OriginDetailType]
    associatedAccountNumberType: typing.Optional[str] = None
    totalWeight: typing.Optional[TotalWeightType] = jstruct.JStruct[TotalWeightType]
    packageCount: typing.Optional[int] = None
    carrierCode: typing.Optional[str] = None
    accountAddressOfRecord: typing.Optional[AccountAddressOfRecordType] = jstruct.JStruct[AccountAddressOfRecordType]
    remarks: typing.Optional[str] = None
    countryRelationships: typing.Optional[str] = None
    pickupType: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    commodityDescription: typing.Optional[str] = None
    expressFreightDetail: typing.Optional[ExpressFreightDetailType] = jstruct.JStruct[ExpressFreightDetailType]
    oversizePackageCount: typing.Optional[int] = None
    pickupNotificationDetail: typing.Optional[PickupNotificationDetailType] = jstruct.JStruct[PickupNotificationDetailType]
