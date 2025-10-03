import logging

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.tracing.models as models
import karrio.server.serializers as serializers

logger = logging.getLogger(__name__)


@utils.error_wrapper
def save_tracing_records(context, tracer: lib.Tracer = None, schema: str = None):
    if conf.settings.PERSIST_SDK_TRACING is False:
        return

    tracer = tracer or getattr(context, "tracer", lib.Tracer())

    # Process Karrio SDK tracing records to persist records of interest.
    @utils.async_wrapper
    @utils.tenant_aware
    def persist_records(**kwarg):
        actor = getattr(context, "user", None)
        if len(tracer.records) == 0 or getattr(actor, "id", None) is None:
            return

        try:
            records = []
            exists = lib.identity(
                models.TracingRecord.access_by(context)
                .filter(
                    meta__request_log_id__isnull=False,
                    meta__request_log_id=tracer.context.get("request_log_id"),
                )
                .exists()
            )

            if exists:
                return

            for record in tracer.records:
                connection: dict = record.metadata.get("connection")

                records.append(
                    models.TracingRecord(
                        key=record.key,
                        record=record.data,
                        timestamp=record.timestamp,
                        created_by_id=getattr(actor, "id", None),
                        test_mode=connection.get("test_mode", False),
                        meta=lib.to_dict(
                            {
                                "tracer_id": tracer.id,
                                "object_id": tracer.context.get("object_id"),
                                "carrier_account_id": connection.get("id"),
                                "carrier_id": connection.get("carrier_id"),
                                "carrier_name": connection.get("carrier_name"),
                                "request_log_id": tracer.context.get("request_log_id"),
                            }
                        ),
                    )
                )

            saved_records = models.TracingRecord.objects.bulk_create(records)

            if getattr(context, "org", None) is not None:
                serializers.bulk_link_org(saved_records, context)

            logger.info("successfully saved tracing records...")
        except Exception as e:
            logger.error(e, exc_info=False)

    persist_records(schema=schema)


@utils.error_wrapper
def bulk_save_tracing_records(tracer: lib.Tracer, context=None):
    if conf.settings.PERSIST_SDK_TRACING is False:
        return

    if len(tracer.records) == 0 or context is None:
        return

    records = []

    for record in tracer.records:
        logger.debug([f"record: {record.key}", record.metadata])
        records.append(
            models.TracingRecord(
                key=record.key,
                record=record.data,
                timestamp=record.timestamp,
                test_mode=getattr(context, "test_mode", False),
                created_by_id=getattr(context.user, "id", None),
                meta=lib.to_dict({"tracer_id": tracer.id, **(record.metadata or {})}),
            )
        )

    saved_records = models.TracingRecord.objects.bulk_create(records)

    if getattr(context, "org", None) is not None:
        serializers.bulk_link_org(saved_records, context)

    logger.info("> tracing records saved...")


def set_tracing_context(**kwargs):

    from karrio.server.core import middleware

    request = middleware.SessionContext.get_current_request()
    request.tracer.add_context(kwargs)
