from django.db.models import signals

from karrio.server.core import utils
from karrio.server.core.logging import logger
from karrio.server import serializers
import karrio.server.documents.models as models


def register_all():
    signals.post_save.connect(document_updated, sender=models.DocumentTemplate)

    logger.info("Signal registration complete", module="karrio.documents")


@utils.disable_for_loaddata
def document_updated(sender, instance, *args, **kwargs):
    changes = kwargs.get("update_fields") or []
    post_create = "created_at" in changes

    if post_create:
        duplicates = models.DocumentTemplate.objects.filter(
            slug=instance.slug,
            **({"org__id": instance.link.org.id} if hasattr(instance, "link") else {})
        ).count()

        if duplicates > 1:
            raise serializers.ValidationError(
                {"slug": "Document template with this slug already exists."}
            )
