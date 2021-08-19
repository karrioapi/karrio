from attr import s
from typing import List, Optional
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Weight:
    value: List[str] = JList[str]
    units: List[str] = JList[str]


@s(auto_attribs=True)
class Messages:
    pickup_suburb: List[str] = JList[str]
    pickup_postcode: List[str] = JList[str]
    delivery_suburb: List[str] = JList[str]
    delivery_postcode: List[str] = JList[str]
    weight: Optional[Weight] = JStruct[Weight]


@s(auto_attribs=True)
class ValidationError:
    messages: Optional[Messages] = JStruct[Messages]
    error: Optional[str] = None
    error_description: Optional[str] = None
