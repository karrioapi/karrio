import click
import inspect
from jinja2 import Template
from purplship.core.utils import to_dict

MODELS_TEMPLATE = Template('''
{% for name, cls in classes.items() %}
- <a name="{{ name }}"></a> {{ name }}
    | Name | Type | Description 
    | --- | --- | --- |
{% for prop, typedef in cls.__annotations__.items() %}    | `{{ prop }}` | {{ typedef }} | 
{% endfor %}
{% endfor %}
''')

SERVICES_TEMPLATE = Template('''
{% for key, value in service_mappers.items() %}
- <a name="services-{{ key }}"></a> {{ mappers[key]["label"] }}
    Code | Identifier
    --- | ---
{% for code, name in value.items() %}    | `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
''')

SHIPMENT_OPTIONS_TEMPLATE = Template('''
{% for key, value in option_mappers.items() %}
- <a name="options-{{ key }}"></a> {{ mappers[key]["label"] }}
    Code | Identifier
    --- | ---
{% for code, name in value.items() %}    | `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
''')

PACKAGING_TYPES_TEMPLATE = Template('''
{% for key, value in option_mappers.items() %}
- <a name="options-{{ key }}"></a> {{ mappers[key]["label"] }}
    Code | Identifier
    --- | ---
{% for code, name in value.items() %}    | `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
''')

SHIPMENT_PRESETS_TEMPLATE = Template('''
{% for key, value in preset_mappers.items() %}
- <a name="presets-{{ key }}"></a> {{ mappers[key]["label"] }}
    Code | Dimensions | Note
    --- | --- | ---
{% for code, dim in value.items() %}    {{ format_dimension(code, dim) }}
{% endfor %}
{% endfor %}
''')


def format_dimension(code, dim):
    return f'| `{ code }` | { f" x ".join([str(d) for d in dim.values() if isinstance(d, float)]) } | { f" x ".join([k for k in dim.keys() if isinstance(dim[k], float)]) }'


def import_pkg(pkg: str):
    *_, carrier, name = pkg.split(".")
    return __import__(pkg, fromlist=[name])


PACKAGE_MAPPERS = {
    'purplship': {
        'label': "Multi-carrier (Purplship)",
        'package': import_pkg('purplship.core.units'),
        'packagingTypes': "PackagingUnit"
    },
    'canadapost': {
        'label': "Canada Post",
        'package': import_pkg('purplship.providers.canadapost.units'),
        'services': "ServiceType",
        'options': "OptionCode",
        'packagePresets': "PackagePresets"
    },
    'canpar': {
        'label': "Canpar",
        'package': import_pkg('purplship.providers.canpar.units'),
        'services': "Service",
        'options': "Option"
    },
    'dhl_express': {
        'label': "DHL Express",
        'package': import_pkg('purplship.providers.dhl_express.units'),
        'services': "Product",
        'options': "SpecialServiceCode",
        'packagePresets': "PackagePresets",
        'packagingTypes': "DCTPackageType"
    },
    'fedex': {
        'label': "FedEx",
        'package': import_pkg('purplship.providers.fedex.units'),
        'services': "ServiceType",
        'options': "SpecialServiceType",
        'packagePresets': "PackagePresets",
        'packagingTypes': "PackagingType"
    },
    'purolator': {
        'label': "Purolator",
        'package': import_pkg('purplship.providers.purolator.units'),
        'services': "Product",
        'options': "Service",
        'packagePresets': "PackagePresets",
        'packagingTypes': "PackagingType"
    },
    'ups': {
        'label': "UPS",
        'package': import_pkg('purplship.providers.ups.units'),
        'services': "ShippingServiceCode",
        'options': "ServiceOption",
        'packagePresets': "PackagePresets",
        'packagingTypes': "RatingPackagingType"
    }
}


@click.group()
def cli():
    pass


@cli.command()
def generate_shipment_options():
    option_mappers = {
        key: {c.name: c.value for c in list(getattr(mapper['package'], mapper['options']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if mapper.get('options') is not None
    }
    click.echo(SHIPMENT_OPTIONS_TEMPLATE.render(option_mappers=option_mappers, mappers=PACKAGE_MAPPERS))


@cli.command()
def generate_package_presets():
    preset_mappers = {
        key: {c.name: to_dict(c.value) for c in list(getattr(mapper['package'], mapper['packagePresets']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if mapper.get('packagePresets') is not None
    }
    click.echo(SHIPMENT_PRESETS_TEMPLATE.render(preset_mappers=preset_mappers, mappers=PACKAGE_MAPPERS, format_dimension=format_dimension))


@cli.command()
def generate_services():
    service_mappers = {
        key: {c.name: c.value for c in list(getattr(mapper['package'], mapper['services']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if mapper.get('services') is not None
    }
    click.echo(SERVICES_TEMPLATE.render(service_mappers=service_mappers, mappers=PACKAGE_MAPPERS))


@cli.command()
def generate_packaging_types():
    service_mappers = {
        key: {c.name: c.value for c in list(getattr(mapper['package'], mapper['packagingTypes']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if mapper.get('packagingTypes') is not None
    }
    click.echo(SERVICES_TEMPLATE.render(service_mappers=service_mappers, mappers=PACKAGE_MAPPERS))


@cli.command()
def generate_models():
    import purplship.core.models as m
    classes = {i: t for i, t in inspect.getmembers(m) if inspect.isclass(t)}
    docstr = MODELS_TEMPLATE.render(
        classes=classes
    ).replace(
        "purplship.core.models.", ""
    ).replace(
        "typing.", ""
    ).replace(
        "<class '", "`"
    ).replace(
        "'>", "`"
    ).replace(
        "Dict", "`dict`"
    )

    for name, _ in classes.items():
        cls = name.strip()
        docstr = docstr.replace(
            f"| `{cls}` |", f"| [{cls}](#{cls}) |"
        ).replace(
            f"[{cls}] ", f"[[{cls}](#{cls})] "
        )

    click.echo(docstr)


if __name__ == '__main__':
    cli()
