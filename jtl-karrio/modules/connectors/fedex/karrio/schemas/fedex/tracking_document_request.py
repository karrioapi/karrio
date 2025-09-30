import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackDocumentDetailType:
    documentType: typing.Optional[str] = None
    documentFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingNumberInfoType:
    trackingNumber: typing.Optional[str] = None
    carrierCode: typing.Optional[str] = None
    trackingNumberUniqueId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackDocumentSpecificationType:
    trackingNumberInfo: typing.Optional[TrackingNumberInfoType] = jstruct.JStruct[TrackingNumberInfoType]
    shipDateBegin: typing.Optional[str] = None
    shipDateEnd: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDocumentRequestType:
    trackDocumentDetail: typing.Optional[TrackDocumentDetailType] = jstruct.JStruct[TrackDocumentDetailType]
    trackDocumentSpecification: typing.Optional[typing.List[TrackDocumentSpecificationType]] = jstruct.JList[TrackDocumentSpecificationType]
