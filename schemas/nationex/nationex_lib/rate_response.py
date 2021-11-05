from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class Charge:
    Id: Optional[str] = None
    Charge: Optional[float] = None
    NameFr: Optional[str] = None
    NameEn: Optional[str] = None
    BeyondId: Optional[int] = None
    Rate: Optional[float] = None


@s(auto_attribs=True)
class RateResponse:
    BasePrice: Optional[float] = None
    SurchargeCharges: List[Charge] = JList[Charge]
    TaxCharges: List[Charge] = JList[Charge]
    AccessoryCharges: List[Charge] = JList[Charge]
    NCVCharge: Optional[float] = None
    FuelRate: Optional[float] = None
    FuelCharge: Optional[float] = None
    SubTotal: Optional[float] = None
    Total: Optional[float] = None
    TotalBillableWeight: Optional[float] = None
    BillingZone: Optional[str] = None
    DelayTransitDays: Optional[int] = None
    EstimatedDeliveryDate: Optional[str] = None
