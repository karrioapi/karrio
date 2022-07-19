import pkgutil
import logging
from typing import Any, Dict

from karrio import gateway
from karrio.server.providers.models.carrier import Carrier, ServiceLevel, register_model
from karrio.server.providers.models.template import LabelTemplate
import karrio.server.providers.extension.models as extensions

logger = logging.getLogger(__name__)


# Register karrio settings defined above
MODELS: Dict[str, Any] = {}


# Register karrio-server models extensions
for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    if name in gateway.providers:
        try:
            extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
            MODELS.update({name: register_model(extension.SETTINGS)})
        except Exception as e:
            logger.warning(f'Failed to register extension "{name}" Model')
            logger.exception(e)
