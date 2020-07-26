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

from purpleserver.core.utils import validate_and_save
from purpleserver.core.serializers import ErrorResponse, AddressData, Address
from purpleserver.manager.serializers import AddressSerializer
from purpleserver.manager.router import router


logger = logging.getLogger(__name__)


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class AddressList(AddressAPIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id="list_addresses",
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
        operation_id="create_address",
        operation_summary="Create an Address",
        request_body=AddressData(),
        responses={200: Address(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new address.
        """
        address = validate_and_save(AddressSerializer, request.data, user=request.user)
        return Response(Address(address).data, status=status.HTTP_201_CREATED)


class AddressDetail(AddressAPIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id="retrieve_address",
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
        operation_id="update_address",
        operation_summary="Update an Address",
        request_body=AddressData(),
        responses={200: Address(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        update an address.
        """
        address = request.user.address_set.get(pk=pk)
        validate_and_save(AddressSerializer, request.data, instance=address)
        return Response(Address(address).data)


router.urls.append(path('addresses', AddressList.as_view(), name="address-list"))
router.urls.append(path('addresses/<str:pk>', AddressDetail.as_view(), name="address-details"))
