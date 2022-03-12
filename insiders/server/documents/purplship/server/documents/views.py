from django.urls import path
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView

from purplship.server.documents import models
from purplship.server.documents.generator import Documents


class DocumentGenerator(VirtualDownloadView):
    def get(
        self,
        request,
        slug: str,
        **kwargs,
    ):
        """Generate a document."""
        template = models.DocumentTemplate.access_by(request).get(slug=slug)
        data = request.GET.dict()

        self.document = Documents.generate(template, data, context=request)
        self.name = f"{slug}.pdf"
        self.attachment = False

        response = super(DocumentGenerator, self).get(request, slug, **kwargs)
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        return ContentFile(self.document.getvalue(), name=self.name)


urlpatterns = [
    path(
        "documents/<str:slug>",
        DocumentGenerator.as_view(),
        name="documents-generator",
    )
]
