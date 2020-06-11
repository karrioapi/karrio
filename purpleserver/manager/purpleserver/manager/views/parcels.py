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
    ErrorResponse as ErrorResponseSerializer, Parcel
)
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)


class ParcelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class ParcelCoreView(ParcelAPIView):

    @swagger_auto_schema(
        tags=['PARCELS'],
        operation_id="Retrieve all parcels",
        responses={400: ErrorResponseSerializer()}
    )
    def get(self, request: Request):
        """
        Retrieve all parcel instance.
        """
        pass

    @swagger_auto_schema(
        tags=['PARCELS'],
        operation_id="Create a parcel",
        responses={200: Parcel(), 400: ErrorResponseSerializer()}
    )
    def post(self, request: Request):
        """
        Create a new parcel instance.
        """
        pass


class ParcelUpdateView(ParcelAPIView):

    @swagger_auto_schema(
        tags=['PARCELS'],
        operation_id="Retrieve a parcel",
        responses={200: Parcel(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, parcel_id: str):
        """
        Retrieve a parcel instance.
        """
        pass

    @swagger_auto_schema(
        tags=['PARCELS'],
        operation_id="Update a parcel",
        responses={200: Parcel(), 400: ErrorResponseSerializer()}
    )
    def patch(self, request: Request, parcel_id: str):
        """
        update a parcel instance.
        """
        pass

    @swagger_auto_schema(
        tags=['PARCELS'],
        operation_id="Delete a parcel",
        responses={400: ErrorResponseSerializer()}
    )
    def delete(self, request: Request, parcel_id: str):
        """
        delete a parcel instance.
        """
        pass


router.urls.append(path('parcels', ParcelCoreView.as_view()))
router.urls.append(path('parcels/<str:pk>', ParcelUpdateView.as_view()))
