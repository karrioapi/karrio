import logging
import concurrent.futures as futures

from karrio.core.settings import Settings
from karrio.core.utils import DP, Tracer
from karrio.server.conf import settings
from karrio.server.core import utils
from karrio.server.tracing import models

logger = logging.getLogger(__name__)


def save_tracing_records(context, tracer: Tracer = None, schema: str = None):
    if settings.PERSIST_SDK_TRACING is False:
        return

    tracer = tracer or getattr(context, "tracer", Tracer())

    # Process Karrio SDK tracing records to persist records of interest.
    @utils.async_wrapper
    @utils.tenant_aware
    def persist_records(**kwarg):
        actor = getattr(context, "user", None)

        if len(tracer.records) == 0 or getattr(actor, "id", None) is None:
            return

        try:
            records = []
            exists = models.TracingRecord.access_by(context).filter(
                meta__request_log_id__isnull=False,
                meta__request_log_id=tracer.context.get("request_log_id")
            ).exists()

            if exists:
                return

            for record in tracer.records:
                connection: Settings = record.metadata.get("connection")

                records.append(
                    models.TracingRecord(
                        key=record.key,
                        record=record.data,
                        timestamp=record.timestamp,
                        created_by_id=getattr(actor, "id", None),
                        test_mode=getattr(connection, "test_mode", False),
                        meta=DP.to_dict(
                            {
                                "tracer_id": tracer.id,
                                "object_id": tracer.context.get("object_id"),
                                "carrier_account_id": getattr(connection, "id", None),
                                "carrier_id": getattr(connection, "carrier_id", None),
                                "carrier_name": getattr(
                                    connection, "carrier_name", None
                                ),
                                "request_log_id": tracer.context.get("request_log_id"),
                            }
                        ),
                    )
                )

            saved_records = models.TracingRecord.objects.bulk_create(records)

            if (settings.MULTI_ORGANIZATIONS) and (
                getattr(context, "org", None) is not None
            ):
                _linked = []

                for record in saved_records:
                    record.link = (
                        record.__class__.link.related.related_model.objects.create(
                            org=context.org, item=record
                        )
                    )

                models.TracingRecord.objects.bulk_update(_linked, fields=["updated_at"])

            logger.info("successfully saved tracing records...")
        except Exception as e:
            logger.error(e, exc_info=False)

    persist_records(schema=schema)


def set_tracing_context(**kwargs):
    from karrio.server.core import middleware

    request = middleware.SessionContext.get_current_request()
    request.tracer.add_context(kwargs)
