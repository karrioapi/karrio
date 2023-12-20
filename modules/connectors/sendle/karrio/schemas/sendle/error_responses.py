from attr import s
from typing import Any, Union, Optional


@s(auto_attribs=True)
class ErrorResponseType:
    messages: Union[dict, Any, str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
