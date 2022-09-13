from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from karrio.server.conf import FEATURE_FLAGS
from karrio.server.core import dataunits

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Metadata = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "VERSION": openapi.Schema(type=openapi.TYPE_STRING),
        "APP_NAME": openapi.Schema(type=openapi.TYPE_STRING),
        "APP_WEBSITE": openapi.Schema(type=openapi.TYPE_STRING),
        **{
            flag: openapi.Schema(type=openapi.TYPE_BOOLEAN)
            for flag in FEATURE_FLAGS
        },
        "ADMIN": openapi.Schema(type=openapi.TYPE_STRING),
        "OPENAPI": openapi.Schema(type=openapi.TYPE_STRING),
        "GRAPHQL": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

@swagger_auto_schema(
    methods=["get"],
    tags=["API"],
    operation_id=f"{ENDPOINT_ID}ping",
    operation_summary="Instance Metadata",
    responses={200: Metadata},
)
@api_view(["GET"])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def view(request: Request) -> Response:
    return Response(dataunits.contextual_metadata(request))
