import logging
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.serializers import (
    TrackingStatus, ErrorResponse, TestFilters
)
from purpleserver.core.utils import SerializerDecorator
from purpleserver.manager.router import router
from purpleserver.manager.serializers import TrackingSerializer

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class TrackingList(GenericAPIView):

    @swagger_auto_schema(
        tags=['Tracking'],
        operation_id=f"{ENDPOINT_ID}statuses",
        operation_summary="List all tracking statuses",
        responses={200: TrackingStatus(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all tracking statuses.
        """
        statuses = request.user.tracking_set.all()
        response = self.paginate_queryset(TrackingStatus(statuses, many=True).data)
        return Response(response)


class TrackingDetails(APIView):

    @swagger_auto_schema(
        tags=['Tracking'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a tracking status",
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
        tracking = request.user.tracking_set.filter(tracking_number=tracking_number).first()

        tracking = SerializerDecorator[TrackingSerializer](
            tracking, data=data).save(user=request.user, carrier_filter=carrier_filter).instance
        return Response(TrackingStatus(tracking).data)


router.urls.append(path('tracking_status', TrackingList.as_view(), name="tracking-status-list"))
router.urls.append(path('tracking_status/<carrier_name>/<tracking_number>', TrackingDetails.as_view(), name="shipment-tracking"))
