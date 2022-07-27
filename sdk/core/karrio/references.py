"""

"""
import attr
import pkgutil
from typing import Dict, List

import karrio.mappers as mappers
import karrio.core.units as units
from karrio.core.utils import DP
from karrio.core.metadata import Metadata


PROVIDERS = None
PROVIDERS_DATA = None
REFERENCES = None


def import_extensions() -> Dict[str, Metadata]:
    global PROVIDERS
    modules = {
        name: __import__(f"{mappers.__name__}.{name}", fromlist=[name])
        for _, name, _ in pkgutil.iter_modules(mappers.__path__)
    }

    PROVIDERS = {
        carrier_name: module.METADATA for carrier_name, module in modules.items()
    }

    return PROVIDERS


def collect_providers_data() -> Dict[str, dict]:
    global PROVIDERS_DATA
    if PROVIDERS is None:
        import_extensions()

    PROVIDERS_DATA = {
        "universal": dict(
            label="Multi-carrier (karrio)",
            packaging_types=units.PackagingUnit,
            options=units.ShippingOption,
        ),
        **{
            carrier_name: attr.asdict(metadata)
            for carrier_name, metadata in PROVIDERS.items()
        },
    }

    return PROVIDERS_DATA


def detect_capabilities(proxy_type: object) -> List[str]:
    return [prop for prop in proxy_type.__dict__.keys() if "_" not in prop[0]]


def collect_references() -> dict:
    global REFERENCES
    if PROVIDERS_DATA is None:
        collect_providers_data()

    services = {
        key: {c.name: c.value for c in list(mapper["services"])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get("services") is not None
    }
    options = {
        key: {c.name: dict(code=c.value.code) for c in list(mapper["options"])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get("options") is not None
    }

    REFERENCES = {
        "countries": {c.name: c.value for c in list(units.Country)},
        "currencies": {c.name: c.value for c in list(units.Currency)},
        "weight_units": {c.name: c.value for c in list(units.WeightUnit)},
        "dimension_units": {c.name: c.value for c in list(units.DimensionUnit)},
        "states": {
            c.name: {s.name: s.value for s in list(c.value)}
            for c in list(units.CountryState)
        },
        "payment_types": {c.name: c.value for c in list(units.PaymentType)},
        "customs_content_type": {
            c.name: c.value for c in list(units.CustomsContentType)
        },
        "incoterms": {c.name: c.value for c in list(units.Incoterm)},
        "carriers": {
            carrier_name: metadata.label for carrier_name, metadata in PROVIDERS.items()
        },
        "carrier_hubs": {
            carrier_name: metadata.label
            for carrier_name, metadata in PROVIDERS.items()
            if metadata.is_hub
        },
        "services": services,
        "options": options,
        "carrier_capabilities": {
            key: detect_capabilities(mapper["Proxy"])
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("Proxy") is not None
        },
        "packaging_types": {
            key: {c.name: c.value for c in list(mapper["packaging_types"])}  # type: ignore
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("packaging_types") is not None
        },
        "package_presets": {
            key: {c.name: DP.to_dict(c.value) for c in list(mapper["package_presets"])}  # type: ignore
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("package_presets") is not None
        },
        "option_names": {
            name: {key: key.upper().replace("_", " ") for key, _ in value.items()}
            for name, value in options.items()
        },
        "service_names": {
            name: {key: key.upper().replace("_", " ") for key, _ in value.items()}
            for name, value in services.items()
        },
        "service_levels": {
            key: DP.to_dict(mapper.get("service_levels"))
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("service_levels") is not None
        },
    }

    return REFERENCES
