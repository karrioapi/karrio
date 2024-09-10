from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class PackageType:
    packageType: Optional[str] = None
    packageCount: Optional[int] = None


@s(auto_attribs=True)
class AddressType:
    streetAddress: Optional[str] = None
    secondaryAddress: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    ZIPCode: Optional[str] = None
    ZIPPlus4: Optional[str] = None
    urbanization: Optional[str] = None


@s(auto_attribs=True)
class ContactType:
    email: Optional[str] = None


@s(auto_attribs=True)
class PickupAddressType:
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    firm: Optional[str] = None
    address: Optional[AddressType] = JStruct[AddressType]
    contact: List[ContactType] = JList[ContactType]


@s(auto_attribs=True)
class PickupLocationType:
    packageLocation: Optional[str] = None
    specialInstructions: Optional[str] = None


@s(auto_attribs=True)
class PickupRequestType:
    pickupDate: Optional[str] = None
    pickupAddress: Optional[PickupAddressType] = JStruct[PickupAddressType]
    packages: List[PackageType] = JList[PackageType]
    estimatedWeight: Optional[int] = None
    pickupLocation: Optional[PickupLocationType] = JStruct[PickupLocationType]
