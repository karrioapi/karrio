import logging

from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.manager.serializers import (
    PaginatedResult,
    ErrorResponse,
    AddressData,
    Address,
    AddressSerializer,
    can_mutate_address,
)
from karrio.server.manager.router import router
import karrio.server.manager.models as models
import karrio.server.openapi as openapi


ENDPOINT_ID = "$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
Addresses = PaginatedResult("AddressList", Address)


class AddressList(GenericAPIView):
    queryset = models.Address.objects
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    serializer_class = Addresses

    @openapi.extend_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listAddresses"},
        summary="List all addresses",
        responses={
            200: Addresses(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all addresses.
        """
        addresses = models.Address.access_by(request).filter(
            **{
                f"{prop}__isnull": True
                for prop in models.Address.HIDDEN_PROPS
                if prop != "org"
            }
        )
        response = self.paginate_queryset(Address(addresses, many=True).data)
        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createAddress"},
        summary="Create an address",
        request=AddressData(),
        responses={
            201: Address(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """
        Create a new address.
        """
        address = (
            AddressSerializer.map(data=request.data, context=request).save().instance
        )
        return Response(Address(address).data, status=status.HTTP_201_CREATED)


class AddressDetail(APIView):

    @openapi.extend_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveAddress"},
        summary="Retrieve an address",
        responses={
            200: Address(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve an address.
        """
        address = models.Address.access_by(request).get(pk=pk)
        return Response(Address(address).data)

    @openapi.extend_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateAddress"},
        summary="Update an address",
        request=AddressData(),
        responses={
            200: Address(),
            400: ErrorResponse(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def patch(self, request: Request, pk: str):
        """
        update an address.
        """
        address = models.Address.access_by(request).get(pk=pk)
        can_mutate_address(address, update=True)

        AddressSerializer.map(address, data=request.data).save()

        return Response(Address(address).data)

    @openapi.extend_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}discard",
        extensions={"x-operationId": "discardAddress"},
        summary="Discard an address",
        responses={
            200: Address(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """
        Discard an address.
        """
        address = models.Address.access_by(request).get(pk=pk)
        can_mutate_address(address, update=True, delete=True)

        address.delete(keep_parents=True)

        return Response(Address(address).data)


router.urls.append(path("addresses", AddressList.as_view(), name="address-list"))
router.urls.append(
    path("addresses/<str:pk>", AddressDetail.as_view(), name="address-details")
)
