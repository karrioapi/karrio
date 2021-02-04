from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class ConsigneeAddress:
    postalCode: Optional[int] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    companyName: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    idNumber: Optional[str] = None
    idType: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    state: Optional[str] = None


@dataclass
class CustomsDetail:
    hsCode: Optional[int] = None
    itemDescription: Optional[str] = None
    countryOfOrigin: Optional[str] = None
    packagedQuantity: Optional[int] = None
    itemValue: Optional[float] = None
    skuNumber: Optional[str] = None


@dataclass
class PackageDetails:
    dgCategory: Optional[int] = None
    billingRef1: Optional[str] = None
    codAmount: Optional[float] = None
    currency: Optional[str] = None
    declaredValue: Optional[float] = None
    deliveryConfirmationNo: Optional[str] = None
    dimensionUom: Optional[str] = None
    dutiesPaid: Optional[str] = None
    insuredValue: Optional[float] = None
    mailType: Optional[int] = None
    orderedProduct: Optional[str] = None
    packageDesc: Optional[str] = None
    packageId: Optional[str] = None
    packageRefName: Optional[str] = None
    serviceEndorsement: Optional[int] = None
    weight: Optional[float] = None
    weightUom: Optional[str] = None
    height: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None


@dataclass
class ReturnAddress:
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    companyName: Optional[str] = None
    country: Optional[str] = None
    name: Optional[str] = None
    postalCode: Optional[str] = None
    state: Optional[str] = None


@dataclass
class Package:
    consigneeAddress: Optional[ConsigneeAddress] = None
    packageDetails: Optional[PackageDetails] = None
    returnAddress: Optional[ReturnAddress] = None
    customsDetails: Optional[List[CustomsDetail]] = None


@dataclass
class Shipment:
    consignmentNumber: Optional[int] = None
    pickupAccount: Optional[str] = None
    distributionCenter: Optional[str] = None
    packages: Optional[List[Package]] = None


@dataclass
class ShippingRequest:
    shipments: Optional[List[Shipment]] = None
