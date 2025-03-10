import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CourierType:
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    reference: typing.Optional[str] = None
    status: typing.Optional[str] = None
    statusChangeDateTime: typing.Optional[str] = None
    purchaseOrderNumber: typing.Optional[str] = None
    trackinglink: typing.Optional[str] = None
    proofOfDeliveryPhotoUrl: typing.Any = None
    signatureUrl: typing.Any = None
    courier: typing.Optional[CourierType] = jstruct.JStruct[CourierType]
