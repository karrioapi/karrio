import click
import inspect
import pydoc
from jinja2 import Template
from purplship.references import collect_providers_data, collect_references
import purplship.core.utils as utils

PROVIDERS_DATA = collect_providers_data()
REFERENCES = collect_references()

MODELS_TEMPLATE = Template('''
{% for name, cls in classes.items() %}
#### {{ name }}

| Name | Type | Description 
| --- | --- | --- |
{% for prop in cls.__attrs_attrs__ %}| `{{ prop.name }}` | {{ prop.type }} | {{ '**required**' if str(prop.default) == 'NOTHING' else '' }}
{% endfor %}
{% endfor %}
''')

SETTINGS_TEMPLATE = Template('''
{% for name, cls in settings.items() %}
#### {{ name }} Settings

| Name | Type | Description 
| --- | --- | --- |
{% for prop in cls.__attrs_attrs__ %}| `{{ prop.name }}` | {{ prop.type }} | {{ '**required**' if str(prop.default) == 'NOTHING' else '' }}
{% endfor %}
{% endfor %}
''')

SERVICES_TEMPLATE = Template('''
{% for key, value in service_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
''')

SHIPMENT_OPTIONS_TEMPLATE = Template('''
{% for key, value in option_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
''')

PACKAGING_TYPES_TEMPLATE = Template('''
{% for key, value in packaging_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
''')

SHIPMENT_PRESETS_TEMPLATE = Template('''
{% for key, value in preset_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Dimensions | Note
| --- | --- | ---
{% for code, dim in value.items() %}{{ format_dimension(code, dim) }}
{% endfor %}
{% endfor %}
''')

UTILS_TOOLS_TEMPLATE = Template('''
{% for tool, import in utils %}
- `{{ tool.__name__ }}`

Usage: 
```python
{{ import }}
```

```text
{{ doc(tool) }}
```

{% endfor %}
''')


def doc(entity):
    return pydoc.render_doc(entity, renderer=pydoc.plaintext)


def format_dimension(code, dim):
    return f'| `{ code }` | { f" x ".join([str(d) for d in dim.values() if isinstance(d, float)]) } | { f" x ".join([k for k in dim.keys() if isinstance(dim[k], float)]) }'


@click.group()
def cli():
    pass


@cli.command()
def generate_shipment_options():
    click.echo(SHIPMENT_OPTIONS_TEMPLATE.render(option_mappers=REFERENCES['options'], mappers=PROVIDERS_DATA))


@cli.command()
def generate_package_presets():
    click.echo(SHIPMENT_PRESETS_TEMPLATE.render(preset_mappers=REFERENCES['package_presets'], mappers=PROVIDERS_DATA, format_dimension=format_dimension))


@cli.command()
def generate_services():
    click.echo(SERVICES_TEMPLATE.render(service_mappers=REFERENCES['services'], mappers=PROVIDERS_DATA))


@cli.command()
def generate_packaging_types():
    click.echo(PACKAGING_TYPES_TEMPLATE.render(packaging_mappers=REFERENCES['packaging_types'], mappers=PROVIDERS_DATA))


@cli.command()
def generate_models():
    import purplship.core.models as m
    classes = {i: t for i, t in inspect.getmembers(m) if inspect.isclass(t)}
    docstr = MODELS_TEMPLATE.render(
        classes=classes,
        str=str
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
            f"| `{cls}` |", f"| [{cls}](#{cls.lower()}) |"
        ).replace(
            f"[{cls}] ", f"[[{cls}](#{cls.lower()})] "
        )

    click.echo(docstr)


@cli.command()
def generate_settings():
    settings = {v['label']: v['Settings'] for k, v in PROVIDERS_DATA.items() if v.get('Settings') is not None}
    docstr = SETTINGS_TEMPLATE.render(
        settings=settings,
        str=str
    )

    click.echo(docstr)


@cli.command()
def generate_utilities_info():
    utilities = [
        (utils.DP, 'from purplship.core.utils import DP'),
        (utils.XP, 'from purplship.core.utils import XP'),
        (utils.DF, 'from purplship.core.utils import DF'),
        (utils.SF, 'from purplship.core.utils import SF'),
        (utils.helpers, 'from purplship.core.utils import [function]'),
    ]
    click.echo(UTILS_TOOLS_TEMPLATE.render(utils=utilities, doc=doc))


if __name__ == '__main__':
    cli()
