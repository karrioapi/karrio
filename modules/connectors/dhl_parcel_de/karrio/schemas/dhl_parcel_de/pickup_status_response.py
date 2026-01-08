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
class OrderDetailsType:
    orderID: typing.Optional[str] = None
    orderState: typing.Optional[str] = None


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
    addressHouse: typing.Optional[int] = None
    postalCode: typing.Optional[int] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None
    state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupLocationType:
    id: typing.Optional[str] = None
    pickupAddress: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]


@attr.s(auto_attribs=True)
class BulkyGoodType:
    comment: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupServicesType:
    bulkyGood: typing.Optional[BulkyGoodType] = jstruct.JStruct[BulkyGoodType]


@attr.s(auto_attribs=True)
class ShipmentShipmentType:
    transportationType: typing.Optional[str] = None
    replacement: typing.Optional[bool] = None
    shipmentNo: typing.Optional[int] = None
    size: typing.Optional[str] = None
    pickupServices: typing.Optional[PickupServicesType] = jstruct.JStruct[PickupServicesType]
    customerReference: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentStateType:
    state: typing.Optional[str] = None
    responseTime: typing.Optional[str] = None
    actualPickupDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentElementType:
    shipment: typing.Optional[ShipmentShipmentType] = jstruct.JStruct[ShipmentShipmentType]
    shipmentState: typing.Optional[ShipmentStateType] = jstruct.JStruct[ShipmentStateType]
    orderDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentDetailsType:
    shipments: typing.Optional[typing.List[ShipmentElementType]] = jstruct.JList[ShipmentElementType]


@attr.s(auto_attribs=True)
class PickupStatusResponseElementType:
    orderDetails: typing.Optional[OrderDetailsType] = jstruct.JStruct[OrderDetailsType]
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    pickupLocation: typing.Optional[PickupLocationType] = jstruct.JStruct[PickupLocationType]
    businessHours: typing.Optional[typing.List[BusinessHourType]] = jstruct.JList[BusinessHourType]
    contactPerson: typing.Optional[typing.List[ContactPersonType]] = jstruct.JList[ContactPersonType]
    pickupDetails: typing.Optional[PickupDetailsType] = jstruct.JStruct[PickupDetailsType]
    shipmentDetails: typing.Optional[ShipmentDetailsType] = jstruct.JStruct[ShipmentDetailsType]
    feedback: typing.Optional[str] = None
