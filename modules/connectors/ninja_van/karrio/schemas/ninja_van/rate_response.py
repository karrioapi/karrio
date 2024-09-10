from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DataType:
    total_fee: Optional[int] = None


@s(auto_attribs=True)
class RateResponseType:
    data: Optional[DataType] = JStruct[DataType]
