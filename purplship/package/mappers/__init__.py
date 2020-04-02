from typing import Dict, Any
import pkgutil
import purplship.extension.mappers as extensions

Providers: Dict[str, Any] = {}

try:
    import purplship.package.mappers.australiapost as australiapost

    Providers.update({"australiapost": australiapost})
except ImportError:
    pass
try:
    import purplship.package.mappers.canadapost as canadapost

    Providers.update({"canadapost": canadapost})
except ImportError:
    pass
try:
    import purplship.package.mappers.dhl as dhl

    Providers.update({"dhl": dhl})
except ImportError:
    pass
try:
    import purplship.package.mappers.fedex as fedex

    Providers.update({"fedex": fedex})
except ImportError:
    pass
try:
    import purplship.package.mappers.purolator as purolator

    Providers.update({"purolator": purolator})
except ImportError:
    pass
try:
    import purplship.package.mappers.ups as ups

    Providers.update({"ups": ups})
except ImportError:
    pass
try:
    import purplship.package.mappers.usps as usps

    Providers.update({"usps": usps})
except ImportError:
    pass
try:
    import purplship.package.mappers.sendle as sendle

    Providers.update({"sendle": sendle})
except ImportError:
    pass


# Register PurplShip extensions

for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    Providers.update(
        {name: __import__(f"{extensions.__name__}.{name}", fromlist=[name])}
    )
