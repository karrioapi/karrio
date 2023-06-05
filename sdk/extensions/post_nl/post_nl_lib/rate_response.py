from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class SustainabilityType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class TimeframeType:
    From: Optional[str] = None
    To: Optional[str] = None
    Options: List[str] = []
    ShippingDate: Optional[str] = None
    Sustainability: Optional[SustainabilityType] = JStruct[SustainabilityType]


@s(auto_attribs=True)
class DeliveryOptionType:
    DeliveryDate: Optional[str] = None
    Timeframe: List[TimeframeType] = JList[TimeframeType]


@s(auto_attribs=True)
class AddressType:
    Street: Optional[str] = None
    Zipcode: Optional[str] = None
    HouseNr: Optional[int] = None
    HouseNrExt: Optional[int] = None
    Countrycode: Optional[str] = None
    CompanyName: Optional[str] = None


@s(auto_attribs=True)
class DayType:
    From: Optional[str] = None
    To: Optional[str] = None


@s(auto_attribs=True)
class OpeningHoursType:
    Monday: Optional[DayType] = JStruct[DayType]
    Tuesday: Optional[DayType] = JStruct[DayType]
    Wednesday: Optional[DayType] = JStruct[DayType]
    Thursday: Optional[DayType] = JStruct[DayType]
    Friday: Optional[DayType] = JStruct[DayType]
    Saturday: Optional[DayType] = JStruct[DayType]
    Sunday: Optional[DayType] = JStruct[DayType]


@s(auto_attribs=True)
class LocationType:
    Address: Optional[AddressType] = JStruct[AddressType]
    PickupTime: Optional[str] = None
    OpeningHours: Optional[OpeningHoursType] = JStruct[OpeningHoursType]
    Distance: Optional[int] = None
    LocationCode: Optional[str] = None
    PartnerID: Optional[str] = None
    Sustainability: Optional[SustainabilityType] = JStruct[SustainabilityType]


@s(auto_attribs=True)
class PickupOptionType:
    PickupDate: Optional[str] = None
    ShippingDate: Optional[str] = None
    Option: Optional[str] = None
    Locations: List[LocationType] = JList[LocationType]


@s(auto_attribs=True)
class WarningType:
    DeliveryDate: Optional[str] = None
    Code: Optional[int] = None
    Description: Optional[str] = None
    Options: List[str] = []


@s(auto_attribs=True)
class RateResponseType:
    DeliveryOptions: List[DeliveryOptionType] = JList[DeliveryOptionType]
    PickupOptions: List[PickupOptionType] = JList[PickupOptionType]
    Warnings: List[WarningType] = JList[WarningType]
