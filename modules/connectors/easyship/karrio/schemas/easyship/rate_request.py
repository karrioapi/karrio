from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CourierSelectionType:
    applyshippingrules: Optional[bool] = None
    showcourierlogourl: Optional[bool] = None


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
    countryalpha2: Optional[str] = None
    city: Optional[str] = None
    companyname: Any = None
    contactemail: Optional[str] = None
    contactname: Optional[str] = None
    contactphone: Any = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    postalcode: Optional[str] = None
    state: Optional[str] = None
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class InsuranceType:
    insuredamount: Optional[float] = None
    insuredcurrency: Optional[str] = None
    isinsured: Optional[bool] = None


@s(auto_attribs=True)
class BoxType:
    height: Optional[int] = None
    length: Optional[int] = None
    weight: Optional[int] = None
    width: Optional[int] = None
    slug: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    containsbatterypi966: Optional[bool] = None
    containsbatterypi967: Optional[bool] = None
    containsliquids: Optional[bool] = None
    declaredcurrency: Optional[str] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    origincountryalpha2: Optional[str] = None
    quantity: Optional[int] = None
    actualweight: Optional[int] = None
    category: Optional[str] = None
    declaredcustomsvalue: Optional[int] = None
    description: Optional[str] = None
    sku: Optional[str] = None


@s(auto_attribs=True)
class ParcelType:
    box: Optional[BoxType] = JStruct[BoxType]
    items: List[ItemType] = JList[ItemType]
    totalactualweight: Optional[int] = None


@s(auto_attribs=True)
class UnitsType:
    dimensions: Optional[str] = None
    weight: Optional[str] = None


@s(auto_attribs=True)
class ShippingSettingsType:
    outputcurrency: Optional[str] = None
    units: Optional[UnitsType] = JStruct[UnitsType]


@s(auto_attribs=True)
class RateRequestType:
    courierselection: Optional[CourierSelectionType] = JStruct[CourierSelectionType]
    destinationaddress: Optional[NAddressType] = JStruct[NAddressType]
    incoterms: Optional[str] = None
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]
    originaddress: Optional[NAddressType] = JStruct[NAddressType]
    parcels: List[ParcelType] = JList[ParcelType]
    shippingsettings: Optional[ShippingSettingsType] = JStruct[ShippingSettingsType]
