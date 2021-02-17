import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
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


@attr.s(auto_attribs=True)
class Piece:
    pieceId: Optional[int] = None
    packingType: Optional[str] = None
    weight: Optional[float] = None


@attr.s(auto_attribs=True)
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


@attr.s(auto_attribs=True)
class Shipment:
    consigneeAddress: Optional[Address] = JStruct[Address]
    shipmentDetails: Optional[ShipmentDetails] = JStruct[ShipmentDetails]
    pieces: Optional[List[Piece]] = None


@attr.s(auto_attribs=True)
class ShipperAddress:
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    companyName: Optional[str] = None
    state: Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequest:
    distributionCenter: Optional[str] = None
    pickupAccount: Optional[str] = None
    isWorkshare: Optional[bool] = None
    pickupAddress: Optional[Address] = JStruct[Address]
    shipperAddress: Optional[ShipperAddress] = JStruct[ShipperAddress]
    shipments: Optional[List[Shipment]] = JList[Shipment]
