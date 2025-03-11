import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CarrierDetailsType:
    UniqueId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    CarrierDetails: typing.Optional[CarrierDetailsType] = jstruct.JStruct[CarrierDetailsType]
    ShipmentId: typing.Optional[str] = None
    PackageOccurrence: typing.Optional[int] = None
    TrackingNumber: typing.Optional[str] = None
    CarrierTrackingUrl: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    Labels: typing.Optional[str] = None
    LabelFormat: typing.Optional[str] = None
    Packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
