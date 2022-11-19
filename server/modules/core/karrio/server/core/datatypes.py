import attr
from typing import List, Dict
from jstruct import JStruct, JList, REQUIRED
from karrio.core.models import (
    DocumentDetails,
    Documents,
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
    TrackingEvent,
    TrackingDetails,
    DocumentFile,
    DocumentUploadRequest,
)


class CarrierSettings:
    def __init__(
        self,
        carrier_name: str,
        carrier_id: str,
        test_mode: bool = None,
        active: bool = None,
        id: str = None,
        **kwargs
    ):
        self.carrier_name = carrier_name
        self.carrier_id = carrier_id
        self.active = active
        self.test_mode = test_mode
        self.id = id

        for name, value in kwargs.items():
            if name not in ["carrier_ptr", "created_by", "active_users", "active_orgs"]:
                self.__setattr__(name, value)

    # TODO: rename this to avoid confusion
    def to_dict(self):
        return {
            name: value
            for name, value in self.__dict__.items()
            if name
            not in [
                "carrier_name",
                "created_by",
                "active",
                "capabilities",
                "active_users",
                "active_orgs",
            ]
        }

    @classmethod
    def create(cls, data: dict):
        return cls(**data)


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

    currency: str = None
    transit_days: int = None
    service: str = None
    total_charge: float = 0.0
    extra_charges: List[ChargeDetails] = []
    id: str = None
    meta: dict = None
    test_mode: bool = None
    object_type: str = "rate"


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
    selected_rate_id: str  # type: ignore

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

    metadata: Dict = {}


@attr.s(auto_attribs=True)
class Shipment:
    carrier_id: str
    carrier_name: str
    tracking_number: str
    shipment_identifier: str
    service: str
    selected_rate_id: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]
    rates: List[Rate] = JList[Rate, REQUIRED]
    selected_rate: Rate = JStruct[Rate, REQUIRED]
    docs: Documents = JStruct[Documents, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]

    options: Dict = {}
    reference: str = ""
    label_type: str = None
    tracking_url: str = None
    tracker_id: str = None
    status: str = ""
    meta: dict = {}
    id: str = None

    metadata: Dict = {}
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
    events: List[TrackingEvent] = JList[TrackingEvent]

    status: str = ""
    delivered: bool = None
    estimated_delivery: str = None
    id: str = None
    test_mode: bool = None
    options: Dict = {}
    meta: dict = None



@attr.s(auto_attribs=True)
class DocumentUploadResponse:
    carrier_name: str
    carrier_id: str
    documents: List[DocumentDetails] = JList[DocumentDetails]
    reference: str = ""

    test_mode: bool = None
    options: Dict = {}
    meta: dict = None
    id: str = None
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
