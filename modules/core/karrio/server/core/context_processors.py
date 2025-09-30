from karrio.server.conf import settings, DEFAULT_ALLOWED_CONFIG


TEMPLATE_SETTINGS_ACCESS_LIST = (
    getattr(settings, "TEMPLATE_SETTINGS_ACCESS_LIST", None) or DEFAULT_ALLOWED_CONFIG
)


def get_settings(request):
    return {
        name: getattr(settings, name, None) for name in TEMPLATE_SETTINGS_ACCESS_LIST
    }
