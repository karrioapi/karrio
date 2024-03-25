from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ConsigneeType:
    name1: Optional[str] = None
    name2: Optional[str] = None
    name3: Optional[str] = None
    dispatchingInformation: Optional[str] = None
    addressStreet: Optional[str] = None
    addressHouse: Optional[str] = None
    additionalAddressInformation1: Optional[str] = None
    additionalAddressInformation2: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    contactName: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    lockerID: Optional[int] = None
    postNumber: Optional[int] = None
    retailID: Optional[int] = None
    poBoxID: Optional[int] = None


@s(auto_attribs=True)
class PostalChargesType:
    currency: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class WeightType:
    uom: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class ItemType:
    itemDescription: Optional[str] = None
    countryOfOrigin: Optional[str] = None
    hsCode: Optional[int] = None
    packagedQuantity: Optional[int] = None
    itemValue: Optional[PostalChargesType] = JStruct[PostalChargesType]
    itemWeight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class CustomsType:
    invoiceNo: Optional[int] = None
    exportType: Optional[str] = None
    exportDescription: Optional[str] = None
    shippingConditions: Optional[str] = None
    permitNo: Optional[int] = None
    attestationNo: Optional[int] = None
    hasElectronicExportNotification: Optional[bool] = None
    MRN: Optional[int] = None
    postalCharges: Optional[PostalChargesType] = JStruct[PostalChargesType]
    officeOfOrigin: Optional[str] = None
    shipperCustomsRef: Optional[int] = None
    consigneeCustomsRef: Optional[int] = None
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
class CashOnDeliveryType:
    currency: Optional[str] = None
    value: Optional[float] = None
    accountHolder: Optional[str] = None
    bankName: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None
    accountReference: Optional[str] = None
    transferNote1: Optional[str] = None
    transferNote2: Optional[str] = None


@s(auto_attribs=True)
class DhlRetoureType:
    billingNumber: Optional[str] = None
    refNo: Optional[str] = None
    returnAddress: Optional[ConsigneeType] = JStruct[ConsigneeType]


@s(auto_attribs=True)
class IdentCheckType:
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    dateOfBirth: Optional[str] = None
    minimumAge: Optional[str] = None


@s(auto_attribs=True)
class ServicesType:
    preferredNeighbour: Optional[str] = None
    preferredLocation: Optional[str] = None
    visualCheckOfAge: Optional[str] = None
    namedPersonOnly: Optional[bool] = None
    identCheck: Optional[IdentCheckType] = JStruct[IdentCheckType]
    signedForByRecipient: Optional[bool] = None
    endorsement: Optional[str] = None
    preferredDay: Optional[str] = None
    noNeighbourDelivery: Optional[bool] = None
    additionalInsurance: Optional[PostalChargesType] = JStruct[PostalChargesType]
    bulkyGoods: Optional[bool] = None
    cashOnDelivery: Optional[CashOnDeliveryType] = JStruct[CashOnDeliveryType]
    individualSenderRequirement: Optional[str] = None
    premium: Optional[bool] = None
    closestDropPoint: Optional[bool] = None
    parcelOutletRouting: Optional[str] = None
    dhlRetoure: Optional[DhlRetoureType] = JStruct[DhlRetoureType]
    postalDeliveryDutyPaid: Optional[bool] = None


@s(auto_attribs=True)
class ShipperType:
    name1: Optional[str] = None
    name2: Optional[str] = None
    name3: Optional[str] = None
    addressStreet: Optional[str] = None
    addressHouse: Optional[str] = None
    postalCode: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    contactName: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    product: Optional[str] = None
    billingNumber: Optional[str] = None
    refNo: Optional[str] = None
    costCenter: Optional[str] = None
    creationSoftware: Optional[str] = None
    shipDate: Optional[str] = None
    shipper: Optional[ShipperType] = JStruct[ShipperType]
    consignee: Optional[ConsigneeType] = JStruct[ConsigneeType]
    details: Optional[DetailsType] = JStruct[DetailsType]
    services: Optional[ServicesType] = JStruct[ServicesType]
    customs: Optional[CustomsType] = JStruct[CustomsType]


@s(auto_attribs=True)
class ShippingRequestType:
    profile: Optional[str] = None
    shipments: List[ShipmentType] = JList[ShipmentType]
