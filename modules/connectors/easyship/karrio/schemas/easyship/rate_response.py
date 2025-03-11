import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PaginationType:
    count: typing.Optional[int] = None
    next: typing.Optional[str] = None
    page: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class MetaType:
    pagination: typing.Optional[PaginationType] = jstruct.JStruct[PaginationType]
    request_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DiscountType:
    amount: typing.Optional[int] = None
    origin_amount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DetailType:
    fee: typing.Optional[int] = None
    name: typing.Optional[str] = None
    origin_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class OtherSurchargesType:
    details: typing.Optional[typing.List[DetailType]] = jstruct.JList[DetailType]
    total_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RatesInOriginCurrencyType:
    additional_services_surcharge: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    ddp_handling_fee: typing.Optional[int] = None
    estimated_import_duty: typing.Optional[int] = None
    estimated_import_tax: typing.Optional[float] = None
    fuel_surcharge: typing.Optional[int] = None
    import_duty_charge: typing.Optional[int] = None
    import_tax_charge: typing.Optional[int] = None
    import_tax_non_chargeable: typing.Optional[int] = None
    insurance_fee: typing.Optional[int] = None
    minimum_pickup_fee: typing.Optional[int] = None
    oversized_surcharge: typing.Optional[int] = None
    provincial_sales_tax: typing.Optional[int] = None
    remote_area_surcharge: typing.Optional[int] = None
    residential_discounted_fee: typing.Optional[int] = None
    residential_full_fee: typing.Optional[int] = None
    sales_tax: typing.Optional[int] = None
    shipment_charge: typing.Optional[int] = None
    shipment_charge_total: typing.Optional[int] = None
    total_charge: typing.Optional[int] = None
    warehouse_handling_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DestinationType:
    base: typing.Optional[int] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RemoteAreaSurchargesType:
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]


@attr.s(auto_attribs=True)
class RateType:
    additional_services_surcharge: typing.Optional[int] = None
    available_handover_options: typing.Optional[typing.List[typing.Any]] = None
    cost_rank: typing.Optional[int] = None
    courier_id: typing.Optional[str] = None
    courier_logo_url: typing.Optional[str] = None
    courier_name: typing.Optional[str] = None
    courier_remarks: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    ddp_handling_fee: typing.Optional[int] = None
    delivery_time_rank: typing.Optional[int] = None
    description: typing.Optional[str] = None
    discount: typing.Optional[DiscountType] = jstruct.JStruct[DiscountType]
    easyship_rating: typing.Optional[int] = None
    estimated_import_duty: typing.Optional[int] = None
    estimated_import_tax: typing.Optional[float] = None
    fuel_surcharge: typing.Optional[int] = None
    full_description: typing.Optional[str] = None
    import_duty_charge: typing.Optional[int] = None
    import_tax_charge: typing.Optional[int] = None
    import_tax_non_chargeable: typing.Optional[int] = None
    incoterms: typing.Optional[str] = None
    insurance_fee: typing.Optional[int] = None
    is_above_threshold: typing.Optional[bool] = None
    max_delivery_time: typing.Optional[int] = None
    min_delivery_time: typing.Optional[int] = None
    minimum_pickup_fee: typing.Optional[int] = None
    other_surcharges: typing.Optional[OtherSurchargesType] = jstruct.JStruct[OtherSurchargesType]
    oversized_surcharge: typing.Optional[int] = None
    payment_recipient: typing.Optional[str] = None
    provincial_sales_tax: typing.Optional[int] = None
    rates_in_origin_currency: typing.Optional[RatesInOriginCurrencyType] = jstruct.JStruct[RatesInOriginCurrencyType]
    remote_area_surcharge: typing.Optional[int] = None
    remote_area_surcharges: typing.Optional[RemoteAreaSurchargesType] = jstruct.JStruct[RemoteAreaSurchargesType]
    residential_discounted_fee: typing.Optional[int] = None
    residential_full_fee: typing.Optional[int] = None
    sales_tax: typing.Optional[int] = None
    shipment_charge: typing.Optional[int] = None
    shipment_charge_total: typing.Optional[int] = None
    total_charge: typing.Optional[int] = None
    tracking_rating: typing.Optional[int] = None
    value_for_money_rank: typing.Optional[int] = None
    warehouse_handling_fee: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
