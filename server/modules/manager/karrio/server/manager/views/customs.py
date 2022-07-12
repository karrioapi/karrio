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
    CustomsData,
    Customs,
    CustomsSerializer,
    can_mutate_customs,
)
from karrio.server.manager.router import router
import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CustomsInfoList = PaginatedResult("CustomsList", Customs)


class CustomsList(GenericAPIView):
    queryset = models.Customs.objects
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    serializer_class = CustomsInfoList

    @swagger_auto_schema(
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all customs info",
        responses={
            200: CustomsInfoList(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request GET \\
                  --url '/v1/customs_info' \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
    )
    def get(self, request: Request):
        """
        Retrieve all stored customs declarations.
        """
        customs_info = models.Customs.access_by(request).filter(
            **{
                f"{prop}__isnull": True
                for prop in models.Customs.HIDDEN_PROPS
                if prop != "org"
            }
        )
        serializer = Customs(customs_info, many=True)
        response = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a customs info",
        request_body=CustomsData(),
        responses={
            201: Customs(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request POST \\
                  --url /v1/customs_info \\
                  --header 'Authorization: Token <API_KEY>' \\
                  --header 'Content-Type: application/json' \\
                  --data '{
                    "content_type": "merchandise",
                    "incoterm": "DDU",
                    "commodities": [
                      {
                        "weight": 2,
                        "weight_unit": "KG",
                        "quantity": 1,
                        "sku": "XXXXX0000123",
                        "value_amount": 30,
                        "value_currency": "USD",
                        "origin_country": "JM"
                      }
                    ],
                    "duty": {
                      "paid_by": "recipient",
                      "currency": "USD",
                      "declared_value": 60,
                    },
                    "certify": true,
                    "signer": "Kex",
                  }'
                """,
            }
        ],
    )
    def post(self, request: Request):
        """
        Create a new customs declaration.
        """
        customs = (
            SerializerDecorator[CustomsSerializer](data=request.data, context=request)
            .save()
            .instance
        )
        return Response(Customs(customs).data, status=status.HTTP_201_CREATED)


class CustomsDetail(APIView):
    @swagger_auto_schema(
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a customs info",
        responses={
            200: Customs(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request GET \\
                  --url /v1/customs_info/<CUSTOMS_INFO_ID> \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve customs declaration.
        """
        address = models.Customs.access_by(request).get(pk=pk)
        return Response(Customs(address).data)

    @swagger_auto_schema(
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a customs info",
        request_body=CustomsData(),
        responses={
            200: Customs(),
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
                  --url /v1/customs_info/<CUSTOMS_INFO_ID> \\
                  --header 'Authorization: Token <API_KEY>' \\
                  --header 'Content-Type: application/json' \\
                  --data '{
                    "content_type": "merchandise",
                    "duty": {
                      "paid_by": "recipient",
                      "currency": "CAD",
                      "declared_value": 100,
                    }
                  }'
                """,
            }
        ],
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing customs declaration.
        """
        customs = models.Customs.access_by(request).get(pk=pk)
        can_mutate_customs(customs)

        SerializerDecorator[CustomsSerializer](
            customs, data=request.data, context=request
        ).save()

        return Response(Customs(customs).data)

    @swagger_auto_schema(
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}discard",
        operation_summary="Discard a customs info",
        responses={
            200: Customs(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request DELETE \\
                  --url /v1/customs_info/<CUSTOMS_INFO_ID> \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
    )
    def delete(self, request: Request, pk: str):
        """
        Discard a customs declaration.
        """
        customs = models.Customs.access_by(request).get(pk=pk)
        can_mutate_customs(customs)

        customs.delete(keep_parents=True)

        return Response(Customs(customs).data)


router.urls.append(path("customs_info", CustomsList.as_view(), name="customs-list"))
router.urls.append(
    path("customs_info/<str:pk>", CustomsDetail.as_view(), name="customs-details")
)
