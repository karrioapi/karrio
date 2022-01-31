from purplship.server.conf import settings, DEFAULT_ALLOWED_CONFIG


TEMPLATE_SETTINGS_ACCESS_LIST = (
    getattr(settings, "TEMPLATE_SETTINGS_ACCESS_LIST", None) or DEFAULT_ALLOWED_CONFIG
)


def get_settings(request):
    tenant = getattr(request, "tenant", None)
    return {name: settings.get(name, tenant) for name in TEMPLATE_SETTINGS_ACCESS_LIST}
