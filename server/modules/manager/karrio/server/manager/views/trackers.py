import logging

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.urls import path
from django.db.models import Q
from django_filters import rest_framework as filters

from karrio.core.utils import DP
import karrio.server.core.dataunits as dataunits
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.serializers import (
    TrackingStatus,
    ErrorResponse,
    TestFilters,
    Operation,
    TrackerStatus,
    CharField,
)
from karrio.server.serializers import SerializerDecorator, PaginatedResult
from karrio.server.manager.router import router
from karrio.server.manager.serializers import TrackingSerializer
import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Trackers = PaginatedResult("TrackerList", TrackingStatus)


class TrackerFilter(TestFilters):
    hub = CharField(
        required=False,
        allow_blank=False,
        allow_null=False,
        max_length=50,
        help_text="A carrier_name of a hub connector",
    )


class TrackersFilter(filters.FilterSet):
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")
    carrier_id = filters.CharFilter(field_name="tracking_carrier__carrier_id")

    parameters = [
        openapi.Parameter(
            "carrier_name",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=dataunits.CARRIER_NAMES,
        ),
        openapi.Parameter("carrier_id", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(
            "status",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=[k.value for k in list(TrackerStatus)],
        ),
        openapi.Parameter("test_mode", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        openapi.Parameter(
            "created_before",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="DateTime in format `YYYY-MM-DD H:M:S.fz`",
        ),
        openapi.Parameter(
            "created_after",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="DateTime in format `YYYY-MM-DD H:M:S.fz`",
        ),
    ]

    class Meta:
        model = models.Tracking
        fields = ["test_mode", "status"]


class TrackerList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TrackersFilter
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

    @swagger_auto_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all shipment trackers",
        responses={200: Trackers(), 400: ErrorResponse()},
        manual_parameters=TrackersFilter.parameters,
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

    @swagger_auto_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a shipment tracker",
        query_serializer=TrackerFilter(),
        responses={200: TrackingStatus(), 404: ErrorResponse()},
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=dataunits.NON_HUBS_CARRIERS,
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

        query = SerializerDecorator[TrackerFilter](data=request.query_params).data
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
            SerializerDecorator[TrackingSerializer](
                instance, data=data, context=request
            )
            .save(carrier_filter=carrier_filter)
            .instance
        )

        return Response(TrackingStatus(tracker).data)


class TrackersDetails(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}retrieves",
        operation_summary="Retrieves a shipment tracker",
        responses={200: TrackingStatus(), 404: ErrorResponse()},
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

    @swagger_auto_schema(
        tags=["Trackers"],
        operation_id=f"{ENDPOINT_ID}remove",
        operation_summary="Discard a shipment tracker",
        responses={200: Operation(), 400: ErrorResponse()},
    )
    def delete(self, request: Request, id_or_tracking_number: str):
        """
        Discard a shipment tracker.
        """
        tracker = models.Tracking.access_by(request).get(
            Q(pk=id_or_tracking_number) | Q(tracking_number=id_or_tracking_number)
        )

        tracker.delete(keep_parents=True)
        serializer = Operation(dict(operation="Discard a tracker", success=True))
        return Response(serializer.data)


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
