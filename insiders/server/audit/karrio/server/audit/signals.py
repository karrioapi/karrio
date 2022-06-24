import logging
from django.db.models import signals
from auditlog.models import LogEntry

from karrio.server.core import utils
from karrio.server.audit import models

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(logentry_created, sender=LogEntry)

    logger.info("karrio.audit signals registered...")


@utils.disable_for_loaddata
def logentry_created(sender, instance, created, *args, **kwargs):
    _log = models.AuditLogEntry.objects.get(pk=instance.pk)
    _content = instance.content_type.model_class().objects.get(pk=instance.object_pk)

    if hasattr(_content, "link") and not hasattr(_log, "link"):
        org = getattr(_content.link, "org", None)
        _log.link = instance.__class__.link.related.related_model.objects.create(
            org=org, item=instance
        )
        _log.save()

        logger.debug("auditlog created.")
