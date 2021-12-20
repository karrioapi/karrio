from purplship.core.utils import Enum, Spec, Flag
from purplship.core.models import ServiceLevel


class Service(Enum):
    generic_standard = "standard"


class Option(Flag):
    generic_tracking_number_reference = Spec.asValue("tracking_number")
    generic_label_template = Spec.asValue("label_template")


DEFAULT_SERVICES = [
    ServiceLevel(
        service_name="Generic Standard",
        service_code="generic_standard",
        cost=0.00,
        currency="USD",
    ),
]
