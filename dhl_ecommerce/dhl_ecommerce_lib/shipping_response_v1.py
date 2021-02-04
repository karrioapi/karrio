from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class BackendError:
    code: Optional[int] = None
    message: Optional[str] = None
    system: Optional[str] = None


@dataclass
class Details:
    msgId: Optional[str] = None


@dataclass
class Reason:
    msg: Optional[str] = None


@dataclass
class Error:
    reasons: Optional[List[Reason]] = None
    details: Optional[Details] = None
    backendError: Optional[BackendError] = None
    message: Optional[str] = None


@dataclass
class LabelResponse:
    packageId: Optional[int] = None
    trackingNumber: Optional[int] = None
    format: Optional[str] = None
    labels: Optional[str] = None


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
class LabelDetail:
    packageId: Optional[int] = None
    templateId: Optional[int] = None
    format: Optional[str] = None
    labelData: Optional[str] = None


@dataclass
class ResponseDetails:
    trackingNumber: Optional[int] = None
    labelDetails: Optional[List[LabelDetail]] = None


@dataclass
class Package:
    consigneeAddress: Optional[ConsigneeAddress] = None
    packageDetails: Optional[PackageDetails] = None
    responseDetails: Optional[ResponseDetails] = None


@dataclass
class Shipment:
    consignmentNumber: Optional[int] = None
    pickupAccount: Optional[str] = None
    distributionCenter: Optional[str] = None
    packages: Optional[List[Package]] = None


@dataclass
class ShippingResponse:
    shipments: Optional[List[Shipment]] = None
