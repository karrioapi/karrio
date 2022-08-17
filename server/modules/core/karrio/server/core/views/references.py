from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer
from drf_yasg.utils import swagger_auto_schema
from django.urls import path
from django.conf import settings

from karrio.server.core.router import router
import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
BASE_PATH = getattr(settings, "BASE_PATH", "")


class References(Serializer):
    VERSION = serializers.CharField()
    APP_NAME = serializers.CharField()
    APP_WEBSITE = serializers.CharField()
    CUSTOM_CARRIER_DEFINITION = serializers.BooleanField()
    DATA_IMPORT_EXPORT = serializers.BooleanField()
    MULTI_ORGANIZATIONS = serializers.BooleanField()
    ALLOW_MULTI_ACCOUNT = serializers.BooleanField()
    ORDERS_MANAGEMENT = serializers.BooleanField()
    APPS_MANAGEMENT = serializers.BooleanField()
    AUDIT_LOGGING = serializers.BooleanField()
    ALLOW_SIGNUP = serializers.BooleanField()
    ALLOW_ADMIN_APPROVED_SIGNUP = serializers.BooleanField()
    PERSIST_SDK_TRACING = serializers.BooleanField()
    ADMIN = serializers.CharField()
    OPENAPI = serializers.CharField()
    GRAPHQL = serializers.CharField()
    ADDRESS_AUTO_COMPLETE = serializers.PlainDictField()

    countries = serializers.PlainDictField()
    currencies = serializers.PlainDictField()
    carriers = serializers.PlainDictField()
    customs_content_type = serializers.PlainDictField()
    incoterms = serializers.PlainDictField()
    states = serializers.PlainDictField()
    services = serializers.PlainDictField()
    service_names = serializers.PlainDictField()
    options = serializers.PlainDictField()
    option_names = serializers.PlainDictField()
    package_presets = serializers.PlainDictField()
    packaging_types = serializers.PlainDictField()
    payment_types = serializers.PlainDictField()
    carrier_capabilities = serializers.PlainDictField()
    service_levels = serializers.PlainDictField()


@swagger_auto_schema(
    methods=["get"],
    tags=["API"],
    operation_id=f"{ENDPOINT_ID}data",
    operation_summary="Data References",
    responses={200: References()},
)
@api_view(["GET"])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def references(request: Request):
    return Response(dataunits.contextual_reference(), status=status.HTTP_200_OK)


router.urls.append(path("references", references))
