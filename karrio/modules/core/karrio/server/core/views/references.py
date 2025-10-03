import yaml  # type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from django.urls import path
from django.conf import settings

from karrio.server.conf import FEATURE_FLAGS
from karrio.server.core.router import router
import karrio.server.core.dataunits as dataunits
import karrio.server.openapi as openapi

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
BASE_PATH = getattr(settings, "BASE_PATH", "")
References = openapi.OpenApiResponse(
    openapi.OpenApiTypes.OBJECT,
    examples=[
        openapi.OpenApiExample(
            name="References",
            value={
                "VERSION": "",
                "APP_NAME": "",
                "APP_WEBSITE": "",
                "HOST": "",
                "ADMIN": "",
                "OPENAPI": "",
                "GRAPHQL": "",
                **{flag: True for flag in FEATURE_FLAGS},
                "ADDRESS_AUTO_COMPLETE": {},
                "countries": {},
                "currencies": {},
                "carriers": {},
                "customs_content_type": {},
                "incoterms": {},
                "states": {},
                "services": {},
                "connection_configs": {},
                "service_names": {},
                "options": {},
                "option_names": {},
                "package_presets": {},
                "packaging_types": {},
                "payment_types": {},
                "carrier_capabilities": {},
                "service_levels": {},
                "integration_status": {},
            },
        )
    ],
)


@openapi.extend_schema(
    auth=[],
    methods=["get"],
    tags=["API"],
    operation_id=f"{ENDPOINT_ID}data",
    summary="Data References",
    responses={200: References},
)
@api_view(["GET"])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def references(request: Request):
    try:
        reduced = bool(yaml.safe_load(request.query_params.get("reduced", "true")))

        return Response(
            dataunits.contextual_reference(reduced=reduced),
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        import logging

        logging.exception(e)
        raise e


router.urls.append(path("references", references))
