import pkgutil
import typing

import karrio.server.events.task_definitions as definitions
from karrio.server.core.logging import logger

DEFINITIONS: list[typing.Any] = []

# Register karrio background tasks
for _, name, _ in pkgutil.iter_modules(definitions.__path__):  # type: ignore
    try:
        definition = __import__(f"{definitions.__name__}.{name}", fromlist=[name])  # type: ignore
        if hasattr(definition, "TASK_DEFINITIONS"):
            DEFINITIONS += definition.TASK_DEFINITIONS
    except Exception as e:
        logger.warning("Failed to register task definition", task_name=name, error=str(e))
        logger.exception("Task definition registration error", task_name=name)

for wrapper in DEFINITIONS:
    globals()[wrapper.task_class.__name__] = wrapper
