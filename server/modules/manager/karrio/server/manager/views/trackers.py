import logging

from django.urls import path
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.serializers import (
    TrackingStatus,
    ErrorResponse,
    ErrorMessages,
    TrackingData,
)
from karrio.server.manager.serializers import (
    process_dictionaries_mutations,
    can_mutate_tracker,
    TrackingSerializer,
    TrackerUpdateData,
)
from karrio.server.manager.router import router
from karrio.server.core.filters import TrackerFilters
import karrio.server.core.dataunits as dataunits
import karrio.server.serializers as serializers
import karrio.server.manager.models as models
import karrio.server.core.filters as filters
import karrio.server.openapi as openapi

ENDPOINT_ID = "$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
Trackers = serializers.PaginatedResult("TrackerList", TrackingStatus)


class TrackerList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
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

    @openapi.extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}list",
        summary="List all package trackers",
        parameters=filters.TrackerFilters.parameters,
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

    @openapi.extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}add",
        summary="Add a package tracker",
        request=TrackingData(),
        responses={
            200: TrackingStatus(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        parameters=[
            openapi.OpenApiParameter(
                "hub",
                location=openapi.OpenApiParameter.QUERY,
                type=openapi.OpenApiTypes.STR,
                required=False,
            ),
        ],
    )
    def post(self, request: Request):
        """
        This API creates or retrieves (if existent) a tracking status object containing the
        details and events of a shipping in progress.
        """
        query = request.query_params
        serializer = TrackingData(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        instance = (
            models.Tracking.access_by(request)
            .filter(tracking_number=data["tracking_number"])
            .first()
        )

        carrier_filter = {
            **{k: v for k, v in query.items() if k != "hub"},
            # If a hub is specified, use the hub as carrier to track the package
            "carrier_name": (
                query.get("hub") if "hub" in query else data["carrier_name"]
            ),
        }
        data = {
            "tracking_number": data["tracking_number"],
            "options": (
                {data["tracking_number"]: {"carrier": data["carrier_name"]}}
                if "hub" in query
                else {}
            ),
        }

        tracker = (
            TrackingSerializer.map(instance, data=data, context=request)
            .save(carrier_filter=carrier_filter)
            .instance
        )

        return Response(
            TrackingStatus(tracker).data,
            status=status.HTTP_202_ACCEPTED,
        )


class TrackersCreate(APIView):
    @openapi.extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}create",
        summary="Create a package tracker",
        deprecated=True,
        responses={
            200: TrackingStatus(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        parameters=[
            openapi.OpenApiParameter(
                "tracking_number",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                required=True,
            ),
            openapi.OpenApiParameter(
                "carrier_name",
                location=openapi.OpenApiParameter.QUERY,
                type=openapi.OpenApiTypes.STR,
                enum=dataunits.NON_HUBS_CARRIERS,
                required=True,
            ),
            openapi.OpenApiParameter(
                "hub",
                location=openapi.OpenApiParameter.QUERY,
                type=openapi.OpenApiTypes.STR,
                required=False,
            ),
        ],
        request=None,
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
            TrackingSerializer.map(instance, data=data, context=request)
            .save(carrier_filter=carrier_filter)
            .instance
        )

        return Response(
            TrackingStatus(tracker).data,
            status=status.HTTP_202_ACCEPTED,
        )


class TrackersDetails(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @openapi.extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}retrieves",
        summary="Retrieves a package tracker",
        responses={
            200: TrackingStatus(),
            404: ErrorMessages(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, id_or_tracking_number: str):
        """
        Retrieve a package tracker
        """
        __filter = Q(pk=id_or_tracking_number) | Q(
            tracking_number=id_or_tracking_number
        )
        trackers = models.Tracking.objects.filter(__filter)

        if len(trackers) == 0:
            models.Tracking.objects.get(__filter)

        return Response(TrackingStatus(trackers.first()).data)

    @openapi.extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}update",
        summary="Update tracker data",
        responses={
            200: TrackingStatus(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        request=TrackerUpdateData(),
    )
    def put(self, request: Request, id_or_tracking_number: str):
        tracker = models.Tracking.access_by(request).get(
            Q(pk=id_or_tracking_number) | Q(tracking_number=id_or_tracking_number)
        )
        can_mutate_tracker(tracker, update=True, payload=request.data)

        payload = TrackerUpdateData.map(data=request.data).data
        update = (
            TrackerUpdateData.map(
                tracker,
                context=request,
                data=process_dictionaries_mutations(
                    ["metadata", "options"], payload, tracker
                ),
            )
            .save()
            .instance
        )

        return Response(TrackingStatus(update).data)

    @openapi.extend_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}remove",
        summary="Discard a package tracker",
        responses={
            200: TrackingStatus(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, id_or_tracking_number: str):
        """
        Discard a package tracker.
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
        "trackers/<str:carrier_name>/<str:tracking_number>",
        TrackersCreate.as_view(),
        name="shipment-tracker",
    )
)
