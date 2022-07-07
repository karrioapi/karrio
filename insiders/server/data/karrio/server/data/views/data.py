import io
from django.http import JsonResponse
from django.urls import re_path, path
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import karrio.server.core.views.api as api
import karrio.server.data.serializers as serializers
import karrio.server.data.resources as resources
from karrio.server.data.serializers.data import ImportDataSerializer

ENDPOINT_ID = "&&&&$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
DataImportParameters = [
    openapi.Parameter(
        name="resource_type",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        enum=[e.name for e in list(serializers.ResourceType)],
        description="The type of the resource to import",
    ),
    openapi.Parameter(
        "data_template",
        in_=openapi.IN_FORM,
        type=openapi.TYPE_STRING,
        required=False,
        description="""
        A data template slug to use for the import.

        **When nothing is specified, the system default headers are expected.**
        """,
    ),
    openapi.Parameter(name="data_file", in_=openapi.IN_FORM, type=openapi.TYPE_FILE),
]


class DataImport(api.BaseAPIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=["Data"],
        operation_id=f"{ENDPOINT_ID}import_file",
        operation_summary="Import data files",
        responses={
            202: serializers.BatchOperation(),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        manual_parameters=DataImportParameters,
    )
    def post(self, request: Request):
        """Import csv, xls and xlsx data files for:
        - tracking data
        - orders data
        - shipments data
        - billing data (soon)

        **This operation will return a batch operation that you can poll to follow
        the import progression.**
        """
        operation = (
            serializers.SerializerDecorator[ImportDataSerializer](
                data=request.data, context=request
            )
            .save()
            .instance
        )

        return Response(
            serializers.BatchOperation(operation).data, status=status.HTTP_202_ACCEPTED
        )


DataExportParameters = [
    openapi.Parameter(
        name="resource_type",
        in_=openapi.IN_PATH,
        type=openapi.TYPE_STRING,
        enum=[e.name for e in list(serializers.ResourceType)],
    ),
    openapi.Parameter(
        name="export_format",
        in_=openapi.IN_PATH,
        type=openapi.TYPE_STRING,
        enum=[e.name for e in list(serializers.ResourceType)],
    ),
    openapi.Parameter(
        "data_template",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
        description="""
        A data template slug to use for the import.

        **When nothing is specified, the system default headers are expected.**
        """,
    ),
]


class DataExport(api.LoginRequiredView, VirtualDownloadView):
    @swagger_auto_schema(
        tags=["Data"],
        operation_id=f"{ENDPOINT_ID}export_file",
        operation_summary="Export data files",
        responses={
            200: openapi.Schema(type=openapi.TYPE_FILE),
            409: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        manual_parameters=DataExportParameters,
    )
    def get(
        self,
        request: Request,
        resource_type: str = "orders",
        export_format: str = "csv",
        **kwargs,
    ):
        try:
            """Generate a file to export."""
            query_params = request.GET
            self.attachment = "download" in query_params
            self.resource = resource_type
            self.format = export_format

            self.dataset = resources.export(
                resource_type, query_params, context=request
            )

            response = super(DataExport, self).get(request, **kwargs)
            response["X-Frame-Options"] = "ALLOWALL"
            return response
        except Exception as e:
            return JsonResponse(
                dict(errors=[{"message": str(e)}]),
                status=status.HTTP_409_CONFLICT,
            )

    def get_file(self):
        content = getattr(self.dataset, self.format, "")
        buffer = io.StringIO() if type(content) == str else io.BytesIO()
        buffer.write(content)

        return ContentFile(buffer.getvalue(), name=f"{self.resource}.{self.format}")


urlpatterns = [
    path("data/import", DataImport.as_view(), name="data-import"),
    re_path(
        r"^data/export/(?P<resource_type>\w+).(?P<export_format>\w+)",
        csrf_exempt(DataExport.as_view()),
        name="data-export",
    ),
]
