import io
import sys
import base64
import logging
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

logger = logging.getLogger(__name__)


class TemplateDocsPrinter(VirtualDownloadView):
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

            self.document = generator.Documents.generate_template(
                template, query_params, context=request
            )
            self.name = f"{slug}.pdf"
            self.attachment = "download" in query_params

            response = super(TemplateDocsPrinter, self).get(request, pk, slug, **kwargs)
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


class ShipmentDocsPrinter(VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(
        self,
        request,
        doc: str = "label",
        format: str = "pdf",
        **kwargs,
    ):
        """Retrieve a shipment label."""
        from karrio.server.manager.models import Shipment

        if doc not in ["label", "invoice"]:
            return JsonResponse(
                dict(error=f"Invalid document type: {doc}"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        query_params = request.GET.dict()
        self.attachment = "download" in query_params
        ids = query_params.get("shipments", "").split(",")

        self.format = (format or "").lower()
        self.name = f"{doc}s - {timezone.now()}.{self.format}"
        _queryset = Shipment.objects.filter(id__in=ids)

        if doc == "label":
            _queryset = _queryset.filter(
                label__isnull=False,
                label_type__contains=self.format.upper(),
            )
        if doc == "invoice":
            _queryset = _queryset.filter(invoice__isnull=False)

        self.documents = _queryset.values_list(doc, "label_type")

        response = super(ShipmentDocsPrinter, self).get(
            request, doc, self.format, **kwargs
        )
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        content = base64.b64decode(
            lib.bundle_base64([doc for doc, _ in self.documents], self.format.upper())
        )
        buffer = io.BytesIO()
        buffer.write(content)

        return ContentFile(buffer.getvalue(), name=self.name)


class OrderDocsPrinter(VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(
        self,
        request,
        doc: str = "label",
        format: str = "pdf",
        **kwargs,
    ):
        """Retrieve a shipment label."""
        from karrio.server.orders.models import Order

        if doc not in ["label", "invoice"]:
            return JsonResponse(
                dict(error=f"Invalid document type: {doc}"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        query_params = request.GET.dict()
        self.attachment = "download" in query_params
        ids = query_params.get("orders", "").split(",")

        self.format = (format or "").lower()
        self.name = f"{doc}s - {timezone.now()}.{self.format}"
        _queryset = Order.objects.filter(
            id__in=ids, shipments__id__isnull=False
        ).distinct()

        if doc == "label":
            _queryset = _queryset.filter(
                shipments__label__isnull=False,
                shipments__label_type__contains=self.format.upper(),
            )
        if doc == "invoice":
            _queryset = _queryset.filter(shipments__invoice__isnull=False)

        self.documents = list(
            set(_queryset.values_list(f"shipments__{doc}", "shipments__label_type"))
        )

        response = super(OrderDocsPrinter, self).get(
            request, doc, self.format, **kwargs
        )
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        content = base64.b64decode(
            lib.bundle_base64([doc for doc, _ in self.documents], self.format.upper())
        )
        buffer = io.BytesIO()
        buffer.write(content)

        return ContentFile(buffer.getvalue(), name=self.name)


class ManifestDocsPrinter(VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(
        self,
        request,
        doc: str = "manifest",
        format: str = "pdf",
        **kwargs,
    ):
        """Retrieve a shipment label."""
        from karrio.server.manager.models import Manifest

        if doc not in ["manifest"]:
            return JsonResponse(
                dict(error=f"Invalid document type: {doc}"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        query_params = request.GET.dict()
        self.attachment = "download" in query_params
        ids = query_params.get("manifests", "").split(",")

        self.format = (format or "").lower()
        self.name = f"{doc}s - {timezone.now()}.{self.format}"
        queryset = Manifest.objects.filter(id__in=ids, manifest__isnull=False)

        self.documents = queryset.values_list(doc, "reference")

        response = super(ManifestDocsPrinter, self).get(
            request, doc, self.format, **kwargs
        )
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
