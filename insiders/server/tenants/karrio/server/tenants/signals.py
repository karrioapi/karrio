import logging
from decouple import config
from django.dispatch import receiver
from django_tenants.models import TenantMixin
from django_tenants.signals import post_schema_sync
from django_tenants.utils import tenant_context
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


def register_all():
    logger.info("karrio.tenants signals registered...")


@receiver(post_schema_sync, sender=TenantMixin)
def check_post_schema_sync(**kwargs):
    UserModel = get_user_model()
    client = kwargs['tenant']

    with tenant_context(client):
        if any(UserModel.objects.all()):
            return

        UserModel.objects.create_superuser(
            config("ADMIN_EMAIL", default="admin@example.com"),
            config("ADMIN_PASSWORD", default="demo"),
            full_name=client.name,
        )

    logger.info("tenant successfully initialized..")
