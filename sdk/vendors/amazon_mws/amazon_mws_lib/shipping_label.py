from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None


@s(auto_attribs=True)
class LabelSpecification:
    labelFormat: Optional[str] = None
    labelStockSize: Optional[str] = None


@s(auto_attribs=True)
class Payload:
    labelStream: Optional[str] = None
    labelSpecification: Optional[LabelSpecification] = JStruct[LabelSpecification]


@s(auto_attribs=True)
class ShippingLabel:
    payload: Optional[Payload] = JStruct[Payload]
    errors: List[Error] = JList[Error]
