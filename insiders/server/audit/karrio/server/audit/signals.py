import logging
from django.db.models import signals
from auditlog.models import LogEntry

from karrio.server.core import utils
from karrio.server.audit import models

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(logentry_created, sender=LogEntry)

    logger.info("karrio.audit signals registered...")


@utils.async_warpper
@utils.disable_for_loaddata
def logentry_created(sender, instance, created, *args, **kwargs):
    try:
        # Attempt to retrieve the auditlog object or gets a previous auditlog related to
        # the same object in case the object has been deleted since then.
        _related = (
            instance.content_type.model_class()
            .objects.filter(pk=instance.object_pk)
            .first()
            or models.AuditLogEntry.objects.filter(
                object_pk=instance.object_pk, link__isnull=False
            ).first()
        )

        if (
            _related is not None
            and hasattr(_related, "link")
            and not hasattr(instance, "link")
        ):
            org = getattr(_related.link, "org", None)
            instance.link = (
                instance.__class__.link.related.related_model.objects.create(
                    org=org, item=instance
                )
            )
            instance.save()

            logger.debug("auditlog created.")
    except Exception as e:
        logger.error(e)
