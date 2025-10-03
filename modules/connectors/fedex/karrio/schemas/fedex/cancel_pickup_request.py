import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountAddressOfRecordType:
    streetLines: typing.Optional[typing.List[str]] = None
    urbanizationCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    addressClassification: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AssociatedAccountNumberType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CancelPickupRequestType:
    associatedAccountNumber: typing.Optional[AssociatedAccountNumberType] = jstruct.JStruct[AssociatedAccountNumberType]
    pickupConfirmationCode: typing.Optional[int] = None
    remarks: typing.Optional[str] = None
    carrierCode: typing.Optional[str] = None
    accountAddressOfRecord: typing.Optional[AccountAddressOfRecordType] = jstruct.JStruct[AccountAddressOfRecordType]
    scheduledDate: typing.Optional[str] = None
    location: typing.Optional[str] = None
