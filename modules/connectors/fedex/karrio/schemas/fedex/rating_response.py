from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AlertType:
    code: Optional[str] = None
    message: Optional[str] = None
    alertType: Optional[str] = None


@s(auto_attribs=True)
class DateDetailType:
    dayOfWeek: Optional[str] = None
    dayCxsFormat: Optional[str] = None


@s(auto_attribs=True)
class CommitType:
    dateDetail: Optional[DateDetailType] = JStruct[DateDetailType]


@s(auto_attribs=True)
class CustomerMessageType:
    code: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class OperationalDetailType:
    originLocationIds: Optional[str] = None
    commitDays: Optional[str] = None
    serviceCode: Optional[str] = None
    airportId: Optional[str] = None
    scac: Optional[str] = None
    originServiceAreas: Optional[str] = None
    deliveryDay: Optional[str] = None
    originLocationNumbers: Optional[int] = None
    destinationPostalCode: Optional[int] = None
    commitDate: Optional[str] = None
    astraDescription: Optional[str] = None
    deliveryDate: Optional[str] = None
    deliveryEligibilities: Optional[str] = None
    ineligibleForMoneyBackGuarantee: Optional[bool] = None
    maximumTransitTime: Optional[str] = None
    astraPlannedServiceLevel: Optional[str] = None
    destinationLocationIds: Optional[str] = None
    destinationLocationStateOrProvinceCodes: Optional[str] = None
    transitTime: Optional[str] = None
    packagingCode: Optional[str] = None
    destinationLocationNumbers: Optional[int] = None
    publishedDeliveryTime: Optional[str] = None
    countryCodes: Optional[str] = None
    stateOrProvinceCodes: Optional[str] = None
    ursaPrefixCode: Optional[int] = None
    ursaSuffixCode: Optional[str] = None
    destinationServiceAreas: Optional[str] = None
    originPostalCodes: Optional[int] = None
    customTransitTime: Optional[str] = None


@s(auto_attribs=True)
class BillingWeightType:
    units: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class SurchargeType:
    type: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    level: Optional[str] = None


@s(auto_attribs=True)
class PackageRateDetailType:
    rateType: Optional[str] = None
    ratedWeightMethod: Optional[str] = None
    baseCharge: Optional[float] = None
    netFreight: Optional[float] = None
    totalSurcharges: Optional[float] = None
    netFedExCharge: Optional[float] = None
    totalTaxes: Optional[float] = None
    netCharge: Optional[float] = None
    totalRebates: Optional[float] = None
    billingWeight: Optional[BillingWeightType] = JStruct[BillingWeightType]
    totalFreightDiscounts: Optional[float] = None
    surcharges: List[SurchargeType] = JList[SurchargeType]
    currency: Optional[str] = None


@s(auto_attribs=True)
class RatedPackageType:
    groupNumber: Optional[float] = None
    effectiveNetDiscount: Optional[float] = None
    packageRateDetail: Optional[PackageRateDetailType] = JStruct[PackageRateDetailType]


@s(auto_attribs=True)
class NameType:
    type: Optional[str] = None
    encoding: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class ServiceDescriptionType:
    serviceId: Optional[str] = None
    serviceType: Optional[str] = None
    code: Optional[str] = None
    names: List[NameType] = JList[NameType]
    operatingOrgCodes: List[str] = []
    description: Optional[str] = None
    astraDescription: Optional[str] = None
    serviceCategory: Optional[str] = None


@s(auto_attribs=True)
class CurrencyExchangeRateType:
    fromCurrency: Optional[str] = None
    intoCurrency: Optional[str] = None
    rate: Optional[float] = None


@s(auto_attribs=True)
class ShipmentRateDetailType:
    rateZone: Optional[str] = None
    dimDivisor: Optional[float] = None
    fuelSurchargePercent: Optional[float] = None
    totalSurcharges: Optional[float] = None
    totalFreightDiscount: Optional[float] = None
    surCharges: List[SurchargeType] = JList[SurchargeType]
    pricingCode: Optional[str] = None
    currencyExchangeRate: Optional[CurrencyExchangeRateType] = JStruct[CurrencyExchangeRateType]
    totalBillingWeight: Optional[BillingWeightType] = JStruct[BillingWeightType]
    currency: Optional[str] = None


@s(auto_attribs=True)
class RatedShipmentDetailType:
    rateType: Optional[str] = None
    ratedWeightMethod: Optional[str] = None
    totalDiscounts: Optional[float] = None
    totalBaseCharge: Optional[float] = None
    totalNetCharge: Optional[float] = None
    totalVatCharge: Optional[float] = None
    totalNetFedExCharge: Optional[float] = None
    totalDutiesAndTaxes: Optional[float] = None
    totalNetChargeWithDutiesAndTaxes: Optional[float] = None
    totalDutiesTaxesAndFees: Optional[float] = None
    totalAncillaryFeesAndTaxes: Optional[float] = None
    shipmentRateDetail: Optional[ShipmentRateDetailType] = JStruct[ShipmentRateDetailType]
    currency: Optional[str] = None
    ratedPackages: List[RatedPackageType] = JList[RatedPackageType]
    anonymouslyAllowable: Optional[bool] = None
    operationalDetail: Optional[OperationalDetailType] = JStruct[OperationalDetailType]
    signatureOptionType: Optional[str] = None
    serviceDescription: Optional[ServiceDescriptionType] = JStruct[ServiceDescriptionType]


@s(auto_attribs=True)
class RateReplyDetailType:
    serviceType: Optional[str] = None
    serviceName: Optional[str] = None
    packagingType: Optional[str] = None
    customerMessages: List[CustomerMessageType] = JList[CustomerMessageType]
    ratedShipmentDetails: List[RatedShipmentDetailType] = JList[RatedShipmentDetailType]
    anonymouslyAllowable: Optional[bool] = None
    operationalDetail: Optional[OperationalDetailType] = JStruct[OperationalDetailType]
    signatureOptionType: Optional[str] = None
    serviceDescription: Optional[ServiceDescriptionType] = JStruct[ServiceDescriptionType]
    commit: Optional[CommitType] = JStruct[CommitType]


@s(auto_attribs=True)
class OutputType:
    rateReplyDetails: List[RateReplyDetailType] = JList[RateReplyDetailType]
    quoteDate: Optional[str] = None
    encoded: Optional[bool] = None
    alerts: List[AlertType] = JList[AlertType]


@s(auto_attribs=True)
class RatingResponseType:
    transactionId: Optional[str] = None
    customerTransactionId: Optional[str] = None
    output: Optional[OutputType] = JStruct[OutputType]
