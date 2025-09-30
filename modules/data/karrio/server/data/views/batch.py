from django.urls import path
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.data.filters import BatchOperationFilter
import karrio.server.data.serializers as serializers
import karrio.server.data.models as models
import karrio.server.core.views.api as api
import karrio.server.openapi as openapi

ENDPOINT_ID = "&&&&$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
BatchOperations = serializers.PaginatedResult(
    "BatchOperations", serializers.BatchOperation
)


class BatchList(api.GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BatchOperationFilter
    serializer_class = BatchOperations
    model = models.BatchOperation

    @openapi.extend_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listBatchOperations"},
        summary="List all batch operations",
        responses={
            200: BatchOperations(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, _: Request):
        """Retrieve all batch operations. `Beta`"""

        batches = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(
            serializers.BatchOperation(batches, many=True).data
        )

        return self.get_paginated_response(response)


class BatchDetails(api.APIView):
    @openapi.extend_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveBatchOperation"},
        summary="Retrieve a batch operation",
        responses={
            200: serializers.BatchOperation(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """Retrieve a batch operation. `Beta`"""
        batch = models.BatchOperation.access_by(request).get(pk=pk)

        return Response(serializers.BatchOperation(batch).data)


urlpatterns = [
    path("batches/operations", BatchList.as_view(), name="batch-list"),
    path("batches/operations/<str:pk>", BatchDetails.as_view(), name="batch-details"),
]
