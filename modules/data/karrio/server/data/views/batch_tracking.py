from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

import karrio.server.data.serializers as serializers
import karrio.server.core.views.api as api
import karrio.server.openapi as openapi

ENDPOINT_ID = "&&&&$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class BatchList(api.APIView):
    @openapi.extend_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}create_trackers",
        summary="Create tracker batch",
        responses={
            200: serializers.BatchOperation(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        request=serializers.BatchTrackerData(),
    )
    def post(self, request: Request):
        """Create tracker batch. `Beta`"""
        operation = (
            serializers.BatchTrackerData.map(data=request.data, context=request)
            .save()
            .instance
        )

        return Response(
            serializers.BatchOperation(operation).data, status=status.HTTP_201_CREATED
        )


urlpatterns = [
    path("batches/trackers", BatchList.as_view(), name="batch-trackers"),
]
