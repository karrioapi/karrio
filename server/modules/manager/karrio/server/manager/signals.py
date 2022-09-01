import logging
from django.db.models import signals

from karrio.server.core import utils
import karrio.server.manager.models as models
import karrio.server.manager.serializers as serializers

logger = logging.getLogger(__name__)
RATE_RELATED_CHANGES = [
    # address related changes
    "address_line1",
    "address_line2",
    "postal_code",
    "city",
    "state_province",
    "country_code",
    "residential",
    # parcel related changes
    "length",
    "width",
    "height",
    "weight",
    "weight_unit",
    "dimension_unit",
    "is_document",
]


def register_signals():
    signals.post_save.connect(address_updated, sender=models.Address)
    signals.post_save.connect(parcel_updated, sender=models.Parcel)
    signals.post_delete.connect(parcel_deleted, sender=models.Parcel)

    logger.info("karrio.manager signals registered...")


@utils.disable_for_loaddata
def address_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """ """
    changes = update_fields or []

    if any([change in RATE_RELATED_CHANGES for change in changes]):
        serializers.reset_related_shipment_rates(instance.shipment)


@utils.disable_for_loaddata
def parcel_updated(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """ """
    changes = update_fields or []

    if instance.reference_number is None:
        count = models.Parcel.objects.filter(
            **({"org__id": instance.link.org.id} if hasattr(instance, "link") else {})
        ).count()

        instance.reference_number = str(count + 1).zfill(10)
        instance.save()

    if any([change in RATE_RELATED_CHANGES for change in changes]):
        serializers.reset_related_shipment_rates(instance.shipment)


@utils.disable_for_loaddata
def parcel_deleted(sender, instance, *args, **kwargs):
    """ """
    serializers.reset_related_shipment_rates(instance.shipment)
