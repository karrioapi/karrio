import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PackageDescriptionType:
    weight: typing.Optional[int] = None
    length: typing.Optional[int] = None
    height: typing.Optional[int] = None
    width: typing.Optional[int] = None
    girth: typing.Optional[int] = None
    mailClass: typing.Optional[str] = None
    extraServices: typing.Optional[typing.List[int]] = None
    packageValue: typing.Optional[int] = None
    mailingDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PaymentAccountType:
    accountType: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PricingOptionType:
    priceType: typing.Optional[str] = None
    paymentAccount: typing.Optional[PaymentAccountType] = jstruct.JStruct[PaymentAccountType]


@attr.s(auto_attribs=True)
class RateRequestType:
    pricingOptions: typing.Optional[typing.List[PricingOptionType]] = jstruct.JList[PricingOptionType]
    originZIPCode: typing.Optional[str] = None
    foreignPostalCode: typing.Optional[str] = None
    destinationCountryCode: typing.Optional[str] = None
    packageDescription: typing.Optional[PackageDescriptionType] = jstruct.JStruct[PackageDescriptionType]
    shippingFilter: typing.Optional[str] = None
