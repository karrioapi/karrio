import logging
from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.filters import UploadRecordFilter
from karrio.server.manager.router import router
from karrio.server.manager.serializers import (
    ErrorResponse,
    ErrorMessages,
    PaginatedResult,
    DocumentUploadData,
    DocumentUploadRecord,
    DocumentUploadSerializer,
    can_upload_shipment_document,
)
import karrio.server.manager.models as models
import karrio.server.openapi as openapi

ENDPOINT_ID = "$$$$$&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
DocumentUploadRecords = PaginatedResult("DocumentUploadRecords", DocumentUploadRecord)


class DocumentList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UploadRecordFilter
    serializer_class = DocumentUploadRecords
    model = models.DocumentUploadRecord

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}uploads",
        summary="List all upload records",
        parameters=UploadRecordFilter.parameters,
        responses={
            200: DocumentUploadRecords(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, _: Request):
        """
        Retrieve all shipping document upload records.
        """
        upload_records = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(
            DocumentUploadRecord(upload_records, many=True).data
        )

        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}upload",
        summary="Upload documents",
        responses={
            201: DocumentUploadRecord(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=DocumentUploadData(),
    )
    def post(self, request: Request):
        """Upload a shipping document."""
        shipment = (
            models.Shipment.access_by(request)
            .filter(
                pk=request.data.get("shipment_id"),
                selected_rate_carrier__isnull=False,
            )
            .first()
        )

        can_upload_shipment_document(shipment)

        upload_record = (
            DocumentUploadSerializer.map(
                getattr(shipment, "shipment_upload_record", None),
                data=request.data,
                context=request,
            )
            .save(shipment=shipment)
            .instance
        )

        return Response(
            DocumentUploadRecord(upload_record).data, status=status.HTTP_201_CREATED
        )


class DocumentDetails(APIView):
    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}retrieve_upload",
        summary="Retrieve upload record",
        responses={
            200: DocumentUploadRecord(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """Retrieve a shipping document upload record."""
        upload_record = models.UploadRecord.access_by(request).get(pk=pk)

        return Response(DocumentUploadRecord(upload_record).data)


router.urls.append(
    path(
        "documents/uploads",
        DocumentList.as_view(),
        name="document-upload-list",
    )
)
router.urls.append(
    path(
        "documents/uploads/<str:pk>",
        DocumentDetails.as_view(),
        name="document-upload-details",
    )
)
