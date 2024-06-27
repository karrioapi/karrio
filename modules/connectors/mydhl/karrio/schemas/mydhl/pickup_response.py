from attr import s
from typing import List


@s(auto_attribs=True)
class PickupResponseType:
    dispatchConfirmationNumbers: List[str] = []
