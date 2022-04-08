from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Address:
    mode: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None
    country: Optional[str] = None
    residential: None
    carrierfacility: None
    name: None
    company: Optional[str] = None
    phone: Optional[str] = None
    email: None
    federaltaxid: None
    statetaxid: None


@s(auto_attribs=True)
class Parcel:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    predefinedpackage: None
    weight: Optional[float] = None


@s(auto_attribs=True)
class ShipmentRequest:
    reference: Optional[str] = None
    toaddress: Optional[Address] = JStruct[Address]
    fromaddress: Optional[Address] = JStruct[Address]
    parcel: Optional[Parcel] = JStruct[Parcel]
    carrieraccounts: List[str] = JList[str]
