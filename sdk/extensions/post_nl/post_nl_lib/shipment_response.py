from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class LabelType:
    Content: Optional[str] = None
    Labeltype: Optional[str] = None
    OutputType: Optional[str] = None


@s(auto_attribs=True)
class MergedLabelType:
    Barcodes: List[str] = []
    Labels: List[LabelType] = JList[LabelType]


@s(auto_attribs=True)
class WarningType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class ResponseShipmentType:
    ProductCodeDelivery: Optional[int] = None
    Labels: List[LabelType] = JList[LabelType]
    Barcode: Optional[str] = None
    Warnings: List[WarningType] = JList[WarningType]


@s(auto_attribs=True)
class ShipmentResponseType:
    MergedLabels: List[MergedLabelType] = JList[MergedLabelType]
    ResponseShipments: List[ResponseShipmentType] = JList[ResponseShipmentType]
