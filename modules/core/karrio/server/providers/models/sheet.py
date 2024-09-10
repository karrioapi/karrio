import functools
import django.db.models as models
import django.utils.translation as translation

import django.conf as conf
import karrio.server.core.models as core

_ = translation.gettext_lazy


@core.register_model
class RateSheet(core.OwnedEntity):
    class Meta:
        db_table = "rate-sheet"
        verbose_name = "Rate Sheet"
        verbose_name_plural = "Rate Sheets"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="rsht_"),
    )
    name = models.CharField(_("name"), max_length=50, db_index=True)
    slug = models.CharField(_("slug"), max_length=50, db_index=True)
    carrier_name = models.CharField(max_length=50, db_index=True)
    is_system = models.BooleanField(default=False, db_index=True)
    services = models.ManyToManyField(
        "ServiceLevel", blank=True, related_name="service_sheet"
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
    )

    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    def delete(self, *args, **kwargs):
        self.services.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "rate-sheet"

    @property
    def carriers(self):
        import karrio.server.providers.models as providers

        return providers.Carrier.objects.filter(
            carrier_code=self.carrier_name, rate_sheet__id=self.id
        )
