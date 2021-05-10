from django.urls import path
from django.conf import settings
from drf_yasg import views, openapi, generators
from rest_framework import permissions


APP_VERSION = getattr(settings, 'VERSION', '')
APP_NAME = getattr(settings, 'APP_NAME', 'Purplship')
EMAIL_SUPPORT = getattr(settings, 'EMAIL_SUPPORT', 'hello@purplship.com')

SCHEMA_VIEW_DESCRIPTION = f"""
## API Reference

Purplship is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.
        
The Purplship API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request
bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

The Purplship API differs for every account as we release new versions.
These docs are customized to your version of the API.


## Versioning

When backwards-incompatible changes are made to the API, a new, dated version is released. 
The current version is `{settings.VERSION}`. 

Read our API changelog and to learn more about backwards compatibility.

As a precaution, use API versioning to check a new API version before committing to an upgrade.
"""

AUTHENTICATION_DESCRIPTION = """
For client-side code, we encourage the use of JSON Web Tokens (JWT) to authenticate your app.
The JWT tokens changes for every new session and have an expiration timestamp.

To authenticate via JWT access key, use `-H "Authorization: Bearer eyJ0eXAxxx...xxxaS86FjLH6U"`.
"""


class OpenAPISchemaGenerator(generators.OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "API",
                "description": AUTHENTICATION_DESCRIPTION
            },
            {
                "name": "Addresses",
                "description": """
                This is an object representing your a Purplship shipping address.
                
                You can retrieve all addresses related to your Purplship account.
                """
            },
            {
                "name": "Proxy",
                "description": """
                In some scenarios, all we need is to send request to a carrier using the Purplship unified API.

                The Proxy API comes handy for that as it turn Purplship into a simple middleware that converts and 
                validate your request and simply forward it to the shipping carrier server.
                
                > **Note**
                >
                > When using the proxy API, no objects are created in the Purplship system.
                """
            },
        ]

        return swagger


schema_view = views.get_schema_view(
    openapi.Info(
        title=f"{APP_NAME} API",
        default_version=APP_VERSION,
        description=SCHEMA_VIEW_DESCRIPTION,
        contact=openapi.Contact(email=EMAIL_SUPPORT),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=OpenAPISchemaGenerator,
)


urlpatterns = [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(settings.OPEN_API_PATH, schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
