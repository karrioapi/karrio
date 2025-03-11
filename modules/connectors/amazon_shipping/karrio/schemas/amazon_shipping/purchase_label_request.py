import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelSpecification:
    labelFormat: typing.Optional[str] = None
    labelStockSize: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PurchaseLabelRequest:
    labelSpecification: typing.Optional[LabelSpecification] = jstruct.JStruct[LabelSpecification]
    rateId: typing.Optional[str] = None
