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
from purpleserver.core.serializers import ShipmentStatus, ErrorResponse, CustomsData, Customs, Operation
from purpleserver.manager.serializers import (
    CustomsSerializer,
    CommodityData,
    CommoditySerializer,
    reset_related_shipment_rates
)
from purpleserver.manager.router import router
import purpleserver.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CustomsInfoList = PaginatedResult('CustomsList', Customs)


class CustomsList(GenericAPIView):
    serializer_class = Customs
    queryset = models.Customs.objects
    pagination_class = type('CustomPagination', (LimitOffsetPagination,), dict(default_limit=20))

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all customs info",
        responses={200: CustomsInfoList(), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored customs declarations.
        """
        customs_info = models.Customs.objects.access_with(request.user).all()
        serializer = Customs(customs_info, many=True)
        response = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a customs info",
        request_body=CustomsData(),
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new customs declaration.
        """
        customs = SerializerDecorator[CustomsSerializer](data=request.data, context_user=request.user).save().instance
        return Response(Customs(customs).data, status=status.HTTP_201_CREATED)


class CustomsDetail(APIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a customs info",
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve customs declaration.
        """
        address = models.Customs.objects.access_with(request.user).get(pk=pk)
        return Response(Customs(address).data)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a customs info",
        request_body=CustomsData(),
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing customs declaration.
        """
        customs = models.Customs.objects.access_with(request.user).get(pk=pk)
        shipment = customs.shipment_set.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this customs info has been 'purchased' and can no longer be modified",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        SerializerDecorator[CustomsSerializer](customs, data=request.data, context_user=request.user).save()
        reset_related_shipment_rates(shipment)
        return Response(Customs(customs).data)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}discard",
        operation_summary="Discard a customs info",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Discard a customs declaration.
        """
        customs = models.Customs.objects.access_with(request.user).get(pk=pk)
        shipment = customs.shipment_set.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this customs info has been 'purchased' and cannot be discarded",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        customs.delete(keep_parents=True)
        shipment.customs = None
        serializer = Operation(dict(operation="Discard customs info", success=True))
        reset_related_shipment_rates(shipment)
        return Response(serializer.data)


class CustomsCommodities(APIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}add_commodity",
        operation_summary="Add a commodity",
        responses={200: Customs(), 400: ErrorResponse()},
        request_body=CommodityData()
    )
    def post(self, request: Request, pk: str):
        """
        Add a customs commodity.
        """
        customs = models.Customs.objects.access_with(request.user).get(pk=pk)
        shipment = customs.shipment_set.first()

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The associated shipment is already 'purchased'",
                status_code=status.HTTP_409_CONFLICT, code='state_error'
            )

        commodity = SerializerDecorator[CommoditySerializer](
            data=request.data, context_user=request.user).save().instance
        customs.commodities.add(commodity)
        return Response(Customs(commodity.customs_set.first()).data)


class DiscardCommodities(APIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}discard_commodity",
        operation_summary="Discard a commodity",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str, ck: str):
        """
        Discard a customs commodity.
        """
        customs = models.Customs.objects.access_with(request.user).get(pk=pk)
        shipment = customs.shipment_set.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this customs info has been 'purchased' and cannot be modified",
                status_code=status.HTTP_409_CONFLICT, code='state_error'
            )

        commodity = customs.commodities.get(pk=ck)
        commodity.delete(keep_parents=True)
        serializer = Operation(dict(operation="Discard customs commodity", success=True))
        return Response(serializer.data)


router.urls.append(path('customs_info', CustomsList.as_view(), name="customs-list"))
router.urls.append(path('customs_info/<str:pk>', CustomsDetail.as_view(), name="customs-details"))
router.urls.append(path('customs_info/<str:pk>/commodities', CustomsCommodities.as_view(), name="customs-commodities"))
router.urls.append(path('customs_info/<str:pk>/commodities/<str:ck>', DiscardCommodities.as_view(), name="commodities"))
