import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    shipmentTrackingNumber: typing.Optional[typing.List[str]] = None
    pieceTrackingNumber: typing.Optional[typing.List[str]] = None
    shipmentReference: typing.Optional[str] = None
    shipmentReferenceType: typing.Optional[str] = None
    shipperAccountNumber: typing.Optional[str] = None
    dateRangeFrom: typing.Optional[str] = None
    dateRangeTo: typing.Optional[str] = None
    trackingView: typing.Optional[str] = None
    levelOfDetail: typing.Optional[str] = None
    requestControlledAccessDataCodes: typing.Optional[bool] = None
