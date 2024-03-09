from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class HeaderType:
    MessageVersion: Optional[str] = None
    MessageIdentifier: Optional[str] = None
    CreateTimestamp: Optional[str] = None
    DocumentType: Optional[str] = None
    Environment: Optional[str] = None
    SourceSystemCode: Optional[str] = None
    MessageSender: Optional[str] = None
    MessageReceiver: Optional[str] = None


@s(auto_attribs=True)
class LabelType:
    pass


@s(auto_attribs=True)
class TollMessageType:
    Header: Optional[HeaderType] = JStruct[HeaderType]
    Label: Optional[LabelType] = JStruct[LabelType]


@s(auto_attribs=True)
class LabelResponseType:
    TollMessage: Optional[TollMessageType] = JStruct[TollMessageType]
