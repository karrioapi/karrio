from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AlertType:
    code: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class LocalizationType:
    localeCode: Optional[str] = None
    languageCode: Optional[str] = None


@s(auto_attribs=True)
class OutputType:
    alerts: List[AlertType] = JList[AlertType]
    localization: Optional[LocalizationType] = JStruct[LocalizationType]
    documentType: Optional[str] = None
    documentFormat: Optional[str] = None
    documents: List[str] = []


@s(auto_attribs=True)
class TrackingDocumentResponseType:
    transactionId: Optional[str] = None
    output: Optional[OutputType] = JStruct[OutputType]
