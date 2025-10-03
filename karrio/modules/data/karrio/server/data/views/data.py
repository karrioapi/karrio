import io
from django.http import JsonResponse
from django.urls import re_path, path
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from karrio.server.data.serializers.data import ImportDataSerializer
import karrio.server.data.serializers as serializers
import karrio.server.data.resources as resources
import karrio.server.core.views.api as api
import karrio.server.openapi as openapi

ENDPOINT_ID = "&&&&$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
DataImportParameters: list = [
    openapi.OpenApiParameter(
        name="resource_type",
        type=openapi.OpenApiTypes.STR,
        enum=[e.name for e in list(serializers.ResourceType)],
        description="The type of the resource to import",
    ),
    openapi.OpenApiParameter(
        "data_template",
        type=openapi.OpenApiTypes.STR,
        required=False,
        description="""A data template slug to use for the import.<br/>
        **When nothing is specified, the system default headers are expected.**
        """,
    ),
    openapi.OpenApiParameter(
        name="data_file",
        type=openapi.OpenApiTypes.BINARY,
    ),
]


class DataImport(api.BaseAPIView):
    parser_classes = [MultiPartParser, FormParser]

    @openapi.extend_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}import_file",
        summary="Import data files",
        responses={
            202: serializers.BatchOperation(),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'resource_type': {
                        'type': 'string',
                    },
                    'data_template': {
                        'type': 'string',
                    },
                    'data_file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        parameters=DataImportParameters,
    )
    def post(self, request: Request):
        """Import csv, xls and xlsx data files for: `Beta`<br/>
        - trackers data
        - orders data
        - shipments data
        - billing data (soon)<br/><br/>
        **This operation will return a batch operation that you can poll to follow
        the import progression.**
        """
        operation = (
            ImportDataSerializer.map(data=request.data, context=request)
            .save()
            .instance
        )

        return Response(
            serializers.BatchOperation(operation).data, status=status.HTTP_202_ACCEPTED
        )


DataExportParameters: list = [
    openapi.OpenApiParameter(
        name="resource_type",
        location=openapi.OpenApiParameter.PATH,
        type=openapi.OpenApiTypes.STR,
        enum=[e.name for e in list(serializers.ResourceType)],
    ),
    openapi.OpenApiParameter(
        name="export_format",
        location=openapi.OpenApiParameter.PATH,
        type=openapi.OpenApiTypes.STR,
        enum=[e.name for e in list(serializers.ResourceType)],
    ),
    openapi.OpenApiParameter(
        "data_template",
        location=openapi.OpenApiParameter.QUERY,
        type=openapi.OpenApiTypes.STR,
        required=False,
        description="""A data template slug to use for the import.<br/>
        **When nothing is specified, the system default headers are expected.**
        """,
    ),
]


class DataExport(api.LoginRequiredView, VirtualDownloadView):
    @openapi.extend_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}export_file",
        summary="Export data files",
        responses={
            (200, "application/octet-stream"): openapi.OpenApiTypes.BINARY,
            409: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        parameters=DataExportParameters,
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
    path("batches/data/import", DataImport.as_view(), name="data-import"),
    re_path(
        r"^batches/data/export/(?P<resource_type>\w+).(?P<export_format>\w+)",
        csrf_exempt(DataExport.as_view()),
        name="data-export",
    ),
]
