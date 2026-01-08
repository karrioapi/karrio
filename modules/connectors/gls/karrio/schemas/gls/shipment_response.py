import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelType:
    trackingNumber: typing.Optional[str] = None
    labelData: typing.Optional[str] = None
    labelFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    parcelId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    weight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipmentId: typing.Optional[str] = None
    trackingNumbers: typing.Optional[typing.List[str]] = None
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    labels: typing.Optional[typing.List[LabelType]] = jstruct.JList[LabelType]
    createdAt: typing.Optional[str] = None
    shippingDate: typing.Optional[str] = None
    status: typing.Optional[str] = None
