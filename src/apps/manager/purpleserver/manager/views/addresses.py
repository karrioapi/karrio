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

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import ErrorResponse, AddressData, Address
from purpleserver.manager.serializers import AddressSerializer
from purpleserver.manager.router import router


logger = logging.getLogger(__name__)
ENDPOINT_ID = "$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class AddressList(AddressAPIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all Addresses",
        responses={200: Address(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all addresses.
        """
        addresses = request.user.address_set.all()
        return Response(Address(addresses, many=True).data)

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create an Address",
        request_body=AddressData(),
        responses={200: Address(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new address.
        """
        address = SerializerDecorator[AddressSerializer](data=request.data).save(user=request.user).instance
        return Response(Address(address).data, status=status.HTTP_201_CREATED)


class AddressDetail(AddressAPIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve an Address",
        responses={200: Address(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve an address.
        """
        address = request.user.address_set.get(pk=pk)
        return Response(Address(address).data)

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update an Address",
        request_body=AddressData(),
        responses={200: Address(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        update an address.
        """
        address = request.user.address_set.get(pk=pk)
        SerializerDecorator[AddressSerializer](address, data=request.data).save()
        return Response(Address(address).data)


router.urls.append(path('addresses', AddressList.as_view(), name="address-list"))
router.urls.append(path('addresses/<str:pk>', AddressDetail.as_view(), name="address-details"))
