"""

"""
import attr
import pkgutil
from typing import Dict

import purplship.mappers as mappers
from purplship.core.utils import DP
from purplship.core.metadata import Metadata
from purplship.core.units import Country, Currency, CountryState, PaymentType, PackagingUnit


def import_extensions() -> Dict[str, Metadata]:
    modules = {
        name: __import__(f"{mappers.__name__}.{name}", fromlist=[name])
        for _, name, _ in pkgutil.iter_modules(mappers.__path__)
    }

    return {
        carrier_name: module.METADATA for carrier_name, module in modules.items()
    }


PROVIDERS = import_extensions()

PROVIDERS_DATA = {
    'universal': dict(
        label="Multi-carrier (purplship)",
        packaging_types=PackagingUnit
    ),
    **{carrier_name: attr.asdict(metadata) for carrier_name, metadata in PROVIDERS.items()},
}

REFERENCES = {
    "countries": {c.name: c.value for c in list(Country)},
    "currencies": {c.name: c.value for c in list(Currency)},
    "states": {c.name: {s.name: s.value for s in list(c.value)} for c in list(CountryState)},
    "payment_types": {c.name: c.value for c in list(PaymentType)},
    "carriers": {carrier_name: metadata.label for carrier_name, metadata in PROVIDERS.items()},
    "services": {
        key: {c.name: c.value for c in list(mapper['services'])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get('services') is not None
    },
    "options": {
        key: {c.name: c.value for c in list(mapper['options'])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get('options') is not None
    },
    "packaging_types": {
        key: {c.name: c.value for c in list(mapper['packaging_types'])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get('packaging_types') is not None
    },
    "package_presets": {
        key: {c.name: DP.to_dict(c.value) for c in list(mapper['package_presets'])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get('package_presets') is not None
    }
}
