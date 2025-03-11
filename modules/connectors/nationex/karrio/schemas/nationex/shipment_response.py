import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ChargeType:
    Id: typing.Optional[str] = None
    Charge: typing.Optional[float] = None
    NameFr: typing.Optional[str] = None
    NameEn: typing.Optional[str] = None
    BeyondId: typing.Optional[int] = None
    Rate: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class RatesDetailType:
    BasePrice: typing.Optional[float] = None
    SurchargeCharges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    TaxCharges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    AccessoryCharges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    NCVCharge: typing.Optional[int] = None
    FuelRate: typing.Optional[float] = None
    FuelCharge: typing.Optional[float] = None
    SubTotal: typing.Optional[float] = None
    Total: typing.Optional[float] = None
    TotalBillableWeight: typing.Optional[int] = None
    BillingZone: typing.Optional[str] = None
    DelayTransitDays: typing.Optional[int] = None
    EstimatedDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    ShipmentId: typing.Optional[int] = None
    ConsolId: typing.Optional[int] = None
    BillingAccount: typing.Optional[int] = None
    ParcelIds: typing.Optional[typing.List[str]] = None
    Barcodes: typing.Optional[typing.List[str]] = None
    RatesDetail: typing.Optional[RatesDetailType] = jstruct.JStruct[RatesDetailType]
