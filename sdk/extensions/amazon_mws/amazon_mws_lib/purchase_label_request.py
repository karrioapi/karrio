from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class LabelSpecification:
    labelFormat: Optional[str] = None
    labelStockSize: Optional[str] = None


@s(auto_attribs=True)
class PurchaseLabelRequest:
    labelSpecification: Optional[LabelSpecification] = JStruct[LabelSpecification]
    rateId: Optional[str] = None
