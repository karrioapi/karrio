from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class MetaType:
    availablebalance: Optional[int] = None
    easyshipshipmentids: List[str] = []
    requestid: Optional[str] = None


@s(auto_attribs=True)
class DefaultForType:
    billing: Optional[bool] = None
    pickup: Optional[bool] = None
    defaultforreturn: Optional[bool] = None
    sender: Optional[bool] = None


@s(auto_attribs=True)
class HkDistrictType:
    area: Optional[str] = None
    district: Optional[str] = None
    id: Optional[int] = None
    zone: Optional[str] = None


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
class AddressType:
    city: Optional[str] = None
    companyname: Optional[str] = None
    contactemail: Optional[str] = None
    contactname: Optional[str] = None
    contactphone: Optional[str] = None
    countryalpha2: Optional[str] = None
    defaultfor: Optional[DefaultForType] = JStruct[DefaultForType]
    hkdistrict: Optional[HkDistrictType] = JStruct[HkDistrictType]
    id: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    postalcode: Optional[str] = None
    state: Optional[str] = None
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class CourierType:
    id: Optional[str] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class PickupType:
    address: Optional[AddressType] = JStruct[AddressType]
    courier: Optional[CourierType] = JStruct[CourierType]
    easyshippickupid: Optional[str] = None
    pickupfee: Optional[int] = None
    pickupreferencenumber: Optional[str] = None
    pickupstate: Optional[str] = None
    providername: Optional[str] = None
    selectedfromtime: Optional[str] = None
    selectedtotime: Optional[str] = None
    shipmentscount: Optional[int] = None
    totalactualweight: Optional[float] = None


@s(auto_attribs=True)
class PickupResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    pickup: Optional[PickupType] = JStruct[PickupType]
