"""Manager background tasks.

Currently hosts the paperless-trade ``post_upload`` job (D14): for carriers
whose customs documents are uploaded *after* the label is created (e.g. GLS),
``core.paperless.finalize_paperless_trade`` stamps a ``pending`` marker on the
shipment and enqueues ``upload_paperless_documents`` here. The label has
already been returned to the caller, so this runs fully decoupled from the
purchase response.

Registered by eager import from ``ManagerConfig.ready()`` so the
``@background_task`` handler is known to the task backend.
"""

from types import SimpleNamespace

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.manager.models as models
import karrio.server.tracing.utils as tracing
from django.utils import timezone
from karrio.server.core.logging import logger
from karrio.server.core.middleware import SessionContext
from karrio.server.core.task_backend import background_task
from karrio.server.core.telemetry import with_task_telemetry
from karrio.server.serializers import get_object_context


def _record_upload_api_log(shipment, record, context, *, status_code: int) -> int | None:
    """Log the post_upload document-upload operation through the platform's default
    API-logging model (``APILogIndex``) and return the log id.

    The async job never passes through a DRF view, so the ``LoggingMixin`` that
    auto-logs ``POST /v1/documents/uploads`` doesn't run for it. We record the same
    operation here using the SAME model + fields the default logging produces (the
    real ``documents/uploads`` path, the upload record as ``data``/``response``),
    but key it to the shipment via ``entity_id`` so it lands on the shipment's
    API-logs view (``LogFilter`` filters ``APILogIndex`` by ``entity_id``). Its id
    is then stamped as ``request_log_id`` on the carrier traces so the timeline
    groups them (``LogType.records``). Best-effort: a logging hiccup must never fail
    the already-completed upload."""

    def _build() -> int | None:
        from karrio.server.core.models import APILogIndex
        from karrio.server.manager.serializers import DocumentUploadRecord as DocumentUploadRecordSerializer
        from karrio.server.serializers.abstract import link_org

        # ``record`` is the persisted DocumentUploadRecord instance — serialise it the
        # same way the real endpoint's response is logged.
        response = lib.to_dict(DocumentUploadRecordSerializer(record).data)
        log = APILogIndex(
            method="POST",
            path="/v1/documents/uploads",
            host=getattr(conf.settings, "APP_NAME", "karrio"),
            requested_at=timezone.now(),
            response_ms=0,
            status_code=status_code,
            entity_id=shipment.id,
            request_id=shipment.id,
            test_mode=getattr(shipment, "test_mode", True),
            data=lib.to_json({"shipment_id": shipment.id}),
            response=lib.to_json(response),
            query_params=lib.to_json({}),
        )
        log.save()
        link_org(log, context)
        return log.id

    return lib.failsafe(_build)


@background_task(queue="karrio-paperless", retries=5, retry_delay=60)
@utils.error_wrapper
@utils.tenant_aware
@with_task_telemetry("upload_paperless_documents")
def upload_paperless_documents(shipment_id: str, **kwargs):
    """post_upload paperless flow (D14): generate the customs invoice, upload it
    to the carrier, and submit customs against the already-created label.

    Idempotent — re-prepares every run (D17): a retry regenerates and
    re-uploads from scratch, and customs is submitted only once all uploads in
    the attempt succeed (the join inside the connector). Failures propagate so
    ``@background_task`` retries; the label itself is never invalidated.

    Owns a ``lib.Tracer()`` and binds it via ``SessionContext.scope`` so the
    carrier HTTP calls (prepare-upload / PUT / customs) land as shipment-
    correlated ``TracingRecord`` rows — workers have no request to carry one
    (see observability.md).
    """
    from karrio.server.manager.serializers.shipment import (
        generate_paperless_invoice,
        upload_customs_forms,
    )

    shipment = models.Shipment.objects.select_related(
        *(("link__org",) if conf.settings.MULTI_ORGANIZATIONS else ()),
    ).get(id=shipment_id)

    state = shipment.meta.get("paperless") or {}
    template = state.get("template")  # per-shipment DocumentTemplate slug, if any
    explicit = (shipment.options.get("doc_files") or [None])[0]
    # Use the merchant-supplied doc as-is; else generate from the per-shipment
    # template slug, falling back to the system-default template body
    # (PAPERLESS_DEFAULT_INVOICE_TEMPLATE) inside generate_paperless_invoice.
    document = explicit or generate_paperless_invoice(shipment, slug=template)

    if document is None:
        # Paperless was applicable (the carrier promised ETD and the merchant opted
        # in) but no document source resolved — neither an explicit doc_files entry
        # nor a template (per-shipment invoice_template / PAPERLESS_DEFAULT_INVOICE_TEMPLATE).
        # D15: never a silent no-op — surface an actionable status the merchant can see.
        reason = (
            "No customs document to upload: the shipment supplied no doc_files and no "
            "invoice template resolved. Set the PAPERLESS_DEFAULT_INVOICE_TEMPLATE system "
            "config (the default invoice template body), or pass options.invoice_template "
            "(a DocumentTemplate slug)."
        )
        logger.warning(f"paperless post_upload skipped: {reason}", shipment_id=shipment_id)
        shipment.meta = {
            **shipment.meta,
            "paperless": {**state, "status": "skipped", "reason": reason},
        }
        shipment.save(update_fields=["meta"])
        return

    # Context (org) is rebuilt from the shipment, not a request — workers have none.
    context = get_object_context(shipment)

    # Own a tracer and bind it as the current request so the internally-resolved
    # carrier.gateway accumulates the HTTP req/resp into it; persist after.
    tracer = lib.Tracer()
    tracer.add_context({"object_id": shipment.id, "request_id": shipment.id})
    request_like = SimpleNamespace(
        tracer=tracer,
        user=context.user,
        org=context.org,
        request_id=shipment.id,
    )

    # gateway.Documents.upload -> connector proxy.upload_document orchestrates
    # prepare-upload + PUT (per doc) -> customs submission (TrackID + documentIds).
    with SessionContext.scope(request_like):
        record = upload_customs_forms(shipment, document, context=context)

    # A carrier rejection (e.g. GLS customs validation) comes back as messages,
    # not an exception — surface it on the marker instead of reporting "done".
    messages = lib.to_dict(getattr(record, "messages", None) or [])
    status = "failed" if messages else "done"

    # Synthesise an APILog for the upload op + stamp its id as request_log_id on the
    # tracer, so the carrier HTTP calls group under it in the dashboard timeline
    # (keyed to the shipment via entity_id). Then persist the traces synchronously.
    log_id = _record_upload_api_log(shipment, record, context, status_code=(424 if messages else 201))
    if log_id is not None:
        tracer.add_context({"request_log_id": log_id})
    tracing.save_tracing_records(context, tracer=tracer, run_synchronous=True)

    paperless = {**state, "status": status, **({"errors": messages} if messages else {})}
    shipment.meta = {**shipment.meta, "paperless": paperless}
    shipment.save(update_fields=["meta"])
    logger.info(f"paperless post_upload {status}", shipment_id=shipment_id)
