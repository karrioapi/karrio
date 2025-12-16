import io
import sys
import base64
from django.urls import re_path
from django.utils import timezone
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView
from rest_framework import status

import karrio.lib as lib
import karrio.server.openapi as openapi
import karrio.server.documents.models as models
import karrio.server.documents.generator as generator
from karrio.server.core.logging import logger
from karrio.server.core.utils import validate_resource_token
from karrio.server.core.authentication import AccessMixin


class TemplateDocsPrinter(AccessMixin, VirtualDownloadView):
    def get(self, request, pk: str, slug: str, **kwargs):
        """Generate a document from template."""
        error = validate_resource_token(request, "template", [pk], "render")
        if error:
            return error

        try:
            template = models.DocumentTemplate.objects.get(pk=pk, slug=slug)
            query_params = request.GET.dict()

            self.document = generator.Documents.generate_template(
                template, query_params, context=request
            )
            self.name = f"{slug}.pdf"
            self.attachment = "download" in query_params

            response = super().get(request, pk, slug, **kwargs)
            response["X-Frame-Options"] = "ALLOWALL"
            return response
        except Exception as e:
            logger.exception(
                "Template document generation failed",
                template_id=pk,
                template_slug=slug,
                error=str(e),
            )
            _, __, exc_traceback = sys.exc_info()
            trace = exc_traceback
            while trace and trace.tb_next:
                trace = trace.tb_next
                if "<template>" in str(trace.tb_frame):
                    break

            return JsonResponse(
                dict(error=str(e), line=getattr(trace, "tb_lineno", None)),
                status=status.HTTP_409_CONFLICT,
            )

    def get_file(self):
        return ContentFile(self.document.getvalue(), name=self.name)


class ShipmentDocsPrinter(AccessMixin, VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(self, request, doc: str = "label", format: str = "pdf", **kwargs):
        """Retrieve batch shipment labels or invoices."""
        from karrio.server.manager.models import Shipment

        if doc not in ["label", "invoice"]:
            return JsonResponse(
                dict(error=f"Invalid document type: {doc}"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        resource_ids = request.GET.get("shipments", "").split(",")
        access_type = "batch_labels" if doc == "label" else "batch_invoices"

        error = validate_resource_token(request, "document", resource_ids, access_type)
        if error:
            return error

        query_params = request.GET.dict()
        self.attachment = "download" in query_params
        self.format = (format or "").lower()
        self.name = f"{doc}s - {timezone.now()}.{self.format}"

        _queryset = Shipment.objects.filter(id__in=resource_ids)
        if doc == "label":
            _queryset = _queryset.filter(
                label__isnull=False,
                label_type__contains=self.format.upper(),
            )
        elif doc == "invoice":
            _queryset = _queryset.filter(invoice__isnull=False)

        self.documents = _queryset.values_list(doc, "label_type")

        response = super().get(request, doc, self.format, **kwargs)
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        content = base64.b64decode(
            lib.bundle_base64([doc for doc, _ in self.documents], self.format.upper())
        )
        buffer = io.BytesIO()
        buffer.write(content)
        return ContentFile(buffer.getvalue(), name=self.name)


class OrderDocsPrinter(AccessMixin, VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(self, request, doc: str = "label", format: str = "pdf", **kwargs):
        """Retrieve batch order labels or invoices."""
        from karrio.server.orders.models import Order

        if doc not in ["label", "invoice"]:
            return JsonResponse(
                dict(error=f"Invalid document type: {doc}"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        resource_ids = request.GET.get("orders", "").split(",")
        access_type = "batch_labels" if doc == "label" else "batch_invoices"

        error = validate_resource_token(request, "order", resource_ids, access_type)
        if error:
            return error

        query_params = request.GET.dict()
        self.attachment = "download" in query_params
        self.format = (format or "").lower()
        self.name = f"{doc}s - {timezone.now()}.{self.format}"

        _queryset = Order.objects.filter(
            id__in=resource_ids, shipments__id__isnull=False
        ).distinct()

        if doc == "label":
            _queryset = _queryset.filter(
                shipments__label__isnull=False,
                shipments__label_type__contains=self.format.upper(),
            )
        elif doc == "invoice":
            _queryset = _queryset.filter(shipments__invoice__isnull=False)

        self.documents = list(
            set(_queryset.values_list(f"shipments__{doc}", "shipments__label_type"))
        )

        response = super().get(request, doc, self.format, **kwargs)
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        content = base64.b64decode(
            lib.bundle_base64([doc for doc, _ in self.documents], self.format.upper())
        )
        buffer = io.BytesIO()
        buffer.write(content)
        return ContentFile(buffer.getvalue(), name=self.name)


class ManifestDocsPrinter(AccessMixin, VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(self, request, doc: str = "manifest", format: str = "pdf", **kwargs):
        """Retrieve batch manifests."""
        from karrio.server.manager.models import Manifest

        if doc not in ["manifest"]:
            return JsonResponse(
                dict(error=f"Invalid document type: {doc}"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        resource_ids = request.GET.get("manifests", "").split(",")

        error = validate_resource_token(request, "document", resource_ids, "batch_manifests")
        if error:
            return error

        query_params = request.GET.dict()
        self.attachment = "download" in query_params
        self.format = (format or "").lower()
        self.name = f"{doc}s - {timezone.now()}.{self.format}"

        queryset = Manifest.objects.filter(id__in=resource_ids, manifest__isnull=False)
        self.documents = queryset.values_list(doc, "reference")

        response = super().get(request, doc, self.format, **kwargs)
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        content = base64.b64decode(
            lib.bundle_base64([doc for doc, _ in self.documents], self.format.upper())
        )
        buffer = io.BytesIO()
        buffer.write(content)
        return ContentFile(buffer.getvalue(), name=self.name)


urlpatterns = [
    re_path(
        r"^documents/templates/(?P<pk>\w+).(?P<slug>\w+)",
        TemplateDocsPrinter.as_view(),
        name="templates-documents-print",
    ),
    re_path(
        r"^documents/shipments/(?P<doc>[a-z0-9]+).(?P<format>[a-zA-Z0-9]+)",
        ShipmentDocsPrinter.as_view(),
        name="shipments-documents-print",
    ),
    re_path(
        r"^documents/orders/(?P<doc>[a-z0-9]+).(?P<format>[a-zA-Z0-9]+)",
        OrderDocsPrinter.as_view(),
        name="orders-documents-print",
    ),
    re_path(
        r"^documents/manifests/(?P<doc>[a-z0-9]+).(?P<format>[a-zA-Z0-9]+)",
        ManifestDocsPrinter.as_view(),
        name="manifests-documents-print",
    ),
]
