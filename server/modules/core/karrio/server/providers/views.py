import io
import base64
import logging
from django.conf import settings
from django.http import JsonResponse
from django.urls import path, re_path
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from karrio.server.serializers import PaginatedResult
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
import karrio.server.core.filters as filters
import karrio.server.openapi as openapi

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CarriersSettingsList = PaginatedResult("CarrierList", CarrierSettings)


class CarrierList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 100

    @openapi.extend_schema(
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}list",
        summary="List all carriers",
        responses={
            200: CarriersSettingsList(),
            400: ErrorResponse(),
        },
        parameters=filters.CarrierFilters.parameters,
    )
    def get(self, request: Request):
        """
        Returns the list of configured carriers
        """
        filter = {**request.query_params, "context": request}

        carriers = [carrier.data for carrier in Carriers.list(**filter)]
        response = self.paginate_queryset(CarrierSettings(carriers, many=True).data)
        return self.get_paginated_response(response)


class CarrierServices(APIView):
    @openapi.extend_schema(
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}get_services",
        summary="Get carrier services",
        parameters=[
            openapi.OpenApiParameter(
                "carrier_name",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                enum=[c for c, _ in CARRIERS],
            )
        ],
        responses={
            200: openapi.OpenApiTypes.OBJECT,
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
