from attr import s
from typing import Optional


@s(auto_attribs=True)
class LabelResponseType:
    label: Optional[str] = None
