from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from karrio.server.core.logging import logger
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
        description="""
        Retrieve all addresses.

        Query Parameters:
        - label: Filter by meta.label (case-insensitive contains)
        - keyword: Search across label, address fields, contact info
        - usage: Filter by meta.usage (exact match in array)
        """,
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
        from django.db.models import Q

        queryset = models.Address.access_by(request).filter(
            **{
                f"{prop}__isnull": True
                for prop in models.Address.HIDDEN_PROPS
                if prop != "org"
            }
        )

        # Apply query parameter filters
        label = request.query_params.get("label")
        keyword = request.query_params.get("keyword")
        usage = request.query_params.get("usage")

        if label:
            queryset = queryset.filter(meta__label__icontains=label)

        if keyword:
            queryset = queryset.filter(
                Q(meta__label__icontains=keyword)
                | Q(address_line1__icontains=keyword)
                | Q(address_line2__icontains=keyword)
                | Q(postal_code__icontains=keyword)
                | Q(person_name__icontains=keyword)
                | Q(company_name__icontains=keyword)
                | Q(country_code__icontains=keyword)
                | Q(city__icontains=keyword)
                | Q(email__icontains=keyword)
                | Q(phone_number__icontains=keyword)
            )

        if usage:
            queryset = queryset.filter(meta__usage__contains=usage)

        response = self.paginate_queryset(Address(queryset, many=True).data)
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
