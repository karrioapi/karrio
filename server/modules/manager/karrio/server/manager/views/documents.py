import logging
import rest_framework.status as status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.filters import UploadRecordFilter
from karrio.server.manager.router import router
from karrio.server.manager.serializers import (
    ErrorResponse,
    ErrorMessages,
    PaginatedResult,
    DocumentUploadData,
    SerializerDecorator,
    DocumentUploadRecord,
    DocumentUploadSerializer,
    can_upload_shipment_document,
)
import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
DocumentUploadRecords = PaginatedResult("DocumentUploadRecords", DocumentUploadRecord)


class DocumentList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UploadRecordFilter
    serializer_class = DocumentUploadRecords
    model = models.DocumentUploadRecord

    @swagger_auto_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all upload records",
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
        response = self.paginate_queryset(DocumentUploadRecord(upload_records, many=True).data)

        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}upload",
        operation_summary="Upload documents",
        responses={
            201: DocumentUploadRecord(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request_body=DocumentUploadData(),
    )
    def post(self, request: Request):
        """Upload a shipping document."""
        shipment = models.Shipment.access_by(request).filter(
            pk=request.data.get("shipment_id"),
            selected_rate_carrier__isnull=False,
        ).first()

        can_upload_shipment_document(shipment)

        upload_record = (
            SerializerDecorator[DocumentUploadSerializer](
                (shipment.shipment_upload_record if hasattr(shipment, "shipment_upload_record") else None),
                data=request.data,
                context=request,
            )
            .save(shipment=shipment)
            .instance
        )

        return Response(DocumentUploadRecord(upload_record).data, status=status.HTTP_201_CREATED)


class DocumentDetails(APIView):
    @swagger_auto_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve an upload record",
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


router.urls.append(path("documents", DocumentList.as_view(), name="document-list"))
router.urls.append(
    path("documents/<str:pk>", DocumentDetails.as_view(), name="document-details")
)
