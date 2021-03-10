import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.serializers import (
    TrackingStatus, ErrorResponse, TestFilters
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


class TrackingDetails(APIView):
    logging_methods = ['GET']

    @swagger_auto_schema(
        tags=['Trackers'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieves or creates a shipment trackers",
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
            "user": request.user
        }
        tracking = request.user.tracking_set.filter(tracking_number=tracking_number, user=request.user).first()

        tracking = SerializerDecorator[TrackingSerializer](
            tracking, data=data).save(user=request.user, carrier_filter=carrier_filter).instance
        return Response(TrackingStatus(tracking).data)


router.urls.append(path('trackers', TrackerList.as_view(), name="trackers-list"))
router.urls.append(path('trackers/<carrier_name>/<tracking_number>', TrackingDetails.as_view(), name="shipment-tracker"))
