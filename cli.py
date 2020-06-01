import click
import inspect
from jinja2 import Template

template = Template('''
{% for name, cls in classes.items() %}
- <a name="{{ name }}"></a> {{ name }}

    | Name | Type | Description 
    | --- | --- | --- |
{% for prop, typedef in cls.__annotations__.items() %}    | `{{ prop }}` | {{ typedef }} | 
{% endfor %}

{% endfor %}
''')


@click.group()
def cli():
    pass


@cli.command()
def generate_models():
    import purplship.core.models as m
    classes = {i: t for i, t in inspect.getmembers(m) if inspect.isclass(t)}
    docstr = template.render(
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
