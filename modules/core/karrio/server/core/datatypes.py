# ruff: noqa: F401, I001
import attr
import jstruct
import karrio.core.units as units
from karrio.core.models import (
    Address as BaseAddress,
)
from karrio.core.models import (
    ChargeDetails,
    Customs,
    DocumentDetails,
    Documents,
    DutiesCalculationDetails,
    Images,
    InsuranceDetails,
    ManifestDocument,
    Message,
    OAuthAuthorizePayload,
    OAuthAuthorizeRequest,
    Parcel,
    Payment,
    RequestPayload,
    TrackingEvent,
    WebhookEventDetails,
    WebhookDeregistrationRequest,
    WebhookRegistrationRequest,
    TrackingInfo,
)
from karrio.core.models import (
    ConfirmationDetails as Confirmation,
)
from karrio.core.models import (
    PickupCancelRequest as BasePickupCancelRequest,
)
from karrio.core.models import (
    PickupRequest as BasePickupRequest,
)
from karrio.core.models import (
    PickupUpdateRequest as BasePickupUpdateRequest,
)
from karrio.core.models import (
    RateRequest as BaseRateRequest,
)
from karrio.core.models import (
    ShipmentRequest as BaseShipmentRequest,
)
from karrio.core.models import (
    ShipmentCancelRequest,
)
from karrio.core.models import (
    TrackingRequest as BaseTrackingRequest,
)

COUNTRIES = [(c.name, c.name) for c in units.Country]
CURRENCIES = [(c.name, c.name) for c in units.Currency]
WEIGHT_UNITS = [(c.name, c.name) for c in units.WeightUnit]
DIMENSION_UNITS = [(c.name, c.name) for c in units.DimensionUnit]
CAPABILITIES_CHOICES = [(c, c) for c in units.CarrierCapabilities.get_capabilities()]
LABEL_TYPES = [(c.name, c.name) for c in list(units.LabelType)]


class CarrierSettings:
    def __init__(
        self,
        carrier_name: str,
        carrier_id: str,
        test_mode: bool = None,
        active: bool = None,
        id: str = None,
        display_name: str = None,
        **kwargs,
    ):
        self.carrier_name = carrier_name
        self.display_name = display_name
        self.carrier_id = carrier_id
        self.active = active
        self.test_mode = test_mode
        self.id = id

        for name, value in kwargs.items():
            if name not in ["carrier_ptr", "created_by"]:
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
                *([] if self.carrier_name == "generic" else ["display_name"]),
            ]
        }

    @property
    def shipping_services(self):
        """Alias for services to be compatible with RatingMixinProxy.

        Converts service dicts to ServiceLevel objects if needed.
        """
        import karrio.lib as lib
        from karrio.core.models import ServiceLevel

        services = getattr(self, "services", [])
        return [lib.to_object(ServiceLevel, s) if isinstance(s, dict) else s for s in services]

    @property
    def account_country_code(self):
        """Account country code for rate calculation, falls back from config or metadata."""
        return (
            getattr(self, "_account_country_code", None)
            or (getattr(self, "config", None) or {}).get("account_country_code")
            or (getattr(self, "metadata", None) or {}).get("account_country_code")
        )

    @account_country_code.setter
    def account_country_code(self, value):
        """Set account country code."""
        self._account_country_code = value

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
    residential: bool = False

    address_line1: str = ""
    address_line2: str = None
    street_number: str = None
    suite: str = None

    federal_tax_id: str = None
    state_tax_id: str = None

    validate_location: bool = None
    validation: jstruct.JStruct[AddressValidation] = None


@attr.s(auto_attribs=True)
class PickupRequest(BasePickupRequest):
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = jstruct.JStruct[Address, jstruct.REQUIRED]

    parcels: list[Parcel] = jstruct.JList[Parcel]
    parcels_count: int = None
    shipment_identifiers: list[str] = []
    package_location: str = None
    instruction: str = None
    pickup_type: str = "one_time"  # one_time, daily, recurring
    recurrence: dict = {}  # For recurring: {frequency, days_of_week, end_date}
    metadata: dict = {}
    options: dict = {}


@attr.s(auto_attribs=True)
class PickupUpdateRequest(BasePickupUpdateRequest):
    confirmation_number: str
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = jstruct.JStruct[Address, jstruct.REQUIRED]

    parcels: list[Parcel] = jstruct.JList[Parcel]
    shipment_identifiers: list[str] = []
    package_location: str = None
    instruction: str = None
    pickup_type: str = "one_time"  # one_time, daily, recurring
    recurrence: dict = {}  # For recurring: {frequency, days_of_week, end_date}
    options: dict = {}


@attr.s(auto_attribs=True)
class PickupCancelRequest(BasePickupCancelRequest):
    confirmation_number: str

    address: Address = jstruct.JStruct[Address]
    pickup_date: str = None
    reason: str = None
    options: dict = {}


@attr.s(auto_attribs=True)
class Rate:
    carrier_name: str
    carrier_id: str

    currency: str = None
    transit_days: int = None
    service: str = None
    total_charge: float = 0.0
    extra_charges: list[ChargeDetails] = []
    estimated_delivery: str = None
    id: str = None
    meta: dict = None
    test_mode: bool = None
    object_type: str = "rate"


@attr.s(auto_attribs=True)
class RateRequest(BaseRateRequest):
    shipper: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    recipient: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    parcels: list[Parcel] = jstruct.JList[Parcel, jstruct.REQUIRED]

    payment: Payment = jstruct.JStruct[Payment]
    customs: Customs = jstruct.JStruct[Customs]
    return_address: Address = jstruct.JStruct[Address]
    billing_address: Address = jstruct.JStruct[Address]

    services: list[str] = []
    options: dict = {}
    reference: str = ""
    is_return: bool = False

    carrier_ids: list[str] = []


@attr.s(auto_attribs=True)
class ShipmentRequest(BaseShipmentRequest):
    service: str
    selected_rate_id: str  # type: ignore

    shipper: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    recipient: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    parcels: list[Parcel] = jstruct.JList[Parcel, jstruct.REQUIRED]
    rates: list[Rate] = jstruct.JList[Rate, jstruct.REQUIRED]

    payment: Payment = jstruct.JStruct[Payment]
    customs: Customs = jstruct.JStruct[Customs]
    return_address: Address = jstruct.JStruct[Address]
    billing_address: Address = jstruct.JStruct[Address]

    options: dict = {}
    reference: str = ""
    order_id: str = ""
    label_type: str = None
    is_return: bool = False
    id: str = None

    metadata: dict = {}


@attr.s(auto_attribs=True)
class Shipment:
    carrier_id: str
    carrier_name: str
    tracking_number: str
    shipment_identifier: str
    service: str
    selected_rate_id: str

    shipper: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    recipient: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    parcels: list[Parcel] = jstruct.JList[Parcel, jstruct.REQUIRED]
    rates: list[Rate] = jstruct.JList[Rate, jstruct.REQUIRED]
    selected_rate: Rate = jstruct.JStruct[Rate, jstruct.REQUIRED]
    docs: Documents = jstruct.JStruct[Documents, jstruct.REQUIRED]

    payment: Payment = jstruct.JStruct[Payment]
    customs: Customs = jstruct.JStruct[Customs]
    billing_address: Address = jstruct.JStruct[Address]

    options: dict = {}
    reference: str = ""
    label_type: str = None
    tracking_url: str = None
    tracker_id: str = None
    status: str = ""
    metadata: dict = {}
    meta: dict = {}
    return_shipment: dict = None
    id: str = None

    messages: list[Message] = jstruct.JList[Message]
    created_at: str = None
    test_mode: bool = None


@attr.s(auto_attribs=True)
class Pickup:
    carrier_id: str
    carrier_name: str

    pickup_date: str
    ready_time: str
    closing_time: str
    confirmation_number: str
    address: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    parcels: list[Parcel] = jstruct.JList[Parcel, jstruct.REQUIRED]

    pickup_charge: ChargeDetails = jstruct.JStruct[ChargeDetails]
    instruction: str = None
    package_location: str = None
    pickup_type: str = None  # one_time, daily, recurring
    recurrence: dict = {}  # For recurring: {frequency, days_of_week, end_date}
    metadata: dict = {}
    options: dict = {}
    meta: dict = {}
    id: str = None

    messages: list[Message] = jstruct.JList[Message]
    test_mode: bool = None


@attr.s(auto_attribs=True)
class TrackingRequest(BaseTrackingRequest):
    tracking_numbers: list[str]
    account_numer: str = None
    reference: str = None
    options: dict = {}
    info: TrackingInfo = jstruct.JStruct[TrackingInfo]


@attr.s(auto_attribs=True)
class Tracking:
    carrier_name: str
    carrier_id: str
    tracking_number: str
    events: list[TrackingEvent] = jstruct.JList[TrackingEvent]

    status: str = "unknown"
    info: TrackingInfo = jstruct.JStruct[TrackingInfo]
    images: Images = jstruct.JStruct[Images]
    estimated_delivery: str = None
    delivered: bool = None
    test_mode: bool = None
    options: dict = {}
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class DocumentUploadResponse:
    carrier_name: str
    carrier_id: str
    documents: list[DocumentDetails] = jstruct.JList[DocumentDetails]
    reference: str = ""

    test_mode: bool = None
    options: dict = {}
    meta: dict = None
    id: str = None
    messages: list[Message] = jstruct.JList[Message]


@attr.s(auto_attribs=True)
class Manifest:
    carrier_id: str
    carrier_name: str

    shipment_identifiers: list[str]
    address: Address = jstruct.JStruct[Address, jstruct.REQUIRED]
    doc: ManifestDocument = jstruct.JStruct[ManifestDocument]

    reference: str = None
    metadata: dict = {}
    options: dict = {}
    meta: dict = {}
    id: str = None

    messages: list[Message] = jstruct.JList[Message]
    test_mode: bool = None


@attr.s(auto_attribs=True)
class ConfirmationResponse:
    messages: list[Message] = jstruct.JList[Message]
    confirmation: Confirmation = jstruct.JStruct[Confirmation]


@attr.s(auto_attribs=True)
class PickupResponse:
    messages: list[Message] = jstruct.JList[Message]
    pickup: Pickup = jstruct.JStruct[Pickup]


@attr.s(auto_attribs=True)
class RateResponse:
    messages: list[Message] = jstruct.JList[Message]
    rates: list[Rate] = jstruct.JList[Rate]


@attr.s(auto_attribs=True)
class TrackingResponse:
    messages: list[Message] = jstruct.JList[Message]
    tracking: Tracking = jstruct.JStruct[Tracking]


@attr.s(auto_attribs=True)
class ManifestResponse:
    messages: list[Message] = jstruct.JList[Message]
    manifest: Manifest = jstruct.JStruct[Manifest]


@attr.s(auto_attribs=True)
class DutiesResponse:
    messages: list[Message] = jstruct.JList[Message]
    duties: DutiesCalculationDetails = jstruct.JStruct[DutiesCalculationDetails]


@attr.s(auto_attribs=True)
class InsuranceResponse:
    messages: list[Message] = jstruct.JList[Message]
    insurance: InsuranceDetails = jstruct.JStruct[InsuranceDetails]


@attr.s(auto_attribs=True)
class Error:
    code: str = None
    message: str = None
    level: str = None
    details: dict = None
