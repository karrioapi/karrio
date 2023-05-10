from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

import karrio.server.core.models as core


class Client(TenantMixin):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    feature_flags = models.JSONField(
        null=True,
        blank=True,
        default=core.field_default({}),
        help_text="The feature flags.",
    )
    app_domains = models.JSONField(
        null=True,
        blank=True,
        default=core.field_default([]),
        help_text="App domains.",
    )

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.name

    @property
    def object_type(self):
        return "tenant"


class Domain(DomainMixin):
    def __str__(self):
        return self.domain

    @property
    def object_type(self):
        return "domain"
