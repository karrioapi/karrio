from django_tenants.utils import tenant_context
from django.contrib.auth import get_user_model

from purpleserver.tenants.models import Client


def created_default_admin(sender: Client, **kwargs):
    with tenant_context(sender):
        if not any(get_user_model().objects.all()):
            get_user_model().objects.create_superuser('admin@domain.com', 'temp')
