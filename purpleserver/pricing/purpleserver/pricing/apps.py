from django.apps import AppConfig


class PricingConfig(AppConfig):
    name = 'purpleserver.pricing'

    def ready(self):
        from purpleserver.pricing.signals import register_rate_post_processing
        register_rate_post_processing()
