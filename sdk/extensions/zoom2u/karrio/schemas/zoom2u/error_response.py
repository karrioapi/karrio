from attr import s
from typing import List, Optional
from jstruct import JStruct


@s(auto_attribs=True)
class ModelStateType:
    getQuoteRequestPickupSuburb: List[str] = []
    getQuoteRequestPickupPostcode: List[str] = []


@s(auto_attribs=True)
class ErrorResponseType:
    errorcode: Optional[str] = None
    message: Optional[str] = None
    modelState: Optional[ModelStateType] = JStruct[ModelStateType]
