from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class TrackDocumentDetailType:
    documentType: Optional[str] = None
    documentFormat: Optional[str] = None


@s(auto_attribs=True)
class TrackingNumberInfoType:
    trackingNumber: Optional[str] = None
    carrierCode: Optional[str] = None
    trackingNumberUniqueId: Optional[str] = None


@s(auto_attribs=True)
class TrackDocumentSpecificationType:
    trackingNumberInfo: Optional[TrackingNumberInfoType] = JStruct[TrackingNumberInfoType]
    shipDateBegin: Optional[str] = None
    shipDateEnd: Optional[str] = None
    accountNumber: Optional[str] = None


@s(auto_attribs=True)
class TrackingDocumentRequestType:
    trackDocumentDetail: Optional[TrackDocumentDetailType] = JStruct[TrackDocumentDetailType]
    trackDocumentSpecification: List[TrackDocumentSpecificationType] = JList[TrackDocumentSpecificationType]
