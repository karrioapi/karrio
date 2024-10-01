from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class PaginationType:
    count: Optional[int] = None
    next: Optional[str] = None
    page: Optional[int] = None


@s(auto_attribs=True)
class MetaType:
    pagination: Optional[PaginationType] = JStruct[PaginationType]
    request_id: Optional[str] = None


@s(auto_attribs=True)
class DiscountType:
    amount: Optional[int] = None
    origin_amount: Optional[int] = None


@s(auto_attribs=True)
class DetailType:
    fee: Optional[int] = None
    name: Optional[str] = None
    origin_fee: Optional[int] = None


@s(auto_attribs=True)
class OtherSurchargesType:
    details: List[DetailType] = JList[DetailType]
    total_fee: Optional[int] = None


@s(auto_attribs=True)
class RatesInOriginCurrencyType:
    additional_services_surcharge: Optional[int] = None
    currency: Optional[str] = None
    ddp_handling_fee: Optional[int] = None
    estimated_import_duty: Optional[int] = None
    estimated_import_tax: Optional[float] = None
    fuel_surcharge: Optional[int] = None
    import_duty_charge: Optional[int] = None
    import_tax_charge: Optional[int] = None
    import_tax_non_chargeable: Optional[int] = None
    insurance_fee: Optional[int] = None
    minimum_pickup_fee: Optional[int] = None
    oversized_surcharge: Optional[int] = None
    provincial_sales_tax: Optional[int] = None
    remote_area_surcharge: Optional[int] = None
    residential_discounted_fee: Optional[int] = None
    residential_full_fee: Optional[int] = None
    sales_tax: Optional[int] = None
    shipment_charge: Optional[int] = None
    shipment_charge_total: Optional[int] = None
    total_charge: Optional[int] = None
    warehouse_handling_fee: Optional[int] = None


@s(auto_attribs=True)
class DestinationType:
    base: Optional[int] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class RemoteAreaSurchargesType:
    destination: Optional[DestinationType] = JStruct[DestinationType]
    origin: Optional[DestinationType] = JStruct[DestinationType]


@s(auto_attribs=True)
class RateType:
    additional_services_surcharge: Optional[int] = None
    available_handover_options: List[Any] = []
    cost_rank: Optional[int] = None
    courier_id: Optional[str] = None
    courier_logo_url: Optional[str] = None
    courier_name: Optional[str] = None
    courier_remarks: Optional[str] = None
    currency: Optional[str] = None
    ddp_handling_fee: Optional[int] = None
    delivery_time_rank: Optional[int] = None
    description: Optional[str] = None
    discount: Optional[DiscountType] = JStruct[DiscountType]
    easyship_rating: Optional[int] = None
    estimated_import_duty: Optional[int] = None
    estimated_import_tax: Optional[float] = None
    fuel_surcharge: Optional[int] = None
    full_description: Optional[str] = None
    import_duty_charge: Optional[int] = None
    import_tax_charge: Optional[int] = None
    import_tax_non_chargeable: Optional[int] = None
    incoterms: Optional[str] = None
    insurance_fee: Optional[int] = None
    is_above_threshold: Optional[bool] = None
    max_delivery_time: Optional[int] = None
    min_delivery_time: Optional[int] = None
    minimum_pickup_fee: Optional[int] = None
    other_surcharges: Optional[OtherSurchargesType] = JStruct[OtherSurchargesType]
    oversized_surcharge: Optional[int] = None
    payment_recipient: Optional[str] = None
    provincial_sales_tax: Optional[int] = None
    rates_in_origin_currency: Optional[RatesInOriginCurrencyType] = JStruct[RatesInOriginCurrencyType]
    remote_area_surcharge: Optional[int] = None
    remote_area_surcharges: Optional[RemoteAreaSurchargesType] = JStruct[RemoteAreaSurchargesType]
    residential_discounted_fee: Optional[int] = None
    residential_full_fee: Optional[int] = None
    sales_tax: Optional[int] = None
    shipment_charge: Optional[int] = None
    shipment_charge_total: Optional[int] = None
    total_charge: Optional[int] = None
    tracking_rating: Optional[int] = None
    value_for_money_rank: Optional[int] = None
    warehouse_handling_fee: Optional[int] = None


@s(auto_attribs=True)
class RateResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    rates: List[RateType] = JList[RateType]
