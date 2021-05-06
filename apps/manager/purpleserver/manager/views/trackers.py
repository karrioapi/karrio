import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.serializers import (
    FlagField, TrackingStatus, ErrorResponse, TestFilters, Operation
)
from purpleserver.core.utils import SerializerDecorator, PaginatedResult
from purpleserver.manager.router import router
from purpleserver.manager.serializers import TrackingSerializer
import purpleserver.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Trackers = PaginatedResult('TrackerList', TrackingStatus)


class TrackerFilters(serializers.Serializer):
    test_mode = FlagField(
        required=False, allow_null=True, default=None,
        help_text="This flag filter out tracker created from carriers in test or live mode")


class TrackerList(GenericAPIView):
    serializer_class = TrackingStatus
    queryset = models.Tracking.objects
    pagination_class = type('CustomPagination', (LimitOffsetPagination,), dict(default_limit=20))

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all shipment trackers",
        responses={200: Trackers(), 400: ErrorResponse()},
        query_serializer=TrackerFilters
    )
    def get(self, request: Request):
        """
        Retrieve all shipment trackers.
        """
        query = (
            SerializerDecorator[TrackerFilters](data=request.query_params).data
            if any(request.query_params) else {}
        )
        trackers = models.Tracking.objects.access_with(request.user).filter(**query)
        response = self.paginate_queryset(TrackingStatus(trackers, many=True).data)
        return self.get_paginated_response(response)


class TrackersCreate(APIView):
    logging_methods = ['GET']

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a shipment tracker",
        query_serializer=TestFilters(),
        responses={200: TrackingStatus(), 404: ErrorResponse()}
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        This API creates or retrieves (if existent) a tracking status object containing the
        details and events of a shipping in progress.
        """
        data = dict(tracking_number=tracking_number)
        carrier_filter = {
            **SerializerDecorator[TestFilters](data=request.query_params).data,
            "carrier_name": carrier_name,
            "user": request.user
        }
        tracking = models.Tracking.objects.access_with(request.user).filter(tracking_number=tracking_number).first()

        instance = SerializerDecorator[TrackingSerializer](
            tracking, data=data, context_user=request.user).save(carrier_filter=carrier_filter).instance
        return Response(TrackingStatus(instance).data)


class TrackersDetails(APIView):

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}retrieves",
        operation_summary="Retrieves a shipment tracker",
        responses={200: TrackingStatus(), 404: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a shipment tracker
        """
        tracker = models.Tracking.objects.access_with(request.user).get(pk=pk)

        return Response(TrackingStatus(tracker).data)

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}remove",
        operation_summary="Discard a shipment tracker",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Discard a shipment tracker.
        """
        tracker = models.Tracking.objects.access_with(request.user).get(pk=pk)

        tracker.delete(keep_parents=True)
        serializer = Operation(dict(operation="Discard a tracker", success=True))
        return Response(serializer.data)


router.urls.append(path('trackers', TrackerList.as_view(), name="trackers-list"))
router.urls.append(path('trackers/<str:pk>', TrackersDetails.as_view(), name="tracker-details"))
router.urls.append(path('trackers/<carrier_name>/<tracking_number>', TrackersCreate.as_view(), name="shipment-tracker"))
