from django.conf import settings


DEFAULT_ALLOWED_CONFIG = [
    'APP_NAME',
    'APP_WEBSITE',
    'SUPPORT_EMAIL',
    'BASE_TEMPLATE',
    'BASE_FOOTER_TEMPLATE',
]
FALLBACK_VALUES = {
    'APP_NAME': 'Purplship',
    'APP_WEBSITE': 'https://purplship.com',
    'SUPPORT_EMAIL': 'hello@purplship.com',
    'BASE_TEMPLATE': 'purpleserver/base_site.html',
    'BASE_FOOTER_TEMPLATE': 'purpleserver/base_footer.html',
}
TEMPLATE_SETTINGS_ACCESS_LIST = getattr(settings, 'TEMPLATE_SETTINGS_ACCESS_LIST', DEFAULT_ALLOWED_CONFIG)


def get_settings(request):
    return {
        name: getattr(settings, name, FALLBACK_VALUES.get(name))
        for name in TEMPLATE_SETTINGS_ACCESS_LIST
    }
