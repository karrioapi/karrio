import typing
import pkgutil
from karrio.server.core.logging import logger
import karrio.server.events.task_definitions as definitions
DEFINITIONS: typing.List[typing.Any] = []

# Register karrio background tasks
for _, name, _ in pkgutil.iter_modules(definitions.__path__):  # type: ignore
    try:
        definition = __import__(f"{definitions.__name__}.{name}", fromlist=[name])  # type: ignore
        if hasattr(definition, "TASK_DEFINITIONS"):
            DEFINITIONS += definition.TASK_DEFINITIONS
    except Exception as e:
        logger.warning(f"Failed to register task definition", task_name=name, error=str(e))
        logger.exception(f"Task definition registration error", task_name=name)

for wrapper in DEFINITIONS:
    globals()[wrapper.task_class.__name__] = wrapper
