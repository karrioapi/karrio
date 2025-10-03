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
    CustomsData,
    Customs,
    CustomsSerializer,
    can_mutate_customs,
)
from karrio.server.manager.router import router
import karrio.server.manager.models as models
import karrio.server.openapi as openapi

ENDPOINT_ID = "$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
CustomsInfoList = PaginatedResult("CustomsList", Customs)


class CustomsList(GenericAPIView):
    queryset = models.Customs.objects
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    serializer_class = CustomsInfoList

    @openapi.extend_schema(
        exclude=True,
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listCustomsInfo"},
        summary="List all customs info",
        responses={
            200: CustomsInfoList(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
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

    @openapi.extend_schema(
        exclude=True,
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createCustomsInfo"},
        summary="Create a customs info",
        request=CustomsData(),
        responses={
            201: Customs(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """
        Create a new customs declaration.
        """
        customs = (
            CustomsSerializer.map(data=request.data, context=request).save().instance
        )
        return Response(Customs(customs).data, status=status.HTTP_201_CREATED)


class CustomsDetail(APIView):

    @openapi.extend_schema(
        exclude=True,
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveCustomsInfo"},
        summary="Retrieve a customs info",
        responses={
            200: Customs(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve customs declaration.
        """
        address = models.Customs.access_by(request).get(pk=pk)
        return Response(Customs(address).data)

    @openapi.extend_schema(
        exclude=True,
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateCustomsInfo"},
        summary="Update a customs info",
        request=CustomsData(),
        responses={
            200: Customs(),
            400: ErrorResponse(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing customs declaration.
        """
        customs = models.Customs.access_by(request).get(pk=pk)
        can_mutate_customs(customs)

        CustomsSerializer.map(customs, data=request.data, context=request).save()

        return Response(Customs(customs).data)

    @openapi.extend_schema(
        exclude=True,
        tags=["Customs"],
        operation_id=f"{ENDPOINT_ID}discard",
        extensions={"x-operationId": "discardCustomsInfo"},
        summary="Discard a customs info",
        responses={
            200: Customs(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
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
