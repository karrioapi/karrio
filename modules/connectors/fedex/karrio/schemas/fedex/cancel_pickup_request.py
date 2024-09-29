from attr import s
from typing import List, Optional
from jstruct import JStruct


@s(auto_attribs=True)
class AccountAddressOfRecordType:
    streetLines: List[str] = []
    urbanizationCode: Optional[str] = None
    city: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    residential: Optional[bool] = None
    addressClassification: Optional[str] = None


@s(auto_attribs=True)
class AssociatedAccountNumberType:
    value: Optional[str] = None


@s(auto_attribs=True)
class CancelPickupRequestType:
    associatedAccountNumber: Optional[AssociatedAccountNumberType] = JStruct[AssociatedAccountNumberType]
    pickupConfirmationCode: Optional[int] = None
    remarks: Optional[str] = None
    carrierCode: Optional[str] = None
    accountAddressOfRecord: Optional[AccountAddressOfRecordType] = JStruct[AccountAddressOfRecordType]
    scheduledDate: Optional[str] = None
    location: Optional[str] = None
