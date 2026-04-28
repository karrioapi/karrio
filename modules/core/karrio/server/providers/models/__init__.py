# Apply @hookable to model classes that need hook extensibility.
# Imported from hooks module (not utils) to avoid circular imports.
from karrio.server.core.hooks import hookable as _hookable
from karrio.server.core.models.base import register_model
from karrio.server.providers.models.carrier import (
    CAPABILITIES_CHOICES,
    COUNTRIES,
    CURRENCIES,
    DIMENSION_UNITS,
    WEIGHT_UNITS,
    CarrierConnection,
    create_carrier_proxy,
)
from karrio.server.providers.models.connection import (
    BrokeredConnection,
    SystemConnection,
)
from karrio.server.providers.models.service import ServiceLevel
from karrio.server.providers.models.sheet import AccountRateSheet, RateSheet, SystemRateSheet
from karrio.server.providers.models.template import LabelTemplate
from karrio.server.providers.models.utils import has_rate_sheet

_hookable(CarrierConnection)
_hookable(SystemConnection)
