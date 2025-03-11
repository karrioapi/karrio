import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CourierSelectionType:
    apply_shipping_rules: typing.Optional[bool] = None
    show_courier_logo_url: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ComparisonType:
    changes: typing.Optional[str] = None
    post: typing.Optional[str] = None
    pre: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationType:
    detail: typing.Optional[str] = None
    status: typing.Optional[str] = None
    comparison: typing.Optional[ComparisonType] = jstruct.JStruct[ComparisonType]


@attr.s(auto_attribs=True)
class NAddressType:
    country_alpha2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    contact_email: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    contact_phone: typing.Optional[str] = None
    line_1: typing.Optional[str] = None
    line_2: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    state: typing.Optional[str] = None
    validation: typing.Optional[ValidationType] = jstruct.JStruct[ValidationType]


@attr.s(auto_attribs=True)
class InsuranceType:
    insured_amount: typing.Optional[float] = None
    insured_currency: typing.Optional[str] = None
    is_insured: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class BoxType:
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    slug: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    contains_battery_pi966: typing.Optional[bool] = None
    contains_battery_pi967: typing.Optional[bool] = None
    contains_liquids: typing.Optional[bool] = None
    declared_currency: typing.Optional[str] = None
    dimensions: typing.Optional[BoxType] = jstruct.JStruct[BoxType]
    origin_country_alpha2: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    actual_weight: typing.Optional[int] = None
    category: typing.Optional[str] = None
    declared_customs_value: typing.Optional[int] = None
    description: typing.Optional[str] = None
    sku: typing.Optional[str] = None
    hs_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    box: typing.Optional[BoxType] = jstruct.JStruct[BoxType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    total_actual_weight: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class UnitsType:
    dimensions: typing.Optional[str] = None
    weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingSettingsType:
    output_currency: typing.Optional[str] = None
    units: typing.Optional[UnitsType] = jstruct.JStruct[UnitsType]


@attr.s(auto_attribs=True)
class RateRequestType:
    courier_selection: typing.Optional[CourierSelectionType] = jstruct.JStruct[CourierSelectionType]
    destination_address: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    incoterms: typing.Optional[str] = None
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    origin_address: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    shipping_settings: typing.Optional[ShippingSettingsType] = jstruct.JStruct[ShippingSettingsType]
