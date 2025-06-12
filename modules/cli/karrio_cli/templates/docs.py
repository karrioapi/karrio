from jinja2 import Template


EMPTY_FILE_TEMPLATE = Template("")


MODELS_TEMPLATE = Template(
    """
{% for name, cls in classes.items() %}
#### {{ name }}

| Name | Type | Description
| --- | --- | --- |
{% for prop in cls.__attrs_attrs__ %}| `{{ prop.name }}` | {{ prop.type }} | {{ '**required**' if str(prop.default) == 'NOTHING' else '' }}
{% endfor %}
{% endfor %}
"""
)

SETTINGS_TEMPLATE = Template(
    """
{% for k, val in settings.items() %}
#### {{ val['label'] }} Settings `[carrier_name = {{k}}]`

| Name | Type | Description
| --- | --- | --- |
{% for prop in val['Settings'].__attrs_attrs__ %}| `{{ prop.name }}` | {{ prop.type }} | {{ '**required**' if str(prop.default) == 'NOTHING' else '' }}
{% endfor %}
{% endfor %}
"""
)

SERVICES_TEMPLATE = Template(
    """
{% for key, value in service_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
"""
)

SHIPMENT_OPTIONS_TEMPLATE = Template(
    """
{% for key, value in option_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier | Description
| --- | --- | ---
{% for code, spec in value.items() %}| `{{ code }}` | {{ spec.get('key') }} | {{ spec.get('type') }}
{% endfor %}
{% endfor %}
"""
)

PACKAGING_TYPES_TEMPLATE = Template(
    """
{% for key, value in packaging_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Identifier
| --- | ---
{% for code, name in value.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}
"""
)

SHIPMENT_PRESETS_TEMPLATE = Template(
    """
{% for key, value in preset_mappers.items() %}
#### {{ mappers[key]["label"] }}

| Code | Dimensions | Note
| --- | --- | ---
{% for code, dim in value.items() %}{{ format_dimension(code, dim) }}
{% endfor %}
{% endfor %}
"""
)

UTILS_TOOLS_TEMPLATE = Template(
    """
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
"""
)

COUNTRY_INFO_TEMPLATES = Template(
    """
## Countries

| Code | Name
| --- | ---
{% for code, name in countries.items() %}| `{{ code }}` | {{ name }}
{% endfor %}

## States and Provinces

{% for country, states in country_states.items() %}

### {{ countries[country] }}

| Code | Name
| --- | ---
{% for code, name in states.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
{% endfor %}

## Currencies

| Code | Name
| --- | ---
{% for code, name in currencies.items() %}| `{{ code }}` | {{ name }}
{% endfor %}
"""
)

UNITS_TEMPLATES = Template(
    """
## WEIGHT UNITS

| Code | Identifier
| --- | ---
{% for code, name in weight_units.items() %}| `{{ code }}` | {{ name }}
{% endfor %}

## DIMENSION UNITS

| Code | Identifier
| --- | ---
{% for code, name in dimension_units.items() %}| `{{ code }}` | {{ name }}
{% endfor %}

"""
)
