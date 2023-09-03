from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Address:
    street: Optional[str] = None
    unit: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    isBusinessAddress: Optional[bool] = None


@s(auto_attribs=True)
class SizeOptions:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class WeightOptions:
    weight: Optional[float] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class Package:
    refNumber: Optional[int] = None
    weightOptions: Optional[WeightOptions] = JStruct[WeightOptions]
    sizeOptions: Optional[SizeOptions] = JStruct[SizeOptions]


@s(auto_attribs=True)
class Recipient:
    name: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class OrderRequest:
    recipient: Optional[Recipient] = JStruct[Recipient]
    recipientAddress: Optional[Address] = JStruct[Address]
    originAddress: Optional[Address] = JStruct[Address]
    packageCount: Optional[int] = None
    service: Optional[str] = None
    notes: Optional[str] = None
    refNumber: Optional[str] = None
    merchantDisplayName: Optional[str] = None
    signatureRequired: Optional[bool] = None
    packages: List[Package] = JList[Package]
