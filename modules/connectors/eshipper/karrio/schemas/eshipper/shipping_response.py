import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ChargeType:
    charge: typing.Optional[str] = None
    amount: typing.Optional[str] = None
    adjustmentReasons: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InvoiceType:
    invoiceNumber: typing.Optional[str] = None
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    total: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BillingType:
    invoices: typing.Optional[typing.List[InvoiceType]] = jstruct.JList[InvoiceType]


@attr.s(auto_attribs=True)
class CarrierType:
    carrierName: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    carrierLogoPath: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsInvoiceType:
    type: typing.Optional[str] = None
    data: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelDataType:
    label: typing.Optional[typing.List[CustomsInvoiceType]] = jstruct.JList[CustomsInvoiceType]


@attr.s(auto_attribs=True)
class OrderType:
    trackingId: typing.Optional[str] = None
    id: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    trackingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupType:
    confirmationNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SurchargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class QuoteType:
    carrierName: typing.Optional[str] = None
    serviceId: typing.Optional[int] = None
    serviceName: typing.Optional[str] = None
    deliveryCarrier: typing.Optional[str] = None
    modeTransport: typing.Optional[str] = None
    transitDays: typing.Optional[str] = None
    baseCharge: typing.Optional[int] = None
    fuelSurcharge: typing.Optional[int] = None
    fuelSurchargePercentage: typing.Optional[int] = None
    carbonNeutralFees: typing.Optional[int] = None
    surcharges: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    totalCharge: typing.Optional[int] = None
    processingFees: typing.Optional[int] = None
    taxes: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    totalChargedAmount: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    carrierLogo: typing.Optional[str] = None
    id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReferenceType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    order: typing.Optional[OrderType] = jstruct.JStruct[OrderType]
    carrier: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    reference: typing.Optional[ReferenceType] = jstruct.JStruct[ReferenceType]
    reference2: typing.Optional[ReferenceType] = jstruct.JStruct[ReferenceType]
    reference3: typing.Optional[ReferenceType] = jstruct.JStruct[ReferenceType]
    transactionId: typing.Optional[str] = None
    billingReference: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    trackingUrl: typing.Optional[str] = None
    brandedTrackingUrl: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    labelData: typing.Optional[LabelDataType] = jstruct.JStruct[LabelDataType]
    customsInvoice: typing.Optional[CustomsInvoiceType] = jstruct.JStruct[CustomsInvoiceType]
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    packingSlip: typing.Optional[str] = None
    quote: typing.Optional[QuoteType] = jstruct.JStruct[QuoteType]
    billing: typing.Optional[BillingType] = jstruct.JStruct[BillingType]
    returnShipment: typing.Optional[str] = None
    message: typing.Optional[str] = None
