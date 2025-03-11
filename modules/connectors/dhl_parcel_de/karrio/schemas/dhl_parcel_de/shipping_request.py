import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ConsigneeType:
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    name3: typing.Optional[str] = None
    dispatchingInformation: typing.Optional[str] = None
    addressStreet: typing.Optional[str] = None
    addressHouse: typing.Optional[str] = None
    additionalAddressInformation1: typing.Optional[str] = None
    additionalAddressInformation2: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country: typing.Optional[str] = None
    contactName: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    name: typing.Optional[str] = None
    lockerID: typing.Optional[int] = None
    postNumber: typing.Optional[int] = None
    retailID: typing.Optional[int] = None
    poBoxID: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PostalChargesType:
    currency: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class WeightType:
    uom: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ItemType:
    itemDescription: typing.Optional[str] = None
    countryOfOrigin: typing.Optional[str] = None
    hsCode: typing.Optional[int] = None
    packagedQuantity: typing.Optional[int] = None
    itemValue: typing.Optional[PostalChargesType] = jstruct.JStruct[PostalChargesType]
    itemWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class CustomsType:
    invoiceNo: typing.Optional[int] = None
    exportType: typing.Optional[str] = None
    exportDescription: typing.Optional[str] = None
    shippingConditions: typing.Optional[str] = None
    permitNo: typing.Optional[int] = None
    attestationNo: typing.Optional[int] = None
    hasElectronicExportNotification: typing.Optional[bool] = None
    MRN: typing.Optional[int] = None
    postalCharges: typing.Optional[PostalChargesType] = jstruct.JStruct[PostalChargesType]
    officeOfOrigin: typing.Optional[str] = None
    shipperCustomsRef: typing.Optional[int] = None
    consigneeCustomsRef: typing.Optional[int] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class DimType:
    uom: typing.Optional[str] = None
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DetailsType:
    dim: typing.Optional[DimType] = jstruct.JStruct[DimType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class CashOnDeliveryType:
    currency: typing.Optional[str] = None
    value: typing.Optional[float] = None
    accountHolder: typing.Optional[str] = None
    bankName: typing.Optional[str] = None
    iban: typing.Optional[str] = None
    bic: typing.Optional[str] = None
    accountReference: typing.Optional[str] = None
    transferNote1: typing.Optional[str] = None
    transferNote2: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DhlRetoureType:
    billingNumber: typing.Optional[str] = None
    refNo: typing.Optional[str] = None
    returnAddress: typing.Optional[ConsigneeType] = jstruct.JStruct[ConsigneeType]


@attr.s(auto_attribs=True)
class IdentCheckType:
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    dateOfBirth: typing.Optional[str] = None
    minimumAge: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServicesType:
    preferredNeighbour: typing.Optional[str] = None
    preferredLocation: typing.Optional[str] = None
    visualCheckOfAge: typing.Optional[str] = None
    namedPersonOnly: typing.Optional[bool] = None
    identCheck: typing.Optional[IdentCheckType] = jstruct.JStruct[IdentCheckType]
    signedForByRecipient: typing.Optional[bool] = None
    endorsement: typing.Optional[str] = None
    preferredDay: typing.Optional[str] = None
    noNeighbourDelivery: typing.Optional[bool] = None
    additionalInsurance: typing.Optional[PostalChargesType] = jstruct.JStruct[PostalChargesType]
    bulkyGoods: typing.Optional[bool] = None
    cashOnDelivery: typing.Optional[CashOnDeliveryType] = jstruct.JStruct[CashOnDeliveryType]
    individualSenderRequirement: typing.Optional[str] = None
    premium: typing.Optional[bool] = None
    closestDropPoint: typing.Optional[bool] = None
    parcelOutletRouting: typing.Optional[str] = None
    dhlRetoure: typing.Optional[DhlRetoureType] = jstruct.JStruct[DhlRetoureType]
    postalDeliveryDutyPaid: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ShipperType:
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    name3: typing.Optional[str] = None
    addressStreet: typing.Optional[str] = None
    addressHouse: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None
    contactName: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    product: typing.Optional[str] = None
    billingNumber: typing.Optional[str] = None
    refNo: typing.Optional[str] = None
    costCenter: typing.Optional[str] = None
    creationSoftware: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    shipper: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    consignee: typing.Optional[ConsigneeType] = jstruct.JStruct[ConsigneeType]
    details: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    services: typing.Optional[ServicesType] = jstruct.JStruct[ServicesType]
    customs: typing.Optional[CustomsType] = jstruct.JStruct[CustomsType]


@attr.s(auto_attribs=True)
class ShippingRequestType:
    profile: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
