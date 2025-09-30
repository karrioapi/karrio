from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppsConfig(AppConfig):
    name = "karrio.server.apps"
    verbose_name = _("Apps")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from django.conf import settings

        # Add AppJWTAuthentication to DRF's authentication classes
        # This is done here to avoid circular imports during Django initialization
        if hasattr(settings, "REST_FRAMEWORK"):
            auth_class = "karrio.server.apps.authentication.AppJWTAuthentication"
            auth_classes = settings.REST_FRAMEWORK.get("DEFAULT_AUTHENTICATION_CLASSES", [])

            if auth_class not in auth_classes:
                # Prepend for higher priority
                settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
                    auth_class
                ] + auth_classes
