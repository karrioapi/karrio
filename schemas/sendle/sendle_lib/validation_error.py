from attr import s
from typing import List, Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Weight:
    value: List[str] = []
    units: List[str] = []


@s(auto_attribs=True)
class Messages:
    pickup_suburb: List[str] = []
    pickup_postcode: List[str] = []
    delivery_suburb: List[str] = []
    delivery_postcode: List[str] = []
    weight: Optional[Weight] = JStruct[Weight]


@s(auto_attribs=True)
class ValidationError:
    messages: Optional[Messages] = JStruct[Messages]
    error: Optional[str] = None
    error_description: Optional[str] = None
