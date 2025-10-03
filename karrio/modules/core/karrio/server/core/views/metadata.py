import rest_framework.request as request
import rest_framework.response as response
import rest_framework.renderers as renderers
import rest_framework.decorators as decorators
import rest_framework.permissions as permissions

import karrio.server.conf as conf
import karrio.server.openapi as openapi
import karrio.server.core.dataunits as dataunits

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Metadata = openapi.OpenApiResponse(
    openapi.OpenApiTypes.OBJECT,
    examples=[
        openapi.OpenApiExample(
            name="Metadata",
            value={
                "VERSION": "",
                "APP_NAME": "",
                "APP_WEBSITE": "",
                "HOST": "",
                "ADMIN": "",
                "OPENAPI": "",
                "GRAPHQL": "",
                **{flag: True for flag in conf.FEATURE_FLAGS},
            },
        )
    ],
)


@openapi.extend_schema(
    auth=[],
    methods=["get"],
    tags=["API"],
    operation_id=f"{ENDPOINT_ID}ping",
    summary="Instance Metadata",
    responses={200: Metadata},
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
@decorators.renderer_classes([renderers.JSONRenderer])
def view(request: request.Request) -> response.Response:
    return response.Response(dataunits.contextual_metadata(request))
