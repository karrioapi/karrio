import attr
from typing import List, Dict
from enum import Enum
from jstruct import JStruct, JList, REQUIRED
from purplship.core.utils import DP
from purplship.core.models import (
    Parcel,
    Message,
    Address as BaseAddress,
    TrackingRequest,
    ShipmentDetails,
    Payment,
    Customs,
    RateRequest as BaseRateRequest,
    ShipmentRequest as BaseShipmentRequest,
    ShipmentCancelRequest,
    ChargeDetails,
    PickupRequest as BasePickupRequest,
    PickupDetails,
    PickupUpdateRequest as BasePickupUpdateRequest,
    PickupCancelRequest as BasePickupCancelRequest,
    ConfirmationDetails as Confirmation,
    TrackingEvent
)


class ShipmentStatus(Enum):
    created = 'created'
    cancelled = 'cancelled'
    purchased = 'purchased'


class CarrierSettings:
    def __init__(self, carrier_name: str, carrier_id: str, test: bool = None, active: bool = None, id: str = None, **kwargs):
        self.carrier_name = carrier_name
        self.carrier_id = carrier_id
        self.active = active
        self.test = test
        self.id = id

        for name, value in kwargs.items():
            if name not in ['carrier_ptr', 'created_by']:
                self.__setattr__(name, value)

    # TODO: rename this to avoid confusion
    def dict(self):
        return {
            name: value for name, value in self.__dict__.items()
            if name not in ['carrier_name', 'created_by', 'active']
        }

    @classmethod
    def create(cls, data: object):
        return cls(**DP.to_dict(data))


@attr.s(auto_attribs=True)
class AddressValidation:
    success: bool
    meta: dict = {}


@attr.s(auto_attribs=True)
class Address(BaseAddress):
    id: str = None
    postal_code: str = None
    city: str = None
    person_name: str = None
    company_name: str = None
    country_code: str = None
    email: str = None
    phone_number: str = None

    state_code: str = None
    suburb: str = None
    residential: bool = False

    address_line1: str = ""
    address_line2: str = ""

    federal_tax_id: str = None
    state_tax_id: str = None

    validate_location: bool = None
    validation: JStruct[AddressValidation] = None


@attr.s(auto_attribs=True)
class PickupRequest(BasePickupRequest):
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    instruction: str = None
    package_location: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupUpdateRequest(BasePickupUpdateRequest):
    confirmation_number: str
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    instruction: str = None
    package_location: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupCancelRequest(BasePickupCancelRequest):
    confirmation_number: str

    address: Address = JStruct[Address]
    pickup_date: str = None
    reason: str = None


@attr.s(auto_attribs=True)
class Rate:
    carrier_name: str
    carrier_id: str
    currency: str

    transit_days: int = None
    service: str = None
    discount: float = None
    base_charge: float = 0.0
    total_charge: float = 0.0
    duties_and_taxes: float = None
    extra_charges: List[ChargeDetails] = []
    id: str = None
    meta: dict = None
    carrier_ref: str = None
    test_mode: bool = None


@attr.s(auto_attribs=True)
class RateRequest(BaseRateRequest):
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    services: List[str] = []
    options: Dict = {}
    reference: str = ""

    carrier_ids: List[str] = []


@attr.s(auto_attribs=True)
class ShipmentRequest(BaseShipmentRequest):
    service: str
    selected_rate_id: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]
    rates: List[Rate] = JList[Rate, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]

    options: Dict = {}
    reference: str = ""
    label_type: str = None
    id: str = None


@attr.s(auto_attribs=True)
class Shipment:
    carrier_id: str
    carrier_name: str
    tracking_number: str
    shipment_identifier: str
    label: str
    service: str
    selected_rate_id: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]
    rates: List[Rate] = JList[Rate, REQUIRED]
    selected_rate: Rate = JStruct[Rate, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]

    options: Dict = {}
    reference: str = ""
    label_type: str = None
    tracking_url: str = None
    status: str = ""
    meta: dict = None
    id: str = None
    created_at: str = None
    test_mode: bool = None
    messages: List[Message] = JList[Message]


@attr.s(auto_attribs=True)
class Pickup:
    carrier_id: str
    carrier_name: str

    pickup_date: str
    ready_time: str
    closing_time: str
    confirmation_number: str
    address: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    pickup_charge: ChargeDetails = JStruct[ChargeDetails]
    instruction: str = None
    package_location: str = None
    options: Dict = {}
    id: str = None
    test_mode: bool = None


@attr.s(auto_attribs=True)
class Tracking:
    carrier_name: str
    carrier_id: str
    tracking_number: str
    events: List[TrackingEvent] = JList[TrackingEvent, REQUIRED]

    delivered: bool = None
    id: str = None
    test_mode: bool = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    messages: List[Message] = JList[Message]


@attr.s(auto_attribs=True)
class ConfirmationResponse:
    messages: List[Message] = JList[Message]
    confirmation: Confirmation = JStruct[Confirmation]


@attr.s(auto_attribs=True)
class PickupResponse:
    messages: List[Message] = JList[Message]
    pickup: Pickup = JStruct[Pickup]


@attr.s(auto_attribs=True)
class RateResponse:
    messages: List[Message] = JList[Message]
    rates: List[Rate] = JList[Rate]


@attr.s(auto_attribs=True)
class TrackingResponse:
    messages: List[Message] = JList[Message]
    tracking: Tracking = JStruct[Tracking]


@attr.s(auto_attribs=True)
class Error:
    message: str = None
    code: str = None
    details: Dict = None
