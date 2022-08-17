import base64
import io
import logging
from django.conf import settings
from django.http import JsonResponse
from drf_yasg import openapi
from django.urls import path, re_path
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


from karrio.server import serializers
from karrio.server.serializers import SerializerDecorator, PaginatedResult
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.gateway import Carriers
from karrio.server.core import datatypes, dataunits
from karrio.server.providers import models
from karrio.server.core.serializers import (
    CarrierSettings,
    ErrorResponse,
    CARRIERS,
)
from karrio.server.providers.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CarriersSettingsList = PaginatedResult("CarrierList", CarrierSettings)


class CarrierFilters(serializers.FlagsSerializer):

    carrier_name = serializers.ChoiceField(
        choices=CARRIERS, required=False, help_text="Indicates a carrier (type)"
    )
    active = serializers.FlagField(
        required=False,
        allow_null=True,
        default=None,
        help_text="This flag indicates whether to return active carriers only",
    )
    system_only = serializers.FlagField(
        required=False,
        allow_null=True,
        default=False,
        help_text="This flag indicates that only system carriers should be returned",
    )


class CarrierList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 100

    @swagger_auto_schema(
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all carriers",
        responses={
            200: CarriersSettingsList(),
            400: ErrorResponse(),
        },
        query_serializer=CarrierFilters,
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request GET \\
                  --url '/v1/carriers' \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
    )
    def get(self, request: Request):
        """
        Returns the list of configured carriers
        """
        filter = {
            **SerializerDecorator[CarrierFilters](data=request.query_params).data,
            "context": request,
        }

        carriers = [carrier.data for carrier in Carriers.list(**filter)]
        response = self.paginate_queryset(CarrierSettings(carriers, many=True).data)
        return self.get_paginated_response(response)


class CarrierServices(APIView):
    @swagger_auto_schema(
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}get_services",
        operation_summary="Get carrier services",
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=[c for c, _ in CARRIERS],
            )
        ],
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, carrier_name: str):
        """
        Retrieve a carrier's services
        """
        references = dataunits.contextual_reference()

        if carrier_name not in references["carriers"]:
            raise Exception(f"Unknown carrier: {carrier_name}")

        services = references["services"].get(carrier_name, {})

        return Response(services, status=status.HTTP_200_OK)


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
            carrier = models.MODELS["generic"].objects.get(pk=pk)

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
        import karrio
        from karrio.core.utils import DP
        from karrio.providers.generic.units import SAMPLE_SHIPMENT_REQUEST

        template = carrier.label_template
        data = (
            template.shipment_sample
            if template is not None and len(template.shipment_sample.items()) > 0
            else SAMPLE_SHIPMENT_REQUEST
        )
        service = data.get("service") or next(
            (s.service_code for s in carrier.services)
        )
        request = DP.to_object(
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
            raise Exception("Failed to generate label")

        return shipment.docs.label


router.urls.append(path("carriers", CarrierList.as_view()))
router.urls.append(
    path(
        "carriers/<str:carrier_name>/services",
        CarrierServices.as_view(),
        name="carrier-services",
    )
)
if settings.CUSTOM_CARRIER_DEFINITION:
    router.urls.append(
        re_path(
            r"^carriers/(?P<pk>\w+)/label.(?P<format>[a-z0-9]+)",
            CarrierLabelPreview.as_view(),
            name="carrier-label-preview",
        )
    )
