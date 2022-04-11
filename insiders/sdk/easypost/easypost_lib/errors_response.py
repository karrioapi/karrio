from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ErrorElement:
    field: Optional[str] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None


@s(auto_attribs=True)
class ReponseError:
    code: Optional[str] = None
    message: Optional[str] = None
    errors: List[ErrorElement] = JList[ErrorElement]


@s(auto_attribs=True)
class Reponse:
    error: Optional[ReponseError] = JStruct[ReponseError]


@s(auto_attribs=True)
class ErrorsResponse:
    reponse: Optional[Reponse] = JStruct[Reponse]
