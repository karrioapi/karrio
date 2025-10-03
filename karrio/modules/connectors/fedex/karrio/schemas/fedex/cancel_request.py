import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountNumberType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CancelRequestType:
    accountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    emailShipment: typing.Optional[bool] = None
    senderCountryCode: typing.Optional[str] = None
    deletionControl: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
