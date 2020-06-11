import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.serializers import (
    ErrorResponse as ErrorResponseSerializer, Address as AddressSerializer
)
from purpleserver.manager.router import router
from purpleserver.manager.models import Address

logger = logging.getLogger(__name__)


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class AddressList(AddressAPIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_summary="List all Addresses",
        responses={200: AddressSerializer(many=True), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request):
        """
        Retrieve all addresses.
        """
        addresses = request.user.address_set.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_summary="Create an Address",
        responses={200: AddressSerializer(), 400: ErrorResponseSerializer()}
    )
    def post(self, request: Request):
        """
        Create a new address.
        """
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Address.objects.create(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddressDetail(AddressAPIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id="addresses_retrieve",
        operation_summary="Retrieve an Address",
        responses={200: AddressSerializer(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve an address.
        """
        address = request.user.address_set.get(pk=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_summary="Update an Address",
        responses={200: AddressSerializer(), 400: ErrorResponseSerializer()}
    )
    def put(self, request: Request, pk: str):
        """
        update an address.
        """
        address = request.user.address_set.get(pk=pk)
        serializer = AddressSerializer(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        for key, val in serializer.validated_data:
            setattr(address, key, val)
        address.save()
        return Response(serializer.data)


router.urls.append(path('addresses', AddressList.as_view()))
router.urls.append(path('addresses/<str:pk>', AddressDetail.as_view()))
