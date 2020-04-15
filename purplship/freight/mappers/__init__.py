from typing import Dict, Any
import pkgutil
import purplship.extension.mappers as extensions

Providers: Dict[str, Any] = {}

try:
    import purplship.freight.mappers.dhl as dhl

    Providers.update({"dhl": dhl})
except ImportError:
    pass
try:
    import purplship.freight.mappers.fedex as fedex

    Providers.update({"fedex": fedex})
except ImportError:
    pass
try:
    import purplship.freight.mappers.ups as ups

    Providers.update({"ups": ups})
except ImportError:
    pass


# Register PurplShip extensions

for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    Providers.update(
        {name: __import__(f"{extensions.__name__}.{name}", fromlist=[name])}
    )
