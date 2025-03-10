import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ReceiverInfoType:
    companyName: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    email: typing.Optional[str] = None
    nickname: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NAddressType:
    countryId: typing.Optional[int] = None
    provinceStateId: typing.Optional[int] = None
    provinceState: typing.Optional[str] = None
    cityVillageId: typing.Optional[int] = None
    cityVillage: typing.Optional[str] = None
    streetId: typing.Optional[int] = None
    street: typing.Optional[str] = None
    buildingId: typing.Optional[int] = None
    building: typing.Optional[str] = None
    apartment: typing.Optional[str] = None
    apartmentId: typing.Optional[int] = None
    address: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    deliveryDate: typing.Optional[str] = None
    receiverInfo: typing.Optional[ReceiverInfoType] = jstruct.JStruct[ReceiverInfoType]


@attr.s(auto_attribs=True)
class CodType:
    amount: typing.Optional[int] = None
    bank: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EnclosureEnclosureType:
    description: typing.Optional[str] = None
    hsCode: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    amount: typing.Optional[int] = None
    countryOfOrigin: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderInfoEnclosureType:
    enclosures: typing.Optional[typing.List[EnclosureEnclosureType]] = jstruct.JList[EnclosureEnclosureType]
    enclosureTypeId: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class OrderInfoType:
    valuedAmount: typing.Optional[int] = None
    valuedAmountCurrency: typing.Optional[int] = None
    enclosure: typing.Optional[typing.List[OrderInfoEnclosureType]] = jstruct.JList[OrderInfoEnclosureType]
    cod: typing.Optional[CodType] = jstruct.JStruct[CodType]


@attr.s(auto_attribs=True)
class TariffRequestElementType:
    customerId: typing.Optional[int] = None
    serviceCategoryDirectionId: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    totalPrice: typing.Optional[int] = None
    currencyId: typing.Optional[int] = None
    comment: typing.Optional[str] = None
    returnRegisteredAddress: typing.Optional[bool] = None
    partner: typing.Optional[int] = None
    externalId: typing.Optional[str] = None
    destinationAddress: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    returnAddress: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    orderInfo: typing.Optional[OrderInfoType] = jstruct.JStruct[OrderInfoType]
    additionalServices: typing.Optional[typing.List[int]] = None
