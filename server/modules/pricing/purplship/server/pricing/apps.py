from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PricingConfig(AppConfig):
    name = 'purplship.server.pricing'
    verbose_name = _('Custom Pricing')

    def ready(self):
        from purplship.server.pricing.signals import register_rate_post_processing
        register_rate_post_processing()
