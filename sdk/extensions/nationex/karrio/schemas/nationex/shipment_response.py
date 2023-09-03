from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ChargeType:
    Id: Optional[str] = None
    Charge: Optional[float] = None
    NameFr: Optional[str] = None
    NameEn: Optional[str] = None
    BeyondId: Optional[int] = None
    Rate: Optional[float] = None


@s(auto_attribs=True)
class RatesDetailType:
    BasePrice: Optional[float] = None
    SurchargeCharges: List[ChargeType] = JList[ChargeType]
    TaxCharges: List[ChargeType] = JList[ChargeType]
    AccessoryCharges: List[ChargeType] = JList[ChargeType]
    NCVCharge: Optional[int] = None
    FuelRate: Optional[float] = None
    FuelCharge: Optional[float] = None
    SubTotal: Optional[float] = None
    Total: Optional[float] = None
    TotalBillableWeight: Optional[int] = None
    BillingZone: Optional[str] = None
    DelayTransitDays: Optional[int] = None
    EstimatedDeliveryDate: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponseType:
    ShipmentId: Optional[int] = None
    ConsolId: Optional[int] = None
    BillingAccount: Optional[int] = None
    ParcelIds: List[str] = []
    Barcodes: List[str] = []
    RatesDetail: Optional[RatesDetailType] = JStruct[RatesDetailType]
