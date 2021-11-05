from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Account:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class ErDetails:
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    countyName: Optional[str] = None


@s(auto_attribs=True)
class CustomerDetails:
    shipperDetails: Optional[ErDetails] = JStruct[ErDetails]
    receiverDetails: Optional[ErDetails] = JStruct[ErDetails]


@s(auto_attribs=True)
class MonetaryAmount:
    typeCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class Dimensions:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class Package:
    typeCode: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dimensions] = JStruct[Dimensions]


@s(auto_attribs=True)
class ValueAddedService:
    serviceCode: Optional[str] = None
    localServiceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ProductsAndService:
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    valueAddedServices: List[ValueAddedService] = JList[ValueAddedService]


@s(auto_attribs=True)
class RatingRequest:
    customerDetails: Optional[CustomerDetails] = JStruct[CustomerDetails]
    accounts: List[Account] = JList[Account]
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    valueAddedServices: List[ValueAddedService] = JList[ValueAddedService]
    productsAndServices: List[ProductsAndService] = JList[ProductsAndService]
    payerCountryCode: Optional[str] = None
    plannedShippingDateAndTime: Optional[str] = None
    unitOfMeasurement: Optional[str] = None
    isCustomsDeclarable: Optional[bool] = None
    monetaryAmount: List[MonetaryAmount] = JList[MonetaryAmount]
    requestAllValueAddedServices: Optional[bool] = None
    returnStandardProductsOnly: Optional[bool] = None
    nextBusinessDay: Optional[bool] = None
    productTypeCode: Optional[str] = None
    packages: List[Package] = JList[Package]
