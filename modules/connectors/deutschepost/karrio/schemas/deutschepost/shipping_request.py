from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ConsigneeType:
    name1: Optional[str] = None
    addressStreet: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    additionalAddressInformation1: Optional[str] = None


@s(auto_attribs=True)
class PostalChargesType:
    currency: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class WeightType:
    uom: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    itemDescription: Optional[str] = None
    packagedQuantity: Optional[int] = None
    hsCode: Optional[int] = None
    countryOfOrigin: Optional[str] = None
    itemValue: Optional[PostalChargesType] = JStruct[PostalChargesType]
    itemWeight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class CustomsType:
    exportType: Optional[str] = None
    postalCharges: Optional[PostalChargesType] = JStruct[PostalChargesType]
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class DimType:
    uom: Optional[str] = None
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None


@s(auto_attribs=True)
class DetailsType:
    dim: Optional[DimType] = JStruct[DimType]
    weight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class ServicesType:
    endorsement: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    product: Optional[str] = None
    billingNumber: Optional[str] = None
    refNo: Optional[str] = None
    shipper: Optional[ConsigneeType] = JStruct[ConsigneeType]
    consignee: Optional[ConsigneeType] = JStruct[ConsigneeType]
    details: Optional[DetailsType] = JStruct[DetailsType]
    customs: Optional[CustomsType] = JStruct[CustomsType]
    services: Optional[ServicesType] = JStruct[ServicesType]


@s(auto_attribs=True)
class ShippingRequestType:
    profile: Optional[str] = None
    shipments: List[ShipmentType] = JList[ShipmentType]
