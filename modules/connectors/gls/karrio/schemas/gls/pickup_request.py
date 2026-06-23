import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupRequestType:
    ContactID: typing.Optional[str] = None
    PreferredPickUpDate: typing.Optional[str] = None
    NumberOfParcels: typing.Optional[int] = None
    Product: typing.Optional[str] = None
    ExpectedTotalWeight: typing.Optional[float] = None
    ContainsHazGoods: typing.Optional[bool] = None
    AdditionalInformation: typing.Optional[str] = None
