from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class LabelSpecification:
    labelFormat: Optional[str] = None
    labelStockSize: Optional[str] = None


@s(auto_attribs=True)
class ShippingLabel:
    labelStream: Optional[str] = None
    labelSpecification: Optional[LabelSpecification] = JStruct[LabelSpecification]
