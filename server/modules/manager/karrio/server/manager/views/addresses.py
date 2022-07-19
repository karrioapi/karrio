import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.manager.serializers import (
    SerializerDecorator,
    PaginatedResult,
    ErrorResponse,
    AddressData,
    Address,
    AddressSerializer,
    can_mutate_address,
)
from karrio.server.manager.router import router
from karrio.server.manager import models


logger = logging.getLogger(__name__)
ENDPOINT_ID = "$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Addresses = PaginatedResult("AddressList", Address)


class AddressList(GenericAPIView):
    queryset = models.Address.objects
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    serializer_class = Addresses

    @swagger_auto_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all addresses",
        responses={
            200: Addresses(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request GET \\
                  --url '/v1/addresses' \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
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

    @swagger_auto_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create an address",
        request_body=AddressData(),
        responses={
            201: Address(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request POST \\
                  --url /v1/addresses \\
                  --header 'Authorization: Token <API_KEY>' \\
                  --header 'Content-Type: application/json' \\
                  --data '{
                    "address_line1": "125 Church St",
                    "person_name": "John Doe",
                    "company_name": "A corp.",
                    "phone_number": "+1 514 000 0000",
                    "city": "Moncton",
                    "country_code": "CA",
                    "postal_code": "E1C4Z8",
                    "residential": false,
                    "state_code": "NB"
                }'
                """,
            }
        ],
    )
    def post(self, request: Request):
        """
        Create a new address.
        """
        address = (
            SerializerDecorator[AddressSerializer](data=request.data, context=request)
            .save()
            .instance
        )
        return Response(Address(address).data, status=status.HTTP_201_CREATED)


class AddressDetail(APIView):
    @swagger_auto_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve an address",
        responses={
            200: Address(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request GET \\
                  --url /v1/addresses/<ADDRESS_ID> \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve an address.
        """
        address = models.Address.access_by(request).get(pk=pk)
        return Response(Address(address).data)

    @swagger_auto_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update an address",
        request_body=AddressData(),
        responses={
            200: Address(),
            400: ErrorResponse(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request PATCH \\
                  --url /v1/addresses/<ADDRESS_ID> \\
                  --header 'Authorization: Token <API_KEY>' \\
                  --header 'Content-Type: application/json' \\
                  --data '{
                    "city": "Pierrefonds"
                }'
                """,
            }
        ],
    )
    def patch(self, request: Request, pk: str):
        """
        update an address.
        """
        address = models.Address.access_by(request).get(pk=pk)
        can_mutate_address(address, update=True)

        SerializerDecorator[AddressSerializer](address, data=request.data).save()

        return Response(Address(address).data)

    @swagger_auto_schema(
        tags=["Addresses"],
        operation_id=f"{ENDPOINT_ID}discard",
        operation_summary="Discard an address",
        responses={
            200: Address(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request DELETE \\
                  --url /v1/addresses/<ADDRESS_ID> \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
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
