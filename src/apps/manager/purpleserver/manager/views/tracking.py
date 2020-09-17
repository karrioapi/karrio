import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from purpleserver.core.serializers import (
    TrackingStatus, ErrorResponse,
)
from purpleserver.core.utils import SerializerDecorator
from purpleserver.manager.router import router
from purpleserver.manager.serializers import TrackingSerializer

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class TrackingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]


class ShipmentTracking(TrackingAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}track",
        operation_summary="Track a shipment",
        operation_description="""Track a shipment.""",
        responses={200: TrackingStatus(), 404: ErrorResponse()}
    )
    def get(self, request: Request, carrier_id: str, tracking_number: str):
        tracking = request.user.tracking_set.filter(tracking_number=tracking_number).first()
        shipment = request.user.shipment_set.filter(tracking_number=tracking_number).first()

        data = dict(
            shipment=shipment,
            carrier_id=carrier_id,
            tracking_number=tracking_number,
        )

        tracking = SerializerDecorator[TrackingSerializer](tracking, data=data).save(user=request.user).instance
        return Response(TrackingStatus(tracking).data)


router.urls.append(path('tracking/<carrier_id>/<tracking_number>', ShipmentTracking.as_view(), name="shipment-tracking"))
