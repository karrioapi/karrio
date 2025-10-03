import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingNumberInfoType:
    trackingNumber: typing.Optional[str] = None
    carrierCode: typing.Optional[str] = None
    trackingNumberUniqueId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingInfoType:
    shipDateBegin: typing.Optional[str] = None
    shipDateEnd: typing.Optional[str] = None
    trackingNumberInfo: typing.Optional[TrackingNumberInfoType] = jstruct.JStruct[TrackingNumberInfoType]


@attr.s(auto_attribs=True)
class TrackingRequestType:
    includeDetailedScans: typing.Optional[bool] = None
    trackingInfo: typing.Optional[typing.List[TrackingInfoType]] = jstruct.JList[TrackingInfoType]
