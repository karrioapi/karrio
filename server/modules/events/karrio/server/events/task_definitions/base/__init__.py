import time
import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

import karrio.server.core.utils as utils

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(
    getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60
)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def background_trackers_update():
    from karrio.server.events.task_definitions.base.tracking import update_trackers

    @utils.run_on_all_tenants
    def _run(**kwargs):
        try:
            update_trackers()
        except Exception as e:
            logger.error(f"failed to crawl tracking statuses: {e}")

    _run()


@db_task()
@utils.tenant_aware
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.task_definitions.base.webhook import (
        notify_webhook_subscribers,
    )

    utils.failsafe(
        lambda: notify_webhook_subscribers(*args, **kwargs),
        "An error occured during webhook notification: $error",
    )


@db_task()
@utils.error_wrapper
@utils.async_wrapper
@utils.tenant_aware
def upload_paperless_document(**kwargs):
    """This function checks if paperless is supported and automatically
    triggers a document upload.
    """ 
    
    if settings.MULTI_TENANTS and kwargs.get('schema') == 'public':
        return
    
    time.sleep(10)
    logger.info("> start invoice upload...")
    try:
        import karrio.server.manager.serializers.document as documents
        import karrio.server.serializers as serializers
        import karrio.server.manager.models as models
        shipment = models.Shipment.objects.get(id=kwargs.get("shipment_id"))
        carrier = getattr(shipment, "selected_rate_carrier")
        context = serializers.get_object_context(shipment)
        document = kwargs["document"]

        # Skip if paperless is not supported
        if (
            "paperless_trade" in carrier.capabilities
            or shipment.options.get("paperless_trade") == True
            or shipment.options.get("fedex_electronic_trade_documents") == True
        ) is False:
            logger.info("> paperless_trade not supported.")
            return

        # upload custom invoice
        (
            documents.DocumentUploadSerializer.map(
                (
                    shipment.shipment_upload_record
                    if hasattr(shipment, "shipment_upload_record")
                    else None
                ),
                data=dict(
                    shipment_id=shipment.id,
                    reference=shipment.tracking_number,
                    tracking_number=shipment.tracking_number,
                    document_files=[
                        dict(
                            doc_file=document["doc_file"],
                            doc_name=document["doc_name"],
                            doc_type=document["doc_type"] or "commercial_invoice",
                        )
                    ],
                ),
                context=context,
            )
            .save(shipment=shipment, carrier=carrier)
            .instance
        )
        logger.info("> invoice successfully uploaded.")
    except Exception as e:
        logger.exception(e)
        logger.info("> document upload failed.")



TASK_DEFINITIONS = [
    background_trackers_update,
    upload_paperless_document,
    notify_webhooks,
]
