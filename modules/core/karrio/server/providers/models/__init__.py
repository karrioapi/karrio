import typing
import pkgutil
import logging

import karrio

from karrio.server.providers.models.sheet import RateSheet
from karrio.server.providers.models.config import CarrierConfig
from karrio.server.providers.models.service import ServiceLevel
from karrio.server.providers.models.template import LabelTemplate
from karrio.server.core.models.base import (
    register_model,
)
from karrio.server.providers.models.utils import (
    has_rate_sheet,
)
from karrio.server.providers.models.carrier import (
    Carrier,
    COUNTRIES,
    CURRENCIES,
    WEIGHT_UNITS,
    DIMENSION_UNITS,
    CAPABILITIES_CHOICES,
    create_carrier_proxy,
)
import karrio.server.providers.extension.models as extensions

logger = logging.getLogger(__name__)


# Register karrio settings defined above
MODELS: typing.Dict[str, typing.Any] = {}


# Register karrio-server models extensions
for _, name, _ in pkgutil.iter_modules(extensions.__path__):  # type: ignore
    if name in karrio.gateway.providers:
        try:
            extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
            MODELS.update({name: register_model(extension.SETTINGS)})
        except Exception as e:
            logger.warning(f'Failed to register extension "{name}" Model')
            logger.exception(e)
