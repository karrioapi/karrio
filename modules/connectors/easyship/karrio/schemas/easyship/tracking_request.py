from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ComparisonType:
    changes: Optional[str] = None
    post: Optional[str] = None
    pre: Optional[str] = None


@s(auto_attribs=True)
class ValidationType:
    detail: Optional[str] = None
    status: Optional[str] = None
    comparison: Optional[ComparisonType] = JStruct[ComparisonType]


@s(auto_attribs=True)
class NAddressType:
    city: Optional[str] = None
    companyname: Optional[str] = None
    contactemail: Optional[str] = None
    contactname: Optional[str] = None
    contactphone: Optional[str] = None
    countryalpha2: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    postalcode: Optional[str] = None
    state: Optional[str] = None
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class ItemType:
    description: Optional[str] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class TrackingRequestType:
    destinationaddress: Optional[NAddressType] = JStruct[NAddressType]
    originaddress: Optional[NAddressType] = JStruct[NAddressType]
    courierid: Optional[str] = None
    originaddressid: Optional[str] = None
    platformordernumber: Optional[int] = None
    items: List[ItemType] = JList[ItemType]
    trackingnumber: Optional[int] = None
