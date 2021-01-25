from django.apps import AppConfig


class TenantsConfig(AppConfig):
    name = 'purpleserver.tenants'

    def ready(self):
        # Setup signal for tenant creation update
        from django_tenants.signals import post_schema_sync
        from purpleserver.tenants.models import Client
        from purpleserver.tenants.signals import created_default_admin
        post_schema_sync.connect(created_default_admin, sender=Client)

        # Init Constance for all tenants
        # from django_tenants.utils import tenant_context
        # for client in Client.objects.all():
        #     with tenant_context(client):
        #         import constance
        #         from purpleserver.core.signals import update_settings
        #         update_settings(constance.config)

