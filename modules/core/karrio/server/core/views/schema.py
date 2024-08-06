import jinja2
import django.conf as django
import drf_spectacular.views as views
import rest_framework.response as response

import django.urls as urls
import karrio.server.conf as conf
import karrio.server.core.dataunits as dataunits

VERSION = getattr(django.settings, "VERSION", "")
non_null = lambda items: [i for i in items if i is not None]
RedocView = views.SpectacularRedocView.as_view(
    url_name="shipping-openapi",
    template_name="openapi/openapi.html",
)


class ShippingOpenAPIView(views.SpectacularAPIView):
    def _get_schema_response(self, request):
        version = (
            self.api_version or request.version or self._get_version_parameter(request)
        )
        generator = self.generator_class(
            urlconf=self.urlconf, api_version=version, patterns=self.patterns
        )
        data = generator.get_schema(request=request, public=self.serve_public)

        data["tags"] = render_tags(request, conf.settings.APP_NAME)
        data["components"]["securitySchemes"] = {
            k: v
            for k, v in data["components"]["securitySchemes"].items()
            if k in ["JWT", "OAuth2", "Token", "TokenBasic"]
        }
        data["info"] = dict(
            description=render_schema_description(conf.settings.APP_NAME),
            title=f"{conf.settings.APP_NAME} API",
            version=conf.settings.VERSION,
        )

        return response.Response(
            data=data,
            headers={
                "Content-Disposition": f'inline; filename="{self._get_filename(request, version)}"'
            },
        )


urlpatterns = [
    urls.path(
        django.settings.OPEN_API_PATH,
        RedocView,
        name="schema-rapi",
    ),
    urls.path(
        "shipping-openapi",
        ShippingOpenAPIView.as_view(),
        name="shipping-openapi",
    ),
]


def render_schema_description(APP_NAME):
    return f"""
{APP_NAME} is a multi-carrier shipping API that simplifies the integration of logistics carrier services.

The {APP_NAME} API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded
request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

The {APP_NAME} API differs for every account as we release new versions.
These docs are customized to your version of the API.


## Versioning

When backwards-incompatible changes are made to the API, a new, dated version is released.
The current version is `{VERSION}`.

Read our API changelog to learn more about backwards compatibility.

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

Updateable {APP_NAME} objects—including Shipment and Order have a metadata parameter.
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
    refs = dataunits.contextual_reference(request, reduced=False)

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

    template = """## Carriers
| Carrier Name | Display Name |
| ------------ | ------------ |
{% for carrier, name in refs.get("carriers", {}).items() -%}{% if carrier != "generic" -%}
| {{ carrier }} | {{ name }} |
{% endif -%}{% endfor %}
---
## Services
The following service level codes can be used to reference specific rates
when purchasing shipping labels using single call label creation.
You can also find all of the possible service levels for each of your carrier
accounts by using [this endpoint](#operation/&&get_services).
{% for carrier, services in refs.get("services", {}).items() -%}{% if carrier != "generic" -%}
### {{ refs.get("carriers", {}).get(carrier, "") }}
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
### {{ refs.get("carriers", {}).get(carrier, "") }}
| Code         | Dimensions   |
| ------------ | ------------ |
{% for code, preset in presets.items() -%}
| {{ code }} | {{ format_preset(preset) }} |
{% endfor %}
{% endfor %}
"""

    return jinja2.Template(template).render(refs=refs, format_preset=format_preset)


def render_tags(request, APP_NAME):
    return non_null(
        [
            {
                "name": "API",
                "description": """API instance metadata resources.
                """,
            },
            {
                "name": "Auth",
                "description": """API authentication resources.
                """,
            },
            {
                "name": "Carriers",
                "description": f"""This is an object representing your {APP_NAME} carrier extension.
                You can retrieve all supported carrier extensions available.
                """,
            },
            {
                "name": "Connections",
                "description": f"""This is an object representing your {APP_NAME} carrier connections.
                You can retrieve all carrier connections available to your account.
                The `carrier_id` is a friendly name you assign to your connection.
                """,
            },
            {
                "name": "Addresses",
                "description": f"""This is an object representing your {APP_NAME} shipping address.
                You can retrieve all addresses related to your {APP_NAME} account.
                Address objects are linked to your shipment history, and can be used for recurring shipping
                to / from the same locations.
                """,
            },
            {
                "name": "Parcels",
                "description": f"""This is an object representing your {APP_NAME} shipping parcel.
                Parcel objects are linked to your shipment history, and can be used for recurring shipping
                using the same packaging.
                """,
            },
            {
                "name": "Shipments",
                "description": f"""This is an object representing your {APP_NAME} shipment.
                A Shipment guides you through process of preparing and purchasing a label for an order.
                A Shipment transitions through multiple statuses throughout its lifetime as the package
                shipped makes its journey to it's destination.
                """,
            },
            {
                "name": "Documents",
                "description": f"""This is an object representing your {APP_NAME} document upload record.
                A Document upload record keep traces of shipping trade documents uploaded to carriers
                to fast track customs and border processing.
                """,
            },
            {
                "name": "Manifests",
                "description": f"""This is an object representing your {APP_NAME} manifest details.
                Some carriers require manifests to be created after labels are generated.
                A manifest is a summary of all the shipments that are being sent out.
                """,
            },
            {
                "name": "Trackers",
                "description": f"""This is an object representing your {APP_NAME} shipment tracker.
                A shipment tracker is an object attached to a shipment by it's tracking number.
                The tracker provide the latest tracking status and events associated with a shipment
                """,
            },
            {
                "name": "Pickups",
                "description": f"""This is an object representing your {APP_NAME} pickup booking.
                You can retrieve all pickup booked historically for your {APP_NAME} account shipments.
                """,
            },
            {
                "name": "Proxy",
                "description": f"""In some scenarios, all we need is to send request to a carrier using the {APP_NAME} unified API.
                The Proxy API comes handy for that as it turn {APP_NAME} into a simple middleware that converts and
                validate your request and simply forward it to the shipping carrier server.<br/>
                **Note:**<br/>
                    When using the proxy API, no objects are created in the {APP_NAME} system.
                    excpet API logs and tracing records for debugging purposes.
                """,
            },
            {
                "name": "Orders",
                "description": f"""This is an object representing your {APP_NAME} order.
                You can create {APP_NAME} orders to organize your shipments and ship line items separately.
                """,
            },
            {
                "name": "Webhooks",
                "description": f"""This is an object representing your {APP_NAME} webhook.
                You can configure webhook endpoints via the API to be notified about events happen in your
                {APP_NAME} account.
                """,
            },
            {
                "name": "Batches",
                "description": f"""This is an object representing your {APP_NAME} batch operation.
                You can retrieve all batch operations historically for your {APP_NAME} account.
                """,
            },
            {
                "name": "Reference & Enums",
                "description": render_reference_descriptions(request),
            },
        ]
    )
