from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.urls import path
from django.conf import settings

from karrio.server.conf import FEATURE_FLAGS
from karrio.server.core.router import router
import karrio.server.core.dataunits as dataunits

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
BASE_PATH = getattr(settings, "BASE_PATH", "")
References = openapi.Schema(
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

        "ADDRESS_AUTO_COMPLETE": openapi.Schema(type=openapi.TYPE_OBJECT),
        "countries": openapi.Schema(type=openapi.TYPE_OBJECT),
        "currencies": openapi.Schema(type=openapi.TYPE_OBJECT),
        "carriers": openapi.Schema(type=openapi.TYPE_OBJECT),
        "custom_carriers": openapi.Schema(type=openapi.TYPE_OBJECT),
        "customs_content_type": openapi.Schema(type=openapi.TYPE_OBJECT),
        "incoterms": openapi.Schema(type=openapi.TYPE_OBJECT),
        "states": openapi.Schema(type=openapi.TYPE_OBJECT),
        "services": openapi.Schema(type=openapi.TYPE_OBJECT),
        "service_names": openapi.Schema(type=openapi.TYPE_OBJECT),
        "options": openapi.Schema(type=openapi.TYPE_OBJECT),
        "option_names": openapi.Schema(type=openapi.TYPE_OBJECT),
        "package_presets": openapi.Schema(type=openapi.TYPE_OBJECT),
        "packaging_types": openapi.Schema(type=openapi.TYPE_OBJECT),
        "payment_types": openapi.Schema(type=openapi.TYPE_OBJECT),
        "carrier_capabilities": openapi.Schema(type=openapi.TYPE_OBJECT),
        "service_levels": openapi.Schema(type=openapi.TYPE_OBJECT),
    },
)


@swagger_auto_schema(
    methods=["get"],
    tags=["API"],
    operation_id=f"{ENDPOINT_ID}data",
    operation_summary="Data References",
    responses={200: References},
)
@api_view(["GET"])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def references(request: Request):
    return Response(dataunits.contextual_reference(), status=status.HTTP_200_OK)


router.urls.append(path("references", references))
