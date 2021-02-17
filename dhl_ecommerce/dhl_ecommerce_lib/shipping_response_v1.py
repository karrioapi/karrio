import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class BackendError:
    code: Optional[int] = None
    message: Optional[str] = None
    system: Optional[str] = None


@attr.s(auto_attribs=True)
class Details:
    msgId: Optional[str] = None


@attr.s(auto_attribs=True)
class Reason:
    msg: Optional[str] = None


@attr.s(auto_attribs=True)
class Error:
    reasons: Optional[List[Reason]] = JStruct[Reason]
    details: Optional[Details] = JStruct[Details]
    backendError: Optional[BackendError] = JStruct[BackendError]
    message: Optional[str] = None


@attr.s(auto_attribs=True)
class LabelResponse:
    packageId: Optional[int] = None
    trackingNumber: Optional[int] = None
    format: Optional[str] = None
    labels: Optional[str] = None


@attr.s(auto_attribs=True)
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


@attr.s(auto_attribs=True)
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


@attr.s(auto_attribs=True)
class LabelDetail:
    packageId: Optional[int] = None
    templateId: Optional[int] = None
    format: Optional[str] = None
    labelData: Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseDetails:
    trackingNumber: Optional[int] = None
    labelDetails: Optional[List[LabelDetail]] = JList[LabelDetail]


@attr.s(auto_attribs=True)
class Package:
    consigneeAddress: Optional[ConsigneeAddress] = JStruct[ConsigneeAddress]
    packageDetails: Optional[PackageDetails] = JStruct[PackageDetails]
    responseDetails: Optional[ResponseDetails] = JStruct[ResponseDetails]


@attr.s(auto_attribs=True)
class Shipment:
    consignmentNumber: Optional[int] = None
    pickupAccount: Optional[str] = None
    distributionCenter: Optional[str] = None
    packages: Optional[List[Package]] = JList[Package]


@attr.s(auto_attribs=True)
class ShippingResponse:
    shipments: Optional[List[Shipment]] = JList[Shipment]
