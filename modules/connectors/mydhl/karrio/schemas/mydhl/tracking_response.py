from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class EventServiceAreaType:
    code: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class EventType:
    date: Optional[str] = None
    time: Optional[str] = None
    GMTOffset: Optional[str] = None
    typeCode: Optional[str] = None
    description: Optional[str] = None
    serviceArea: List[EventServiceAreaType] = JList[EventServiceAreaType]
    signedBy: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class ShipperReferenceType:
    value: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class PieceType:
    number: Optional[int] = None
    typeCode: Optional[str] = None
    shipmentTrackingNumber: Optional[str] = None
    trackingNumber: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = None
    dimensionalWeight: Optional[float] = None
    actualWeight: Optional[float] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    actualDimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    unitOfMeasurements: Optional[str] = None
    shipperReferences: List[ShipperReferenceType] = JList[ShipperReferenceType]
    events: List[EventType] = JList[EventType]


@s(auto_attribs=True)
class PostalAddressType:
    cityName: Optional[str] = None
    countyName: Optional[str] = None
    postalCode: Optional[str] = None
    provinceCode: Optional[str] = None
    countryCode: Optional[str] = None


@s(auto_attribs=True)
class ReceiverDetailsServiceAreaType:
    code: Optional[str] = None
    description: Optional[str] = None
    facilityCode: Optional[str] = None
    inboundSortCode: Optional[str] = None


@s(auto_attribs=True)
class ReceiverDetailsType:
    name: Optional[str] = None
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    serviceArea: List[ReceiverDetailsServiceAreaType] = JList[ReceiverDetailsServiceAreaType]


@s(auto_attribs=True)
class ShipperDetailsServiceAreaType:
    code: Optional[str] = None
    description: Optional[str] = None
    outboundSortCode: Optional[str] = None


@s(auto_attribs=True)
class ShipperDetailsType:
    name: Optional[str] = None
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    serviceArea: List[ShipperDetailsServiceAreaType] = JList[ShipperDetailsServiceAreaType]


@s(auto_attribs=True)
class ShipmentType:
    shipmentTrackingNumber: Optional[int] = None
    status: Optional[str] = None
    shipmentTimestamp: Optional[str] = None
    productCode: Optional[str] = None
    description: Optional[str] = None
    shipperDetails: Optional[ShipperDetailsType] = JStruct[ShipperDetailsType]
    receiverDetails: Optional[ReceiverDetailsType] = JStruct[ReceiverDetailsType]
    totalWeight: Optional[int] = None
    unitOfMeasurements: Optional[str] = None
    shipperReferences: List[ShipperReferenceType] = JList[ShipperReferenceType]
    events: List[EventType] = JList[EventType]
    numberOfPieces: Optional[int] = None
    pieces: List[PieceType] = JList[PieceType]
    estimatedDeliveryDate: Optional[str] = None
    childrenShipmentIdentificationNumbers: List[int] = []
    controlledAccessDataCodes: List[str] = []


@s(auto_attribs=True)
class TrackingResponseType:
    shipments: List[ShipmentType] = JList[ShipmentType]
