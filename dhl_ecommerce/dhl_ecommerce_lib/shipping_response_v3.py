from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class Details:
    msgId: Optional[str] = None


@dataclass
class Reason:
    msg: Optional[str] = None


@dataclass
class Error:
    status: Optional[int] = None
    code: Optional[int] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    instance: Optional[str] = None
    reasons: Optional[List[Reason]] = None
    details: Optional[Details] = None


@dataclass
class LabelPiece:
    trackingNumber: Optional[int] = None
    id: Optional[str] = None
    format: Optional[str] = None
    labels: Optional[List[str]] = None


@dataclass
class Label:
    pieces: Optional[List[LabelPiece]] = None


@dataclass
class Piece:
    trackingNumber: Optional[int] = None
    id: Optional[str] = None
    format: Optional[str] = None
    labels: Optional[List[str]] = None
    status: Optional[int] = None
    title: Optional[str] = None


@dataclass
class ShipmentPiece:
    pieceId: Optional[int] = None
    trackingNumber: Optional[int] = None
    title: Optional[str] = None
    status: Optional[int] = None
    code: Optional[int] = None
    detail: Optional[str] = None
    labels: Optional[List[str]] = None


@dataclass
class Shipment:
    id: Optional[int] = None
    status: Optional[str] = None
    url: Optional[str] = None
    pieces: Optional[List[ShipmentPiece]] = None


@dataclass
class ShippingResponse:
    shipments: Optional[List[Shipment]] = None
