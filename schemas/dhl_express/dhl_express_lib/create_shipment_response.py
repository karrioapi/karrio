from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Document:
    imageFormat: Optional[str] = None
    content: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class Package:
    referenceNumber: Optional[int] = None
    trackingNumber: Optional[str] = None
    trackingUrl: Optional[str] = None
    volumetricWeight: Optional[float] = None
    documents: List[Document] = JList[Document]


@s(auto_attribs=True)
class ServiceBreakdown:
    name: Optional[str] = None
    price: Optional[int] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class ShipmentCharge:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    price: Optional[int] = None
    serviceBreakdown: List[ServiceBreakdown] = JList[ServiceBreakdown]


@s(auto_attribs=True)
class ContactInformation:
    companyName: Optional[str] = None
    fullName: Optional[str] = None


@s(auto_attribs=True)
class PostalAddress:
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    cityDistrictName: Optional[str] = None


@s(auto_attribs=True)
class ErDetails:
    postalAddress: Optional[PostalAddress] = JStruct[PostalAddress]
    contactInformation: Optional[ContactInformation] = JStruct[ContactInformation]


@s(auto_attribs=True)
class CustomerDetails:
    shipperDetails: Optional[ErDetails] = JStruct[ErDetails]
    receiverDetails: Optional[ErDetails] = JStruct[ErDetails]


@s(auto_attribs=True)
class ShipmentDetail:
    serviceHandlingFeatureCodes: List[str] = JList[str]
    volumetricWeight: Optional[float] = None
    billingCode: Optional[str] = None
    serviceContentCode: Optional[str] = None
    customerDetails: Optional[CustomerDetails] = JStruct[CustomerDetails]


@s(auto_attribs=True)
class CreateShipmentResponse:
    url: Optional[str] = None
    shipmentTrackingNumber: Optional[int] = None
    cancelPickupUrl: Optional[str] = None
    trackingUrl: Optional[str] = None
    dispatchConfirmationNumber: Optional[str] = None
    packages: List[Package] = JList[Package]
    documents: List[Document] = JList[Document]
    onDemandDeliveryURL: Optional[str] = None
    shipmentDetails: List[ShipmentDetail] = JList[ShipmentDetail]
    shipmentCharges: List[ShipmentCharge] = JList[ShipmentCharge]
    warnings: List[str] = JList[str]
