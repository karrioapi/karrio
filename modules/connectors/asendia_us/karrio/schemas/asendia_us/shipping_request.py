import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ItemType:
    sku: typing.Optional[str] = None
    itemDescription: typing.Optional[str] = None
    unitPrice: typing.Optional[int] = None
    quantity: typing.Optional[int] = None
    unitWeight: typing.Optional[int] = None
    countryOfOrigin: typing.Optional[str] = None
    htsNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    accountNumber: typing.Optional[str] = None
    subAccountNumber: typing.Optional[str] = None
    processingLocation: typing.Optional[str] = None
    includeRate: typing.Optional[bool] = None
    labelType: typing.Optional[str] = None
    orderNumber: typing.Optional[str] = None
    dispatchNumber: typing.Optional[str] = None
    packageID: typing.Optional[str] = None
    recipientTaxID: typing.Optional[str] = None
    returnFirstName: typing.Optional[str] = None
    returnLastName: typing.Optional[str] = None
    returnCompanyName: typing.Optional[str] = None
    returnAddressLine1: typing.Optional[str] = None
    returnAddressLine2: typing.Optional[str] = None
    returnAddressLine3: typing.Optional[str] = None
    returnCity: typing.Optional[str] = None
    returnProvince: typing.Optional[str] = None
    returnPostalCode: typing.Optional[str] = None
    returnCountryCode: typing.Optional[str] = None
    returnPhone: typing.Optional[str] = None
    returnEmail: typing.Optional[str] = None
    recipientFirstName: typing.Optional[str] = None
    recipientLastName: typing.Optional[str] = None
    recipientBusinessName: typing.Optional[str] = None
    recipientAddressLine1: typing.Optional[str] = None
    recipientAddressLine2: typing.Optional[str] = None
    recipientAddressLine3: typing.Optional[str] = None
    recipientCity: typing.Optional[str] = None
    recipientProvince: typing.Optional[str] = None
    recipientPostalCode: typing.Optional[str] = None
    recipientCountryCode: typing.Optional[str] = None
    recipientPhone: typing.Optional[str] = None
    recipientEmail: typing.Optional[str] = None
    totalPackageWeight: typing.Optional[int] = None
    weightUnit: typing.Optional[str] = None
    dimLength: typing.Optional[int] = None
    dimWidth: typing.Optional[int] = None
    dimHeight: typing.Optional[int] = None
    dimUnit: typing.Optional[str] = None
    totalPackageValue: typing.Optional[int] = None
    currencyType: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    customerReferenceNumber1: typing.Optional[str] = None
    customerReferenceNumber2: typing.Optional[str] = None
    customerReferenceNumber3: typing.Optional[str] = None
    contentType: typing.Optional[str] = None
    packageContentDescription: typing.Optional[str] = None
    vatNumber: typing.Optional[str] = None
    sellerName: typing.Optional[str] = None
    sellerAddressLine1: typing.Optional[str] = None
    sellerAddressLine2: typing.Optional[str] = None
    sellerAddressLine3: typing.Optional[str] = None
    sellerCity: typing.Optional[str] = None
    sellerProvince: typing.Optional[str] = None
    sellerPostalCode: typing.Optional[str] = None
    sellerCountryCode: typing.Optional[str] = None
    sellerPhone: typing.Optional[str] = None
    sellerEmail: typing.Optional[str] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
