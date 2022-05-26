import io
from django.http import JsonResponse
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from rest_framework import status

from karrio.server.core.views.api import LoginRequiredView
import karrio.server.data.resources as resources


class DataExport(LoginRequiredView, VirtualDownloadView):
    def get(
        self,
        request,
        resource: str = "users",
        format: str = "csv",
        **kwargs,
    ):
        try:
            """Generate a file to export."""
            query_params = request.GET
            self.attachment = "download" in query_params
            self.resource = resource
            self.format = format

            self.dataset = resources.export(resource, query_params, context=request)

            response = super(DataExport, self).get(request, **kwargs)
            response["X-Frame-Options"] = "ALLOWALL"
            return response
        except Exception as e:
            return JsonResponse(dict(error=str(e)), status=status.HTTP_409_CONFLICT)

    def get_file(self):
        content = getattr(self.dataset, self.format, "")
        buffer = io.StringIO() if type(content) == str else io.BytesIO()
        buffer.write(content)

        return ContentFile(buffer.getvalue(), name=f"{self.resource}.{self.format}")


urlpatterns = [
    re_path(
        r"^export/(?P<resource>\w+).(?P<format>\w+)",
        csrf_exempt(DataExport.as_view()),
        name="data-export",
    )
]
