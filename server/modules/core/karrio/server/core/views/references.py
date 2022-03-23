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
from karrio.server.core.serializers import PlainDictField, CharField, BooleanField
from karrio.server.core import dataunits

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
BASE_PATH = getattr(settings, "BASE_PATH", "")


class References(Serializer):
    APP_NAME = CharField()
    APP_VERSION = CharField()
    APP_WEBSITE = CharField()
    CUSTOM_CARRIER_DEFINITION = BooleanField()
    MULTI_ORGANIZATIONS = BooleanField()
    ORDERS_MANAGEMENT = BooleanField()
    APPS_MANAGEMENT = BooleanField()
    ALLOW_SIGNUP = BooleanField()
    ADMIN = CharField()
    OPENAPI = CharField()
    GRAPHQL = CharField()
    ADDRESS_AUTO_COMPLETE = PlainDictField()

    countries = PlainDictField()
    currencies = PlainDictField()
    carriers = PlainDictField()
    customs_content_type = PlainDictField()
    incoterms = PlainDictField()
    states = PlainDictField()
    services = PlainDictField()
    service_names = PlainDictField()
    options = PlainDictField()
    option_names = PlainDictField()
    package_presets = PlainDictField()
    packaging_types = PlainDictField()
    payment_types = PlainDictField()
    carrier_capabilities = PlainDictField()
    service_levels = PlainDictField()


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
    return Response(dataunits.contextual_reference(request), status=status.HTTP_200_OK)


router.urls.append(path("references", references))
