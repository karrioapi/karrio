"""
JTL Tenant Onboarding API View

Handles tenant onboarding for JTL Hub integration with clean separation of concerns.
"""

import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import karrio.server.openapi as openapi
from karrio.server.core.serializers import ErrorResponse
from karrio.server.jtl.serializers import (
    JTLOnboardingRequestSerializer,
    JTLOnboardingResponseSerializer,
)
from karrio.server.jtl.helpers import onboard_jtl_tenant

logger = logging.getLogger(__name__)
ENDPOINT_ID = "jtl$"  # Unique endpoint ID for operation naming


class JTLTenantOnboardingView(APIView):
    """
    JTL tenant onboarding endpoint.

    Creates or retrieves organizations and users based on JTL tenantId and userId,
    ensuring idempotent operations.

    POST /jtl/tenants/onboarding

    Request:
        {
            "tenantId": "uuid-string",
            "userId": "uuid-string",
            "email": "user@example.com",
            "password": "user-password"
        }

    Response (200 OK):
        {
            "access_token": "...",
            "refresh_token": "...",
            "user": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "User Name"
            },
            "org": {
                "id": "org_uuid",
                "name": "Organization Name",
                "slug": "org-slug"
            },
            "org_user": {
                "id": "org_user_uuid",
                "is_owner": true,
                "roles": ["admin"]
            }
        }
    """

    authentication_classes = []  # Public endpoint
    permission_classes = []  # No permissions required

    @openapi.extend_schema(
        tags=["JTL"],
        operation_id=f"{ENDPOINT_ID}onboard_tenant",
        extensions={"x-operationId": "onboardJTLTenant"},
        summary="Onboard a JTL tenant",
        request=JTLOnboardingRequestSerializer(),
        responses={
            200: JTLOnboardingResponseSerializer(),
            400: ErrorResponse(),
        },
        exclude=True,
    )
    def post(self, request):
        """
        Onboard JTL tenant and user.

        Validates request payload, orchestrates onboarding process,
        and returns JWT tokens with user/organization information.
        """
        # Validate request data
        serializer = JTLOnboardingRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data

        try:
            # Onboard tenant
            user, org, org_user, is_owner = onboard_jtl_tenant(
                tenant_id=validated_data['tenantId'],
                user_id=validated_data['userId'],
                email=validated_data['email'],
                password=validated_data['password']
            )

            # Create response with JWT tokens
            response_data = JTLOnboardingResponseSerializer.create_response(
                user, org, org_user, is_owner
            )

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"JTL tenant onboarding error: {e}", exc_info=True)
            return Response(
                {'error': f'Onboarding failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
