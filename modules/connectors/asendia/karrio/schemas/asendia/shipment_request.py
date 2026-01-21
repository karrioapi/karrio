import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ImporterType:
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    address3: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    email: typing.Optional[str] = None
    mobile: typing.Optional[str] = None
    phone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PudoAddressType:
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    address3: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    pudoId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressesType:
    sender: typing.Optional[ImporterType] = jstruct.JStruct[ImporterType]
    receiver: typing.Optional[ImporterType] = jstruct.JStruct[ImporterType]
    importer: typing.Optional[ImporterType] = jstruct.JStruct[ImporterType]
    seller: typing.Optional[ImporterType] = jstruct.JStruct[ImporterType]
    pudoAddress: typing.Optional[PudoAddressType] = jstruct.JStruct[PudoAddressType]


@attr.s(auto_attribs=True)
class ReturnLabelOptionType:
    enabled: typing.Optional[bool] = None
    type: typing.Optional[str] = None
    payment: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AsendiaServiceType:
    format: typing.Optional[str] = None
    product: typing.Optional[str] = None
    service: typing.Optional[str] = None
    options: typing.Optional[typing.List[str]] = None
    insurance: typing.Optional[str] = None
    returnLabelOption: typing.Optional[ReturnLabelOptionType] = jstruct.JStruct[ReturnLabelOptionType]


@attr.s(auto_attribs=True)
class ItemType:
    articleDescription: typing.Optional[str] = None
    articleUrl: typing.Optional[str] = None
    articleNumber: typing.Optional[str] = None
    articleComposition: typing.Optional[str] = None
    unitValue: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    harmonizationCode: typing.Optional[str] = None
    originCountry: typing.Optional[str] = None
    unitWeight: typing.Optional[float] = None
    quantity: typing.Optional[int] = None
    volatileOrganicCompoundInGrams: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CustomsInfoType:
    currency: typing.Optional[str] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    customerId: typing.Optional[str] = None
    labelType: typing.Optional[str] = None
    referencenumber: typing.Optional[str] = None
    sequencenumber: typing.Optional[str] = None
    senderEORI: typing.Optional[str] = None
    sellerEORI: typing.Optional[str] = None
    senderTaxId: typing.Optional[str] = None
    receiverTaxId: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    shippingCost: typing.Optional[float] = None
    asendiaService: typing.Optional[AsendiaServiceType] = jstruct.JStruct[AsendiaServiceType]
    addresses: typing.Optional[AddressesType] = jstruct.JStruct[AddressesType]
    customsInfo: typing.Optional[CustomsInfoType] = jstruct.JStruct[CustomsInfoType]
