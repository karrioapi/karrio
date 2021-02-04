from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class Address:
    postalCode: Optional[int] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    companyName: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    state: Optional[str] = None
    idNumber: Optional[str] = None
    idType: Optional[str] = None


@dataclass
class Piece:
    pieceId: Optional[int] = None
    packingType: Optional[str] = None
    weight: Optional[float] = None


@dataclass
class ShipmentDetails:
    shipmentId: Optional[int] = None
    dgCategory: Optional[int] = None
    billingRef1: Optional[str] = None
    orderedProduct: Optional[str] = None
    shipmentDesc: Optional[str] = None
    dutiesPaid: Optional[str] = None
    insuranceCharges: Optional[float] = None
    freightCharges: Optional[float] = None
    taxCharges: Optional[float] = None
    weightUom: Optional[str] = None
    dimensionUom: Optional[str] = None
    currency: Optional[str] = None
    isCompleteDelivery: Optional[bool] = None


@dataclass
class Shipment:
    consigneeAddress: Optional[Address] = None
    shipmentDetails: Optional[ShipmentDetails] = None
    pieces: Optional[List[Piece]] = None


@dataclass
class ShipperAddress:
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    companyName: Optional[str] = None
    state: Optional[str] = None


@dataclass
class ShippingRequest:
    distributionCenter: Optional[str] = None
    pickupAccount: Optional[str] = None
    isWorkshare: Optional[bool] = None
    pickupAddress: Optional[Address] = None
    shipperAddress: Optional[ShipperAddress] = None
    shipments: Optional[List[Shipment]] = None
