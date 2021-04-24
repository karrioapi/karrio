import pkgutil
import logging
from typing import Any, Dict

from purplship import gateway
from purpleserver.providers.models.carrier import Carrier
import purpleserver.providers.extension.models as extensions

logger = logging.getLogger(__name__)


# Register purplship settings defined above
MODELS: Dict[str, Any] = {}


# Register purplship-server models extensions
for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    if name in gateway.providers:
        try:
            extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
            MODELS.update({name: extension.SETTINGS})
        except Exception as e:
            logger.warning(f'Failed to register extension "{name}" Model')
            logger.exception(e)
