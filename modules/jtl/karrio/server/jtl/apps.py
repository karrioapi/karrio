"""
Django app configuration for JTL Custom core module.
"""

from django.apps import AppConfig


class JTLConfig(AppConfig):
    """JTL Custom core module app configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'karrio.server.jtl'
    verbose_name = 'JTL Custom core'
    label = 'jtl'

    def ready(self):
        """Add JTL JWT authentication to REST framework authentication classes."""
        from django.conf import settings

        # Add JTLJWTAuthentication to DRF's authentication classes
        # This is done here to avoid circular imports during Django initialization
        if hasattr(settings, "REST_FRAMEWORK"):
            auth_class = "karrio.server.jtl.authentication.JTLJWTAuthentication"
            auth_classes = settings.REST_FRAMEWORK.get("DEFAULT_AUTHENTICATION_CLASSES", [])

            if auth_class not in auth_classes:
                # Prepend for higher priority (before standard JWT)
                settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
                    auth_class
                ] + auth_classes
