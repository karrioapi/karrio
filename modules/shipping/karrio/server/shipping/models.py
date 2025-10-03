import functools
import django.conf as conf
import django.db.models as models
import django.utils.translation as translation

import karrio.server.core.models as core

_ = translation.gettext_lazy


class ShippingMethodManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@core.register_model
class ShippingMethod(core.OwnedEntity):
    objects = ShippingMethodManager()

    class Meta:
        db_table = "shipping-methods"
        verbose_name = "Shipping Method"
        verbose_name_plural = "Shipping Methods"
        ordering = ["-created_at"]

    def natural_key(self):
        return (self.slug,)

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="mtd_"),
        editable=False,
    )
    name = models.CharField(_("name"), max_length=100)
    slug = models.CharField(_("slug"), max_length=150, db_index=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    carrier_code = models.CharField(_("carrier_code"), max_length=100)
    carrier_service = models.CharField(_("carrier_service"), max_length=150)
    carrier_ids = models.JSONField(blank=True, null=True, default=core.field_default([]))
    carrier_options = models.JSONField(blank=True, null=True, default=core.field_default({}))
    
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))
    is_active = models.BooleanField(null=False, default=False)
    test_mode = models.BooleanField()

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    org = models.ManyToManyField(
        "orgs.Organization",
        related_name="shipping_methods",
        through="ShippingMethodLink"
    )

    # Compute fields
    @property
    def object_type(self):
        return "shipping-method"


class ShippingMethodLink(models.Model):
    """Link table for Organization to ShippingMethod one-to-many relationship"""

    org = models.ForeignKey(
        "orgs.Organization",
        on_delete=models.CASCADE,
        related_name="shipping_method_links",
    )
    item = models.OneToOneField(
        ShippingMethod,
        on_delete=models.CASCADE,
        related_name="link"
    )
