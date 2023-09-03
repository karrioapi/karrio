from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class DocumentType:
    imageFormat: Optional[str] = None
    content: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    referenceNumber: Optional[int] = None
    trackingNumber: Optional[str] = None
    trackingUrl: Optional[str] = None
    volumetricWeight: Optional[float] = None
    documents: List[DocumentType] = JList[DocumentType]


@s(auto_attribs=True)
class ServiceBreakdownType:
    name: Optional[str] = None
    price: Optional[int] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class ShipmentChargeType:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    price: Optional[int] = None
    serviceBreakdown: List[ServiceBreakdownType] = JList[ServiceBreakdownType]


@s(auto_attribs=True)
class ContactInformationType:
    companyName: Optional[str] = None
    fullName: Optional[str] = None


@s(auto_attribs=True)
class PostalAddressType:
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    cityDistrictName: Optional[str] = None


@s(auto_attribs=True)
class ErDetailsType:
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    contactInformation: Optional[ContactInformationType] = JStruct[ContactInformationType]


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]
    receiverDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]


@s(auto_attribs=True)
class ShipmentDetailType:
    serviceHandlingFeatureCodes: List[str] = []
    volumetricWeight: Optional[float] = None
    billingCode: Optional[str] = None
    serviceContentCode: Optional[str] = None
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]


@s(auto_attribs=True)
class ShipmentResponseType:
    url: Optional[str] = None
    shipmentTrackingNumber: Optional[int] = None
    cancelPickupUrl: Optional[str] = None
    trackingUrl: Optional[str] = None
    dispatchConfirmationNumber: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]
    documents: List[DocumentType] = JList[DocumentType]
    onDemandDeliveryURL: Optional[str] = None
    shipmentDetails: List[ShipmentDetailType] = JList[ShipmentDetailType]
    shipmentCharges: List[ShipmentChargeType] = JList[ShipmentChargeType]
    warnings: List[str] = []
