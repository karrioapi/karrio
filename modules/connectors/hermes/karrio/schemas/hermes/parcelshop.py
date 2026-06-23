import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class HourType:
    weekday: typing.Optional[int] = None
    openFrom: typing.Optional[str] = None
    openTil: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelshopType:
    parcelShopNumber: typing.Optional[str] = None
    typeID: typing.Optional[int] = None
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    city: typing.Optional[str] = None
    zip: typing.Optional[str] = None
    countryIsoA2Code: typing.Optional[str] = None
    countryIsoA3Code: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    distance: typing.Optional[float] = None
    openToday: typing.Optional[str] = None
    hours: typing.Optional[typing.List[HourType]] = jstruct.JList[HourType]
