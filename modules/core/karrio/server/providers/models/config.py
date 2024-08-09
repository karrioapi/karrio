import functools
import django.db.models as models
import karrio.server.core.models as core


@core.register_model
class CarrierConfig(core.OwnedEntity):
    class Meta:
        db_table = "carrier-config"
        verbose_name = "Carrier Config"
        verbose_name_plural = "Carrier Configs"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="cfg_"),
    )
    carrier = models.ForeignKey(
        "Carrier",
        null=False,
        related_name="configs",
        on_delete=models.CASCADE,
    )
    config = models.JSONField(
        null=False,
        blank=False,
        default=core.field_default({}),
    )
