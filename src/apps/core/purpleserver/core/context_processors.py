from django.conf import settings


DEFAULT_ALLOWED_CONFIG = [
    'APP_NAME',
    'BASE_TEMPLATE',
    'APP_WEBSITE',
]
FALLBACK_VALUES = {
    'APP_NAME': 'Purplship',
    'BASE_TEMPLATE': 'purpleserver/base_site.html',
    'APP_WEBSITE': 'https://purplship.com',
}
TEMPLATE_SETTINGS_ACCESS_LIST = getattr(settings, 'TEMPLATE_SETTINGS_ACCESS_LIST', DEFAULT_ALLOWED_CONFIG)


def settings(request):
    return {
        name: getattr(settings, name, FALLBACK_VALUES.get(name))
        for name in TEMPLATE_SETTINGS_ACCESS_LIST
    }
