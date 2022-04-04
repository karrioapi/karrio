from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer
from drf_yasg.utils import swagger_auto_schema

from karrio.server.core.serializers import CharField, BooleanField
from karrio.server.core import dataunits

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class Metadata(Serializer):
    APP_NAME = CharField()
    APP_VERSION = CharField()
    APP_WEBSITE = CharField(required=False, allow_null=True)
    CUSTOM_CARRIER_DEFINITION = BooleanField()
    MULTI_ORGANIZATIONS = BooleanField()
    ORDERS_MANAGEMENT = BooleanField()
    APPS_MANAGEMENT = BooleanField()
    ALLOW_SIGNUP = BooleanField()
    ADMIN = CharField()
    OPENAPI = CharField()
    GRAPHQL = CharField()


@swagger_auto_schema(
    methods=["get"],
    tags=["API"],
    operation_id=f"{ENDPOINT_ID}ping",
    operation_summary="Instance Metadata",
    responses={200: Metadata()},
)
@api_view(["GET"])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def view(request: Request) -> Response:
    return Response(dataunits.contextual_metadata(request))
