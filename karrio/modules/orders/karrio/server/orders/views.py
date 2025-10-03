import logging

from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.serializers import (
    process_dictionaries_mutations,
    PaginatedResult,
)
from karrio.server.orders.router import router
from karrio.server.orders.serializers import (
    ErrorResponse,
    OrderStatus,
    OrderData,
    Order,
)
from karrio.server.orders.serializers.order import (
    OrderSerializer,
    OrderUpdateData,
    can_mutate_order,
)
from karrio.server.orders.filters import OrderFilters
import karrio.server.orders.models as models
import karrio.server.core.views.api as api
import karrio.server.openapi as openapi

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Orders = PaginatedResult("OrderList", Order)


class OrderList(api.GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilters
    serializer_class = Orders
    model = models.Order

    @openapi.extend_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listOrders"},
        summary="List all orders",
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

    @openapi.extend_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createOrder"},
        summary="Create an order",
        responses={
            201: Order(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
        request=OrderData(),
    )
    def post(self, request: Request):
        """
        Create a new order object.
        """
        order = OrderSerializer.map(data=request.data, context=request).save().instance

        return Response(Order(order).data, status=status.HTTP_201_CREATED)


class OrderDetail(api.APIView):

    @openapi.extend_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveOrder"},
        summary="Retrieve an order",
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

    @openapi.extend_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateOrder"},
        summary="Update an order",
        responses={
            200: Order(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        request=OrderUpdateData(),
    )
    def put(self, request: Request, pk: str):
        """
        This operation allows for updating properties of an order including `options` and `metadata`.
        It is not for editing the line items of an order.
        """
        order = models.Order.access_by(request).get(pk=pk)
        payload = OrderUpdateData.map(data=request.data).data

        can_mutate_order(order, update=True, payload=request.data)

        update = (
            OrderSerializer.map(
                order,
                context=request,
                data=process_dictionaries_mutations(
                    ["metadata", "options"], payload, order
                ),
            )
            .save()
            .instance
        )

        return Response(Order(update).data)

    @openapi.extend_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}dismiss",
        extensions={"x-operationId": "dismissOrder"},
        summary="Dismiss an order",
        deprecated=True,
        responses={
            200: Order(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """Dismiss an order from fulfillment."""
        order = models.Order.access_by(request).get(pk=pk)
        can_mutate_order(order, delete=True)

        order.status = OrderStatus.cancelled.value
        order.save(update_fields=["status"])

        return Response(Order(order).data)


class OrderCancel(api.APIView):

    @openapi.extend_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}cancel",
        extensions={"x-operationId": "cancelOrder"},
        summary="Cancel an order",
        responses={
            200: Order(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
        request=None,
    )
    def post(self, request: Request, pk: str):
        """Cancel an order."""
        order = models.Order.access_by(request).get(pk=pk)
        can_mutate_order(order, delete=True)

        order.status = OrderStatus.cancelled.value
        order.save(update_fields=["status"])

        return Response(Order(order).data)


router.urls.append(path("orders", OrderList.as_view(), name="order-list"))
router.urls.append(path("orders/<str:pk>", OrderDetail.as_view(), name="order-detail"))
router.urls.append(
    path("orders/<str:pk>/cancel", OrderCancel.as_view(), name="order-cancel")
)
