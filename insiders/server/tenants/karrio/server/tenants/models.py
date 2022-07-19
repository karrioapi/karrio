from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

import karrio.server.conf as conf
import karrio.server.core.models as core
import karrio.server.core.fields as fields

FEATURE_FLAGS = [(f, f) for f in conf.FEATURE_FLAGS]


class Client(TenantMixin):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    feature_flags = fields.MultiChoiceField(
        models.CharField(max_length=100, choices=FEATURE_FLAGS),
        default=core.field_default(conf.FEATURE_FLAGS),
        help_text="The list of feature flags.",
    )

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    def __str__(self):
        return self.domain
