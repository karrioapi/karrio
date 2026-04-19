import karrio.server.admin.schema as schema
import karrio.server.core.views.api as api
import karrio.server.graph.views as views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class IsStaffPermission(IsAuthenticated):
    """Only allow staff users."""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and getattr(request.user, "is_staff", False)


class AdminDataImport(api.BaseAPIView):
    """Admin-only rate sheet import — creates SystemRateSheet."""

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsStaffPermission]

    def post(self, request: Request):
        import karrio.server.data.serializers.batch_rate_sheets as batch_rate_sheets

        data_file = request.data.get("data_file")
        if not data_file:
            return Response(
                {"errors": [{"message": "data_file is required"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        dry_run = str(request.data.get("dry_run", "false")).lower() in (
            "true",
            "1",
            "yes",
        )
        rate_sheet_id = request.data.get("rate_sheet_id")
        create_mode = str(request.data.get("create_mode", "false")).lower() in (
            "true",
            "1",
            "yes",
        )
        try:
            result = batch_rate_sheets.process_rate_sheet_import(
                data_file=data_file,
                context=request,
                dry_run=dry_run,
                rate_sheet_id=rate_sheet_id,
                system=True,
                create_mode=create_mode,
            )
        except Exception as exc:
            return Response(
                {"errors": [{"message": str(exc)}]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if result.get("errors"):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)


urlpatterns = [
    path(
        "admin/graphql/",
        csrf_exempt(views.GraphQLView.as_view(schema=schema.schema)),
        name="admin-graph",
    ),
    path(
        "admin/graphql",
        csrf_exempt(views.GraphQLView.as_view(schema=schema.schema)),
        name="admin-graph",
    ),
    path(
        "admin/batches/data/import",
        AdminDataImport.as_view(),
        name="admin-data-import",
    ),
]
