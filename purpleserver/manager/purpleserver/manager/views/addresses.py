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
    ErrorResponse as ErrorResponseSerializer, Address
)
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class AddressCoreView(AddressAPIView):

    @swagger_auto_schema(
        tags=['ADDRESSES'],
        operation_id="Retrieve all addresses",
        responses={400: ErrorResponseSerializer()}
    )
    def get(self, request: Request):
        """
        Retrieve all address instance.
        """
        pass

    @swagger_auto_schema(
        tags=['ADDRESSES'],
        operation_id="Create an address",
        responses={200: Address(), 400: ErrorResponseSerializer()}
    )
    def post(self, request: Request):
        """
        Create a new address instance.
        """
        pass


class AddressUpdateView(AddressAPIView):

    @swagger_auto_schema(
        tags=['ADDRESSES'],
        operation_id="Retrieve an address",
        responses={200: Address(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, address_id: str):
        """
        Retrieve a address instance.
        """
        pass

    @swagger_auto_schema(
        tags=['ADDRESSES'],
        operation_id="Update an address",
        responses={200: Address(), 400: ErrorResponseSerializer()}
    )
    def patch(self, request: Request, address_id: str):
        """
        update a address instance.
        """
        pass

    @swagger_auto_schema(
        tags=['ADDRESSES'],
        operation_id="Delete an address",
        responses={400: ErrorResponseSerializer()}
    )
    def delete(self, request: Request, address_id: str):
        """
        delete a address instance.
        """
        pass


router.urls.append(path('addresses', AddressCoreView.as_view()))
router.urls.append(path('addresses/<str:pk>', AddressUpdateView.as_view()))
