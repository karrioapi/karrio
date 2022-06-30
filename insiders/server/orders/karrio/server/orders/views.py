import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from karrio.core.utils import DP
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.serializers import (
    SerializerDecorator,
    PaginatedResult,
    process_dictionaries_mutations,
)
from karrio.server.orders.router import router
from karrio.server.orders.serializers import (
    TestFilters,
    OrderStatus,
    ErrorResponse,
    Order,
    OrderData,
)
from karrio.server.orders.serializers.order import (
    OrderSerializer,
    OrderUpdateData,
    can_mutate_order,
)
from karrio.server.orders.filters import OrderFilters
import karrio.server.orders.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Orders = PaginatedResult("OrderList", Order)


class OrderList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilters
    serializer_class = Orders
    model = models.Order

    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all orders",
        responses={
            200: Orders(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all orders.
        """
        orders = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(Order(orders, many=True).data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create an order",
        responses={
            201: Order(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
        request_body=OrderData(),
        query_serializer=TestFilters(),
    )
    def post(self, request: Request):
        """
        Create a new order object.
        """
        order = (
            SerializerDecorator[OrderSerializer](data=request.data, context=request)
            .save(mode_filter=request.query_params)
            .instance
        )

        return Response(Order(order).data, status=status.HTTP_201_CREATED)


class OrderDetail(APIView):
    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve an order",
        responses={
            200: Order(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve an order.
        """
        order = models.Order.access_by(request).get(pk=pk)

        return Response(Order(order).data)

    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update an order",
        responses={
            200: Order(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        request_body=OrderUpdateData(),
    )
    def put(self, request: Request, pk: str):
        """
        This operation allows for updating properties of an order including `options` and `metadata`.
        It is not for editing the line items of an order.
        """
        order = models.Order.access_by(request).get(pk=pk)
        can_mutate_order(order, update=True)

        payload = SerializerDecorator[OrderUpdateData](data=request.data).data
        SerializerDecorator[OrderSerializer](
            order,
            context=request,
            data=process_dictionaries_mutations(
                ["metadata", "options"], payload, order
            ),
        ).save()

        return Response(Order(order).data)

    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}cancel",
        operation_summary="Cancel an order",
        responses={
            200: Order(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """
        Cancel an order.
        """
        order = models.Order.access_by(request).get(pk=pk)
        can_mutate_order(order, delete=True)

        order.status = OrderStatus.cancelled.value
        order.save(update_fields=["status"])

        return Response(Order(order).data)


router.urls.append(path("orders", OrderList.as_view(), name="order-list"))
router.urls.append(path("orders/<str:pk>", OrderDetail.as_view(), name="order-detail"))
