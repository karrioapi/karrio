from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class AddressType:
    AddressType: Optional[str] = None
    Street: Optional[str] = None
    HouseNr: Optional[int] = None
    HouseNrExt: Optional[str] = None
    Zipcode: Optional[str] = None
    City: Optional[str] = None
    Countrycode: Optional[str] = None


@s(auto_attribs=True)
class CutOffTimeType:
    Day: Optional[str] = None
    Available: Optional[bool] = None
    Type: Optional[str] = None
    Time: Optional[str] = None


@s(auto_attribs=True)
class RateRequestType:
    OrderDate: Optional[str] = None
    ShippingDuration: Optional[int] = None
    CutOffTimes: List[CutOffTimeType] = JList[CutOffTimeType]
    HolidaySorting: Optional[bool] = None
    Options: List[str] = []
    Locations: Optional[int] = None
    Days: Optional[int] = None
    Addresses: List[AddressType] = JList[AddressType]
