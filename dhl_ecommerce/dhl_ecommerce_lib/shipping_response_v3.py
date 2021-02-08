import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Details:
    msgId: Optional[str] = None


@attr.s(auto_attribs=True)
class Reason:
    msg: Optional[str] = None


@attr.s(auto_attribs=True)
class Error:
    status: Optional[int] = None
    code: Optional[int] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    instance: Optional[str] = None
    reasons: Optional[List[Reason]] = JList[Reason]
    details: Optional[Details] = None


@attr.s(auto_attribs=True)
class LabelPiece:
    trackingNumber: Optional[int] = None
    id: Optional[str] = None
    format: Optional[str] = None
    labels: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class Label:
    pieces: Optional[List[LabelPiece]] = JList[LabelPiece]


@attr.s(auto_attribs=True)
class Piece:
    trackingNumber: Optional[int] = None
    id: Optional[str] = None
    format: Optional[str] = None
    labels: Optional[List[str]] = None
    status: Optional[int] = None
    title: Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentPiece:
    pieceId: Optional[int] = None
    trackingNumber: Optional[int] = None
    title: Optional[str] = None
    status: Optional[int] = None
    code: Optional[int] = None
    detail: Optional[str] = None
    labels: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class Shipment:
    id: Optional[int] = None
    status: Optional[str] = None
    url: Optional[str] = None
    pieces: Optional[List[ShipmentPiece]] = JList[ShipmentPiece]


@attr.s(auto_attribs=True)
class ShippingResponse:
    shipments: Optional[List[Shipment]] = JList[Shipment]
