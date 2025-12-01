"""Generic Resource Access Token API.

This module provides a generic endpoint for generating limited-access tokens
for various resources (documents, exports, etc.).
"""

from datetime import datetime, timezone
from django.urls import path
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import karrio.server.openapi as openapi
from karrio.server.core.utils import ResourceAccessToken

ENDPOINT_ID = "&&"  # Unique endpoint ID for OpenAPI operation IDs


# Serializers
class ResourceTokenRequest(serializers.Serializer):
    resource_type = serializers.ChoiceField(
        choices=[
            ("shipment", "Shipment"),
            ("manifest", "Manifest"),
            ("order", "Order"),
            ("template", "Template"),
            ("document", "Document"),
        ],
        help_text="The type of resource to grant access to.",
    )
    resource_ids = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="List of resource IDs to grant access to.",
    )
    access = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                ("label", "Label"),
                ("invoice", "Invoice"),
                ("manifest", "Manifest"),
                ("render", "Render template"),
                ("batch_labels", "Batch labels"),
                ("batch_invoices", "Batch invoices"),
                ("batch_manifests", "Batch manifests"),
            ]
        ),
        min_length=1,
        help_text="List of access permissions to grant.",
    )
    format = serializers.ChoiceField(
        choices=[
            ("pdf", "PDF"),
            ("png", "PNG"),
            ("zpl", "ZPL"),
            ("gif", "GIF"),
        ],
        required=False,
        allow_null=True,
        help_text="Document format (optional).",
    )
    expires_in = serializers.IntegerField(
        required=False,
        min_value=60,
        max_value=3600,
        default=300,
        help_text="Token expiration time in seconds (60-3600, default: 300).",
    )


class ResourceTokenResponse(serializers.Serializer):
    token = serializers.CharField(help_text="The JWT access token.")
    expires_at = serializers.DateTimeField(help_text="Token expiration timestamp.")
    resource_urls = serializers.DictField(
        child=serializers.CharField(),
        help_text="Map of resource IDs to their access URLs with token.",
    )


# URL builders for different resource types
def _build_shipment_urls(resource_ids: list, access: list, format_ext: str, token: str) -> dict:
    access_type = access[0] if access else "label"
    return {rid: f"/v1/shipments/{rid}/{access_type}.{format_ext}?token={token}" for rid in resource_ids}


def _build_manifest_urls(resource_ids: list, format_ext: str, token: str) -> dict:
    return {rid: f"/v1/manifests/{rid}/manifest.{format_ext}?token={token}" for rid in resource_ids}


def _build_order_urls(resource_ids: list, access: list, format_ext: str, token: str) -> dict:
    order_ids = ",".join(resource_ids)
    access_type = access[0] if access else "batch_labels"
    doc_type = "invoice" if access_type == "batch_invoices" else "label"
    return {"batch": f"/documents/orders/{doc_type}.{format_ext}?orders={order_ids}&token={token}"}


def _build_template_urls(resource_ids: list, token: str) -> dict:
    from karrio.server.documents.models import DocumentTemplate

    # Query templates to get their slugs
    templates = DocumentTemplate.objects.filter(pk__in=resource_ids).values("pk", "slug")
    template_map = {t["pk"]: t["slug"] for t in templates}

    return {
        rid: f"/documents/templates/{rid}.{template_map.get(rid, 'doc')}?token={token}"
        for rid in resource_ids
    }


def _build_document_urls(resource_ids: list, access: list, format_ext: str, token: str) -> dict:
    access_type = access[0] if access else "batch_labels"
    ids = ",".join(resource_ids)
    url_map = {
        "batch_labels": f"/documents/shipments/label.{format_ext}?shipments={ids}&token={token}",
        "batch_invoices": f"/documents/shipments/invoice.{format_ext}?shipments={ids}&token={token}",
        "batch_manifests": f"/documents/manifests/manifest.{format_ext}?manifests={ids}&token={token}",
    }
    return {"batch": url_map.get(access_type, url_map["batch_labels"])}


def build_resource_urls(
    resource_type: str,
    resource_ids: list,
    access: list,
    format: str,
    token: str,
) -> dict:
    """Build resource URLs with token for each resource ID."""
    format_ext = (format or "pdf").lower()

    builders = {
        "shipment": lambda: _build_shipment_urls(resource_ids, access, format_ext, token),
        "manifest": lambda: _build_manifest_urls(resource_ids, format_ext, token),
        "order": lambda: _build_order_urls(resource_ids, access, format_ext, token),
        "template": lambda: _build_template_urls(resource_ids, token),
        "document": lambda: _build_document_urls(resource_ids, access, format_ext, token),
    }

    return builders.get(resource_type, lambda: {})()



class ResourceTokenView(APIView):
    """Generate limited-access tokens for resources."""

    permission_classes = [IsAuthenticated]

    @openapi.extend_schema(
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}generate_resource_token",
        summary="Generate resource access token",
        description="""
Generate a short-lived JWT token for accessing specific resources.

This endpoint is used to create secure, time-limited access tokens for
resources like shipment labels, manifests, and document templates.

**Use cases:**
- Generate a token to allow document preview in a new browser window
- Create shareable links for documents with automatic expiration
- Enable secure document downloads without exposing API keys

**Token lifetime:** Default 5 minutes, configurable up to 1 hour.
        """,
        request=ResourceTokenRequest,
        responses={
            201: ResourceTokenResponse,
            400: openapi.OpenApiTypes.OBJECT,
            401: openapi.OpenApiTypes.OBJECT,
        },
    )
    def post(self, request: Request) -> Response:
        serializer = ResourceTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        resource_type = data["resource_type"]
        resource_ids = data["resource_ids"]
        access = data["access"]
        format = data.get("format")
        expires_in = data.get("expires_in", 300)

        # Get org_id for multi-tenant environments
        org_id = None
        if hasattr(request, "org") and request.org:
            org_id = request.org.id

        # Get test_mode from request context
        test_mode = getattr(request, "test_mode", None)

        # Generate the token
        token = ResourceAccessToken.for_resource(
            user=request.user,
            resource_type=resource_type,
            resource_ids=resource_ids,
            access=access,
            format=format,
            org_id=org_id,
            test_mode=test_mode,
            expires_in=expires_in,
        )

        token_string = str(token)

        # Calculate expiration time
        expires_at = datetime.fromtimestamp(token["exp"], tz=timezone.utc)

        # Build resource URLs
        resource_urls = build_resource_urls(
            resource_type=resource_type,
            resource_ids=resource_ids,
            access=access,
            format=format,
            token=token_string,
        )

        response = Response(
            {
                "token": token_string,
                "expires_at": expires_at.isoformat(),
                "resource_urls": resource_urls,
            },
            status=status.HTTP_201_CREATED,
        )

        # Prevent caching of tokens
        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"

        return response


urlpatterns = [
    path("api/tokens", ResourceTokenView.as_view(), name="resource-tokens"),
]
