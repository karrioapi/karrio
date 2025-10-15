"""
JTL Onboarding Serializers

Handles validation and serialization for JTL tenant onboarding.
"""

import logging
import karrio.server.serializers as serializers
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger(__name__)


class JTLOnboardingRequestSerializer(serializers.Serializer):
    """Validates JTL tenant onboarding request payload."""

    tenantId = serializers.CharField(
        required=True,
        help_text="JTL tenant UUID identifier"
    )
    userId = serializers.CharField(
        required=True,
        help_text="JTL user UUID identifier"
    )
    email = serializers.EmailField(
        required=True,
        help_text="User email address for Karrio account"
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text="User password for Karrio account"
    )


class OrganizationResponseSerializer(serializers.Serializer):
    """Organization details in response."""

    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class OrganizationUserResponseSerializer(serializers.Serializer):
    """Organization user details in response."""

    id = serializers.CharField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    roles = serializers.ListField(child=serializers.CharField(), read_only=True)


class UserResponseSerializer(serializers.Serializer):
    """User details in response."""

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)


class JTLOnboardingResponseSerializer(serializers.Serializer):
    """JTL tenant onboarding response with Karrio JWT tokens."""

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = UserResponseSerializer(read_only=True)
    org = OrganizationResponseSerializer(read_only=True)
    org_user = OrganizationUserResponseSerializer(read_only=True)

    @staticmethod
    def create_response(user, org, org_user, is_owner):
        """
        Create onboarding response with JWT tokens.

        Args:
            user: User instance
            org: Organization instance
            org_user: OrganizationUser instance
            is_owner: Boolean indicating ownership

        Returns:
            dict: Serialized response data
        """
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        refresh['org_id'] = str(org.id)
        refresh['is_verified'] = True

        response_data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
            },
            'org': {
                'id': str(org.id),
                'name': org.name,
                'slug': org.slug,
            },
            'org_user': {
                'id': str(org_user.id),
                'is_owner': is_owner,
                'roles': org_user.roles,
            }
        }

        logger.info(
            f"JTL tenant onboarding successful - "
            f"User: {user.email}, Org: {org.id}, Owner: {is_owner}"
        )

        return response_data
