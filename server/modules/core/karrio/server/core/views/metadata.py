from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
import karrio.server.openapi as openapi

from karrio.server.conf import FEATURE_FLAGS
from karrio.server.core import dataunits

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
                **{
                    flag: True
                    for flag in FEATURE_FLAGS
                },
                "ADMIN": "",
                "OPENAPI": "",
                "GRAPHQL": "",
            }
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
@api_view(["GET"])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def view(request: Request) -> Response:
    return Response(dataunits.contextual_metadata(request))
