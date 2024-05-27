from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ChargeType:
    charge: Optional[str] = None
    amount: Optional[str] = None
    adjustmentReasons: Optional[str] = None


@s(auto_attribs=True)
class InvoiceType:
    invoiceNumber: Optional[str] = None
    charges: List[ChargeType] = JList[ChargeType]
    total: Optional[int] = None


@s(auto_attribs=True)
class BillingType:
    invoices: List[InvoiceType] = JList[InvoiceType]


@s(auto_attribs=True)
class CarrierType:
    carrierName: Optional[str] = None
    serviceName: Optional[str] = None
    carrierLogoPath: Optional[str] = None


@s(auto_attribs=True)
class CustomsInvoiceType:
    type: Optional[str] = None
    data: Optional[str] = None


@s(auto_attribs=True)
class LabelDataType:
    label: List[CustomsInvoiceType] = JList[CustomsInvoiceType]


@s(auto_attribs=True)
class OrderType:
    trackingId: Optional[str] = None
    orderId: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    trackingNumber: Optional[str] = None


@s(auto_attribs=True)
class PickupType:
    confirmationNumber: Optional[str] = None


@s(auto_attribs=True)
class SurchargeType:
    name: Optional[str] = None
    amount: Optional[int] = None


@s(auto_attribs=True)
class QuoteType:
    carrierName: Optional[str] = None
    serviceId: Optional[int] = None
    serviceName: Optional[str] = None
    deliveryCarrier: Optional[str] = None
    modeTransport: Optional[str] = None
    transitDays: Optional[str] = None
    baseCharge: Optional[int] = None
    fuelSurcharge: Optional[int] = None
    fuelSurchargePercentage: Optional[int] = None
    carbonNeutralFees: Optional[int] = None
    surcharges: List[SurchargeType] = JList[SurchargeType]
    totalCharge: Optional[int] = None
    processingFees: Optional[int] = None
    taxes: List[SurchargeType] = JList[SurchargeType]
    totalChargedAmount: Optional[int] = None
    currency: Optional[str] = None
    carrierLogo: Optional[str] = None
    id: Optional[str] = None


@s(auto_attribs=True)
class ReferenceType:
    code: Optional[str] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class ShippingResponseType:
    order: Optional[OrderType] = JStruct[OrderType]
    carrier: Optional[CarrierType] = JStruct[CarrierType]
    reference: Optional[ReferenceType] = JStruct[ReferenceType]
    reference2: Optional[ReferenceType] = JStruct[ReferenceType]
    reference3: Optional[ReferenceType] = JStruct[ReferenceType]
    transactionId: Optional[str] = None
    billingReference: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]
    trackingUrl: Optional[str] = None
    brandedTrackingUrl: Optional[str] = None
    trackingNumber: Optional[str] = None
    labelData: Optional[LabelDataType] = JStruct[LabelDataType]
    customsInvoice: Optional[CustomsInvoiceType] = JStruct[CustomsInvoiceType]
    pickup: Optional[PickupType] = JStruct[PickupType]
    packingSlip: Optional[str] = None
    quote: Optional[QuoteType] = JStruct[QuoteType]
    billing: Optional[BillingType] = JStruct[BillingType]
    returnShipment: Optional[str] = None
    message: Optional[str] = None
