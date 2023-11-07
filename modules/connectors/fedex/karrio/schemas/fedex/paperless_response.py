from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class MetaType:
    documentType: Optional[str] = None
    docId: Optional[str] = None
    folderId: List[str] = []


@s(auto_attribs=True)
class OutputType:
    meta: Optional[MetaType] = JStruct[MetaType]


@s(auto_attribs=True)
class PaperlessResponseType:
    output: Optional[OutputType] = JStruct[OutputType]
    customerTransactionId: Optional[str] = None
