import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers

from drf_yasg import openapi
from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from purplship.server.core.views.api import GenericAPIView, APIView
from purplship.server.core.exceptions import PurplshipAPIException
from purplship.server.serializers import SerializerDecorator, PaginatedResult
from purplship.server.orders.router import router
from purplship.server.orders.serializers import (
    TestFilters,
    OrderStatus,
    ErrorResponse,
    Order,
    OrderData,
    ShipmentSerializer,
    OrderShipmentData,
)
from purplship.server.orders.serializers.order import (
    OrderSerializer,
    shipment_has_order_line_items,
)
import purplship.server.orders.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Orders = PaginatedResult("OrderList", Order)


class OrderFilters(filters.FilterSet):
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    parameters = [
        openapi.Parameter("test_mode", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        openapi.Parameter(
            "status",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=[c.value for c in list(OrderStatus)],
        ),
        openapi.Parameter(
            "created_before",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="DateTime in format `YYYY-MM-DD H:M:S.fz`",
        ),
        openapi.Parameter(
            "created_after",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="DateTime in format `YYYY-MM-DD H:M:S.fz`",
        ),
    ]

    class Meta:
        model = models.Order
        fields = ["test_mode", "status"]


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
        responses={200: Orders(), 400: ErrorResponse()},
        manual_parameters=OrderFilters.parameters,
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
        responses={200: Order(), 400: ErrorResponse()},
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
        responses={200: Order(), 400: ErrorResponse()},
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve an order.
        """
        order = models.Order.access_by(request).get(pk=pk)

        return Response(Order(order).data)

    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}cancel",
        operation_summary="Cancel an order",
        responses={200: Order(), 400: ErrorResponse()},
    )
    def delete(self, request: Request, pk: str):
        """
        Cancel an order.
        """
        order = models.Order.access_by(request).get(pk=pk)

        if order.status in [
            OrderStatus.delivered.value,
            OrderStatus.cancelled.value,
        ]:
            raise PurplshipAPIException(
                f"The order is '{order.status}' and can not be cancelled anymore...",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        if order.status in [
            OrderStatus.fulfilled.value,
            OrderStatus.partially_fulfilled.value,
        ]:
            raise PurplshipAPIException(
                f"The order is '{order.status}' please cancel all related shipments before...",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        order.status = OrderStatus.cancelled.value
        order.save(update_fields=["status"])

        return Response(Order(order).data)


class OrderShipments(APIView):
    @swagger_auto_schema(
        tags=["Orders"],
        operation_id=f"{ENDPOINT_ID}add_shipment",
        operation_summary="Add a shipment",
        responses={200: Order(), 400: ErrorResponse()},
        request_body=OrderShipmentData(),
    )
    def post(self, request: Request, pk: str):
        """
        Add a shipment to an order.
        """
        order = (
            models.Order.access_by(request)
            .exclude(status=OrderStatus.cancelled.value)
            .get(pk=pk)
        )

        if order.status == OrderStatus.fulfilled.value:
            raise PurplshipAPIException(
                f"The order is '{order.status}', no additional shipment can be added.",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        serializer = SerializerDecorator[ShipmentSerializer](
            context=request,
            data={
                **dict(recipient=Order(order).data["shipping_address"]),
                **SerializerDecorator[OrderShipmentData](data=request.data).data,
            },
        )

        if not shipment_has_order_line_items(order, serializer.data):
            raise PurplshipAPIException(
                f"The shipment does not contain any line items from the targetted order.",
                code="invalid",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        shipment = serializer.save(carrier_filter=dict(test=order.test_mode))

        # Update order state
        SerializerDecorator[OrderSerializer](order, data={}, context=request).save(
            shipments=[shipment.instance]
        )

        return Response(Order(order).data, status=status.HTTP_201_CREATED)


router.urls.append(path("orders", OrderList.as_view(), name="order-list"))
router.urls.append(path("orders/<str:pk>", OrderDetail.as_view(), name="order-detail"))
router.urls.append(
    path("orders/<str:pk>/shipments", OrderShipments.as_view(), name="order-shipments")
)
