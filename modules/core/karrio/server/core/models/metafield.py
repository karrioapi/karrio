import functools
import django.conf as conf
import django.db.models as models
import django.utils.translation as translation

import karrio.server.core.models.base as core
import karrio.server.core.models.entity as entity

_ = translation.gettext_lazy


@core.register_model
class Metafield(entity.OwnedEntity):
    class Meta:
        db_table = "metafield"
        verbose_name = "Metafield"
        verbose_name_plural = "Metafields"

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="metaf_"),
    )
    key = models.CharField(_("name"), max_length=50, db_index=True)
    value = models.CharField(null=True, blank=True, max_length=250)
    type = models.CharField(
        _("type"),
        max_length=50,
        choices=core.METAFIELD_TYPE,
        default=core.METAFIELD_TYPE[0][0],
        db_index=True,
    )
    is_required = models.BooleanField(null=False, default=False)

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    @property
    def object_type(self):
        return "metafield"
