"""
Product REST API Views

Provides full CRUD operations for product templates (commodities with meta.label).
Products are reusable commodity templates for customs declarations and shipment items.

Endpoints:
    GET    /v1/products          - List all products
    POST   /v1/products          - Create a new product
    GET    /v1/products/<pk>     - Retrieve a product
    PATCH  /v1/products/<pk>     - Update a product
    DELETE /v1/products/<pk>     - Delete a product
"""
import logging

from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from karrio.server.manager.router import router
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.manager.serializers import (
    PaginatedResult,
    ErrorResponse,
    CommodityData,
    Commodity,
    CommoditySerializer,
    can_mutate_commodity,
)
import karrio.server.manager.models as models
import karrio.server.openapi as openapi

logger = logging.getLogger(__name__)

# Unique endpoint ID for OpenAPI operation IDs
ENDPOINT_ID = "$&"  # This endpoint id is used to make operation ids unique make sure not to duplicate

# Response serializer for paginated list
Products = PaginatedResult("ProductList", Commodity)


class ProductList(GenericAPIView):
    """
    List and create product templates.

    Products are commodity templates that can be reused across shipments
    and customs declarations. They are identified by having a `meta.label` field.
    """

    queryset = models.Commodity.objects
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    serializer_class = Products

    @openapi.extend_schema(
        tags=["Products"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listProducts"},
        summary="List all products",
        description="""
        Retrieve all product templates.

        Products are reusable commodity definitions that can be used
        in customs declarations and shipment items.

        Query Parameters:
        - label: Filter by meta.label (case-insensitive contains)
        - keyword: Search across label, title, sku, description, hs_code
        - usage: Filter by meta.usage (exact match in array)
        """,
        responses={
            200: Products(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all stored products.
        """
        from django.db.models import Q

        # Filter to only show product templates (those with meta.label)
        # Also exclude products linked to other entities (parcels, customs)
        queryset = models.Commodity.access_by(request).filter(
            meta__label__isnull=False,  # Only templates with labels
            **{
                f"{prop}__isnull": True
                for prop in models.Commodity.HIDDEN_PROPS
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
                | Q(title__icontains=keyword)
                | Q(sku__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(hs_code__icontains=keyword)
            )

        if usage:
            queryset = queryset.filter(meta__usage__contains=usage)

        serializer = Commodity(queryset, many=True)
        response = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Products"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createProduct"},
        summary="Create a product",
        description="""
        Create a new product template.

        Products must include a `meta.label` to be identified as templates.
        """,
        request=CommodityData(),
        responses={
            201: Commodity(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """
        Create a new product template.
        """
        # Ensure meta.label is set for product templates
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)

        # Validate that meta.label is provided
        meta = data.get("meta", {}) or {}
        if not meta.get("label"):
            return Response(
                {"error": "Product templates require a meta.label field"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = (
            CommoditySerializer.map(data=data, context=request).save().instance
        )
        return Response(Commodity(product).data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    """
    Retrieve, update, and delete individual product templates.
    """

    @openapi.extend_schema(
        tags=["Products"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveProduct"},
        summary="Retrieve a product",
        description="Retrieve a product template by ID.",
        responses={
            200: Commodity(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a product template.
        """
        product = models.Commodity.access_by(request).get(pk=pk)
        return Response(Commodity(product).data)

    @openapi.extend_schema(
        tags=["Products"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateProduct"},
        summary="Update a product",
        description="Update an existing product template.",
        request=CommodityData(),
        responses={
            200: Commodity(),
            400: ErrorResponse(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def patch(self, request: Request, pk: str):
        """
        Update an existing product template.
        """
        product = models.Commodity.access_by(request).get(pk=pk)
        can_mutate_commodity(product, update=True)

        CommoditySerializer.map(product, data=request.data).save()

        return Response(Commodity(product).data)

    @openapi.extend_schema(
        tags=["Products"],
        operation_id=f"{ENDPOINT_ID}discard",
        extensions={"x-operationId": "discardProduct"},
        summary="Remove a product",
        description="Delete a product template.",
        responses={
            200: Commodity(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a product template.
        """
        product = models.Commodity.access_by(request).get(pk=pk)
        can_mutate_commodity(product, update=True, delete=True)

        product.delete(keep_parents=True)

        return Response(Commodity(product).data)


# Register routes with the router
router.urls.append(path("products", ProductList.as_view(), name="product-list"))
router.urls.append(
    path("products/<str:pk>", ProductDetail.as_view(), name="product-details")
)
