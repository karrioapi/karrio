import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AlertType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    alertType: typing.Optional[str] = None
    parameterList: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class DateDetailType:
    dayOfWeek: typing.Optional[str] = None
    dayFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DerivedNDetailType:
    countryCode: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    serviceArea: typing.Optional[str] = None
    locationId: typing.Optional[str] = None
    locationNumber: typing.Optional[int] = None
    airportId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransitDaysType:
    minimumTransitTime: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommitType:
    label: typing.Optional[str] = None
    commitMessageDetails: typing.Optional[str] = None
    commodityName: typing.Optional[str] = None
    deliveryMessages: typing.Optional[typing.List[str]] = None
    derivedOriginDetail: typing.Optional[DerivedNDetailType] = jstruct.JStruct[DerivedNDetailType]
    derivedDestinationDetail: typing.Optional[DerivedNDetailType] = jstruct.JStruct[DerivedNDetailType]
    saturdayDelivery: typing.Optional[bool] = None
    dateDetail: typing.Optional[DateDetailType] = jstruct.JStruct[DateDetailType]
    transitDays: typing.Optional[TransitDaysType] = jstruct.JStruct[TransitDaysType]


@attr.s(auto_attribs=True)
class CustomerMessageType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OperationalDetailType:
    originLocationIds: typing.Optional[typing.List[str]] = None
    originLocationNumbers: typing.Optional[typing.List[int]] = None
    originServiceAreas: typing.Optional[typing.List[str]] = None
    destinationLocationIds: typing.Optional[typing.List[str]] = None
    destinationLocationNumbers: typing.Optional[typing.List[int]] = None
    destinationServiceAreas: typing.Optional[typing.List[str]] = None
    destinationLocationStateOrProvinceCodes: typing.Optional[typing.List[str]] = None
    ineligibleForMoneyBackGuarantee: typing.Optional[bool] = None
    astraDescription: typing.Optional[str] = None
    originPostalCodes: typing.Optional[typing.List[str]] = None
    stateOrProvinceCodes: typing.Optional[typing.List[str]] = None
    countryCodes: typing.Optional[typing.List[str]] = None
    airportId: typing.Optional[str] = None
    serviceCode: typing.Optional[str] = None
    destinationPostalCode: typing.Optional[str] = None
    deliveryDate: typing.Optional[str] = None
    deliveryDay: typing.Optional[str] = None
    commitDate: typing.Optional[str] = None
    commitDays: typing.Optional[typing.List[str]] = None
    transitTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AncillaryFeesAndTaxType:
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    level: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    units: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class PackageRateDetailType:
    rateType: typing.Optional[str] = None
    ratedWeightMethod: typing.Optional[str] = None
    baseCharge: typing.Optional[float] = None
    netFreight: typing.Optional[float] = None
    totalSurcharges: typing.Optional[float] = None
    netFedExCharge: typing.Optional[float] = None
    totalTaxes: typing.Optional[float] = None
    netCharge: typing.Optional[float] = None
    totalRebates: typing.Optional[int] = None
    billingWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    totalFreightDiscounts: typing.Optional[int] = None
    surcharges: typing.Optional[typing.List[AncillaryFeesAndTaxType]] = jstruct.JList[AncillaryFeesAndTaxType]
    dimWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RatedPackageType:
    groupNumber: typing.Optional[int] = None
    effectiveNetDiscount: typing.Optional[int] = None
    packageRateDetail: typing.Optional[PackageRateDetailType] = jstruct.JStruct[PackageRateDetailType]
    sequenceNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CurrencyExchangeRateType:
    fromCurrency: typing.Optional[str] = None
    intoCurrency: typing.Optional[str] = None
    rate: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ShipmentRateDetailType:
    rateZone: typing.Optional[str] = None
    dimDivisor: typing.Optional[int] = None
    fuelSurchargePercent: typing.Optional[float] = None
    totalSurcharges: typing.Optional[float] = None
    totalFreightDiscount: typing.Optional[int] = None
    surCharges: typing.Optional[typing.List[AncillaryFeesAndTaxType]] = jstruct.JList[AncillaryFeesAndTaxType]
    pricingCode: typing.Optional[str] = None
    currencyExchangeRate: typing.Optional[CurrencyExchangeRateType] = jstruct.JStruct[CurrencyExchangeRateType]
    totalBillingWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimDivisorType: typing.Optional[str] = None
    totalDimWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    currency: typing.Optional[str] = None
    rateScale: typing.Optional[str] = None
    totalRateScaleWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    taxes: typing.Optional[typing.List[AncillaryFeesAndTaxType]] = jstruct.JList[AncillaryFeesAndTaxType]


@attr.s(auto_attribs=True)
class RatedShipmentDetailType:
    rateType: typing.Optional[str] = None
    ratedWeightMethod: typing.Optional[str] = None
    totalDiscounts: typing.Optional[int] = None
    totalBaseCharge: typing.Optional[float] = None
    totalNetCharge: typing.Optional[float] = None
    totalVatCharge: typing.Optional[int] = None
    totalNetFedExCharge: typing.Optional[float] = None
    totalDutiesAndTaxes: typing.Optional[int] = None
    totalNetChargeWithDutiesAndTaxes: typing.Optional[float] = None
    totalDutiesTaxesAndFees: typing.Optional[float] = None
    totalAncillaryFeesAndTaxes: typing.Optional[float] = None
    shipmentRateDetail: typing.Optional[ShipmentRateDetailType] = jstruct.JStruct[ShipmentRateDetailType]
    ratedPackages: typing.Optional[typing.List[RatedPackageType]] = jstruct.JList[RatedPackageType]
    currency: typing.Optional[str] = None
    ancillaryFeesAndTaxes: typing.Optional[typing.List[AncillaryFeesAndTaxType]] = jstruct.JList[AncillaryFeesAndTaxType]


@attr.s(auto_attribs=True)
class NameType:
    type: typing.Optional[str] = None
    encoding: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceDescriptionType:
    serviceId: typing.Optional[str] = None
    serviceType: typing.Optional[str] = None
    code: typing.Optional[str] = None
    names: typing.Optional[typing.List[NameType]] = jstruct.JList[NameType]
    serviceCategory: typing.Optional[str] = None
    description: typing.Optional[str] = None
    astraDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateReplyDetailType:
    serviceType: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    packagingType: typing.Optional[str] = None
    commit: typing.Optional[CommitType] = jstruct.JStruct[CommitType]
    customerMessages: typing.Optional[typing.List[CustomerMessageType]] = jstruct.JList[CustomerMessageType]
    ratedShipmentDetails: typing.Optional[typing.List[RatedShipmentDetailType]] = jstruct.JList[RatedShipmentDetailType]
    operationalDetail: typing.Optional[OperationalDetailType] = jstruct.JStruct[OperationalDetailType]
    signatureOptionType: typing.Optional[str] = None
    serviceDescription: typing.Optional[ServiceDescriptionType] = jstruct.JStruct[ServiceDescriptionType]
    deliveryStation: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OutputType:
    alerts: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    rateReplyDetails: typing.Optional[typing.List[RateReplyDetailType]] = jstruct.JList[RateReplyDetailType]
    quoteDate: typing.Optional[str] = None
    encoded: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class RatingResponseType:
    transactionId: typing.Optional[str] = None
    output: typing.Optional[OutputType] = jstruct.JStruct[OutputType]
