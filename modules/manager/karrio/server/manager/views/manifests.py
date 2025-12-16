import io
import base64
import django_downloadview
import django.urls as urls
import django.core.files.base as base
import rest_framework.status as status
import rest_framework.request as request
import rest_framework.response as response
import rest_framework.pagination as pagination
import rest_framework.throttling as throttling
import django_filters.rest_framework as django_filters

from karrio.server.core.utils import validate_resource_token
from karrio.server.core.authentication import AccessMixin
import karrio.server.openapi as openapi
import karrio.server.core.views.api as api
import karrio.server.core.filters as filters
import karrio.server.manager.models as models
import karrio.server.manager.router as router
import karrio.server.manager.serializers as serializers
from karrio.server.core.serializers import ShippingDocument

ENDPOINT_ID = "$$$$&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Manifests = serializers.PaginatedResult("ManifestList", serializers.Manifest)


class ManifestList(api.GenericAPIView):
    throttle_scope = "carrier_request"
    pagination_class = type(
        "CustomPagination", (pagination.LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = filters.ManifestFilters
    serializer_class = Manifests
    model = models.Manifest

    def get_throttles(self):
        if self.request.method == "POST":
            return [throttling.ScopedRateThrottle()]
        return super().get_throttles()

    @openapi.extend_schema(
        tags=["Manifests"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listManifests"},
        summary="List manifests",
        responses={
            200: Manifests(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
        parameters=filters.ManifestFilters.parameters,
    )
    def get(self, request: request.Request):
        """
        Retrieve all manifests.
        """
        manifests = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(
            serializers.Manifest(manifests, many=True).data
        )
        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Manifests"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createManifest"},
        summary="Create a manifest",
        responses={
            201: serializers.Manifest(),
            400: serializers.ErrorResponse(),
            424: serializers.ErrorMessages(),
            500: serializers.ErrorResponse(),
        },
        request=serializers.ManifestData(),
    )
    def post(self, request: request.HttpRequest):
        """Create a manifest for one or many shipments with labels already purchased."""

        manifest = (
            serializers.ManifestSerializer.map(data=request.data, context=request)
            .save()
            .instance
        )

        return response.Response(
            serializers.Manifest(manifest).data, status=status.HTTP_201_CREATED
        )


class ManifestDetails(api.APIView):

    @openapi.extend_schema(
        tags=["Manifests"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveManifest"},
        summary="Retrieve a manifest",
        responses={
            200: serializers.Manifest(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: request.Request, pk: str):
        """Retrieve a shipping manifest."""
        manifest = models.Manifest.access_by(request).get(pk=pk)
        return response.Response(serializers.Manifest(manifest).data)


class ManifestDoc(AccessMixin, django_downloadview.VirtualDownloadView):
    @openapi.extend_schema(exclude=True)
    def get(self, req: request.Request, pk: str, doc: str = "manifest", format: str = "pdf", **kwargs):
        """Retrieve a manifest file."""
        error = validate_resource_token(req, "manifest", [pk], "manifest")
        if error:
            return error

        query_params = req.GET.dict()

        self.manifest = models.Manifest.objects.filter(pk=pk, manifest__isnull=False).first()

        if self.manifest is None:
            return response.Response(
                {"errors": [{"message": f"Manifest '{pk}' not found or has no document"}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.document = getattr(self.manifest, doc, None)
        self.name = f"{doc}_{self.manifest.id}.{format}"

        self.preview = "preview" in query_params
        self.attachment = "download" in query_params

        resp = super(ManifestDoc, self).get(req, pk, doc, format, **kwargs)
        resp["X-Frame-Options"] = "ALLOWALL"
        return resp

    def get_file(self):
        content = base64.b64decode(self.document or "")
        buffer = io.BytesIO()
        buffer.write(content)

        return base.ContentFile(buffer.getvalue(), name=self.name)


class ManifestDocumentDownload(api.APIView):

    @openapi.extend_schema(
        tags=["Manifests"],
        operation_id=f"{ENDPOINT_ID}document",
        extensions={"x-operationId": "retrieveManifestDocument"},
        summary="Retrieve a manifest document",
        request=None,
        responses={
            200: ShippingDocument(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def post(self, req: request.Request, pk: str):
        """
        Retrieve a manifest document as base64 encoded content.
        """
        manifest = models.Manifest.access_by(req).filter(pk=pk, manifest__isnull=False).first()

        if manifest is None:
            return response.Response(
                {"errors": [{"message": f"Manifest '{pk}' not found or has no document"}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Build the GET URL for the document
        doc_url = f"/v1/manifests/{pk}/manifest.pdf"

        return response.Response(
            ShippingDocument(
                {
                    "category": "manifest",
                    "format": "PDF",
                    "base64": manifest.manifest,
                    "url": doc_url,
                }
            ).data
        )


router.router.urls.append(
    urls.path(
        "manifests",
        ManifestList.as_view(),
        name="manifest-list",
    )
)
router.router.urls.append(
    urls.path(
        "manifests/<str:pk>",
        ManifestDetails.as_view(),
        name="manifest-details",
    )
)
router.router.urls.append(
    urls.path(
        "manifests/<str:pk>/document",
        ManifestDocumentDownload.as_view(),
        name="manifest-document-download",
    )
)
router.router.urls.append(
    urls.re_path(
        r"^manifests/(?P<pk>\w+)/(?P<doc>[a-z0-9]+)\.(?P<format>[a-z0-9]+)",
        ManifestDoc.as_view(),
        name="manifest-docs",
    )
)
