import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.utils import SerializerDecorator, PaginatedResult
from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.core.serializers import ShipmentStatus, ErrorResponse, AddressData, Address
from purpleserver.manager.serializers import AddressSerializer, reset_related_shipment_rates
from purpleserver.manager.router import router


logger = logging.getLogger(__name__)
ENDPOINT_ID = "$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Addresses = PaginatedResult('AddressList', Address)


class AddressList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 20

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all addresses",
        responses={200: Addresses(), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all addresses.
        """
        addresses = request.user.address_set.all()
        response = self.paginate_queryset(Address(addresses, many=True).data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create an address",
        request_body=AddressData(),
        responses={200: Address(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new address.
        """
        address = SerializerDecorator[AddressSerializer](data=request.data).save(created_by=request.user).instance
        return Response(Address(address).data, status=status.HTTP_201_CREATED)


class AddressDetail(APIView):

    @swagger_auto_schema(
        tags=['Addresses'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve an address",
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
        operation_summary="Update an address",
        request_body=AddressData(),
        responses={200: Address(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        update an address.
        """
        address = request.user.address_set.get(pk=pk)
        shipment = address.shipper.first() or address.recipient.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this address has been 'purchased' and can no longer be modified",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        SerializerDecorator[AddressSerializer](address, data=request.data).save()
        reset_related_shipment_rates(shipment)
        return Response(Address(address).data)


router.urls.append(path('addresses', AddressList.as_view(), name="address-list"))
router.urls.append(path('addresses/<str:pk>', AddressDetail.as_view(), name="address-details"))
