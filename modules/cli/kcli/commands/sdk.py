import os
import time
import typer
import string
import pathlib
from rich.progress import Progress, SpinnerColumn, TextColumn
import kcli.common.templates as templates
import kcli.common.utils as utils
import typing
import datetime


def _add_extension(
    id: str,
    name: str,
    feature: str,
    version: str,
    is_xml_api: bool,
    path: str,
):
    # Resolve the provided path
    base_dir = pathlib.Path(path).resolve()

    # Create full path for confirmation
    full_path = base_dir / id

    features = [f.strip() for f in feature.split(",")]
    context = dict(
        id=id,
        name=name,
        features=features,
        version=version,
        is_xml_api=is_xml_api,
        compact_name=name.strip()
        .replace("-", "")
        .replace("_", "")
        .replace("&", "")
        .replace(" ", ""),
    )

    # Update the directory templates with the base directory
    root_dir = full_path
    schemas_dir = root_dir / "schemas"
    tests_dir = root_dir / "tests" / id
    mappers_dir = root_dir / "karrio" / "mappers" / id
    providers_dir = root_dir / "karrio" / "providers" / id
    schema_datatypes_dir = root_dir / "karrio" / "schemas" / id

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        os.makedirs(tests_dir, exist_ok=True)
        os.makedirs(schemas_dir, exist_ok=True)
        os.makedirs(mappers_dir, exist_ok=True)
        os.makedirs(providers_dir, exist_ok=True)
        os.makedirs(schema_datatypes_dir, exist_ok=True)
        time.sleep(1)

        # project files
        templates.SETUP_TEMPLATE.stream(**context).dump(
            f"{root_dir}/setup.py"
        )
        templates.README_TEMPLATE.stream(**context).dump(
            f"{root_dir}/README.md"
        )
        (
            templates.XML_GENERATE_TEMPLATE
            if is_xml_api
            else templates.JSON_GENERATE_TEMPLATE
        ).stream(**context).dump(f"{root_dir}/generate")

        # schema files
        (
            templates.XML_SCHEMA_TEMPLATE
            if is_xml_api
            else templates.JSON_SCHEMA_TEMPLATE
        ).stream(**context).dump(
            f"{schemas_dir}/error_response.{'xsd' if is_xml_api else 'json'}"
        )
        templates.EMPTY_FILE_TEMPLATE.stream(**context).dump(
            f"{schema_datatypes_dir}/__init__.py"
        )

        # tests files
        templates.TEST_FIXTURE_TEMPLATE.stream(**context).dump(
            f"{tests_dir}/fixture.py"
        )
        templates.TEST_PROVIDER_IMPORTS_TEMPLATE.stream(**context).dump(
            f"{tests_dir}/__init__.py"
        )
        templates.TEST_IMPORTS_TEMPLATE.stream(**context).dump(
            f"{root_dir}/tests/__init__.py"
        )

        # mappers files
        templates.MAPPER_TEMPLATE.stream(**context).dump(
            f"{mappers_dir}/mapper.py"
        )
        templates.MAPPER_PROXY_TEMPLATE.stream(**context).dump(
            f"{mappers_dir}/proxy.py"
        )
        templates.MAPPER_SETTINGS_TEMPLATE.stream(**context).dump(
            f"{mappers_dir}/settings.py"
        )
        templates.MAPPER_METADATA_TEMPLATE.stream(**context).dump(
            f"{mappers_dir}/__init__.py"
        )

        # providers files
        templates.PROVIDER_ERROR_TEMPLATE.stream(**context).dump(
            f"{providers_dir}/error.py"
        )
        templates.PROVIDER_UNITS_TEMPLATE.stream(**context).dump(
            f"{providers_dir}/units.py"
        )
        templates.PROVIDER_UTILS_TEMPLATE.stream(**context).dump(
            f"{providers_dir}/utils.py"
        )
        templates.PROVIDER_IMPORTS_TEMPLATE.stream(**context).dump(
            f"{providers_dir}/__init__.py"
        )

        if "address" in features:
            templates.TEST_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_address.py"
            )

            templates.PROVIDER_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/address.py"
            )

        if "rating" in features:
            templates.TEST_RATE_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_rate.py"
            )

            templates.PROVIDER_RATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/rate.py"
            )

        if "tracking" in features:
            templates.TEST_TRACKING_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_tracking.py"
            )

            templates.PROVIDER_TRACKING_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/tracking.py"
            )

        if "document" in features:
            templates.TEST_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_document.py"
            )

            templates.PROVIDER_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/document.py"
            )

        if "manifest" in features:
            templates.TEST_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_manifest.py"
            )

            templates.PROVIDER_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/manifest.py"
            )

        if "shipping" in features:
            templates.TEST_SHIPMENT_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_shipment.py"
            )

            os.makedirs(f"{providers_dir}/shipment", exist_ok=True)
            templates.PROVIDER_SHIPMENT_CANCEL_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/shipment/cancel.py"
            )
            templates.PROVIDER_SHIPMENT_CREATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/shipment/create.py"
            )
            templates.PROVIDER_SHIPMENT_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/shipment/__init__.py"
            )

        if "pickup" in features:
            templates.TEST_PICKUP_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_pickup.py"
            )

            os.makedirs(f"{providers_dir}/pickup", exist_ok=True)
            templates.PROVIDER_PICKUP_CANCEL_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/cancel.py"
            )
            templates.PROVIDER_PICKUP_CREATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/create.py"
            )
            templates.PROVIDER_PICKUP_UPDATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/update.py"
            )
            templates.PROVIDER_PICKUP_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/__init__.py"
            )

    typer.echo("Done!")


def _add_features(
    id: str,
    name: str,
    feature: str,
    is_xml_api: bool,
    path: str,
):
    # Resolve the provided path
    base_dir = pathlib.Path(path).resolve()

    # Create full path for confirmation
    full_path = base_dir / id

    features = [f.strip() for f in feature.split(",")]
    context = dict(
        id=id,
        name=name,
        features=features,
        is_xml_api=is_xml_api,
        compact_name=name.strip()
        .replace("-", "")
        .replace("_", "")
        .replace("&", "")
        .replace(" ", ""),
    )

    # Update the directory templates with the base directory
    root_dir = full_path
    schemas_dir = root_dir / "schemas"
    tests_dir = root_dir / "tests" / id
    mappers_dir = root_dir / "karrio" / "mappers" / id
    providers_dir = root_dir / "karrio" / "providers" / id
    schema_datatypes_dir = root_dir / "karrio" / "schemas" / id

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        os.makedirs(tests_dir, exist_ok=True)
        os.makedirs(schemas_dir, exist_ok=True)
        os.makedirs(mappers_dir, exist_ok=True)
        os.makedirs(providers_dir, exist_ok=True)
        os.makedirs(schema_datatypes_dir, exist_ok=True)
        time.sleep(1)

        if "address" in features:
            templates.TEST_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_address.py"
            )

            templates.PROVIDER_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/address.py"
            )

        if "rating" in features:
            templates.TEST_RATE_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_rate.py"
            )

            templates.PROVIDER_RATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/rate.py"
            )

        if "tracking" in features:
            templates.TEST_TRACKING_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_tracking.py"
            )

            templates.PROVIDER_TRACKING_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/tracking.py"
            )

        if "document" in features:
            templates.TEST_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_document.py"
            )

            templates.PROVIDER_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/document.py"
            )

        if "manifest" in features:
            templates.TEST_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_manifest.py"
            )

            templates.PROVIDER_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/manifest.py"
            )

        if "shipping" in features:
            templates.TEST_SHIPMENT_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_shipment.py"
            )

            os.makedirs(f"{providers_dir}/shipment", exist_ok=True)
            templates.PROVIDER_SHIPMENT_CANCEL_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/shipment/cancel.py"
            )
            templates.PROVIDER_SHIPMENT_CREATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/shipment/create.py"
            )
            templates.PROVIDER_SHIPMENT_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/shipment/__init__.py"
            )

        if "pickup" in features:
            templates.TEST_PICKUP_TEMPLATE.stream(**context).dump(
                f"{tests_dir}/test_pickup.py"
            )

            os.makedirs(f"{providers_dir}/pickup", exist_ok=True)
            templates.PROVIDER_PICKUP_CANCEL_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/cancel.py"
            )
            templates.PROVIDER_PICKUP_CREATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/create.py"
            )
            templates.PROVIDER_PICKUP_UPDATE_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/update.py"
            )
            templates.PROVIDER_PICKUP_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{providers_dir}/pickup/__init__.py"
            )

    typer.echo("Done!")


app = typer.Typer()


@app.command()
def add_extension(
    path: str = typer.Option(..., "--path", "-p", help="Path where the extension will be created"),
    carrier_slug: str = typer.Option(
        ...,
        prompt=True,
        help="The unique identifier for the carrier (e.g., dhl_express, ups, fedex, canadapost)"
    ),
    display_name: str = typer.Option(
        ...,
        prompt=True,
        help="The human-readable name for the carrier (e.g., DHL, UPS, FedEx, Canada Post)"
    ),
    features: typing.Optional[str] = typer.Option(
        ", ".join(utils.DEFAULT_FEATURES), prompt=True
    ),
    version: typing.Optional[str] = typer.Option(
        f"{datetime.datetime.now().strftime('%Y.%-m')}", prompt=True
    ),
    is_xml_api: typing.Optional[bool] = typer.Option(False, prompt="Is XML API?"),
):
    # Resolve the provided path for confirmation
    full_path = pathlib.Path(path).resolve() / carrier_slug.lower()

    confirmation_text = (
        f"\nGenerate new carrier extension with:\n"
        f"  Name:     {display_name}\n"
        f"  Alias:    {carrier_slug}\n"
        f"  Features: [{features}]\n"
        f"  Path:     {full_path}\n"
    )

    typer.echo(confirmation_text)
    typer.confirm("Do you want to proceed?", abort=True)

    _add_extension(
        carrier_slug.lower(),
        display_name,
        features,
        version,
        is_xml_api,
        path,
    )


@app.command()
def add_features(
    carrier_slug: str = typer.Option(
        ...,
        prompt=True,
        help="The unique identifier for the carrier (e.g., dhl_express, ups, fedex, canadapost)"
    ),
    display_name: str = typer.Option(
        ...,
        prompt=True,
        help="The human-readable name for the carrier (e.g., DHL, UPS, FedEx, Canada Post)"
    ),
    features: typing.Optional[str] = typer.Option(
        ", ".join(utils.DEFAULT_FEATURES), prompt=True
    ),
    is_xml_api: typing.Optional[bool] = typer.Option(False, prompt="Is XML API?"),
    path: str = typer.Option(..., "--path", "-p", help="Path where the features will be created"),
):
    # Resolve the provided path for confirmation
    full_path = pathlib.Path(path).resolve() / carrier_slug.lower()

    confirmation_text = (
        f"\nBootstrap features for carrier extension with:\n"
        f"  Name:     {display_name}\n"
        f"  ID:       {carrier_slug}\n"
        f"  Features: [{features.replace(',', ', ')}]\n"
        f"  Path:     {full_path}\n"
    )

    typer.echo(confirmation_text)
    typer.confirm("Do you want to proceed?", abort=True)

    features = features.split(",")
    features = [feature.strip() for feature in features]
    _add_features(carrier_slug, display_name, ",".join(features), is_xml_api, path)
