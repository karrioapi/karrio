import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ShipmentType:
    shipment_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManifestRequestType:
    order_reference: typing.Optional[str] = None
    payment_method: typing.Optional[str] = None
    consignor: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
