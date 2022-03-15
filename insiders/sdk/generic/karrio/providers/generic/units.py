from karrio.core.utils import Enum, Spec, Flag
from karrio.core.models import ServiceLevel


class Service(Enum):
    standard_service = "standard"


class Option(Flag):
    tracking_number_reference = Spec.asValue("tracking_number")


DEFAULT_SERVICES = [
    ServiceLevel(
        service_name="Standard Service",
        service_code="standard_service",
        cost=0.00,
        currency="USD",
    ),
]
