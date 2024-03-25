from attr import s
from typing import Optional


@s(auto_attribs=True)
class ProductRequestType:
    sender_address_line1: Optional[str] = None
    sender_address_line2: Optional[str] = None
    sender_suburb: Optional[str] = None
    sender_postcode: Optional[str] = None
    sender_country: Optional[str] = None
    receiver_address_line1: Optional[str] = None
    receiver_address_line2: Optional[str] = None
    receiver_suburb: Optional[str] = None
    receiver_postcode: Optional[str] = None
    receiver_country: Optional[str] = None
    weight_value: Optional[float] = None
    weight_units: Optional[str] = None
    volume_value: Optional[str] = None
    volume_units: Optional[str] = None
    length_value: Optional[float] = None
    width_value: Optional[float] = None
    height_value: Optional[float] = None
    dimension_units: Optional[str] = None
