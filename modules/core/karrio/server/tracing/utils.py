import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.serializers as serializers
import karrio.server.tracing.models as models
from karrio.server.core.logging import logger


def _json_safe(value):
    """Coerce a trace payload into something the ``record`` JSONField can store.

    Carriers that send binary bodies (e.g. GLS uploads a document to a
    pre-signed URL with raw PDF bytes) put ``bytes`` into the trace data, which
    is not JSON-serializable and silently breaks persistence. Elide bytes to a
    size marker — also keeps raw document/PII bytes out of the trace records
    (see observability.md).
    """
    if isinstance(value, (bytes, bytearray)):
        return f"<{len(value)} bytes elided>"
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value


@utils.error_wrapper
def save_tracing_records(context, tracer: lib.Tracer = None, schema: str = None, run_synchronous: bool = False):
    """Persist a tracer's records as ``TracingRecord`` rows.

    ``run_synchronous=True`` writes inline rather than on a background thread —
    use it from a Huey task so the records are committed before the task returns
    (the request path leaves it async; see observability.md).
    """
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
                        record=_json_safe(record.data),
                        timestamp=record.timestamp,
                        created_by_id=getattr(actor, "id", None),
                        test_mode=connection.get("test_mode", False),
                        meta=lib.to_dict(
                            {
                                "tracer_id": tracer.id,
                                "request_id": tracer.context.get("request_id"),
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

            logger.info("Tracing records saved successfully", record_count=len(saved_records))
        except Exception as e:
            logger.error("Failed to save tracing records", error=str(e))

    persist_records(schema=schema, run_synchronous=run_synchronous)


@utils.error_wrapper
def bulk_save_tracing_records(tracer: lib.Tracer, context=None):
    if conf.settings.PERSIST_SDK_TRACING is False:
        return

    if len(tracer.records) == 0 or context is None:
        return

    records = []

    for record in tracer.records:
        logger.debug("Processing tracing record", record_key=record.key, metadata=record.metadata)
        records.append(
            models.TracingRecord(
                key=record.key,
                record=_json_safe(record.data),
                timestamp=record.timestamp,
                test_mode=getattr(context, "test_mode", False),
                created_by_id=getattr(context.user, "id", None),
                meta=lib.to_dict({"tracer_id": tracer.id, **(record.metadata or {})}),
            )
        )

    saved_records = models.TracingRecord.objects.bulk_create(records)

    if getattr(context, "org", None) is not None:
        serializers.bulk_link_org(saved_records, context)

    logger.info("Tracing records saved successfully", record_count=len(saved_records))


def set_tracing_context(**kwargs):

    from karrio.server.core import middleware

    request = middleware.SessionContext.get_current_request()
    tracer = getattr(request, "tracer", None)
    if tracer is not None:
        tracer.add_context(kwargs)

    _propagate_to_sentry(kwargs)


_SENTRY_TAG_KEYS = {"shipment_id", "tracking_number", "object_id"}


def _propagate_to_sentry(context: dict):
    """Propagate shipment-related context to Sentry tags and structured context."""
    try:
        import sentry_sdk
    except ImportError:
        return

    try:
        for key in _SENTRY_TAG_KEYS:
            value = context.get(key)
            if value:
                sentry_sdk.set_tag(key, value)

        shipment_id = context.get("shipment_id")
        tracking_number = context.get("tracking_number")
        if shipment_id or tracking_number:
            sentry_sdk.set_context(
                "shipment",
                lib.to_dict(
                    {
                        "shipment_id": shipment_id,
                        "tracking_number": tracking_number,
                    }
                ),
            )
    except Exception as e:
        logger.debug("Failed to propagate tracing context to sentry", error=str(e))
