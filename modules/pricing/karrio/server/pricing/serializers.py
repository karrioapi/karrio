import enum
import karrio.server.core.dataunits as dataunits
from karrio.server.core.serializers import (
    CARRIERS,
)


class SurchargeType(enum.Enum):
    AMOUNT = "$"
    PERCENTAGE = "%"


CARRIER_SERVICES = [
    dataunits.REFERENCE_MODELS["services"][name]
    for name in sorted(dataunits.REFERENCE_MODELS["services"].keys())
]
SERVICES = [(code, code) for services in CARRIER_SERVICES for code in services]
SURCHAGE_TYPE = [(c.name, c.value) for c in list(SurchargeType)]
