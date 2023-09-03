from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountType:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class ErDetailsType:
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    countyName: Optional[str] = None


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]
    receiverDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]


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
    weight: Optional[float] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: Optional[str] = None
    localServiceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ProductsAndServiceType:
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    valueAddedServices: List[ValueAddedServiceType] = JList[ValueAddedServiceType]


@s(auto_attribs=True)
class RatingRequestType:
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    accounts: List[AccountType] = JList[AccountType]
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    valueAddedServices: List[ValueAddedServiceType] = JList[ValueAddedServiceType]
    productsAndServices: List[ProductsAndServiceType] = JList[ProductsAndServiceType]
    payerCountryCode: Optional[str] = None
    plannedShippingDateAndTime: Optional[str] = None
    unitOfMeasurement: Optional[str] = None
    isCustomsDeclarable: Optional[bool] = None
    monetaryAmount: List[MonetaryAmountType] = JList[MonetaryAmountType]
    requestAllValueAddedServices: Optional[bool] = None
    returnStandardProductsOnly: Optional[bool] = None
    nextBusinessDay: Optional[bool] = None
    productTypeCode: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]
