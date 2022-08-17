import os
import time
import typer
import typing
import string
import pathlib
from rich.progress import Progress, SpinnerColumn, TextColumn
import commands.templates as templates

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

ROOT_DIR = string.Template(f'{BASE_DIR}/sdk/extensions/$id')
TESTS_DIR = string.Template(f'{BASE_DIR}/sdk/extensions/$id/tests/$id')
MAPPERS_DIR = string.Template(f'{BASE_DIR}/sdk/extensions/$id/karrio/mappers/$id')
PROVIDERS_DIR = string.Template(f'{BASE_DIR}/sdk/extensions/$id/karrio/providers/$id')


def add_extension(
    id: str,
    name: str,
    feature: str,
    version: str,
    is_xml_api: bool,
):
    typer.confirm(f'Generate new carrier: "{name}" extension with id "{id}" and features [{feature}]', abort=True)

    features = [f.strip() for f in feature.split(',')]
    context = dict(
        id=id,
        name=name,
        features=features,
        version=version,
        is_xml_api=is_xml_api,
        compact_name=name.strip().replace("-", "").replace("_", "").replace("&", "").replace(" ", ""),
    )

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:

        progress.add_task(description="Processing...", total=None)
        os.makedirs(TESTS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(MAPPERS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(PROVIDERS_DIR.substitute(id=id), exist_ok=True)
        time.sleep(1)

        #project files
        templates.SETUP_TEMPLATE.stream(**context).dump(f'{ROOT_DIR.substitute(id=id)}/setup.py')
        templates.README_TEMPLATE.stream(**context).dump(f'{ROOT_DIR.substitute(id=id)}/README.md')
        templates.PYPROJECT_TEMPLATE.stream(**context).dump(f'{ROOT_DIR.substitute(id=id)}/pyproject.toml')

        # tests files
        templates.TEST_FIXTURE_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/fixture.py')
        templates.TEST_PROVIDER_IMPORTS_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/__init__.py')
        templates.TEST_IMPORTS_TEMPLATE.stream(**context).dump(f'{ROOT_DIR.substitute(id=id)}/tests/__init__.py')

        # mappers files
        templates.MAPPER_TEMPLATE.stream(**context).dump(f'{MAPPERS_DIR.substitute(id=id)}/mapper.py')
        templates.MAPPER_PROXY_TEMPLATE.stream(**context).dump(f'{MAPPERS_DIR.substitute(id=id)}/proxy.py')
        templates.MAPPER_SETTINGS_TEMPLATE.stream(**context).dump(f'{MAPPERS_DIR.substitute(id=id)}/settings.py')
        templates.MAPPER_METADATA_TEMPLATE.stream(**context).dump(f'{MAPPERS_DIR.substitute(id=id)}/__init__.py')

        # providers files
        templates.PROVIDER_ERROR_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/error.py')
        templates.PROVIDER_UNITS_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/units.py')
        templates.PROVIDER_UTILS_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/utils.py')
        templates.PROVIDER_IMPORTS_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/__init__.py')


        if "address" in features:
            templates.TEST_ADDRESS_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/address.py')

            templates.PROVIDER_ADDRESS_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/address.py')

        if "rating" in features:
            templates.TEST_RATE_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/rate.py')

            templates.PROVIDER_RATE_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/rate.py')

        if "tracking" in features:
            templates.TEST_TRACKING_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/tracking.py')

            templates.PROVIDER_TRACKING_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/tracking.py')

        if "document" in features:
            templates.TEST_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/document.py')

            templates.PROVIDER_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/document.py')

        if "shipping" in features:
            templates.TEST_SHIPMENT_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/shipment.py')

            os.makedirs(f'{PROVIDERS_DIR.substitute(id=id)}/shipment', exist_ok=True)
            templates.PROVIDER_SHIPMENT_CANCEL_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/shipment/cancel.py')
            templates.PROVIDER_SHIPMENT_CREATE_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/shipment/create.py')
            templates.PROVIDER_SHIPMENT_IMPORTS_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/shipment/__init__.py')

        if "pickup" in features:
            templates.TEST_PICKUP_TEMPLATE.stream(**context).dump(f'{TESTS_DIR.substitute(id=id)}/pickup.py')

            os.makedirs(f'{PROVIDERS_DIR.substitute(id=id)}/pickup', exist_ok=True)
            templates.PROVIDER_PICKUP_CANCEL_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/pickup/cancel.py')
            templates.PROVIDER_PICKUP_CREATE_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/pickup/create.py')
            templates.PROVIDER_PICKUP_UPDATE_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/pickup/update.py')
            templates.PROVIDER_PICKUP_IMPORTS_TEMPLATE.stream(**context).dump(f'{PROVIDERS_DIR.substitute(id=id)}/pickup/__init__.py')

    typer.echo("Done!")

def add_features(extension: str, feature: typing.List[str]):
    pass
