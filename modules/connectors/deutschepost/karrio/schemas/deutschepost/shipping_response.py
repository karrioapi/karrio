from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CodLabelType:
    b64: Optional[str] = None
    zpl2: Optional[str] = None
    url: Optional[str] = None
    fileFormat: Optional[str] = None
    printFormat: Optional[str] = None


@s(auto_attribs=True)
class StatusType:
    title: Optional[str] = None
    statusCode: Optional[int] = None
    instance: Optional[str] = None
    detail: Optional[str] = None


@s(auto_attribs=True)
class ValidationMessageType:
    property: Optional[str] = None
    validationMessage: Optional[str] = None
    validationState: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    shipmentNo: Optional[str] = None
    returnShipmentNo: Optional[str] = None
    sstatus: Optional[StatusType] = JStruct[StatusType]
    shipmentRefNo: Optional[str] = None
    label: Optional[CodLabelType] = JStruct[CodLabelType]
    returnLabel: Optional[CodLabelType] = JStruct[CodLabelType]
    customsDoc: Optional[CodLabelType] = JStruct[CodLabelType]
    codLabel: Optional[CodLabelType] = JStruct[CodLabelType]
    validationMessages: List[ValidationMessageType] = JList[ValidationMessageType]


@s(auto_attribs=True)
class ShippingResponseType:
    status: Optional[StatusType] = JStruct[StatusType]
    items: List[ItemType] = JList[ItemType]
