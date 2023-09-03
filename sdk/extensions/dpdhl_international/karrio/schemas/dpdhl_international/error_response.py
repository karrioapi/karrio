from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class ErrorResponseType:
    correlationId: Optional[str] = None
    messages: List[str] = []
