from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ConsigneeAddressClass:
    name: Optional[str] = None
    companyName: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    isBusiness: Optional[bool] = None
    idNumber: Optional[int] = None
    idType: Optional[int] = None
    taxId: Optional[int] = None
    taxIdType: Optional[int] = None


@s(auto_attribs=True)
class CustomsDetail:
    itemDescription: Optional[str] = None
    countryOfOrigin: Optional[str] = None
    hsCode: Optional[int] = None
    packagedQuantity: Optional[int] = None
    itemValue: Optional[float] = None
    currency: Optional[str] = None
    skuNumber: Optional[str] = None
    productUrl: Optional[str] = None


@s(auto_attribs=True)
class EstimatedDeliveryDate:
    calculate: Optional[bool] = None
    expectedShipDate: Optional[str] = None
    expectedTransit: Optional[int] = None
    deliveryBy: Optional[str] = None


@s(auto_attribs=True)
class Dimension:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    unitOfMeasure: Optional[str] = None


@s(auto_attribs=True)
class ShippingCost:
    currency: Optional[str] = None
    tax: Optional[float] = None
    freight: Optional[float] = None
    duty: Optional[float] = None
    declaredValue: Optional[float] = None
    insuredValue: Optional[int] = None
    dutiesPaid: Optional[bool] = None
    taxesPaid: Optional[bool] = None


@s(auto_attribs=True)
class Weight:
    value: Optional[float] = None
    unitOfMeasure: Optional[str] = None


@s(auto_attribs=True)
class PackageDetail:
    packageId: Optional[str] = None
    packageDescription: Optional[str] = None
    packageReference: Optional[str] = None
    service: Optional[str] = None
    serviceEndorsement: Optional[int] = None
    billingReference1: Optional[str] = None
    billingReference2: Optional[str] = None
    contentCategory: Optional[str] = None
    orderSource: Optional[str] = None
    customsCertificate: Optional[str] = None
    customsLicense: Optional[str] = None
    weight: Optional[Weight] = JStruct[Weight]
    dimension: Optional[Dimension] = JStruct[Dimension]
    shippingCost: Optional[ShippingCost] = JStruct[ShippingCost]


@s(auto_attribs=True)
class PickupAddressClass:
    name: Optional[str] = None
    companyName: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@s(auto_attribs=True)
class Rate:
    calculate: Optional[bool] = None
    rateDate: Optional[str] = None
    maxPrice: Optional[int] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class CreateLabelRequest:
    pickup: Optional[int] = None
    orderedProductId: Optional[str] = None
    distributionCenter: Optional[str] = None
    merchantId: Optional[str] = None
    consigneeAddress: Optional[ConsigneeAddressClass] = JStruct[ConsigneeAddressClass]
    shipperAddress: Optional[ConsigneeAddressClass] = JStruct[ConsigneeAddressClass]
    returnAddress: Optional[PickupAddressClass] = JStruct[PickupAddressClass]
    pickupAddress: Optional[PickupAddressClass] = JStruct[PickupAddressClass]
    packageDetail: Optional[PackageDetail] = JStruct[PackageDetail]
    customsDetails: List[CustomsDetail] = JList[CustomsDetail]
    rate: Optional[Rate] = JStruct[Rate]
    estimatedDeliveryDate: Optional[EstimatedDeliveryDate] = JStruct[EstimatedDeliveryDate]
