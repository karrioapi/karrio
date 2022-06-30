from django.urls import path
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

import karrio.server.core.views.api as api
import karrio.server.data.models as models
import karrio.server.data.serializers as serializers

ENDPOINT_ID = "&&&&$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
BatchOperations = serializers.PaginatedResult(
    "BatchOperations", serializers.BatchOperation
)


class BatchList(api.GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = BatchOperations
    model = models.BatchOperation

    @swagger_auto_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all batch operations",
        responses={
            200: BatchOperations(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, _: Request):
        """
        Retrieve all batch operations.
        """

        batches = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(
            serializers.BatchOperation(batches, many=True).data
        )

        return self.get_paginated_response(response)


class BatchDetails(api.APIView):
    @swagger_auto_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a batch operation",
        responses={
            200: serializers.BatchOperation(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """Retrieve a batch operation."""
        batch = models.BatchOperation.access_by(request).get(pk=pk)

        return Response(serializers.BatchOperation(batch).data)


urlpatterns = [
    path("batches", BatchList.as_view(), name="batch-list"),
    path("batches/<str:pk>", BatchDetails.as_view(), name="batch-details"),
]
