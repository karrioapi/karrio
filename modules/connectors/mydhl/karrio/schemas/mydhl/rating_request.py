from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountType:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class ErDetailsType:
    postalCode: Optional[str] = None
    cityName: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    countryCode: Optional[str] = None
    addressLine3: Optional[str] = None


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]
    receiverDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]


@s(auto_attribs=True)
class EstimatedDeliveryDateType:
    isRequested: Optional[bool] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class MonetaryAmountType:
    typeCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class PackageType:
    typeCode: Optional[str] = None
    weight: Optional[int] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class ProductsAndServiceType:
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None


@s(auto_attribs=True)
class RatingRequestType:
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    accounts: List[AccountType] = JList[AccountType]
    productsAndServices: List[ProductsAndServiceType] = JList[ProductsAndServiceType]
    payerCountryCode: Optional[str] = None
    plannedShippingDateAndTime: Optional[str] = None
    unitOfMeasurement: Optional[str] = None
    isCustomsDeclarable: Optional[bool] = None
    monetaryAmount: List[MonetaryAmountType] = JList[MonetaryAmountType]
    estimatedDeliveryDate: Optional[EstimatedDeliveryDateType] = JStruct[EstimatedDeliveryDateType]
    getAdditionalInformation: List[EstimatedDeliveryDateType] = JList[EstimatedDeliveryDateType]
    returnStandardProductsOnly: Optional[bool] = None
    nextBusinessDay: Optional[bool] = None
    productTypeCode: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]
