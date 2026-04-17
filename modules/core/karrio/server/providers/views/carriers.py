import io
import base64
import re
from django.http import JsonResponse
from django.urls import path, re_path
from django.conf import settings
from django.utils import translation
from rest_framework import status, views
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView

import karrio.lib as lib
import karrio.server.openapi as openapi
import karrio.server.samples as samples
import karrio.server.core.views.api as api
import karrio.server.providers.models as models
from karrio.server.core.logging import logger
from karrio.server.core import datatypes, dataunits, serializers
ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


def _validate_lang(request: Request):
    """Validate and return the lang query parameter, or None."""
    lang = request.query_params.get("lang")
    if lang:
        supported = {code for code, _ in settings.LANGUAGES}
        if lang not in supported:
            return None, Response(
                {"error": f"Unsupported language: {lang}. Supported: {sorted(supported)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return lang, None


def _resolve_lang(request: Request, lang: str = None) -> str:
    """Resolve language: explicit param > Accept-Language header > default."""
    return lang or getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)


def _translated_references(request: Request, lang: str = None, reduced: bool = False):
    """Build contextual references with optional i18n translation."""
    from karrio.core.i18n import translate_references

    resolved = _resolve_lang(request, lang)
    with translation.override(resolved):
        references = dataunits.contextual_reference(reduced=reduced)
        return translate_references(references)


class CarrierList(views.APIView):
    permission_classes = []

    @openapi.extend_schema(
        auth=[],
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listCarriers"},
        summary="List all carriers",
        parameters=[
            openapi.OpenApiParameter(
                "lang",
                location=openapi.OpenApiParameter.QUERY,
                type=openapi.OpenApiTypes.STR,
                required=False,
                description="Language code for translated labels (e.g., 'de', 'en').",
            ),
        ],
        responses={
            200: serializers.CarrierDetails(many=True),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        examples=[
            openapi.OpenApiExample(
                name="Carrier List",
                value=lib.to_dict(samples.CARRIER_DETAILS_SAMPLE),
            )
        ],
    )
    def get(self, request: Request):
        """Returns the list of configured carriers"""
        lang, error_response = _validate_lang(request)
        if error_response:
            return error_response

        references = _translated_references(request, lang=lang, reduced=False)
        carriers = [
            dataunits.get_carrier_details(
                carrier_name,
                contextual_reference=references,
            )
            for carrier_name in references["carriers"].keys()
        ]

        return Response(carriers, status=status.HTTP_200_OK)


class CarrierDetails(api.APIView):
    permission_classes = []

    @openapi.extend_schema(
        auth=[],
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}get_details",
        extensions={"x-operationId": "getDetails"},
        summary="Get carrier details",
        parameters=[
            openapi.OpenApiParameter(
                "carrier_name",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                description=(
                    "The unique carrier slug. <br/>"
                    f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
                ),
            )
        ],
        responses={
            200: serializers.CarrierDetails(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: Request, carrier_name: str):
        """
        Retrieve a carrier's details
        """
        lang, error_response = _validate_lang(request)
        if error_response:
            return error_response

        references = _translated_references(request, lang=lang, reduced=False)

        if carrier_name not in references["carriers"]:
            raise NotFound(f"Unknown carrier: {carrier_name}")

        carrier_details = dataunits.get_carrier_details(
            carrier_name,
            contextual_reference=references,
        )

        return Response(carrier_details, status=status.HTTP_200_OK)


class CarrierServices(api.APIView):
    permission_classes = []

    @openapi.extend_schema(
        auth=[],
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}get_services",
        extensions={"x-operationId": "getServices"},
        summary="Get carrier services",
        parameters=[
            openapi.OpenApiParameter(
                "carrier_name",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                description=(
                    "The unique carrier slug. <br/>"
                    f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
                ),
            )
        ],
        responses={
            200: openapi.OpenApiTypes.OBJECT,
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        examples=[
            openapi.OpenApiExample(
                name="Carrier List",
                value=lib.to_dict(samples.CARRIER_SERICES_SAMPLE),
            )
        ],
    )
    def get(self, request: Request, carrier_name: str):
        """
        Retrieve a carrier's services
        """
        lang, error_response = _validate_lang(request)
        if error_response:
            return error_response

        references = _translated_references(request, lang=lang)

        if carrier_name not in references["carriers"]:
            raise NotFound(f"Unknown carrier: {carrier_name}")

        services = references["services"].get(carrier_name, {})

        return Response(services, status=status.HTTP_200_OK)


class CarrierOptions(api.APIView):
    permission_classes = []

    @openapi.extend_schema(
        auth=[],
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}get_options",
        extensions={"x-operationId": "getOptions"},
        summary="Get carrier options",
        parameters=[
            openapi.OpenApiParameter(
                "carrier_name",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                description=(
                    "The unique carrier slug. <br/>"
                    f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
                ),
            )
        ],
        responses={
            200: openapi.OpenApiTypes.OBJECT,
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        examples=[
            openapi.OpenApiExample(
                name="Carrier Options",
                value=lib.to_dict(samples.CARRIER_OPTIONS_SAMPLE),
            )
        ],
    )
    def get(self, request: Request, carrier_name: str):
        """
        Retrieve a carrier's options
        """
        lang, error_response = _validate_lang(request)
        if error_response:
            return error_response

        references = _translated_references(request, lang=lang)

        if carrier_name not in references["carriers"]:
            raise NotFound(f"Unknown carrier: {carrier_name}")

        options = references["options"].get(carrier_name, {})

        return Response(options, status=status.HTTP_200_OK)


class CarrierLabelPreview(VirtualDownloadView):
    def get(
        self,
        request: Request,
        pk: str,
        format: str = "pdf",
        **kwargs,
    ):
        """
        Preview a carrier label template...
        """
        try:
            query_params = request.GET.dict()
            carrier = models.CarrierConnection.objects.get(carrier_code="generic", pk=pk)

            self.document = self._generate_label(carrier, format)
            self.name = f"{carrier.custom_carrier_name}_label.{format}"
            self.attachment = query_params.get("download", False)

            response = super(CarrierLabelPreview, self).get(
                request, pk, format, **kwargs
            )
            response["X-Frame-Options"] = "ALLOWALL"
            return response
        except Exception as e:
            return JsonResponse(dict(error=str(e)), status=status.HTTP_409_CONFLICT)

    def get_file(self):
        content = base64.b64decode(self.document or "")
        buffer = io.BytesIO()
        buffer.write(content)

        return ContentFile(buffer.getvalue(), name=self.name)

    def _generate_label(self, carrier, format):
        import karrio.sdk as karrio
        import karrio.providers.generic.units as units

        template = carrier.label_template
        data = lib.identity(
            template.shipment_sample
            if template is not None and len(template.shipment_sample.items()) > 0
            else units.SAMPLE_SHIPMENT_REQUEST
        )
        service = lib.identity(
            data.get("service") or next((s.service_code for s in carrier.services))
        )
        request = lib.to_object(
            datatypes.ShipmentRequest,
            {
                **data,
                "service": service,
                "label_type": format.upper(),
                "selected_rate_id": data.get("selected_rate_id") or "",
                "rates": data.get("rates") or [],
            },
        )

        shipment, _ = karrio.Shipment.create(request).from_(carrier.gateway).parse()

        if shipment is None:
            raise ValidationError("Failed to generate label")

        return shipment.docs.label


urlpatterns = [
    path("carriers", CarrierList.as_view(), name="carrier-list"),
    path("carriers/<str:carrier_name>", CarrierDetails.as_view(), name="carrier-details"),
    path("carriers/<str:carrier_name>/services", CarrierServices.as_view(), name="carrier-services"),
    path("carriers/<str:carrier_name>/options", CarrierOptions.as_view(), name="carrier-options"),
    re_path(
        r"^carriers/(?P<pk>\w+)/label.(?P<format>[a-z0-9]+)",
        CarrierLabelPreview.as_view(),
        name="carrier-label",
    ),
]
