import logging
import concurrent.futures as futures
from django.conf import settings
from karrio.core.settings import Settings

from karrio.core.utils import DP, Tracer
from karrio.server.tracing import models

logger = logging.getLogger(__name__)


def save_tracing_records(context, tracer: Tracer = None):
    tracer = tracer or getattr(context, "tracer", Tracer())

    # Process Karrio SDK tracing records to persist records of interest.
    def persist_records():
        if len(tracer.records) == 0:
            return

        try:
            actor = getattr(context, "user", None)
            records = []

            for record in tracer.records:
                connection: Settings = record.metadata.get("connection")

                records.append(
                    models.TracingRecord(
                        key=record.key,
                        record=record.data,
                        timestamp=record.timestamp,
                        created_by_id=getattr(actor, "id", None),
                        test_mode=getattr(connection, "test", False),
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

    futures.ThreadPoolExecutor(max_workers=1).submit(persist_records)


def set_tracing_context(**kwargs):
    from karrio.server.core import middleware

    request = middleware.SessionContext.get_current_request()
    request.tracer.add_context(kwargs)
