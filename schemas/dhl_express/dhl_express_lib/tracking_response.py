from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class EventServiceArea:
    code: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class Event:
    date: Optional[str] = None
    time: Optional[str] = None
    typeCode: Optional[str] = None
    description: Optional[str] = None
    serviceArea: List[EventServiceArea] = JList[EventServiceArea]
    signedBy: Optional[str] = None


@s(auto_attribs=True)
class Dimensions:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class ShipperReference:
    value: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class Piece:
    number: Optional[int] = None
    typeCode: Optional[str] = None
    shipmentTrackingNumber: Optional[str] = None
    trackingNumber: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = None
    dimensionalWeight: Optional[float] = None
    actualWeight: Optional[float] = None
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    actualDimensions: Optional[Dimensions] = JStruct[Dimensions]
    unitOfMeasurements: Optional[str] = None
    shipperReferences: List[ShipperReference] = JList[ShipperReference]
    events: List[Event] = JList[Event]


@s(auto_attribs=True)
class PostalAddress:
    cityName: Optional[str] = None
    countyName: Optional[str] = None
    postalCode: Optional[int] = None
    provinceCode: Optional[str] = None
    countryCode: Optional[str] = None


@s(auto_attribs=True)
class ReceiverDetailsServiceArea:
    code: Optional[str] = None
    description: Optional[str] = None
    facilityCode: Optional[str] = None
    inboundSortCode: Optional[str] = None


@s(auto_attribs=True)
class ReceiverDetails:
    name: Optional[str] = None
    postalAddress: Optional[PostalAddress] = JStruct[PostalAddress]
    serviceArea: List[ReceiverDetailsServiceArea] = JList[ReceiverDetailsServiceArea]


@s(auto_attribs=True)
class ShipperDetailsServiceArea:
    code: Optional[str] = None
    description: Optional[str] = None
    outboundSortCode: Optional[str] = None


@s(auto_attribs=True)
class ShipperDetails:
    name: Optional[str] = None
    postalAddress: Optional[PostalAddress] = JStruct[PostalAddress]
    serviceArea: List[ShipperDetailsServiceArea] = JList[ShipperDetailsServiceArea]
    accountNumber: Optional[str] = None


@s(auto_attribs=True)
class Shipment:
    shipmentTrackingNumber: Optional[int] = None
    status: Optional[str] = None
    shipmentTimestamp: Optional[str] = None
    productCode: Optional[str] = None
    description: Optional[str] = None
    shipperDetails: Optional[ShipperDetails] = JStruct[ShipperDetails]
    receiverDetails: Optional[ReceiverDetails] = JStruct[ReceiverDetails]
    totalWeight: Optional[int] = None
    unitOfMeasurements: Optional[str] = None
    shipperReferences: List[ShipperReference] = JList[ShipperReference]
    events: List[Event] = JList[Event]
    numberOfPieces: Optional[int] = None
    pieces: List[Piece] = JList[Piece]
    estimatedDeliveryDate: Optional[str] = None
    childrenShipmentIdentificationNumbers: List[int] = JList[int]


@s(auto_attribs=True)
class TrackingResponse:
    shipments: List[Shipment] = JList[Shipment]
