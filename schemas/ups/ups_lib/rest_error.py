from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Error:
    code: Optional[int] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class Response:
    errors: List[Error] = JList[Error]


@s(auto_attribs=True)
class RESTError:
    response: Optional[Response] = JStruct[Response]
