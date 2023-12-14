from attr import s
from typing import Any, Union, Optional


@s(auto_attribs=True)
class MessagesClassType:
    pass


@s(auto_attribs=True)
class ErrorResponseType:
    messages: Union[MessagesClassType, Any, str]
    error: Optional[str] = None
    errordescription: Optional[str] = None
