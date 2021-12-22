from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "purplship.server.orders"

    def ready(self):
        from purplship.server.orders import signals

        signals.register_signals()
