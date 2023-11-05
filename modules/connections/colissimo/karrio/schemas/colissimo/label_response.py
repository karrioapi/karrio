from attr import s
from typing import Optional, Any, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class LabelV2Response:
    parcelNumber: Optional[str] = None
    parcelNumberPartner: Optional[str] = None
    pdfUrl: Any = None
    fields: Any = None


@s(auto_attribs=True)
class Message:
    id: Optional[int] = None
    type: Optional[str] = None
    messageContent: Optional[str] = None
    replacementValues: List[Any] = []


@s(auto_attribs=True)
class LabelResponse:
    messages: List[Message] = JList[Message]
    labelXmlV2Reponse: Any = None
    labelV2Response: Optional[LabelV2Response] = JStruct[LabelV2Response]
