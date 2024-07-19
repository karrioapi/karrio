from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AlertType:
    code: Optional[str] = None
    message: Optional[str] = None
    alertType: Optional[str] = None
    parameterList: List[Any] = []


@s(auto_attribs=True)
class DateDetailType:
    dayOfWeek: Optional[str] = None
    dayFormat: Optional[str] = None


@s(auto_attribs=True)
class DerivedNDetailType:
    countryCode: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[str] = None
    serviceArea: Optional[str] = None
    locationId: Optional[str] = None
    locationNumber: Optional[int] = None
    airportId: Optional[str] = None


@s(auto_attribs=True)
class TransitDaysType:
    minimumTransitTime: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class CommitType:
    label: Optional[str] = None
    commitMessageDetails: Optional[str] = None
    commodityName: Optional[str] = None
    deliveryMessages: List[str] = []
    derivedOriginDetail: Optional[DerivedNDetailType] = JStruct[DerivedNDetailType]
    derivedDestinationDetail: Optional[DerivedNDetailType] = JStruct[DerivedNDetailType]
    saturdayDelivery: Optional[bool] = None
    dateDetail: Optional[DateDetailType] = JStruct[DateDetailType]
    transitDays: Optional[TransitDaysType] = JStruct[TransitDaysType]


@s(auto_attribs=True)
class CustomerMessageType:
    code: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class OperationalDetailType:
    originLocationIds: List[str] = []
    originLocationNumbers: List[int] = []
    originServiceAreas: List[str] = []
    destinationLocationIds: List[str] = []
    destinationLocationNumbers: List[int] = []
    destinationServiceAreas: List[str] = []
    destinationLocationStateOrProvinceCodes: List[str] = []
    ineligibleForMoneyBackGuarantee: Optional[bool] = None
    astraDescription: Optional[str] = None
    originPostalCodes: List[str] = []
    stateOrProvinceCodes: List[str] = []
    countryCodes: List[str] = []
    airportId: Optional[str] = None
    serviceCode: Optional[str] = None
    destinationPostalCode: Optional[str] = None
    deliveryDate: Optional[str] = None
    deliveryDay: Optional[str] = None
    commitDate: Optional[str] = None
    commitDays: List[str] = []
    transitTime: Optional[str] = None


@s(auto_attribs=True)
class AncillaryFeesAndTaxType:
    type: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    level: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    units: Optional[str] = None
    value: Optional[float] = None


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
    totalRebates: Optional[int] = None
    billingWeight: Optional[WeightType] = JStruct[WeightType]
    totalFreightDiscounts: Optional[int] = None
    surcharges: List[AncillaryFeesAndTaxType] = JList[AncillaryFeesAndTaxType]
    dimWeight: Optional[WeightType] = JStruct[WeightType]
    currency: Optional[str] = None


@s(auto_attribs=True)
class RatedPackageType:
    groupNumber: Optional[int] = None
    effectiveNetDiscount: Optional[int] = None
    packageRateDetail: Optional[PackageRateDetailType] = JStruct[PackageRateDetailType]
    sequenceNumber: Optional[int] = None


@s(auto_attribs=True)
class CurrencyExchangeRateType:
    fromCurrency: Optional[str] = None
    intoCurrency: Optional[str] = None
    rate: Optional[float] = None


@s(auto_attribs=True)
class ShipmentRateDetailType:
    rateZone: Optional[str] = None
    dimDivisor: Optional[int] = None
    fuelSurchargePercent: Optional[float] = None
    totalSurcharges: Optional[float] = None
    totalFreightDiscount: Optional[int] = None
    surCharges: List[AncillaryFeesAndTaxType] = JList[AncillaryFeesAndTaxType]
    pricingCode: Optional[str] = None
    currencyExchangeRate: Optional[CurrencyExchangeRateType] = JStruct[CurrencyExchangeRateType]
    totalBillingWeight: Optional[WeightType] = JStruct[WeightType]
    dimDivisorType: Optional[str] = None
    totalDimWeight: Optional[WeightType] = JStruct[WeightType]
    currency: Optional[str] = None
    rateScale: Optional[str] = None
    totalRateScaleWeight: Optional[WeightType] = JStruct[WeightType]
    taxes: List[AncillaryFeesAndTaxType] = JList[AncillaryFeesAndTaxType]


@s(auto_attribs=True)
class RatedShipmentDetailType:
    rateType: Optional[str] = None
    ratedWeightMethod: Optional[str] = None
    totalDiscounts: Optional[int] = None
    totalBaseCharge: Optional[float] = None
    totalNetCharge: Optional[float] = None
    totalVatCharge: Optional[int] = None
    totalNetFedExCharge: Optional[float] = None
    totalDutiesAndTaxes: Optional[int] = None
    totalNetChargeWithDutiesAndTaxes: Optional[float] = None
    totalDutiesTaxesAndFees: Optional[float] = None
    totalAncillaryFeesAndTaxes: Optional[float] = None
    shipmentRateDetail: Optional[ShipmentRateDetailType] = JStruct[ShipmentRateDetailType]
    ratedPackages: List[RatedPackageType] = JList[RatedPackageType]
    currency: Optional[str] = None
    ancillaryFeesAndTaxes: List[AncillaryFeesAndTaxType] = JList[AncillaryFeesAndTaxType]


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
    serviceCategory: Optional[str] = None
    description: Optional[str] = None
    astraDescription: Optional[str] = None


@s(auto_attribs=True)
class RateReplyDetailType:
    serviceType: Optional[str] = None
    serviceName: Optional[str] = None
    packagingType: Optional[str] = None
    commit: Optional[CommitType] = JStruct[CommitType]
    customerMessages: List[CustomerMessageType] = JList[CustomerMessageType]
    ratedShipmentDetails: List[RatedShipmentDetailType] = JList[RatedShipmentDetailType]
    operationalDetail: Optional[OperationalDetailType] = JStruct[OperationalDetailType]
    signatureOptionType: Optional[str] = None
    serviceDescription: Optional[ServiceDescriptionType] = JStruct[ServiceDescriptionType]
    deliveryStation: Optional[str] = None


@s(auto_attribs=True)
class OutputType:
    alerts: List[AlertType] = JList[AlertType]
    rateReplyDetails: List[RateReplyDetailType] = JList[RateReplyDetailType]
    quoteDate: Optional[str] = None
    encoded: Optional[bool] = None


@s(auto_attribs=True)
class RatingResponseType:
    transactionId: Optional[str] = None
    output: Optional[OutputType] = JStruct[OutputType]
