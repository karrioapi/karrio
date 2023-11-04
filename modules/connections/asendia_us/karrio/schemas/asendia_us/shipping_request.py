from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class ItemType:
    sku: Optional[str] = None
    itemDescription: Optional[str] = None
    unitPrice: Optional[int] = None
    quantity: Optional[int] = None
    unitWeight: Optional[int] = None
    countryOfOrigin: Optional[str] = None
    htsNumber: Optional[str] = None


@s(auto_attribs=True)
class ShippingRequestType:
    accountNumber: Optional[str] = None
    subAccountNumber: Optional[str] = None
    processingLocation: Optional[str] = None
    includeRate: Optional[bool] = None
    labelType: Optional[str] = None
    orderNumber: Optional[str] = None
    dispatchNumber: Optional[str] = None
    packageID: Optional[str] = None
    recipientTaxID: Optional[str] = None
    returnFirstName: Optional[str] = None
    returnLastName: Optional[str] = None
    returnCompanyName: Optional[str] = None
    returnAddressLine1: Optional[str] = None
    returnAddressLine2: Optional[str] = None
    returnAddressLine3: Optional[str] = None
    returnCity: Optional[str] = None
    returnProvince: Optional[str] = None
    returnPostalCode: Optional[str] = None
    returnCountryCode: Optional[str] = None
    returnPhone: Optional[str] = None
    returnEmail: Optional[str] = None
    recipientFirstName: Optional[str] = None
    recipientLastName: Optional[str] = None
    recipientBusinessName: Optional[str] = None
    recipientAddressLine1: Optional[str] = None
    recipientAddressLine2: Optional[str] = None
    recipientAddressLine3: Optional[str] = None
    recipientCity: Optional[str] = None
    recipientProvince: Optional[str] = None
    recipientPostalCode: Optional[str] = None
    recipientCountryCode: Optional[str] = None
    recipientPhone: Optional[str] = None
    recipientEmail: Optional[str] = None
    totalPackageWeight: Optional[int] = None
    weightUnit: Optional[str] = None
    dimLength: Optional[int] = None
    dimWidth: Optional[int] = None
    dimHeight: Optional[int] = None
    dimUnit: Optional[str] = None
    totalPackageValue: Optional[int] = None
    currencyType: Optional[str] = None
    productCode: Optional[str] = None
    customerReferenceNumber1: Optional[str] = None
    customerReferenceNumber2: Optional[str] = None
    customerReferenceNumber3: Optional[str] = None
    contentType: Optional[str] = None
    packageContentDescription: Optional[str] = None
    vatNumber: Optional[str] = None
    sellerName: Optional[str] = None
    sellerAddressLine1: Optional[str] = None
    sellerAddressLine2: Optional[str] = None
    sellerAddressLine3: Optional[str] = None
    sellerCity: Optional[str] = None
    sellerProvince: Optional[str] = None
    sellerPostalCode: Optional[str] = None
    sellerCountryCode: Optional[str] = None
    sellerPhone: Optional[str] = None
    sellerEmail: Optional[str] = None
    items: List[ItemType] = JList[ItemType]
