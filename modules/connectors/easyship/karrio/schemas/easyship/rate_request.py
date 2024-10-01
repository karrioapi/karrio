from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CourierSelectionType:
    apply_shipping_rules: Optional[bool] = None
    show_courier_logo_url: Optional[bool] = None


@s(auto_attribs=True)
class ComparisonType:
    changes: Optional[str] = None
    post: Optional[str] = None
    pre: Optional[str] = None


@s(auto_attribs=True)
class ValidationType:
    detail: Optional[str] = None
    status: Optional[str] = None
    comparison: Optional[ComparisonType] = JStruct[ComparisonType]


@s(auto_attribs=True)
class NAddressType:
    country_alpha2: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class InsuranceType:
    insured_amount: Optional[float] = None
    insured_currency: Optional[str] = None
    is_insured: Optional[bool] = None


@s(auto_attribs=True)
class BoxType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    slug: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    contains_battery_pi966: Optional[bool] = None
    contains_battery_pi967: Optional[bool] = None
    contains_liquids: Optional[bool] = None
    declared_currency: Optional[str] = None
    dimensions: Optional[BoxType] = JStruct[BoxType]
    origin_country_alpha2: Optional[str] = None
    quantity: Optional[int] = None
    actual_weight: Optional[int] = None
    category: Optional[str] = None
    declared_customs_value: Optional[int] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    hs_code: Optional[str] = None


@s(auto_attribs=True)
class ParcelType:
    box: Optional[BoxType] = JStruct[BoxType]
    items: List[ItemType] = JList[ItemType]
    total_actual_weight: Optional[int] = None


@s(auto_attribs=True)
class UnitsType:
    dimensions: Optional[str] = None
    weight: Optional[str] = None


@s(auto_attribs=True)
class ShippingSettingsType:
    output_currency: Optional[str] = None
    units: Optional[UnitsType] = JStruct[UnitsType]


@s(auto_attribs=True)
class RateRequestType:
    courier_selection: Optional[CourierSelectionType] = JStruct[CourierSelectionType]
    destination_address: Optional[NAddressType] = JStruct[NAddressType]
    incoterms: Optional[str] = None
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]
    origin_address: Optional[NAddressType] = JStruct[NAddressType]
    parcels: List[ParcelType] = JList[ParcelType]
    shipping_settings: Optional[ShippingSettingsType] = JStruct[ShippingSettingsType]
