import sys
import logging
from django.http import JsonResponse
from django.urls import re_path
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from rest_framework import status

from karrio.server.documents import models
from karrio.server.documents.generator import Documents

logger = logging.getLogger(__name__)


class DocumentGenerator(VirtualDownloadView):
    def get(
        self,
        request,
        pk: str,
        slug: str,
        **kwargs,
    ):
        try:
            """Generate a document."""
            template = models.DocumentTemplate.objects.get(pk=pk, slug=slug)
            query_params = request.GET.dict()

            self.document = Documents.generate(template, query_params, context=request)
            self.name = f"{slug}.pdf"
            self.attachment = "download" in query_params

            response = super(DocumentGenerator, self).get(request, pk, slug, **kwargs)
            response["X-Frame-Options"] = "ALLOWALL"
            return response
        except Exception as e:
            logger.exception(e)
            _, __, exc_traceback = sys.exc_info()
            trace = exc_traceback
            while True:
                trace = trace.tb_next
                if "<template>" in str(trace.tb_frame) or not trace.tb_next:
                    break

            return JsonResponse(
                dict(error=str(e), line=getattr(trace, "tb_lineno", None)),
                status=status.HTTP_409_CONFLICT,
            )

    def get_file(self):
        return ContentFile(self.document.getvalue(), name=self.name)


urlpatterns = [
    re_path(
        r"^documents/(?P<pk>\w+).(?P<slug>\w+)",
        DocumentGenerator.as_view(),
        name="documents-generator",
    )
]
