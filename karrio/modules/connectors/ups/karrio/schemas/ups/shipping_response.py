import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AlertType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseType:
    ResponseStatus: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    Alert: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class BillingWeightType:
    UnitOfMeasurement: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    Weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ControlLogReceiptType:
    ImageFormat: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    GraphicImage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CodTurnInPageType:
    Image: typing.Optional[ControlLogReceiptType] = jstruct.JStruct[ControlLogReceiptType]


@attr.s(auto_attribs=True)
class FreightDensityRateType:
    Density: typing.Optional[str] = None
    TotalCubicFeet: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdjustedHeightType:
    Value: typing.Optional[str] = None
    UnitOfMeasurement: typing.Optional[AlertType] = jstruct.JStruct[AlertType]


@attr.s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    Length: typing.Optional[str] = None
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HandlingUnitType:
    Quantity: typing.Optional[str] = None
    Type: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    AdjustedHeight: typing.Optional[AdjustedHeightType] = jstruct.JStruct[AdjustedHeightType]


@attr.s(auto_attribs=True)
class TotalChargeType:
    CurrencyCode: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransportationChargesType:
    GrossCharge: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    DiscountAmount: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    DiscountPercentage: typing.Optional[str] = None
    NetCharge: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]


@attr.s(auto_attribs=True)
class FRSShipmentDataType:
    TransportationCharges: typing.Optional[TransportationChargesType] = jstruct.JStruct[TransportationChargesType]
    FreightDensityRate: typing.Optional[FreightDensityRateType] = jstruct.JStruct[FreightDensityRateType]
    HandlingUnits: typing.Optional[typing.List[HandlingUnitType]] = jstruct.JList[HandlingUnitType]


@attr.s(auto_attribs=True)
class FormType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    Image: typing.Optional[ControlLogReceiptType] = jstruct.JStruct[ControlLogReceiptType]
    FormGroupId: typing.Optional[str] = None
    FormGroupIdName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemizedChargeType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    CurrencyCode: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None
    SubType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxChargeType:
    Type: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NegotiatedRateChargesType:
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeType]] = jstruct.JList[ItemizedChargeType]
    TaxCharges: typing.Optional[typing.List[TaxChargeType]] = jstruct.JList[TaxChargeType]
    TotalCharge: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    TotalChargesWithTaxes: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]


@attr.s(auto_attribs=True)
class NegotiatedChargesType:
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeType]] = jstruct.JList[ItemizedChargeType]


@attr.s(auto_attribs=True)
class RateModifierType:
    ModifierType: typing.Optional[str] = None
    ModifierDesc: typing.Optional[str] = None
    CurrencyCode: typing.Optional[str] = None
    Amount: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingLabelType:
    ImageFormat: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    GraphicImage: typing.Optional[str] = None
    GraphicImagePart: typing.Optional[typing.List[str]] = None
    InternationalSignatureGraphicImage: typing.Optional[str] = None
    HTMLImage: typing.Optional[str] = None
    PDF417: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageResultType:
    TrackingNumber: typing.Optional[str] = None
    RateModifier: typing.Optional[RateModifierType] = jstruct.JStruct[RateModifierType]
    BaseServiceCharge: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    ServiceOptionsCharges: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    ShippingLabel: typing.Optional[ShippingLabelType] = jstruct.JStruct[ShippingLabelType]
    ShippingReceipt: typing.Optional[ControlLogReceiptType] = jstruct.JStruct[ControlLogReceiptType]
    USPSPICNumber: typing.Optional[str] = None
    CN22Number: typing.Optional[str] = None
    Accessorial: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    Form: typing.Optional[FormType] = jstruct.JStruct[FormType]
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeType]] = jstruct.JList[ItemizedChargeType]
    NegotiatedCharges: typing.Optional[NegotiatedChargesType] = jstruct.JStruct[NegotiatedChargesType]


@attr.s(auto_attribs=True)
class ShipmentChargesType:
    RateChart: typing.Optional[str] = None
    BaseServiceCharge: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    TransportationCharges: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeType]] = jstruct.JList[ItemizedChargeType]
    ServiceOptionsCharges: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    TaxCharges: typing.Optional[typing.List[TaxChargeType]] = jstruct.JList[TaxChargeType]
    TotalCharges: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]
    TotalChargesWithTaxes: typing.Optional[TotalChargeType] = jstruct.JStruct[TotalChargeType]


@attr.s(auto_attribs=True)
class ShipmentResultsType:
    Disclaimer: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    ShipmentCharges: typing.Optional[ShipmentChargesType] = jstruct.JStruct[ShipmentChargesType]
    NegotiatedRateCharges: typing.Optional[NegotiatedRateChargesType] = jstruct.JStruct[NegotiatedRateChargesType]
    FRSShipmentData: typing.Optional[FRSShipmentDataType] = jstruct.JStruct[FRSShipmentDataType]
    RatingMethod: typing.Optional[str] = None
    BillableWeightCalculationMethod: typing.Optional[str] = None
    BillingWeight: typing.Optional[BillingWeightType] = jstruct.JStruct[BillingWeightType]
    ShipmentIdentificationNumber: typing.Optional[str] = None
    MIDualReturnShipmentKey: typing.Optional[str] = None
    BarCodeImage: typing.Optional[str] = None
    PackageResults: typing.Optional[typing.List[PackageResultType]] = jstruct.JList[PackageResultType]
    ControlLogReceipt: typing.Optional[typing.List[ControlLogReceiptType]] = jstruct.JList[ControlLogReceiptType]
    Form: typing.Optional[FormType] = jstruct.JStruct[FormType]
    CODTurnInPage: typing.Optional[CodTurnInPageType] = jstruct.JStruct[CodTurnInPageType]
    HighValueReport: typing.Optional[CodTurnInPageType] = jstruct.JStruct[CodTurnInPageType]
    LabelURL: typing.Optional[str] = None
    LocalLanguageLabelURL: typing.Optional[str] = None
    ReceiptURL: typing.Optional[str] = None
    LocalLanguageReceiptURL: typing.Optional[str] = None
    DGPaperImage: typing.Optional[typing.List[str]] = None
    MasterCartonID: typing.Optional[str] = None
    RoarRatedIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
    ShipmentResults: typing.Optional[ShipmentResultsType] = jstruct.JStruct[ShipmentResultsType]


@attr.s(auto_attribs=True)
class ShippingResponseType:
    ShipmentResponse: typing.Optional[ShipmentResponseType] = jstruct.JStruct[ShipmentResponseType]
