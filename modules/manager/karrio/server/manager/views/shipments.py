import io
import base64
import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_downloadview import VirtualDownloadView
from django.core.files.base import ContentFile
from django.urls import path, re_path

import karrio.lib as lib
import karrio.server.openapi as openapi
import karrio.server.core.filters as filters
import karrio.server.manager.models as models
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.filters import ShipmentFilters
from karrio.server.manager.router import router
from karrio.server.manager.serializers import (
    process_dictionaries_mutations,
    fetch_shipment_rates,
    PaginatedResult,
    ErrorResponse,
    ErrorMessages,
    Shipment,
    ShipmentData,
    buy_shipment_label,
    can_mutate_shipment,
    ShipmentSerializer,
    ShipmentRateData,
    ShipmentUpdateData,
    ShipmentPurchaseData,
    ShipmentCancelSerializer,
)

ENDPOINT_ID = "$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
Shipments = PaginatedResult("ShipmentList", Shipment)


class ShipmentList(GenericAPIView):
    throttle_scope = "carrier_request"
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ShipmentFilters
    serializer_class = Shipments
    model = models.Shipment

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listShipments"},
        summary="List all shipments",
        parameters=filters.ShipmentFilters.parameters,
        responses={
            200: Shipment(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, _: Request):
        """
        Retrieve all shipments.
        """
        shipments = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(Shipment(shipments, many=True).data)

        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createShipment"},
        summary="Create a shipment",
        responses={
            201: Shipment(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=ShipmentData(),
    )
    def post(self, request: Request):
        """
        Create a new shipment instance.
        """
        shipment = (
            ShipmentSerializer.map(data=request.data, context=request).save().instance
        )

        return Response(Shipment(shipment).data, status=status.HTTP_201_CREATED)


class ShipmentDetails(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveShipment"},
        summary="Retrieve a shipment",
        responses={
            200: Shipment(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a shipment.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        return Response(Shipment(shipment).data)

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateShipment"},
        summary="Update a shipment",
        responses={
            200: Shipment(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=ShipmentUpdateData(),
    )
    def put(self, request: Request, pk: str):
        """
        This operation allows for updating properties of a shipment including `label_type`, `reference`, `payment`, `options` and `metadata`.
        It is not for editing the parcels of a shipment.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)
        payload = ShipmentUpdateData.map(data=request.data).data
        can_mutate_shipment(shipment, update=True, payload=request.data)

        update = (
            ShipmentSerializer.map(
                shipment,
                context=request,
                data=process_dictionaries_mutations(
                    ["metadata", "options"], payload, shipment
                ),
            )
            .save()
            .instance
        )

        return Response(Shipment(update).data)


class ShipmentCancel(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}cancel",
        extensions={"x-operationId": "cancelShipment"},
        summary="Cancel a shipment",
        request=None,
        responses={
            200: Shipment(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request, pk: str):
        """
        Void a shipment with the associated label.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)
        can_mutate_shipment(shipment, delete=True)

        update = ShipmentCancelSerializer.map(shipment, context=request).save().instance

        return Response(Shipment(update).data)


class ShipmentRates(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}rates",
        summary="Fetch new shipment rates",
        responses={
            200: Shipment(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=ShipmentRateData(),
    )
    def post(self, request: Request, pk: str):
        """
        Refresh the list of the shipment rates
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)
        can_mutate_shipment(shipment, update=True)

        payload = ShipmentRateData.map(data=request.data).data

        update = fetch_shipment_rates(
            shipment,
            context=request,
            data=process_dictionaries_mutations(
                ["metadata", "options"], payload, shipment
            ),
        )

        return Response(Shipment(update).data)


class ShipmentPurchase(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}purchase",
        summary="Buy a shipment label",
        responses={
            200: Shipment(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=ShipmentPurchaseData(),
    )
    def post(self, request: Request, pk: str):
        """
        Select your preferred rates to buy a shipment label.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)
        can_mutate_shipment(shipment, purchase=True, update=True)

        payload = ShipmentPurchaseData.map(data=request.data).data

        update = buy_shipment_label(
            shipment,
            context=request,
            data=process_dictionaries_mutations(["metadata"], payload, shipment),
        )

        return Response(Shipment(update).data)


class ShipmentDocs(VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(
        self,
        request: Request,
        pk: str,
        doc: str = "label",
        format: str = "pdf",
        **kwargs,
    ):
        """Retrieve a shipment label."""
        self.shipment = models.Shipment.objects.get(pk=pk, label__isnull=False)
        self.document = getattr(self.shipment, doc, None)
        self.name = f"{doc}_{self.shipment.tracking_number}.{format}"

        query_params = request.GET.dict()
        self.preview = "preview" in query_params
        self.attachment = "download" in query_params

        response = super(ShipmentDocs, self).get(request, pk, doc, format, **kwargs)
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        content = base64.b64decode(self.document or "")
        buffer = io.BytesIO()

        if self.preview and "ZPL" in self.shipment.label_type or "":
            width, height, dpmm = (4, 6, 12)

            if "8" in self.shipment.label_type:
                width, height, dpmm = (8, 4, 12)

            _label = lib.failsafe(
                lambda: lib.zpl_to_pdf(
                    self.document,
                    width,
                    height,
                    dpmm=dpmm,
                )
            )

            if _label is not None:
                content = base64.b64decode(_label)
                self.name = self.name.replace("zpl", "pdf")

        buffer.write(content)

        return ContentFile(buffer.getvalue(), name=self.name)


router.urls.append(path("shipments", ShipmentList.as_view(), name="shipment-list"))
router.urls.append(
    path("shipments/<str:pk>", ShipmentDetails.as_view(), name="shipment-details")
)
router.urls.append(
    path("shipments/<str:pk>/cancel", ShipmentCancel.as_view(), name="shipment-cancel")
)
router.urls.append(
    path("shipments/<str:pk>/rates", ShipmentRates.as_view(), name="shipment-rates")
)
router.urls.append(
    path(
        "shipments/<str:pk>/purchase",
        ShipmentPurchase.as_view(),
        name="shipment-purchase",
    )
)
router.urls.append(
    re_path(
        r"^shipments/(?P<pk>\w+)/(?P<doc>[a-z0-9]+).(?P<format>[a-z0-9]+)",
        ShipmentDocs.as_view(),
        name="shipment-docs",
    )
)
