import karrio.server.core.dataunits as dataunits
import karrio.server.openapi as openapi
import yaml  # type: ignore
from django.conf import settings
from django.urls import path
from django.utils import translation
from karrio.server.conf import FEATURE_FLAGS
from karrio.server.core.router import router
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

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
@authentication_classes([])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def references(request: Request):
    try:
        reduced = bool(yaml.safe_load(request.query_params.get("reduced", "true")))

        lang = request.query_params.get("lang")
        if lang:
            supported = {code for code, _ in settings.LANGUAGES}
            if lang not in supported:
                return Response(
                    {"error": f"Unsupported language: {lang}. Supported: {sorted(supported)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        from karrio.core.i18n import translate_references

        with translation.override(lang or getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)):
            data = dataunits.contextual_reference(reduced=reduced)
            data = translate_references(data)

        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        from karrio.server.core.logging import logger

        logger.exception("Failed to retrieve references", error=str(e))
        raise e


router.urls.append(path("references", references))
