"""Unit tests for the paperless-trade helpers in ``karrio.server.core.paperless``.

These cover the flow dispatch, capability gate, and the prepare → augment →
finalize composition. Only the external document upload is mocked; the rest is
pure logic, so no DB is needed. The end-to-end purchase path is covered by the
integration tests in test_shipments.py.
"""

import unittest
from types import SimpleNamespace
from unittest import mock

import karrio.server.core.paperless as paperless
import karrio.server.manager.models as models
import karrio.server.tracing.models as tracing_models
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from karrio.server.core.middleware import SessionContext
from karrio.server.core.models import APILogIndex
from karrio.server.manager.tasks import upload_paperless_documents

# Patch targets for the lazy-imported manager-side helpers. These live where
# they're defined; ``core.paperless`` only references them by re-import at
# call time, so patches MUST target the canonical paths below.
# ``generate_paperless_invoice`` resolves the per-shipment template slug, else
# the system-default template body — both prepare() and the post_upload job use it.
GENERATE_INVOICE = "karrio.server.manager.serializers.shipment.generate_paperless_invoice"
UPLOAD_FORMS = "karrio.server.manager.serializers.shipment.upload_customs_forms"
CARRIER_SNAPSHOT = "karrio.server.core.utils.create_carrier_snapshot"
# post_upload dispatches this Huey task (D14); finalize enqueues by calling it.
UPLOAD_TASK = "karrio.server.manager.tasks.upload_paperless_documents"

DOCUMENT = {
    "doc_format": "PDF",
    "doc_name": "commercial_invoice.pdf",
    "doc_type": "commercial_invoice",
    "doc_file": "base64==",
}


def _carrier(name="fedex", capabilities=("paperless",)):
    # carrier is a gateway object (not an ORM model) — a light fake is appropriate.
    return SimpleNamespace(carrier_name=name, capabilities=list(capabilities))


def _shipment(options=None, meta=None):
    # post_upload finalize stamps meta + saves; give the fake an id, meta, and a no-op save.
    return SimpleNamespace(
        id="shp_test",
        options=options or {},
        meta=meta if meta is not None else {},
        save=lambda **kwargs: None,
    )


class TestPaperlessTradeHelpers(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_carrier_flow_reads_optionenum_meta(self):
        """Flow comes from the carrier's ``ShippingOption.paperless_trade``
        ``meta["flow"]``. Defaults to ``doc_files`` when paperless is declared
        without a flow."""
        with mock.patch.object(paperless, "_carrier_paperless_meta", return_value={"flow": "doc_files"}):
            self.assertEqual(paperless.carrier_paperless_flow(_carrier()), paperless.PAPERLESS_FLOW_DOC_FILES)
        with mock.patch.object(paperless, "_carrier_paperless_meta", return_value={"flow": "flag_only"}):
            self.assertEqual(paperless.carrier_paperless_flow(_carrier()), paperless.PAPERLESS_FLOW_FLAG_ONLY)
        # Empty meta falls back to doc_files.
        with mock.patch.object(paperless, "_carrier_paperless_meta", return_value={}):
            self.assertEqual(paperless.carrier_paperless_flow(_carrier()), paperless.PAPERLESS_FLOW_DOC_FILES)

    def test_carrier_upload_flow_only_when_meta_declares_it(self):
        """``upload_flow`` lives next to ``flow`` and powers the hybrid promotion."""
        with mock.patch.object(
            paperless,
            "_carrier_paperless_meta",
            return_value={"flow": "flag_only", "upload_flow": "doc_references"},
        ):
            self.assertEqual(
                paperless.carrier_paperless_upload_flow(_carrier()),
                paperless.PAPERLESS_FLOW_DOC_REFERENCES,
            )
        with mock.patch.object(paperless, "_carrier_paperless_meta", return_value={"flow": "doc_files"}):
            self.assertIsNone(paperless.carrier_paperless_upload_flow(_carrier()))

    def test_prepare_promotes_to_upload_flow_when_document_supplied(self):
        """A carrier declaring both ``flow`` and ``upload_flow`` is promoted to
        the upload flow when the merchant supplies an explicit document or
        invoice template — otherwise the default flow stays in effect."""
        meta = {"flow": "flag_only", "upload_flow": "doc_references"}
        with mock.patch.object(paperless, "_carrier_paperless_meta", return_value=meta):
            # No template, no doc → stays flag_only, no document generated.
            plan = paperless.prepare_paperless_trade(
                _shipment({"paperless_trade": True}),
                _carrier(),
                invoice_template=None,
            )
            self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_FLAG_ONLY)
            self.assertFalse(plan.generated)

            # With invoice_template → promoted to doc_references, document generated.
            with (
                mock.patch(GENERATE_INVOICE, return_value=DOCUMENT) as gen,
                mock.patch(CARRIER_SNAPSHOT, return_value=None),
            ):
                plan = paperless.prepare_paperless_trade(
                    _shipment({"paperless_trade": True}),
                    _carrier(),
                    invoice_template="commercial_invoice",
                )
                self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_DOC_REFERENCES)
                self.assertTrue(plan.generated)
                gen.assert_called_once()

    def test_prepare_flag_only_fires_without_invoice_template(self):
        """Flag-only carriers don't need an invoice_template — paperless still
        applies, no document is generated."""
        with mock.patch.object(paperless, "_carrier_paperless_meta", return_value={"flow": "flag_only"}):
            plan = paperless.prepare_paperless_trade(
                _shipment({"paperless_trade": True}),
                _carrier(),
                invoice_template=None,
            )
            self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_FLAG_ONLY)
            self.assertFalse(plan.generated)

    def test_resolve_invoice_template_returns_per_shipment_slug(self):
        """resolve_invoice_template returns ONLY the per-shipment slug."""
        self.assertEqual(
            paperless.resolve_invoice_template(_shipment({"invoice_template": "per_shipment"})),
            "per_shipment",
        )

    def test_resolve_invoice_template_ignores_system_default_body(self):
        """The system default is a template *body* applied at generation time by
        ``generate_paperless_invoice`` — NOT a slug. resolve_invoice_template must
        not surface it (returns None with no per-shipment slug), so the two
        interfaces (slug vs. body) never get conflated."""
        with override_settings(PAPERLESS_DEFAULT_INVOICE_TEMPLATE="<html>default body</html>"):
            self.assertIsNone(paperless.resolve_invoice_template(_shipment({})))

    def test_supports_requires_capability_and_option(self):
        self.assertTrue(
            paperless.supports_paperless_trade(
                _carrier(capabilities=["paperless"]),
                _shipment({"paperless_trade": True}),
            )
        )
        self.assertFalse(
            paperless.supports_paperless_trade(_carrier(capabilities=[]), _shipment({"paperless_trade": True}))
        )
        self.assertFalse(paperless.supports_paperless_trade(_carrier(capabilities=["paperless"]), _shipment({})))

    def test_value_object_flags(self):
        self.assertFalse(paperless.PaperlessTrade().applies)
        self.assertFalse(paperless.PaperlessTrade().generated)
        self.assertTrue(paperless.PaperlessTrade(flow="flag_only").applies)
        self.assertFalse(paperless.PaperlessTrade(flow="flag_only").generated)
        self.assertTrue(paperless.PaperlessTrade(flow="doc_files", document=DOCUMENT).generated)

    def test_augment_doc_files_attaches_inline(self):
        plan = paperless.PaperlessTrade(flow=paperless.PAPERLESS_FLOW_DOC_FILES, document=DOCUMENT)
        options = paperless.augment_options_with_paperless({"paperless_trade": True}, plan, _shipment())
        self.assertDictEqual(options, {"paperless_trade": True, "doc_files": [DOCUMENT]})

    def test_augment_noop_when_not_generated(self):
        base = {"paperless_trade": True}
        self.assertDictEqual(
            paperless.augment_options_with_paperless(base, paperless.PaperlessTrade(flow="flag_only"), _shipment()),
            base,
        )

    def test_augment_doc_references_uploads_before_create(self):
        plan = paperless.PaperlessTrade(flow=paperless.PAPERLESS_FLOW_DOC_REFERENCES, document=DOCUMENT)
        with mock.patch(UPLOAD_FORMS, return_value=SimpleNamespace(documents=[{"doc_id": "X"}])) as upload:
            options = paperless.augment_options_with_paperless({"a": 1}, plan, _shipment())
        upload.assert_called_once()
        self.assertDictEqual(options, {"a": 1, "doc_references": [{"doc_id": "X"}]})

    def test_finalize_dispatches_job_only_for_post_upload(self):
        """finalize ENQUEUES the upload job for post_upload (D14) — never inline —
        and is a noop for every pre-create flow."""
        with mock.patch(UPLOAD_TASK) as task:
            paperless.finalize_paperless_trade(
                _shipment(),
                paperless.PaperlessTrade(flow="doc_files", document=DOCUMENT),
            )
            task.assert_not_called()

            shipment = _shipment(meta={})
            paperless.finalize_paperless_trade(
                shipment,
                paperless.PaperlessTrade(flow=paperless.PAPERLESS_FLOW_POST_UPLOAD, template="commercial_invoice"),
            )
            task.assert_called_once_with("shp_test")
            # stamps a pending marker the merchant/dashboard can read
            self.assertEqual(shipment.meta["paperless"]["status"], "pending")
            self.assertEqual(shipment.meta["paperless"]["template"], "commercial_invoice")


class TestPerCarrierPaperlessFlows(unittest.TestCase):
    """End-to-end paperless flow per supporting carrier.

    Reads the actual ``ShippingOption.paperless_trade`` meta off each connector
    via ``_carrier_paperless_meta`` (real ``pydoc.locate`` lookup), then runs
    ``prepare → augment → finalize`` with only the external boundaries mocked
    (``generate_custom_invoice`` and ``upload_customs_forms``). Mirrors the
    "mock the carrier identity, exercise the rest" pattern from the shipment
    purchase tests in ``test_shipments.py``.

    Verifies, per carrier:
      - the declared ``flow`` and ``upload_flow`` on the alias's meta
      - what document (if any) is generated and what shape gets attached on
        ``options`` before the carrier ``create_shipment`` call
      - what (if anything) ``finalize_paperless_trade`` does after create
    """

    # (carrier_name, expected default flow, expected upload_flow, generation needed, augmented option key)
    CARRIER_FLOWS = (
        ("fedex", paperless.PAPERLESS_FLOW_DOC_FILES, None, True, "doc_files"),
        ("mydhl", paperless.PAPERLESS_FLOW_DOC_FILES, None, True, "doc_files"),
        # GLS generates the invoice pre-create but uploads + submits customs
        # AFTER label creation (keyed off the TrackID) — the post_upload flow.
        # Nothing is injected onto options pre-create.
        ("gls", paperless.PAPERLESS_FLOW_POST_UPLOAD, None, True, None),
        ("seko", paperless.PAPERLESS_FLOW_DOC_FILES, None, True, "doc_files"),
        ("dhl_express", paperless.PAPERLESS_FLOW_FLAG_ONLY, None, False, None),
        ("dhl_parcel_de", paperless.PAPERLESS_FLOW_FLAG_ONLY, None, False, None),
        ("ups", paperless.PAPERLESS_FLOW_FLAG_ONLY, paperless.PAPERLESS_FLOW_DOC_REFERENCES, False, None),
    )

    def setUp(self):
        self.maxDiff = None

    def test_each_supporting_carrier_declares_paperless_trade_with_meta(self):
        """Every supporting connector aliases ``paperless_trade`` to a
        carrier-specific OptionEnum with ``category="PAPERLESS"`` + declared
        ``flow``."""
        for carrier_name, expected_flow, upload_flow, *_ in self.CARRIER_FLOWS:
            with self.subTest(carrier=carrier_name):
                meta = paperless._carrier_paperless_meta(_carrier(carrier_name))
                self.assertEqual(
                    meta.get("category"),
                    "PAPERLESS",
                    f"{carrier_name} paperless_trade meta missing category=PAPERLESS",
                )
                self.assertEqual(
                    meta.get("flow"),
                    expected_flow,
                    f"{carrier_name} expected flow={expected_flow}, got {meta.get('flow')}",
                )
                if upload_flow is None:
                    self.assertNotIn(
                        "upload_flow",
                        meta,
                        f"{carrier_name} should not declare upload_flow",
                    )
                else:
                    self.assertEqual(
                        meta.get("upload_flow"),
                        upload_flow,
                        f"{carrier_name} expected upload_flow={upload_flow}",
                    )

    def test_doc_files_carriers_attach_generated_invoice_inline(self):
        """Carriers declared with ``flow="doc_files"`` (FedEx / MyDHL / GLS /
        SEKO) generate a commercial invoice pre-create and attach it inline
        under ``options.doc_files``."""
        for carrier_name, _, _, needs_generation, augmented_key in self.CARRIER_FLOWS:
            if augmented_key != "doc_files":
                continue
            with self.subTest(carrier=carrier_name):
                with (
                    mock.patch(GENERATE_INVOICE, return_value=DOCUMENT) as gen,
                    mock.patch(CARRIER_SNAPSHOT, return_value=None),
                ):
                    plan = paperless.prepare_paperless_trade(
                        _shipment({"paperless_trade": True}),
                        _carrier(carrier_name),
                        invoice_template="commercial_invoice",
                    )
                    self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_DOC_FILES)
                    self.assertTrue(plan.generated)
                    if needs_generation:
                        gen.assert_called_once()

                    options = paperless.augment_options_with_paperless(
                        {"paperless_trade": True},
                        plan,
                        _shipment(),
                    )
                    self.assertEqual(
                        options,
                        {"paperless_trade": True, "doc_files": [DOCUMENT]},
                        f"{carrier_name}: doc_files flow must inject [document] under options.doc_files",
                    )

                # finalize is a noop for doc_files
                with mock.patch(UPLOAD_FORMS) as upload:
                    paperless.finalize_paperless_trade(_shipment(), plan)
                    upload.assert_not_called()

    def test_post_upload_carriers_defer_generation_then_dispatch_after_create(self):
        """Carriers declared with ``flow="post_upload"`` (GLS) DEFER invoice
        generation to the background job (D14): ``prepare`` generates nothing and
        carries the template, ``augment`` injects nothing pre-create, and
        ``finalize`` stamps a pending marker + enqueues the upload job."""
        for carrier_name, expected_flow, *_ in self.CARRIER_FLOWS:
            if expected_flow != paperless.PAPERLESS_FLOW_POST_UPLOAD:
                continue
            with self.subTest(carrier=carrier_name):
                with (
                    mock.patch(GENERATE_INVOICE) as gen,
                    mock.patch(CARRIER_SNAPSHOT, return_value=None),
                ):
                    plan = paperless.prepare_paperless_trade(
                        _shipment({"paperless_trade": True}),
                        _carrier(carrier_name),
                        invoice_template="commercial_invoice",
                    )
                    self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_POST_UPLOAD)
                    # generation is deferred to the job — NOT done in prepare
                    gen.assert_not_called()
                    self.assertFalse(plan.generated)
                    self.assertEqual(plan.template, "commercial_invoice")

                    # Nothing injected pre-create — the upload happens after.
                    base = {"paperless_trade": True}
                    options = paperless.augment_options_with_paperless(base, plan, _shipment())
                    self.assertEqual(
                        options,
                        base,
                        f"{carrier_name}: post_upload must NOT inject doc_files/doc_references pre-create",
                    )

                # finalize dispatches the job (does not upload inline)
                with mock.patch(UPLOAD_TASK) as task:
                    shipment = _shipment(meta={})
                    paperless.finalize_paperless_trade(shipment, plan)
                    task.assert_called_once_with("shp_test")
                    self.assertEqual(shipment.meta["paperless"]["status"], "pending")

    def test_flag_only_carriers_apply_without_generating_a_document(self):
        """Carriers declared with ``flow="flag_only"`` (DHL Express /
        DHL Parcel DE; UPS's default) fire paperless without generating
        an invoice. Augment is a noop — the carrier renders its own
        paperwork from the option flag alone."""
        for carrier_name, expected_flow, _upload_flow, _, _ in self.CARRIER_FLOWS:
            if expected_flow != paperless.PAPERLESS_FLOW_FLAG_ONLY:
                continue
            with self.subTest(carrier=carrier_name):
                with (
                    mock.patch(GENERATE_INVOICE) as gen,
                    mock.patch(CARRIER_SNAPSHOT, return_value=None),
                ):
                    plan = paperless.prepare_paperless_trade(
                        _shipment({"paperless_trade": True}),
                        _carrier(carrier_name),
                        invoice_template=None,
                    )
                gen.assert_not_called()
                self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_FLAG_ONLY)
                self.assertFalse(plan.generated)

                base = {"paperless_trade": True}
                options = paperless.augment_options_with_paperless(base, plan, _shipment())
                self.assertEqual(options, base, f"{carrier_name}: flag_only augment must be a noop")

                with mock.patch(UPLOAD_FORMS) as upload:
                    paperless.finalize_paperless_trade(_shipment(), plan)
                    upload.assert_not_called()

    def test_ups_hybrid_stays_flag_only_when_no_doc_or_template(self):
        """UPS default — ``flag_only``, no invoice generated."""
        with mock.patch(GENERATE_INVOICE) as gen:
            plan = paperless.prepare_paperless_trade(
                _shipment({"paperless_trade": True}),
                _carrier("ups"),
                invoice_template=None,
            )
        gen.assert_not_called()
        self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_FLAG_ONLY)
        self.assertFalse(plan.generated)

    def test_ups_hybrid_promotes_to_doc_references_with_invoice_template(self):
        """UPS hybrid — when an invoice_template is supplied, promote from
        ``flag_only`` to ``doc_references``; ``augment`` uploads the generated
        invoice and writes ``options.doc_references`` for the create call."""
        with (
            mock.patch(GENERATE_INVOICE, return_value=DOCUMENT) as gen,
            mock.patch(CARRIER_SNAPSHOT, return_value=None),
            mock.patch(UPLOAD_FORMS, return_value=SimpleNamespace(documents=[{"doc_id": "UPS_DOC_REF_42"}])) as upload,
        ):
            plan = paperless.prepare_paperless_trade(
                _shipment({"paperless_trade": True}),
                _carrier("ups"),
                invoice_template="commercial_invoice",
            )
            self.assertEqual(plan.flow, paperless.PAPERLESS_FLOW_DOC_REFERENCES)
            self.assertTrue(plan.generated)
            gen.assert_called_once()

            options = paperless.augment_options_with_paperless({}, plan, _shipment())
            upload.assert_called_once()
            self.assertEqual(options, {"doc_references": [{"doc_id": "UPS_DOC_REF_42"}]})


class TestUploadPaperlessDocumentsTask(TestCase):
    """DB-backed test for the post_upload background job (D14/D17).

    Only the external boundaries are mocked — ``generate_custom_invoice`` (the
    document generator) and ``upload_customs_forms`` (the carrier upload). The
    shipment is a real DB row and the meta-state transitions are real.
    """

    def setUp(self):
        self.maxDiff = None
        self.user = get_user_model().objects.create_user("paperless@example.com", "test")

    def _shipment(self, *, options=None, meta_template="commercial_invoice"):
        return models.Shipment.objects.create(
            shipper={"id": "adr_1", "country_code": "DE", "city": "Berlin", "address_line1": "Str 1"},
            recipient={"id": "adr_2", "country_code": "US", "city": "NYC", "address_line1": "5th Ave"},
            parcels=[{"id": "pcl_1", "weight": 1.0, "weight_unit": "KG"}],
            options=options or {},
            created_by=self.user,
            test_mode=True,
            meta={"paperless": {"status": "pending", "template": meta_template}},
        )

    def test_generates_uploads_and_marks_done(self):
        """template path: generate the invoice, upload it, flip status to done."""
        shipment = self._shipment()
        with (
            mock.patch(GENERATE_INVOICE, return_value=DOCUMENT) as gen,
            mock.patch(UPLOAD_FORMS, return_value=SimpleNamespace(documents=[{"doc_id": "X"}])) as upload,
        ):
            upload_paperless_documents.call_local(shipment.id)

        gen.assert_called_once()
        self.assertEqual(gen.call_args.kwargs["slug"], "commercial_invoice")
        upload.assert_called_once()
        self.assertEqual(upload.call_args.args[1], DOCUMENT)  # uploads the generated doc
        shipment.refresh_from_db()
        self.assertEqual(shipment.meta["paperless"]["status"], "done")

    def test_uses_explicit_doc_files_without_generating(self):
        """explicit-doc path: a merchant-supplied doc_files is uploaded as-is."""
        shipment = self._shipment(options={"doc_files": [DOCUMENT]}, meta_template=None)
        with (
            mock.patch(GENERATE_INVOICE) as gen,
            mock.patch(UPLOAD_FORMS, return_value=SimpleNamespace(documents=[])) as upload,
        ):
            upload_paperless_documents.call_local(shipment.id)

        gen.assert_not_called()
        upload.assert_called_once()
        self.assertEqual(upload.call_args.args[1], DOCUMENT)
        shipment.refresh_from_db()
        self.assertEqual(shipment.meta["paperless"]["status"], "done")

    def test_customs_rejection_marks_failed_and_surfaces_messages(self):
        """A carrier rejection comes back as messages (not an exception) — the
        marker must read 'failed' and carry the errors, not silently 'done'."""
        shipment = self._shipment()
        rejection = SimpleNamespace(
            documents=[{"doc_id": "X"}],
            messages=[
                {
                    "code": "REQUIRED",
                    "message": "Importer EORI number is required for shipments to GB",
                    "details": {"field": "/importer/eoriNumber"},
                }
            ],
        )
        with (
            mock.patch(GENERATE_INVOICE, return_value=DOCUMENT),
            mock.patch(UPLOAD_FORMS, return_value=rejection),
        ):
            upload_paperless_documents.call_local(shipment.id)

        shipment.refresh_from_db()
        self.assertEqual(shipment.meta["paperless"]["status"], "failed")
        self.assertEqual(shipment.meta["paperless"]["errors"][0]["code"], "REQUIRED")

    def test_no_source_marks_skipped_without_uploading(self):
        """No doc_files and nothing resolvable to generate (no per-shipment slug and
        no system-default body, so ``generate_paperless_invoice`` returns None) →
        nothing to send; mark skipped with an actionable reason, don't upload."""
        shipment = self._shipment(meta_template=None)
        with (
            # generate_paperless_invoice resolves the source (slug → default body);
            # None means neither resolved. The job must not invent an upload.
            mock.patch(GENERATE_INVOICE, return_value=None) as gen,
            mock.patch(UPLOAD_FORMS) as upload,
        ):
            upload_paperless_documents.call_local(shipment.id)

        gen.assert_called_once()
        self.assertIsNone(gen.call_args.kwargs["slug"])
        upload.assert_not_called()
        shipment.refresh_from_db()
        self.assertEqual(shipment.meta["paperless"]["status"], "skipped")
        # D15: never a silent no-op — the skip carries an actionable reason.
        self.assertIn("reason", shipment.meta["paperless"])
        self.assertIn("PAPERLESS_DEFAULT_INVOICE_TEMPLATE", shipment.meta["paperless"]["reason"])

    def test_generates_from_system_default_body_when_no_slug(self):
        """No per-shipment slug but a system default body is configured →
        generate_paperless_invoice produces the doc, upload + mark done."""
        shipment = self._shipment(meta_template=None)
        with (
            mock.patch(GENERATE_INVOICE, return_value=DOCUMENT) as gen,
            mock.patch(UPLOAD_FORMS, return_value=SimpleNamespace(documents=[{"doc_id": "X"}])) as upload,
        ):
            upload_paperless_documents.call_local(shipment.id)

        gen.assert_called_once()
        self.assertIsNone(gen.call_args.kwargs["slug"])  # falls back to the default body
        upload.assert_called_once()
        self.assertEqual(upload.call_args.args[1], DOCUMENT)
        shipment.refresh_from_db()
        self.assertEqual(shipment.meta["paperless"]["status"], "done")

    @override_settings(PERSIST_SDK_TRACING=True)
    def test_carrier_http_calls_persist_shipment_correlated_tracing_records(self):
        """The job binds its own tracer (workers have no request), so the carrier
        HTTP calls land as TracingRecords correlated to the shipment via
        meta.object_id — alongside the DocumentUploadRecord."""
        shipment = self._shipment()

        conn_meta = {"connection": {"id": "car_gls_1", "carrier_id": "gls", "carrier_name": "gls", "test_mode": True}}

        def _fake_upload(shp, document, context=None):
            # Proves the tracer is bound during the upload — the gateway would
            # read it the same way. Simulate the GLS HTTP calls, INCLUDING the
            # S3 PUT whose body is raw bytes (the regression that broke
            # persistence: bytes aren't JSON-serializable).
            req = SessionContext.get_current_request()
            self.assertIsNotNone(req, "expected a bound request scope during upload")
            req.tracer.trace({"url": "https://gls/prepare-upload", "data": "{}"}, "request", metadata=conn_meta)
            req.tracer.trace({"url": "https://s3/put", "data": b"%PDF-1.4 binary"}, "request", metadata=conn_meta)
            req.tracer.trace({"url": "https://gls/customs", "data": "{}"}, "request", metadata=conn_meta)
            return SimpleNamespace(documents=[{"doc_id": "X"}])

        with (
            mock.patch(GENERATE_INVOICE, return_value=DOCUMENT),
            mock.patch(UPLOAD_FORMS, side_effect=_fake_upload),
        ):
            upload_paperless_documents.call_local(shipment.id)

        records = list(tracing_models.TracingRecord.objects.filter(meta__object_id=shipment.id))
        # all three traces persisted despite the binary PUT body (bytes elided, not crashed)
        self.assertEqual(len(records), 3, "expected all carrier HTTP traces correlated to the shipment")
        self.assertEqual(records[0].meta["carrier_name"], "gls")
        put = next(r for r in records if (r.record or {}).get("url") == "https://s3/put")
        self.assertEqual(put.record["data"], "<15 bytes elided>")  # bytes coerced to a marker
        # scope is restored after the job — no leaked current request
        self.assertIsNone(SessionContext.get_current_request())

        # The upload op is logged (APILog keyed to the shipment via entity_id) and every
        # carrier trace is stamped with that log id — the dashboard timeline groups
        # traces by meta.request_log_id (LogType.records), so without this they'd be invisible.
        log = APILogIndex.objects.filter(entity_id=shipment.id).first()
        self.assertIsNotNone(log, "expected an APILog entry for the upload operation")
        self.assertTrue(
            all(r.meta.get("request_log_id") == log.id for r in records),
            "every upload trace must carry the APILog id so it appears in the timeline",
        )

    def test_uploaded_documents_surface_in_shipping_documents(self):
        """A DocumentUploadRecord's carrier-uploaded docs appear in the shipment's
        shipping_documents[] (so the REST API / print modal / CLI can list them)."""
        from karrio.server.manager.serializers.shipment import PurchasedShipment

        shipment = self._shipment()
        models.DocumentUploadRecord.objects.create(
            shipment=shipment,
            documents=[
                {"doc_id": "gls_doc_1", "file_name": "commercial-invoice.pdf", "doc_type": "commercial_invoice"}
            ],
            messages=[],
            reference=shipment.id,
            created_by=self.user,
        )

        docs = PurchasedShipment(shipment).data.get("shipping_documents") or []
        customs = [d for d in docs if d.get("doc_id") == "gls_doc_1"]
        self.assertEqual(len(customs), 1, "uploaded customs doc must appear in shipping_documents")
        self.assertEqual(customs[0]["category"], "commercial_invoice")
        self.assertEqual(customs[0]["file_name"], "commercial-invoice.pdf")


if __name__ == "__main__":
    unittest.main()
