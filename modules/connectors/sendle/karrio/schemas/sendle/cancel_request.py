from attr import s
from typing import Optional


@s(auto_attribs=True)
class CancelRequestType:
    id: Optional[int] = None
