from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AlertType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[AlertType] = JStruct[AlertType]
    Alert: Optional[AlertType] = JStruct[AlertType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class BillingWeightType:
    UnitOfMeasurement: Optional[AlertType] = JStruct[AlertType]
    Weight: Optional[str] = None


@s(auto_attribs=True)
class ControlLogReceiptType:
    ImageFormat: Optional[AlertType] = JStruct[AlertType]
    GraphicImage: Optional[str] = None


@s(auto_attribs=True)
class CodTurnInPageType:
    Image: Optional[ControlLogReceiptType] = JStruct[ControlLogReceiptType]


@s(auto_attribs=True)
class FreightDensityRateType:
    Density: Optional[str] = None
    TotalCubicFeet: Optional[str] = None


@s(auto_attribs=True)
class AdjustedHeightType:
    Value: Optional[str] = None
    UnitOfMeasurement: Optional[AlertType] = JStruct[AlertType]


@s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: Optional[AlertType] = JStruct[AlertType]
    Length: Optional[str] = None
    Width: Optional[str] = None
    Height: Optional[str] = None


@s(auto_attribs=True)
class HandlingUnitType:
    Quantity: Optional[str] = None
    Type: Optional[AlertType] = JStruct[AlertType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    AdjustedHeight: Optional[AdjustedHeightType] = JStruct[AdjustedHeightType]


@s(auto_attribs=True)
class TotalChargeType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class TransportationChargesType:
    GrossCharge: Optional[TotalChargeType] = JStruct[TotalChargeType]
    DiscountAmount: Optional[TotalChargeType] = JStruct[TotalChargeType]
    DiscountPercentage: Optional[str] = None
    NetCharge: Optional[TotalChargeType] = JStruct[TotalChargeType]


@s(auto_attribs=True)
class FRSShipmentDataType:
    TransportationCharges: Optional[TransportationChargesType] = JStruct[TransportationChargesType]
    FreightDensityRate: Optional[FreightDensityRateType] = JStruct[FreightDensityRateType]
    HandlingUnits: List[HandlingUnitType] = JList[HandlingUnitType]


@s(auto_attribs=True)
class FormType:
    Code: Optional[str] = None
    Description: Optional[str] = None
    Image: Optional[ControlLogReceiptType] = JStruct[ControlLogReceiptType]
    FormGroupId: Optional[str] = None
    FormGroupIdName: Optional[str] = None


@s(auto_attribs=True)
class ItemizedChargeType:
    Code: Optional[str] = None
    Description: Optional[str] = None
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None
    SubType: Optional[str] = None


@s(auto_attribs=True)
class TaxChargeType:
    Type: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class NegotiatedRateChargesType:
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]
    TaxCharges: List[TaxChargeType] = JList[TaxChargeType]
    TotalCharge: Optional[TotalChargeType] = JStruct[TotalChargeType]
    TotalChargesWithTaxes: Optional[TotalChargeType] = JStruct[TotalChargeType]


@s(auto_attribs=True)
class NegotiatedChargesType:
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]


@s(auto_attribs=True)
class RateModifierType:
    ModifierType: Optional[str] = None
    ModifierDesc: Optional[str] = None
    CurrencyCode: Optional[str] = None
    Amount: Optional[str] = None


@s(auto_attribs=True)
class ShippingLabelType:
    ImageFormat: Optional[AlertType] = JStruct[AlertType]
    GraphicImage: Optional[str] = None
    GraphicImagePart: List[str] = []
    InternationalSignatureGraphicImage: Optional[str] = None
    HTMLImage: Optional[str] = None
    PDF417: Optional[str] = None


@s(auto_attribs=True)
class PackageResultType:
    TrackingNumber: Optional[str] = None
    RateModifier: Optional[RateModifierType] = JStruct[RateModifierType]
    BaseServiceCharge: Optional[TotalChargeType] = JStruct[TotalChargeType]
    ServiceOptionsCharges: Optional[TotalChargeType] = JStruct[TotalChargeType]
    ShippingLabel: Optional[ShippingLabelType] = JStruct[ShippingLabelType]
    ShippingReceipt: Optional[ControlLogReceiptType] = JStruct[ControlLogReceiptType]
    USPSPICNumber: Optional[str] = None
    CN22Number: Optional[str] = None
    Accessorial: List[AlertType] = JList[AlertType]
    Form: Optional[FormType] = JStruct[FormType]
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]
    NegotiatedCharges: Optional[NegotiatedChargesType] = JStruct[NegotiatedChargesType]


@s(auto_attribs=True)
class ShipmentChargesType:
    RateChart: Optional[str] = None
    BaseServiceCharge: Optional[TotalChargeType] = JStruct[TotalChargeType]
    TransportationCharges: Optional[TotalChargeType] = JStruct[TotalChargeType]
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]
    ServiceOptionsCharges: Optional[TotalChargeType] = JStruct[TotalChargeType]
    TaxCharges: List[TaxChargeType] = JList[TaxChargeType]
    TotalCharges: Optional[TotalChargeType] = JStruct[TotalChargeType]
    TotalChargesWithTaxes: Optional[TotalChargeType] = JStruct[TotalChargeType]


@s(auto_attribs=True)
class ShipmentResultsType:
    Disclaimer: List[AlertType] = JList[AlertType]
    ShipmentCharges: Optional[ShipmentChargesType] = JStruct[ShipmentChargesType]
    NegotiatedRateCharges: Optional[NegotiatedRateChargesType] = JStruct[NegotiatedRateChargesType]
    FRSShipmentData: Optional[FRSShipmentDataType] = JStruct[FRSShipmentDataType]
    RatingMethod: Optional[str] = None
    BillableWeightCalculationMethod: Optional[str] = None
    BillingWeight: Optional[BillingWeightType] = JStruct[BillingWeightType]
    ShipmentIdentificationNumber: Optional[str] = None
    MIDualReturnShipmentKey: Optional[str] = None
    BarCodeImage: Optional[str] = None
    PackageResults: List[PackageResultType] = JList[PackageResultType]
    ControlLogReceipt: List[ControlLogReceiptType] = JList[ControlLogReceiptType]
    Form: Optional[FormType] = JStruct[FormType]
    CODTurnInPage: Optional[CodTurnInPageType] = JStruct[CodTurnInPageType]
    HighValueReport: Optional[CodTurnInPageType] = JStruct[CodTurnInPageType]
    LabelURL: Optional[str] = None
    LocalLanguageLabelURL: Optional[str] = None
    ReceiptURL: Optional[str] = None
    LocalLanguageReceiptURL: Optional[str] = None
    DGPaperImage: List[str] = []
    MasterCartonID: Optional[str] = None
    RoarRatedIndicator: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponseType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    ShipmentResults: Optional[ShipmentResultsType] = JStruct[ShipmentResultsType]


@s(auto_attribs=True)
class ShippingResponseType:
    ShipmentResponse: Optional[ShipmentResponseType] = JStruct[ShipmentResponseType]
