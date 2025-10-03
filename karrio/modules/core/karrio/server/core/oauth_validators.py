import hashlib
import base64
from oauth2_provider.oauth2_validators import OAuth2Validator
from django.contrib.auth import get_user_model


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None

    def get_additional_claims(self):
        return {
            "name": lambda request: getattr(request.user, 'full_name', '') if request.user else '',
            "email": lambda request: getattr(request.user, 'email', '') if request.user else '',
        }

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        """
        Validate grant type with proper format conversion.

        django-oauth-toolkit stores grant types with hyphens (e.g., 'authorization-code')
        but OAuth2 spec uses underscores (e.g., 'authorization_code').
        This method handles the conversion.
        """
        # Convert OAuth2 spec format to django-oauth-toolkit format
        grant_type_mapping = {
            'authorization_code': 'authorization-code',
            'client_credentials': 'client-credentials',
            'refresh_token': 'refresh-token',
            'password': 'password',
        }

        # Get the stored grant type format
        stored_grant_type = grant_type_mapping.get(grant_type, grant_type)

        # Check if the client supports this grant type
        if client and hasattr(client, 'authorization_grant_type'):
            is_valid = client.authorization_grant_type == stored_grant_type
            if is_valid:
                return True

        # Fall back to parent implementation
        return super().validate_grant_type(client_id, grant_type, client, request, *args, **kwargs)

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        """
        Override validate_code to ensure proper grant type handling for authorization code flow.
        """
        # First validate the code using parent implementation
        is_valid = super().validate_code(client_id, code, client, request, *args, **kwargs)

        if is_valid and client:
            # Ensure the client supports authorization code flow
            # Convert the request grant type to stored format for comparison
            if request.grant_type == 'authorization_code':
                return client.authorization_grant_type == 'authorization-code'

        return is_valid

    def validate_client_id(self, client_id, request, *args, **kwargs):
        """
        Validate the client_id and set the user context for different flows.
        """
        is_valid = super().validate_client_id(client_id, request, *args, **kwargs)

        if is_valid:
            try:
                from oauth2_provider.models import Application
                application = Application.objects.get(client_id=client_id)

                # Set application on request for later use
                request.oauth_application = application

                # For client credentials flow, set the user from the OAuth application owner
                if request.grant_type == 'client_credentials' and application.user:
                    request.user = application.user

            except Application.DoesNotExist:
                pass

        return is_valid

    def validate_redirect_uri(self, client_id, redirect_uri, request, *args, **kwargs):
        """
        Validate redirect URI for Authorization Code Flow with enhanced security.
        """
        is_valid = super().validate_redirect_uri(client_id, redirect_uri, request, *args, **kwargs)

        if is_valid and redirect_uri:
            # Additional security: ensure HTTPS in production
            from django.conf import settings
            if not settings.DEBUG and not redirect_uri.startswith('https://'):
                return False

        return is_valid

    def validate_code_challenge(self, challenge, request, *args, **kwargs):
        """
        Validate PKCE code challenge for enhanced security.
        """
        # This is called when PKCE is enabled
        if challenge:
            # Validate that the challenge is base64url encoded and has proper length
            try:
                decoded = base64.urlsafe_b64decode(challenge + '==')  # Add padding
                return len(decoded) >= 32  # At least 256 bits
            except Exception:
                return False

        # If PKCE is required but no challenge provided, reject
        from django.conf import settings
        oauth_settings = getattr(settings, 'OAUTH2_PROVIDER', {})
        if oauth_settings.get('PKCE_REQUIRED', False):
            return False

        return True

    def validate_code_verifier(self, verifier, challenge, challenge_method, request, *args, **kwargs):
        """
        Validate PKCE code verifier against the challenge.
        """
        if challenge_method == 'S256':
            # SHA256 challenge method
            verifier_hash = hashlib.sha256(verifier.encode('ascii')).digest()
            verifier_challenge = base64.urlsafe_b64encode(verifier_hash).decode('ascii').rstrip('=')
            return verifier_challenge == challenge
        elif challenge_method == 'plain':
            # Plain text challenge method (less secure, but allowed)
            return verifier == challenge

        return False

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        """
        Return default scopes for the application.
        """
        try:
            from oauth2_provider.models import Application
            application = Application.objects.get(client_id=client_id)

            # For Karrio apps, default to read scope
            if hasattr(application, 'oauth_app'):
                return ['read']

        except Application.DoesNotExist:
            pass

        return super().get_default_scopes(client_id, request, *args, **kwargs)

    def save_authorization_code(self, client_id, code, request, *args, **kwargs):
        """
        Store authorization code with additional security measures.
        """
        # Store the authorization code with enhanced security
        super().save_authorization_code(client_id, code, request, *args, **kwargs)

        # Log OAuth events for audit purposes
        import logging
        logger = logging.getLogger('karrio.server.oauth')
        logger.info(f"Authorization code granted for client {client_id}")

    def authenticate_user(self, request):
        """
        Authenticate user for Authorization Code Flow.
        """
        user = super().authenticate_user(request)

        if user:
            # Set additional user context
            request.oauth_user = user

        return user
