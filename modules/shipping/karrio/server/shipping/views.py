import logging

from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.shipping.router import router
import karrio.server.shipping.serializers as serializers
import karrio.server.shipping.filters as filters
import karrio.server.shipping.models as models
import karrio.server.core.views.api as api
import karrio.server.openapi as openapi

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&&$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
ShippingMethods = serializers.PaginatedResult(
    "ShippingMethodList", serializers.ShippingMethod
)


class ShippingMethodList(api.GenericAPIView):
    throttle_scope = "carrier_request"
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=25)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.ShippingMethodFilters
    serializer_class = ShippingMethods
    model = models.ShippingMethod

    @openapi.extend_schema(
        tags=["ShippingMethods"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listShippingMethods"},
        summary="List all shipping methods",
        parameters=filters.ShippingMethodFilters.parameters,
        responses={
            200: serializers.ShippingMethod(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, _: Request):
        """
        Retrieve all shipping methods.
        """
        methods = self.filter_queryset(self.get_queryset()).order_by("-created_at")
        response = self.paginate_queryset(
            serializers.ShippingMethod(methods, many=True).data
        )

        return self.get_paginated_response(response)


class BuyShippingMethodLabel(api.APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["ShippingMethods"],
        operation_id=f"{ENDPOINT_ID}order_label",
        extensions={"x-operationId": "orderLabel"},
        summary="Order shipping label",
        responses={
            201: serializers.ShippingLabelResponse(),
            400: serializers.ErrorResponse(),
            424: serializers.ErrorMessages(),
            500: serializers.ErrorResponse(),
        },
        request=serializers.ShipmentData(),
    )
    def post(self, request: Request, pk: str):
        """
        Order a shipping label for a shipping method.
        """
        method = models.ShippingMethod.access_by(request).get(pk=pk)
        data = serializers.ShipmentData.map(
            data={
                **request.data,
                **({"carrier_ids": [method.carrier_id]} if method.carrier_id else {}),
                "service": method.carrier_service,
                "options": {
                    **method.carrier_options,
                    **request.data.get("options", {}),
                },
            },
            context=request,
        ).data
        shipment = (
            serializers.ShipmentSerializer.map(data=data, context=request)
            .save()
            .instance
        )

        return Response(
            serializers.ShippingLabelResponse(shipment).data,
            status=status.HTTP_201_CREATED,
        )


router.urls.append(
    path(
        "shipping-methods",
        ShippingMethodList.as_view(),
        name="shipping-method-list",
    ),
)
router.urls.append(
    path(
        "shipping-methods/<str:pk>/labels",
        BuyShippingMethodLabel.as_view(),
        name="buy-method-label",
    )
)
