from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CarrierDetailsType:
    UniqueId: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    CarrierDetails: Optional[CarrierDetailsType] = JStruct[CarrierDetailsType]
    ShipmentId: Optional[str] = None
    PackageOccurrence: Optional[int] = None
    TrackingNumber: Optional[str] = None
    CarrierTrackingUrl: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponseType:
    Labels: Optional[str] = None
    LabelFormat: Optional[str] = None
    Packages: List[PackageType] = JList[PackageType]
