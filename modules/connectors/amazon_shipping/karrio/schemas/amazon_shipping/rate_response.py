import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class IneligibilityReason:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IneligibleRate:
    carrierId: typing.Optional[str] = None
    carrierName: typing.Optional[str] = None
    serviceId: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    ineligibilityReasons: typing.Optional[typing.List[IneligibilityReason]] = jstruct.JList[IneligibilityReason]


@attr.s(auto_attribs=True)
class BilledWeight:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Window:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Promise:
    deliveryWindow: typing.Optional[Window] = jstruct.JStruct[Window]
    pickupWindow: typing.Optional[Window] = jstruct.JStruct[Window]


@attr.s(auto_attribs=True)
class RateItemList:
    rateItemCharge: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    rateItemID: typing.Optional[str] = None
    rateItemNameLocalization: typing.Optional[str] = None
    rateItemType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SupportedDocumentDetail:
    name: typing.Optional[str] = None
    isMandatory: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PrintOption:
    supportedDPIs: typing.Optional[typing.List[int]] = None
    supportedPageLayouts: typing.Optional[typing.List[str]] = None
    supportedFileJoiningOptions: typing.Optional[typing.List[bool]] = None
    supportedDocumentDetails: typing.Optional[typing.List[SupportedDocumentDetail]] = jstruct.JList[SupportedDocumentDetail]


@attr.s(auto_attribs=True)
class Size:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SupportedDocumentSpecification:
    format: typing.Optional[str] = None
    size: typing.Optional[Size] = jstruct.JStruct[Size]
    printOptions: typing.Optional[typing.List[PrintOption]] = jstruct.JList[PrintOption]


@attr.s(auto_attribs=True)
class Rate:
    rateId: typing.Optional[str] = None
    carrierId: typing.Optional[str] = None
    carrierName: typing.Optional[str] = None
    billedWeight: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    totalCharge: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    serviceId: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    promise: typing.Optional[Promise] = jstruct.JStruct[Promise]
    supportedDocumentSpecifications: typing.Optional[typing.List[SupportedDocumentSpecification]] = jstruct.JList[SupportedDocumentSpecification]
    availableValueAddedServiceGroups: typing.Any = None
    requiresAdditionalInputs: typing.Optional[bool] = None
    rateItemList: typing.Optional[typing.List[RateItemList]] = jstruct.JList[RateItemList]
    paymentType: typing.Optional[str] = None
    benefits: typing.Any = None


@attr.s(auto_attribs=True)
class Payload:
    requestToken: typing.Optional[str] = None
    rates: typing.Optional[typing.List[Rate]] = jstruct.JList[Rate]
    ineligibleRates: typing.Optional[typing.List[IneligibleRate]] = jstruct.JList[IneligibleRate]


@attr.s(auto_attribs=True)
class RateResponse:
    payload: typing.Optional[Payload] = jstruct.JStruct[Payload]
