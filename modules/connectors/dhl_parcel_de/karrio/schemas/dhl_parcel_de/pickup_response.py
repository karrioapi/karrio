import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ConfirmedShipmentType:
    transportationType: typing.Optional[str] = None
    shipmentNo: typing.Optional[int] = None
    orderDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValueType:
    orderID: typing.Optional[str] = None
    pickupDate: typing.Optional[str] = None
    freeOfCharge: typing.Optional[bool] = None
    pickupType: typing.Optional[str] = None
    confirmedShipments: typing.Optional[typing.List[ConfirmedShipmentType]] = jstruct.JList[ConfirmedShipmentType]


@attr.s(auto_attribs=True)
class ConfirmationType:
    type: typing.Optional[str] = None
    value: typing.Optional[ValueType] = jstruct.JStruct[ValueType]


@attr.s(auto_attribs=True)
class PickupResponseType:
    confirmation: typing.Optional[ConfirmationType] = jstruct.JStruct[ConfirmationType]
