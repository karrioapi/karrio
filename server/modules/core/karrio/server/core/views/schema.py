from jinja2 import Template
from django import conf as django
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg import views, openapi, generators, inspectors

from karrio.server.conf import settings
from karrio.server.core.dataunits import contextual_reference

VERSION = getattr(settings, "VERSION", "")
non_null = lambda items: [i for i in items if i is not None]


def render_schema_description(APP_NAME):
    return f"""
    ## API Reference

    {APP_NAME} is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.

    The {APP_NAME} API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded
    request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

    The {APP_NAME} API differs for every account as we release new versions.
    These docs are customized to your version of the API.


    ## Versioning

    When backwards-incompatible changes are made to the API, a new, dated version is released.
    The current version is `{VERSION}`.

    Read our API changelog and to learn more about backwards compatibility.

    As a precaution, use API versioning to check a new API version before committing to an upgrade.


    ## Environments

    The {APP_NAME} API offer the possibility to create and retrieve certain objects in `test_mode`.
    In development, it is therefore possible to add carrier connections, get live rates,
    buy labels, create trackers and schedule pickups in `test_mode`.


    ## Pagination

    All top-level API resources have support for bulk fetches via "list" API methods. For instance, you can list addresses,
    list shipments, and list trackers. These list API methods share a common structure, taking at least these
    two parameters: limit, and offset.

    {APP_NAME} utilizes offset-based pagination via the offset and limit parameters.
    Both parameters take a number as value (see below) and return objects in reverse chronological order.
    The offset parameter returns objects listed after an index.
    The limit parameter take a limit on the number of objects to be returned from 1 to 100.


    ```json
    {{
        "count": 100,
        "next": "/v1/shipments?limit=25&offset=50",
        "previous": "/v1/shipments?limit=25&offset=25",
        "results": [
            {{ ... }},
        ]
    }}
    ```

    ## Metadata

    Updateable {APP_NAME} objects—including Shipment and Order—have a metadata parameter.
    You can use this parameter to attach key-value data to these {APP_NAME} objects.

    Metadata is useful for storing additional, structured information on an object.
    As an example, you could store your user's full name and corresponding unique identifier
    from your system on a {APP_NAME} Order object.

    Do not store any sensitive information as metadata.

    ## Authentication

    API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.

    Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret
    API keys in publicly accessible areas such as GitHub, client-side code, and so forth.

    Authentication to the API is performed via HTTP Basic Auth. Provide your API token as
    the basic auth username value. You do not need to provide a password.

    ```shell
    $ curl https://instance.api.com/v1/shipments \\
        -u key_xxxxxx:
    # The colon prevents curl from asking for a password.
    ```

    If you need to authenticate via bearer auth (e.g., for a cross-origin request),
    use `-H "Authorization: Token key_xxxxxx"` instead of `-u key_xxxxxx`.

    All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure).
    API requests without authentication will also fail.

    """


def render_reference_descriptions(request):
    refs = contextual_reference(reduced=False)

    def format_preset(preset: dict):
        vals = [
            str(v)
            for v in [
                preset.get("width"),
                preset.get("height"),
                preset.get("length"),
            ]
            if v is not None
        ]

        return f'{" x ".join(vals)} {preset.get("dimension_unit").lower()}'

    return Template(
        """
    ## Carriers

    | Carrier Name | Display Name |
    | ------------ | ------------ |
    {% for carrier, name in carriers.items() -%}{% if carrier != "generic" -%}
    | {{ carrier }} | {{ name }} |
    {% endif -%}{% endfor %}

    ---

    ## Services

    The following service level codes can be used to reference specific rates
    when purchasing shipping labels using single call label creation.

    You can also find all of the possible service levels for each of your carrier
    accounts by using [this endpoint](#operation/&&get_services).


    {% for carrier, services in refs.get("services", {}).items() -%}{% if carrier != "generic" -%}

    ### {{ carriers.get(carrier, "") }}


    | Code         | Service Name |
    | ------------ | ------------ |
    {% for code, name in services.items() -%}
    | {{ code }} | {{ name }} |
    {% endfor %}

    {% endif -%}{% endfor %}

    ---

    ## Parcel Templates

    Use any of the following templates when you ship with special carrier packaging.


    {% for carrier, presets in refs.get("package_presets", {}).items() -%}

    ### {{ carriers.get(carrier, "") }}


    | Code         | Dimensions   |
    | ------------ | ------------ |
    {% for code, preset in presets.items() -%}
    | {{ code }} | {{ format_preset(preset) }} |
    {% endfor %}
    {% endfor %}

    """
    ).render(
        refs=refs,
        format_preset=format_preset,
        carriers={**refs.get("carriers", {}), **refs.get("custom_carriers", {})}
    )


class OpenAPISchemaGenerator(generators.OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""
        tenant = getattr(request, "tenant", None)
        APP_NAME = settings.APP_NAME

        if tenant:
            self.info = openapi.Info(
                title=f"{APP_NAME} API",
                default_version=VERSION,
                description=render_schema_description(APP_NAME),
                contact=openapi.Contact(email=""),
            )

        swagger = super().get_schema(request, public)
        swagger.tags = non_null(
            [
                {
                    "name": "API",
                    "description": """
                API instance metadata and authentication resources.
                """,
                },
                {
                    "name": "Carriers",
                    "description": f"""
                This is an object representing your a {APP_NAME} carrier account connectsions.
                You can retrieve all configured connections available to your {APP_NAME} account.

                The `carrier_id` is a nickname you assign to your connection.
                """,
                },
                {
                    "name": "Addresses",
                    "description": f"""
                This is an object representing your a {APP_NAME} shipping address.
                You can retrieve all addresses related to your {APP_NAME} account.

                Address objects are linked to your shipment history, and can be used for recurring shipping
                to / from the same locations.
                """,
                },
                {
                    "name": "Parcels",
                    "description": f"""
                This is an object representing your a {APP_NAME} shipping parcel.

                Parcel objects are linked to your shipment history, and can be used for recurring shipping
                using the same packaging.
                """,
                },
                {
                    "name": "Customs",
                    "description": f"""
                This is an object representing your a {APP_NAME} shipping customs declaration.
                You can retrieve all customs declarations used historically with your {APP_NAME} account shipments.
                """,
                },
                {
                    "name": "Shipments",
                    "description": f"""
                This is an object representing your a {APP_NAME} shipment.

                A Shipment guides you through process of preparing and purchasing a label for an order.

                A Shipment transitions through multiple statuses throughout its lifetime as the package
                shipped makes its journey to it's destination.
                """,
                },
                {
                    "name": "Documents",
                    "description": f"""
                This is an object representing your a {APP_NAME} document upload record.

                A Document upload record keep traces of shipping trade documents uploaded to carriers
                to fast track customs processing.
                """,
                },
                {
                    "name": "Trackers",
                    "description": f"""
                This is an object representing your a {APP_NAME} shipment tracker.

                A shipment tracker is an object attached to a shipment by it's tracking number.
                The tracker provide the latest tracking status and events associated with a shipment
                """,
                },
                {
                    "name": "Pickups",
                    "description": f"""
                This is an object representing your a {APP_NAME} pickup booking.
                You can retrieve all pickup booked historically for your {APP_NAME} account shipments.
                """,
                },
                {
                    "name": "Proxy",
                    "description": f"""
                In some scenarios, all we need is to send request to a carrier using the {APP_NAME} unified API.

                The Proxy API comes handy for that as it turn {APP_NAME} into a simple middleware that converts and
                validate your request and simply forward it to the shipping carrier server.

                > **Note**
                >
                > When using the proxy API, no objects are created in the {APP_NAME} system.
                """,
                },
                (
                    {
                        "name": "Orders",
                        "description": f"""
                This is an object representing your a {APP_NAME} order.

                You can create {APP_NAME} orders to organize your shipments and ship line items separately.
                """,
                    }
                    if django.settings.ORDERS_MANAGEMENT
                    else None
                ),
                {
                    "name": "Webhooks",
                    "description": f"""
                This is an object representing your a {APP_NAME} webhook.

                You can configure webhook endpoints via the API to be notified about events that happen in your
                {APP_NAME} account.
                """,
                },
                (
                    {
                        "name": "Data",
                        "description": f"""
                    These operations allow you import or export data from your {APP_NAME} account.
                    """,
                    }
                    if django.settings.DATA_IMPORT_EXPORT
                    else None
                ),
                (
                    {
                        "name": "Batches",
                        "description": f"""
                    This is an object representing your a {APP_NAME} batch operation.
                    You can retrieve all batch operations historically for your {APP_NAME} account.
                    """,
                    }
                    if django.settings.DATA_IMPORT_EXPORT
                    else None
                ),
                {
                    "name": "Reference & Enums",
                    "description": render_reference_descriptions(request),
                },
            ]
        )

        return swagger


class SwaggerAutoSchema(inspectors.SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        return openapi.Operation(
            operation.operation_id,
            **{k: v for k, v in operation.items() if k != operation.operation_id},
            **{"x-codeSamples": self.overrides.get("code_examples")},
        )


swagger_info = openapi.Info(
    title=f"{settings.APP_NAME} API",
    default_version=VERSION,
    description=render_schema_description(settings.APP_NAME),
    contact=openapi.Contact(email=""),
)


view = views.get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=OpenAPISchemaGenerator,
)


urlpatterns = [
    re_path(
        r"^shipping-openapi(?P<format>\.json|\.yaml)$",
        view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        settings.OPEN_API_PATH,
        view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
