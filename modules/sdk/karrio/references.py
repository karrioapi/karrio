"""Karrio Interface references."""

import attr
import pydoc
import typing
import pkgutil

import karrio.lib as lib
import karrio.mappers as mappers
import karrio.core.units as units
import karrio.core.metadata as metadata


PROVIDERS = None
PROVIDERS_DATA = None
REFERENCES = None
COMMON_FIELDS = [
    "id",
    "test_mode",
    "carrier_id",
    "account_country_code",
    "metadata",
    "config",
    # "services",
]


def import_extensions() -> typing.Dict[str, metadata.Metadata]:
    global PROVIDERS
    modules = {
        name: __import__(f"{mappers.__name__}.{name}", fromlist=[name])
        for _, name, _ in pkgutil.iter_modules(mappers.__path__)
    }

    PROVIDERS = {
        carrier_name: module.METADATA for carrier_name, module in modules.items()
    }

    return PROVIDERS


def collect_providers_data() -> typing.Dict[str, dict]:
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


def detect_capabilities(proxy_methods: typing.List[str]) -> typing.List[str]:
    r = set([units.CarrierCapabilities.map_capability(prop) for prop in proxy_methods])

    return list(r)


def detect_proxy_methods(proxy_type: object) -> typing.List[str]:
    return [
        prop
        for prop in proxy_type.__dict__.keys()
        if "_" not in prop[0] and prop != "settings"
    ]


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
        key: {c.name: dict(code=c.value.code, type=parse_type(c.value.type)) for c in list(mapper["options"])}  # type: ignore
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get("options") is not None
    }
    connection_configs = {
        key: {
            c.name: lib.to_dict(
                dict(
                    name=c.name,
                    code=c.value.code,
                    required=False,
                    type=parse_type(c.value.type),
                    enum=lib.identity(
                        None
                        if "enum" not in str(c.value.type).lower()
                        else [c.name for c in c.value.type]
                    ),
                )
            )
            for c in list(mapper["connection_configs"])
        }
        for key, mapper in PROVIDERS_DATA.items()
        if mapper.get("connection_configs") is not None
    }  # type: ignore
    connection_fields = {
        mapper["id"]: {
            _.name: lib.to_dict(
                dict(
                    name=_.name,
                    type=parse_type(_.type),
                    required="NOTHING" in str(_.default),
                    default=lib.identity(
                        lib.to_dict(lib.to_json(_.default))
                        if ("NOTHING" not in str(_.default))
                        else None
                    ),
                    enum=lib.identity(
                        None
                        if "enum" not in str(_.type).lower()
                        else [c.name for c in _.type]
                    ),
                )
            )
            for _ in mapper["Settings"].__attrs_attrs__
            if (_.name not in COMMON_FIELDS)
            or (mapper.get("has_intl_accounts") and _.name == "account_country_code")
        }
        for _, mapper in PROVIDERS_DATA.items()
        if mapper.get("Settings") is not None
    }  # type: ignore

    REFERENCES = {
        "countries": {c.name: c.value for c in list(units.Country)},
        "currencies": {c.name: c.value for c in list(units.Currency)},
        "weight_units": {c.name: c.value for c in list(units.WeightUnit)},
        "dimension_units": {c.name: c.value for c in list(units.DimensionUnit)},
        "states": {
            c.name: {s.name: s.value for s in list(c.value)}  # type: ignore
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
        "connection_fields": connection_fields,
        "connection_configs": connection_configs,
        "carrier_capabilities": {
            key: detect_capabilities(detect_proxy_methods(mapper["Proxy"]))
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("Proxy") is not None
        },
        "packaging_types": {
            key: {c.name: c.value for c in list(mapper["packaging_types"])}  # type: ignore
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("packaging_types") is not None
        },
        "package_presets": {
            key: {c.name: lib.to_dict(c.value) for c in list(mapper["package_presets"])}  # type: ignore
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
            key: lib.to_dict(mapper.get("service_levels"))
            for key, mapper in PROVIDERS_DATA.items()
            if mapper.get("service_levels") is not None
        },
    }

    return REFERENCES


def get_carrier_capabilities(carrier_name) -> typing.List[str]:
    proxy_class = pydoc.locate(f"karrio.mappers.{carrier_name}.Proxy")
    proxy_methods = detect_proxy_methods(proxy_class)
    return detect_capabilities(proxy_methods)


def parse_type(_type: type) -> str:
    _name = getattr(_type, "__name__", None)

    if _name is not None and _name == "bool":
        return "boolean"
    if _name is not None and _name == "str":
        return "string"
    if _name is not None and (_name == "int" or "to_int" in _name):
        return "integer"
    if _name is not None and _name == "float":
        return "float"
    if _name is not None and "money" in _name:
        return "float"
    if "Address" in str(_type):
        return "Address"
    if "enum" in str(_type):
        return "string"
    if _name is not None and ("list" in _name or "List" in _name):
        return "list"
    if _name is not None and ("dict" in _name or "Dict" in _name):
        return "object"

    return str(_type)
