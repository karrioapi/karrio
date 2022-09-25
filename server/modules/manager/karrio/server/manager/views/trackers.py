import logging

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.urls import path
from django.db.models import Q
from django_filters import rest_framework as filters

import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.serializers import (
    TrackingStatus,
    ErrorResponse,
    ErrorMessages,
)
from karrio.server.core.filters import TrackerFilters
from karrio.server.manager.router import router
from karrio.server.manager.serializers import TrackingSerializer
import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Trackers = serializers.PaginatedResult("TrackerList", TrackingStatus)


class TrackerList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TrackerFilters
    serializer_class = Trackers
    model = models.Tracking

    def get_queryset(self):
        queryset = super().get_queryset()
        _filters = tuple()
        query_params = getattr(self.request, "query_params", {})
        carrier_name = query_params.get("carrier_name")

        if carrier_name is not None:
            _filters += (
                Q(
                    **{
                        f"tracking_carrier__{carrier_name.replace('_', '')}settings__isnull": False
                    }
                ),
            )

        return queryset.filter(*_filters)

    @extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}list",
        summary="List all shipment trackers",
        responses={
            200: Trackers(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all shipment trackers.
        """
        trackers = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(TrackingStatus(trackers, many=True).data)
        return self.get_paginated_response(response)


class TrackersCreate(APIView):
    logging_methods = ["GET"]

    @extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}create",
        summary="Create a shipment tracker",
        responses={
            200: TrackingStatus(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        parameters=[
            OpenApiParameter(
                "carrier_name",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                enum=dataunits.NON_HUBS_CARRIERS,
                required=True,
            ),
            OpenApiParameter(
                "tracking_number",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
            ),
            OpenApiParameter(
                "hub",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                required=False,
            ),
        ],
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        This API creates or retrieves (if existent) a tracking status object containing the
        details and events of a shipping in progress.
        """
        instance = (
            models.Tracking.access_by(request)
            .filter(tracking_number=tracking_number)
            .first()
        )

        query = request.query_params
        carrier_filter = {
            **{k: v for k, v in query.items() if k != "hub"},
            # If a hub is specified, use the hub as carrier to track the package
            "carrier_name": (query.get("hub") if "hub" in query else carrier_name),
        }
        data = {
            "tracking_number": tracking_number,
            "options": (
                {tracking_number: {"carrier": carrier_name}} if "hub" in query else {}
            ),
        }

        tracker = (
            serializers.SerializerDecorator[TrackingSerializer](
                instance, data=data, context=request
            )
            .save(carrier_filter=carrier_filter)
            .instance
        )

        return Response(TrackingStatus(tracker).data)


class TrackersDetails(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}retrieves",
        summary="Retrieves a shipment tracker",
        responses={
            200: TrackingStatus(),
            404: ErrorMessages(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, id_or_tracking_number: str):
        """
        Retrieve a shipment tracker
        """
        __filter = Q(pk=id_or_tracking_number) | Q(
            tracking_number=id_or_tracking_number
        )
        trackers = models.Tracking.objects.filter(__filter)

        if len(trackers) == 0:
            models.Tracking.objects.get(__filter)

        return Response(TrackingStatus(trackers.first()).data)

    @extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}remove",
        summary="Discard a shipment tracker",
        responses={
            200: TrackingStatus(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, id_or_tracking_number: str):
        """
        Discard a shipment tracker.
        """
        tracker = models.Tracking.access_by(request).get(
            Q(pk=id_or_tracking_number) | Q(tracking_number=id_or_tracking_number)
        )

        tracker.delete(keep_parents=True)

        return Response(TrackingStatus(tracker).data)


router.urls.append(path("trackers", TrackerList.as_view(), name="trackers-list"))
router.urls.append(
    path(
        "trackers/<str:id_or_tracking_number>",
        TrackersDetails.as_view(),
        name="tracker-details",
    )
)
router.urls.append(
    path(
        "trackers/<carrier_name>/<tracking_number>",
        TrackersCreate.as_view(),
        name="shipment-tracker",
    )
)
