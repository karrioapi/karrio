import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.serializers import (
    TrackingStatus, ErrorResponse, TestFilters, Operation
)
from purpleserver.core.utils import SerializerDecorator, PaginatedResult
from purpleserver.manager.router import router
from purpleserver.manager.serializers import TrackingSerializer

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Trackers = PaginatedResult('TrackerList', TrackingStatus)


class TrackerList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 20

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all shipment trackers",
        responses={200: Trackers(), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all shipment trackers.
        """
        trackers = request.user.tracking_set.all()
        response = self.paginate_queryset(TrackingStatus(trackers, many=True).data)
        return self.get_paginated_response(response)


class TrackersCreate(APIView):
    logging_methods = ['GET']

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a shipment tracker",
        query_serializer=TestFilters(),
        responses={200: TrackingStatus(), 404: ErrorResponse()}
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        This API retrieves or creates (if non existent) a tracking status object containing the
        details and events of a shipping in progress.
        """
        data = dict(tracking_number=tracking_number)
        carrier_filter = {
            **SerializerDecorator[TestFilters](data=request.query_params).data,
            "carrier_name": carrier_name,
            "created_by": request.user
        }
        tracking = request.user.tracking_set.filter(tracking_number=tracking_number, created_by=request.user).first()

        tracking = SerializerDecorator[TrackingSerializer](
            tracking, data=data).save(created_by=request.user, carrier_filter=carrier_filter).instance
        return Response(TrackingStatus(tracking).data)


class TrackersDetails(APIView):

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}remove",
        operation_summary="Remove a shipment tracker",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a shipment tracker.
        """
        tracker = request.user.tracking_set.get(pk=pk)

        tracker.delete(keep_parents=True)
        serializer = Operation(dict(operation="Remove a tracker", success=True))
        return Response(serializer.data)


router.urls.append(path('trackers', TrackerList.as_view(), name="trackers-list"))
router.urls.append(path('trackers/<str:pk>', TrackersDetails.as_view(), name="tracker-details"))
router.urls.append(path('trackers/<carrier_name>/<tracking_number>', TrackersCreate.as_view(), name="shipment-tracker"))
