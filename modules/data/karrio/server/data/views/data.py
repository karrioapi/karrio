import io
from django.http import JsonResponse, HttpResponse
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
import karrio.server.data.resources.rate_sheets as rate_sheet_resource
import karrio.server.data.serializers.batch_rate_sheets as batch_rate_sheets
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
            200: openapi.OpenApiTypes.OBJECT,
            202: serializers.BatchOperation(),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'resource_type': {'type': 'string'},
                    'data_template': {'type': 'string'},
                    'dry_run': {'type': 'boolean'},
                    'data_file': {'type': 'string', 'format': 'binary'},
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
        - rate_sheet data (Excel/CSV)<br/><br/>
        **For rate_sheet imports, pass dry_run=true to validate and preview a diff
        without writing. For other resource types, a BatchOperation is returned.**
        """
        resource_type = request.data.get("resource_type", "")

        # Rate sheet import is handled synchronously (data is small, no queue needed)
        if resource_type == "rate_sheet":
            data_file = request.data.get("data_file")
            if not data_file:
                return Response(
                    {"errors": [{"message": "data_file is required"}]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            dry_run = str(request.data.get("dry_run", "false")).lower() in ("true", "1", "yes")
            rate_sheet_id = request.data.get("rate_sheet_id")
            try:
                result = batch_rate_sheets.process_rate_sheet_import(
                    data_file=data_file,
                    context=request,
                    dry_run=dry_run,
                    rate_sheet_id=rate_sheet_id,
                )
            except Exception as exc:
                return Response(
                    {"errors": [{"message": str(exc)}]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if result.get("errors"):
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)

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


class DataExport(api.BaseAPIView):
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

            # Rate sheet export — dedicated xlsx handler
            if resource_type == "rate_sheet":
                from karrio.server.providers.models import RateSheet, SystemRateSheet
                sheet_id = query_params.get("id")
                if not sheet_id:
                    return JsonResponse(
                        {"errors": [{"message": "id query param is required for rate_sheet export"}]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                sheet = (
                    RateSheet.access_by(request).filter(id=sheet_id).first()
                    or RateSheet.access_by(request).filter(slug=sheet_id).first()
                )
                if sheet is None:
                    # Try system rate sheet (admin access)
                    sheet = (
                        SystemRateSheet.objects.filter(id=sheet_id).first()
                        or SystemRateSheet.objects.filter(slug=sheet_id).first()
                    )
                if sheet is None:
                    return JsonResponse(
                        {"errors": [{"message": f"Rate sheet '{sheet_id}' not found"}]},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                xlsx_bytes = rate_sheet_resource.export_rate_sheet_xlsx(sheet)
                slug = getattr(sheet, "slug", sheet_id) or sheet_id
                response = HttpResponse(
                    xlsx_bytes,
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                response["Content-Disposition"] = f'attachment; filename="rate-sheet-{slug}.xlsx"'
                response["X-Frame-Options"] = "ALLOWALL"
                return response

            # Standard tablib export
            dataset = resources.export(
                resource_type, query_params, context=request
            )

            # Get the content
            content = getattr(dataset, export_format, "")

            # Determine content type
            content_types = {
                'csv': 'text/csv',
                'xls': 'application/vnd.ms-excel',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            }
            content_type = content_types.get(export_format, 'application/octet-stream')

            # Create response
            if isinstance(content, str):
                response = HttpResponse(content.encode('utf-8'), content_type=content_type)
            else:
                response = HttpResponse(content, content_type=content_type)

            # Set headers
            filename = f"{resource_type}.{export_format}"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['X-Frame-Options'] = 'ALLOWALL'

            return response

        except Exception as e:
            return JsonResponse(
                dict(errors=[{"message": str(e)}]),
                status=status.HTTP_409_CONFLICT,
            )


urlpatterns = [
    path("batches/data/import", DataImport.as_view(), name="data-import"),
    re_path(
        r"^batches/data/export/(?P<resource_type>\w+).(?P<export_format>\w+)",
        csrf_exempt(DataExport.as_view()),
        name="data-export",
    ),
]
