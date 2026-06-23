"""Paperless trade (electronic trade documents) — core orchestration.

A carrier declares its paperless support on the ``paperless_trade``
``OptionEnum`` alias in its ``ShippingOption`` enum. The ``meta`` dict on
that alias carries:

  - ``category="PAPERLESS"`` — discovered at registration time by
    ``references.detect_capabilities`` to populate
    ``Connection.capabilities``.
  - ``flow``      — one of ``doc_files`` / ``doc_references`` /
                    ``post_upload`` / ``flag_only``. Encodes HOW the
                    generated invoice is delivered to the carrier and
                    WHEN (pre- vs post-create).
  - ``upload_flow`` — optional. When present alongside a ``flag_only``
                    default, the carrier is treated as hybrid: ``flag_only``
                    unless the merchant supplies an explicit ``doc_files``
                    or an ``invoice_template`` to generate from, in which
                    case the flow is promoted to ``upload_flow`` (typically
                    ``doc_references``). UPS is the canonical hybrid.

``buy_shipment_label`` composes three steps over this module:

  prepare_paperless_trade(...)          # decide + maybe generate the invoice
  augment_options_with_paperless(...)   # pre-create option injection
  finalize_paperless_trade(...)         # post-create upload (post_upload flow)

None of those steps run unless the carrier supports paperless and the
shipment opted in.
"""

import pydoc

import attr

PAPERLESS_FLOW_DOC_FILES = "doc_files"
PAPERLESS_FLOW_DOC_REFERENCES = "doc_references"
PAPERLESS_FLOW_POST_UPLOAD = "post_upload"
PAPERLESS_FLOW_FLAG_ONLY = "flag_only"


@attr.s(auto_attribs=True)
class PaperlessTrade:
    """Resolved paperless-trade plan for a single shipment purchase."""

    flow: str = ""  # empty when paperless does not apply
    document: dict | None = None  # generated invoice (None for flag_only / when generation is deferred)
    template: str | None = None  # carried for post_upload — the background job generates from this

    @property
    def applies(self) -> bool:
        return bool(self.flow)

    @property
    def generated(self) -> bool:
        return self.document is not None


def resolve_invoice_template(shipment) -> str | None:
    """The merchant's per-shipment invoice ``DocumentTemplate`` **slug**, if set.

    This is distinct from the system-wide default, which is a template *body*
    (``PAPERLESS_DEFAULT_INVOICE_TEMPLATE``) applied at generation time by
    ``generate_paperless_invoice`` — not a slug. Returning only the per-shipment
    slug here keeps the two interfaces (slug vs. body) from being conflated."""
    return shipment.options.get("invoice_template") or None


def supports_paperless_trade(carrier, shipment) -> bool:
    """Whether ETD applies: the carrier advertises `paperless` and the shipment opted in."""
    return bool("paperless" in carrier.capabilities and shipment.options.get("paperless_trade"))


def carrier_paperless_flow(carrier) -> str:
    """The carrier's declared paperless flow, read from its ``paperless_trade``
    ``OptionEnum`` ``meta["flow"]``. Defaults to ``doc_files`` when a carrier
    declares paperless support without specifying a flow."""
    return _carrier_paperless_meta(carrier).get("flow") or PAPERLESS_FLOW_DOC_FILES


def carrier_paperless_upload_flow(carrier) -> str | None:
    """The flow a carrier promotes to when a document is explicitly supplied.

    Read from ``meta["upload_flow"]`` on the carrier's ``paperless_trade``
    OptionEnum. UPS is the canonical case: ``flow="flag_only"`` by default,
    ``upload_flow="doc_references"`` when ``doc_files`` or ``invoice_template``
    is provided.
    """
    return _carrier_paperless_meta(carrier).get("upload_flow")


def _carrier_paperless_meta(carrier) -> dict:
    """Resolve ``meta`` from the carrier's ``ShippingOption.paperless_trade``
    alias. Returns an empty dict if the carrier doesn't declare paperless."""
    options_cls = pydoc.locate(f"karrio.providers.{carrier.carrier_name}.units.ShippingOption")
    if options_cls is None:
        return {}
    member = getattr(options_cls, "paperless_trade", None)
    if member is None:
        return {}
    return getattr(member.value, "meta", None) or {}


def prepare_paperless_trade(
    shipment,
    carrier,
    invoice_template: str | None,
    selected_rate: dict | None = None,
) -> PaperlessTrade:
    """Decide whether/how paperless applies and pre-generate the invoice when the flow needs it.

    Returns an inert ``PaperlessTrade()`` when paperless does not apply, so callers
    compose unconditionally. Carriers declaring an ``upload_flow`` are promoted
    from their default flow to that upload flow when the merchant supplies
    ``doc_files`` explicitly or provides an ``invoice_template`` to generate from.
    """
    if not supports_paperless_trade(carrier, shipment):
        return PaperlessTrade()

    flow = carrier_paperless_flow(carrier)
    upload_flow = carrier_paperless_upload_flow(carrier)
    has_explicit_document = bool(shipment.options.get("doc_files") or invoice_template)
    if upload_flow and has_explicit_document:
        flow = upload_flow

    if flow == PAPERLESS_FLOW_FLAG_ONLY:
        return PaperlessTrade(flow=flow)

    # An explicit ``doc_files`` supplied by the merchant is used as-is (no
    # generation) for every doc-requiring flow — the caller already has the PDF.
    explicit_docs = shipment.options.get("doc_files") or []
    explicit_doc = explicit_docs[0] if isinstance(explicit_docs, list) and explicit_docs else None

    # ``post_upload`` (GLS) DEFERS generation to the background job (D14): nothing
    # is generated or injected pre-create. Carry the explicit doc if supplied,
    # else the template the job will generate from. Paperless still applies — no
    # silent no-op when no template is set (D15); the job resolves the source.
    if flow == PAPERLESS_FLOW_POST_UPLOAD:
        return PaperlessTrade(flow=flow, document=explicit_doc, template=invoice_template)

    # Pre-create flows (``doc_files`` / ``doc_references``) need the document NOW
    # because it must ride / precede the carrier ``create`` call.
    if explicit_doc is not None:
        return PaperlessTrade(flow=flow, document=explicit_doc)

    # Late-import the carrier-side helpers to keep core/paperless.py free of a
    # hard dependency on the manager module (which owns the document
    # generation + upload plumbing).
    from karrio.server.core.utils import create_carrier_snapshot
    from karrio.server.manager.serializers.shipment import generate_paperless_invoice

    # Generation reads the carrier/rate snapshot off the shipment for the template context.
    shipment.carrier = create_carrier_snapshot(carrier)
    shipment.selected_rate = selected_rate
    # Generate from the per-shipment template slug, else the system-default
    # template body (PAPERLESS_DEFAULT_INVOICE_TEMPLATE). Stay inert pre-create
    # only when neither resolves — there's no document to ride the create call.
    document = generate_paperless_invoice(shipment, slug=invoice_template)
    return PaperlessTrade(flow=flow, document=document) if document is not None else PaperlessTrade()


def _inject_doc_files(options: dict, document: dict, shipment, context) -> dict:
    return {**options, "doc_files": [document]}


def _inject_doc_references(options: dict, document: dict, shipment, context) -> dict:
    from karrio.server.manager.serializers.shipment import upload_customs_forms

    upload = upload_customs_forms(shipment, document, context=context)
    return {**options, "doc_references": upload.documents}


def _inject_nothing(options: dict, document: dict, shipment, context) -> dict:
    return options  # flag_only (no doc) and post_upload (handled after create)


# flow -> pre-create option injector
PAPERLESS_PRE_PURCHASE_INJECTORS = {
    PAPERLESS_FLOW_DOC_FILES: _inject_doc_files,
    PAPERLESS_FLOW_DOC_REFERENCES: _inject_doc_references,
    PAPERLESS_FLOW_POST_UPLOAD: _inject_nothing,
    PAPERLESS_FLOW_FLAG_ONLY: _inject_nothing,
}


def augment_options_with_paperless(
    options: dict,
    paperless: PaperlessTrade,
    shipment,
    context=None,
) -> dict:
    """Pre-create option augmentation, dispatched by flow. Returns ``options`` unchanged when N/A."""
    if not paperless.generated:
        return options

    inject = PAPERLESS_PRE_PURCHASE_INJECTORS.get(paperless.flow, _inject_nothing)
    return inject(options, paperless.document, shipment, context)


def finalize_paperless_trade(
    purchased_shipment,
    paperless: PaperlessTrade,
    context=None,
) -> None:
    """post_upload flow (D14): stamp a ``pending`` marker on the shipment and
    DISPATCH the upload to a background job — never inline. The job generates
    the invoice, uploads it, submits customs against the created label, and
    attaches the ``DocumentUploadRecord``. The label has already been returned
    to the caller; an upload failure retries and never invalidates it.
    """
    if paperless.flow != PAPERLESS_FLOW_POST_UPLOAD:
        return

    purchased_shipment.meta = {
        **(purchased_shipment.meta or {}),
        "paperless": {"status": "pending", "template": paperless.template},
    }
    purchased_shipment.save(update_fields=["meta"])

    # Late import: calling the @background_task wrapper ENQUEUES (it does not run
    # inline). Keeps core free of an import-time dependency on the manager tasks.
    from django.db import transaction
    from karrio.server.manager.tasks import upload_paperless_documents

    # Enqueue AFTER the purchase transaction commits. The purchase runs in
    # ``@transaction.atomic`` (ShipmentSerializer.create), and under HUEY immediate
    # mode (dev) the task would otherwise run inline INSIDE that transaction — before
    # the shipment's org link is committed/visible — so ``get_object_context(shipment)``
    # would resolve org=None and the upload + tracing records would be mis-scoped
    # (org=None / wrong tenant). ``on_commit`` defers the dispatch until the row and
    # its org link are durable; it's also correct for the async worker (never enqueue
    # a job for a shipment that may roll back). Runs immediately if no transaction is active.
    shipment_id = purchased_shipment.id
    transaction.on_commit(lambda: upload_paperless_documents(shipment_id))
