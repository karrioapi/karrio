import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.serializers import (
    ErrorResponse as ErrorResponseSerializer, ShipmentResponse, Shipment
)
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)


class ShipmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class ShipmentCoreView(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['SHIPMENTS'],
        operation_id="Retrieve all shipments",
        responses={400: ErrorResponseSerializer()}
    )
    def get(self, request: Request):
        """
        Retrieve all shipment instance.
        """
        pass

    @swagger_auto_schema(
        tags=['SHIPMENTS'],
        operation_id="Create a shipment",
        responses={200: ShipmentResponse(), 400: ErrorResponseSerializer()}
    )
    def post(self, request: Request):
        """
        Create a new shipment instance.
        """
        pass


class ShipmentUpdateView(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['SHIPMENTS'],
        operation_id="Retrieve a shipment",
        responses={200: Shipment(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, shipment_id: str):
        """
        Retrieve a shipment instance.
        """
        pass

    @swagger_auto_schema(
        tags=['SHIPMENTS'],
        operation_id="Update a shipment",
        responses={200: Shipment(), 400: ErrorResponseSerializer()}
    )
    def patch(self, request: Request, shipment_id: str):
        """
        update a shipment instance.
        """
        pass

    @swagger_auto_schema(
        tags=['SHIPMENTS'],
        operation_id="Delete a shipment",
        responses={400: ErrorResponseSerializer()}
    )
    def delete(self, request: Request, shipment_id: str):
        """
        delete a shipment instance.
        """
        pass


router.urls.append(path('shipments', ShipmentCoreView.as_view()))
router.urls.append(path('shipments/<str:pk>', ShipmentUpdateView.as_view()))
