import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BusinessHourType:
    timeFrom: typing.Optional[str] = None
    timeUntil: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EmailNotificationType:
    sendPickupConfirmationEmail: typing.Optional[bool] = None
    sendPickupTimeWindowEmail: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ContactPersonType:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    emailNotification: typing.Optional[EmailNotificationType] = jstruct.JStruct[EmailNotificationType]


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    accountNumber: typing.Optional[str] = None
    billingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupDateType:
    type: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TotalWeightType:
    uom: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupDetailsType:
    pickupDate: typing.Optional[PickupDateType] = jstruct.JStruct[PickupDateType]
    totalWeight: typing.Optional[TotalWeightType] = jstruct.JStruct[TotalWeightType]
    comment: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupAddressType:
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    addressStreet: typing.Optional[str] = None
    addressHouse: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None
    state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupLocationType:
    type: typing.Optional[str] = None
    pickupAddress: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]
    asId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BulkyGoodType:
    comment: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PrintLabelType:
    consignee: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]


@attr.s(auto_attribs=True)
class PickupServicesType:
    bulkyGood: typing.Optional[BulkyGoodType] = jstruct.JStruct[BulkyGoodType]
    printLabel: typing.Optional[PrintLabelType] = jstruct.JStruct[PrintLabelType]


@attr.s(auto_attribs=True)
class ShipmentType:
    transportationType: typing.Optional[str] = None
    replacement: typing.Optional[bool] = None
    shipmentNo: typing.Optional[str] = None
    size: typing.Optional[str] = None
    pickupServices: typing.Optional[PickupServicesType] = jstruct.JStruct[PickupServicesType]
    customerReference: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentDetailsType:
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]


@attr.s(auto_attribs=True)
class PickupRequestType:
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    pickupLocation: typing.Optional[PickupLocationType] = jstruct.JStruct[PickupLocationType]
    businessHours: typing.Optional[typing.List[BusinessHourType]] = jstruct.JList[BusinessHourType]
    contactPerson: typing.Optional[typing.List[ContactPersonType]] = jstruct.JList[ContactPersonType]
    pickupDetails: typing.Optional[PickupDetailsType] = jstruct.JStruct[PickupDetailsType]
    shipmentDetails: typing.Optional[ShipmentDetailsType] = jstruct.JStruct[ShipmentDetailsType]
