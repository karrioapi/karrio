"""GLS Group carrier shipment tests."""

import datetime
import logging
import unittest
from unittest import mock
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import cached_auth, gateway, gateway_with_customs

logger = logging.getLogger(__name__)


class TestGLSGroupShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.IntlShipmentRequest = models.ShipmentRequest(**IntlShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        """Baseline assert: a request with no options must come out as the
        DefaultShipmentRequest shape — Middleware fixed to "JTLviaGLS", no
        top-level PartnerReference, Identifier="KARRIO" (the configured
        app_identifier), and NO Service keys (neither shipment-level nor
        unit-level), so jstruct's `[None]` JList default never leaks."""
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, DefaultShipmentRequest)

    def test_middleware_is_fixed_billing_marker(self):
        """`Shipment.Middleware` is mandatory and always carries the fixed
        GLS billing marker "JTLviaGLS" — never a per-connection value — and
        there is no top-level PartnerReference field (GLS rejects it)."""
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        request_dict = lib.to_dict(request.serialize())
        self.assertEqual(request_dict["Shipment"]["Middleware"], "JTLviaGLS")
        self.assertNotIn("PartnerReference", request_dict)

    def test_system_config_fallback_supplies_identifier(self):
        """A connection that doesn't set `app_identifier` in its config must
        still emit `Shipment.Identifier` when the platform-wide
        `GLS_APP_IDENTIFIER` is set in the system config — same fallback chain
        DHL Parcel DE uses for its OAuth creds. Middleware stays the fixed
        billing marker regardless."""
        from karrio.sdk import gateway as gw

        system_gateway = gw["gls"].create(
            {
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "contact_id": "TEST_CONTACT_ID",
                "test_mode": True,
                # no `config` block — purely system-config driven
            },
            cache=lib.Cache(**cached_auth),
            system_config=lib.SystemConfig(
                GLS_APP_IDENTIFIER="SYS-APP",
            ),
        )
        request = system_gateway.mapper.create_shipment_request(self.ShipmentRequest)
        request_dict = lib.to_dict(request.serialize())
        self.assertEqual(request_dict["Shipment"]["Middleware"], "JTLviaGLS")
        self.assertEqual(request_dict["Shipment"]["Identifier"], "SYS-APP")

    def test_create_shipment(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(mock_req.call_args[1]["url"], f"{gateway.settings.shipment_api_url}/rs/shipments")

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.return_value = ShipmentResponse
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.return_value = ErrorResponse
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentErrorResponse)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        self.assertEqual(request.serialize(), "ZHO9AXAC")

    def test_cancel_shipment(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.return_value = '{"TrackID":"ZHO9AXAC","Result":"OK"}'
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            self.assertEqual(
                mock_req.call_args[1]["url"],
                f"{gateway.settings.shipment_api_url}/rs/shipments/cancel/ZHO9AXAC",
            )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.return_value = '{"TrackID":"ZHO9AXAC","Result":"OK"}'
            parsed_response = karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            confirmation, _ = parsed_response
            self.assertIsNotNone(confirmation)
            self.assertTrue(confirmation.success)

    def test_multi_piece_request_emits_one_unit_per_parcel(self):
        payload = {
            **ShipmentPayload,
            "parcels": [
                {"weight": 2.0, "weight_unit": "KG"},
                {"weight": 3.5, "weight_unit": "KG"},
                {"weight": 1.2, "weight_unit": "KG"},
            ],
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, MultiPieceRequest)

    def test_shop_return_option_emits_service_block(self):
        payload = {**ShipmentPayload, "options": {"gls_shop_return": True}}
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, ShopReturnRequest)

    def test_pick_and_return_option_emits_service_block(self):
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_pick_and_return": True,
                "shipping_date": "2026-05-10T08:00",
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, PickAndReturnRequest)

    def test_shipping_date_falls_back_to_today_when_unset(self):
        """ShippingDate and any PickAndReturn PickupDate must always be set
        on the wire — when the caller omits `shipping_date`, both fall back
        to today (DHL Parcel DE / UPS convention)."""
        today = datetime.date.today().isoformat()
        payload = {**ShipmentPayload, "options": {"gls_pick_and_return": True}}
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        expected = {
            **DefaultShipmentRequest,
            "Shipment": {
                **DefaultShipmentRequest["Shipment"],
                "ShippingDate": today,
                "Service": [
                    {"PickAndReturn": {"PickupDate": today, "ServiceName": "service_pickandreturn"}},
                ],
            },
        }
        self.assertDictEqual(request_dict, expected)

    def test_flag_options_emit_simple_service_entries(self):
        """The flag-style options translate into `Shipment.Service[]` entries
        carrying the fixed GLS `service_*` ServiceName (doxygen "(w/o
        attributes)" services). Express is a Product, not a service, so it
        emits no entry."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_saturday_delivery": True,
                "gls_flex_delivery": True,
                "gls_addressee_only": True,
                "gls_signature_service": True,
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, FlagOptionsRequest)

    def test_deposit_option_emits_deposit_service_block(self):
        """Deposit needs the place description on the wire — DepositType only
        carries `ServiceName + PlaceOfDeposit`, so the description rides as
        the place verbatim."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_deposit_service": True,
                "gls_deposit_description": "Behind the garage",
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, DepositRequest)

    def test_shop_delivery_option_emits_parcelshop_id(self):
        """ShopDelivery rides as a dedicated wrapper carrying the ParcelShopID
        when the caller picks one; an auto-select call omits the ID."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_shop_delivery": True,
                "gls_shop_id": "DE-0142-BERLIN",
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, ShopDeliveryRequest)

    def test_ident_pin_option_emits_identpin_block_with_pin_and_birthdate(self):
        """IdentPin is wrapped under its own key — PIN is mandatory per
        doxygen (4-digit), Birthdate optional."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_ident_pin_service": True,
                "gls_ident_pin": "1234",
                "gls_ident_pin_birthdate": "1980-02-03",
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        self.assertDictEqual(lib.to_dict(request.serialize()), IdentPinRequest)

    # NOTE: tests for the following doxygen services were removed for the JTL
    # launch service-set scope (see SPECS.md). Implementations stay in
    # create.py / units.py; re-enable the tests when a customer needs them:
    #   - Ident (full PII; IdentPin is the launch-set alternative)
    #   - DeliveryAtWork
    #   - Intercompany
    #   - Exchange
    #   - PickAndShip

    def test_cash_uses_cod_amount_and_reason(self):
        """Cash rides per ShipmentUnit, sourcing Amount from the karrio
        standard `cash_on_delivery` option and Reason from gls_cash_reason."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_cash_service": True,
                "cash_on_delivery": 75.50,
                "gls_cash_reason": "Order #12345",
                "currency": "EUR",
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        self.assertDictEqual(lib.to_dict(request.serialize()), CashRequest)

    # Per the JTL launch service-set scope, tests for HazardousGoods,
    # ExWorks, and the extended-flag set (Guaranteed24 / T24 / T48 / Tyre /
    # PrivateDelivery / InboundLogistics / DocumentReturn /
    # CompleteDeliveryConsignment) are not run. Implementations remain.

    def test_time_definite_option_carries_value_into_servicename(self):
        """GLS encodes the cut-off in the ServiceName itself (e.g.
        `service_0800`). The option value is forwarded when it is a recognised
        GLS time-definite code so callers can target the right cut-off."""
        payload = {
            **ShipmentPayload,
            "options": {"gls_time_definite_service": "service_0800"},
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, TimeDefiniteRequest)

    def test_insurance_option_emits_unit_level_addonliability(self):
        """The karrio-standard `insurance` option rides per parcel inside
        `ShipmentUnit[].Service[]` as an AddonLiability entry, currency
        resolved from the shipment options."""
        payload = {
            **ShipmentPayload,
            "options": {"insurance": 250.0, "currency": "EUR"},
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, InsuranceRequest)

    def test_limited_quantity_option_emits_unit_level_lq_block(self):
        """LimitedQuantity is per-parcel — it lives on ShipmentUnit.Service[]
        with the declared dangerous-goods weight."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_limited_quantity": True,
                "gls_limited_quantity_weight": 0.5,
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, LimitedQuantityRequest)

    def test_unit_services_replicate_across_every_parcel(self):
        """Multi-piece shipments need each unit to carry the per-parcel
        services (the carrier doesn't fan them out for us)."""
        payload = {
            **ShipmentPayload,
            "parcels": [
                {"weight": 2.0, "weight_unit": "KG"},
                {"weight": 3.0, "weight_unit": "KG"},
            ],
            "options": {"insurance": 100.0, "currency": "EUR"},
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, MultiPieceInsuranceRequest)

    def test_shipment_level_and_return_services_coexist(self):
        """A caller may combine the Saturday service with ShopReturn — both
        must appear in `Shipment.Service[]`, return service last so the
        mutual-exclusion check above still runs against the latest entry."""
        payload = {
            **ShipmentPayload,
            "options": {"gls_saturday_delivery": True, "gls_shop_return": True},
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, SaturdayPlusShopReturnRequest)

    def test_return_services_are_mutually_exclusive(self):
        """ShopReturn and PickAndReturn cannot both ride on the same parcel
        per GLS — if a caller sets both options, PickAndReturn wins and
        ShopReturn is dropped so we never ship a confused Service[] array."""
        payload = {
            **ShipmentPayload,
            "options": {
                "gls_shop_return": True,
                "gls_pick_and_return": True,
                "shipping_date": "2026-05-22T08:00",
            },
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())
        self.assertDictEqual(request_dict, MutualExclusionRequest)

    def test_create_shipment_fires_only_the_label_call(self):
        """After the PR-#805 ``flow="post_upload"`` refactor, the customs +
        document-upload chain lives in ``proxy.upload_document`` (the unified
        karrio Document interface). ``Shipment.create`` is back to a single
        ShipIT createParcels call — no customs side effects."""
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.side_effect = [IntlShipmentResponse]
            karrio.Shipment.create(self.IntlShipmentRequest).from_(gateway_with_customs)

            self.assertEqual(mock_req.call_count, 1)
            self.assertTrue(mock_req.call_args[1]["url"].endswith("/rs/shipments"))

    def test_document_upload_request_packs_customs_consignment_from_options(self):
        """When the manager-side ``DocumentUploadSerializer`` plumbs the
        shipment's customs + shipper + recipient through ``options``, the GLS
        provider shapes a ``CustomsConsignmentRequestType`` into ctx so the
        proxy can fire the v3 leg after the prepare-upload + PUT chain."""
        upload_payload = models.DocumentUploadRequest(
            document_files=[
                models.DocumentFile(
                    doc_file="JVBERi0xLjQKJVRFU1QK",
                    doc_name="JTL-INV-2026-0042.pdf",
                    doc_format="pdf",
                    doc_type="commercial_invoice",
                )
            ],
            tracking_number="GBINTL01",
            reference="INTL-001",
            options={
                "shipper": IntlShipmentPayload["shipper"],
                "recipient": IntlShipmentPayload["recipient"],
                "customs": IntlShipmentPayload["customs"],
                "currency": "EUR",
            },
        )
        request = gateway.mapper.create_document_upload_request(upload_payload)
        consignment = (request.ctx or {}).get("customs_consignment")
        self.assertIsNotNone(consignment)
        self.assertDictEqual(lib.to_dict(consignment), IntlCustomsConsignment)
        self.assertEqual(request.ctx.get("tracking_number"), "GBINTL01")

    def test_upload_document_fires_prepare_upload_put_and_customs_chain(self):
        """``Document.upload`` against the GLS gateway runs the 4-step
        Timo-described chain: prepare-upload + PUT per file, then a single
        Customs Consignment v3 POST stamping ``parcelNumbers`` (TrackID) and
        ``linkedDocuments`` (documentIds)."""
        upload_request = models.DocumentUploadRequest(
            document_files=[
                models.DocumentFile(
                    doc_file="JVBERi0xLjQKJVRFU1QK",
                    doc_name="JTL-INV-2026-0042.pdf",
                    doc_format="pdf",
                    doc_type="commercial_invoice",
                )
            ],
            tracking_number="GBINTL01",
            reference="INTL-001",
            options={
                "shipper": IntlShipmentPayload["shipper"],
                "recipient": IntlShipmentPayload["recipient"],
                "customs": IntlShipmentPayload["customs"],
                "currency": "EUR",
            },
        )
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.side_effect = [
                {"documentId": "00000000-1111-2222-3333-444444444444", "uploadURL": "https://upload.example/abc"},
                None,  # PUT to pre-signed uploadURL — no body
                CustomsConsignmentResponse,
            ]
            karrio.Document.upload(upload_request).from_(gateway).parse()

            urls = [c[1]["url"] for c in mock_req.call_args_list]
            self.assertEqual(len(urls), 3)
            self.assertTrue(urls[0].endswith("/documents/customs/prepare-upload"))
            self.assertEqual(urls[1], "https://upload.example/abc")
            self.assertTrue(urls[2].endswith("/customs-consignments"))

            prepare_body = lib.to_dict(mock_req.call_args_list[0][1]["data"])
            self.assertEqual(prepare_body["attributes"]["documentType"], "COMMERCIAL_INVOICE")
            self.assertEqual(prepare_body["attributes"]["displayFileName"], "JTL-INV-2026-0042.pdf")

            customs_body = lib.to_dict(mock_req.call_args_list[2][1]["data"])
            self.assertEqual(customs_body["parcelNumbers"], ["GBINTL01"])
            self.assertEqual(
                customs_body["linkedDocuments"],
                [{"documentId": "00000000-1111-2222-3333-444444444444"}],
            )

    def test_domestic_shipment_does_not_fire_customs_consignment_call(self):
        """No customs destination → no second call. Guards against the
        proxy accidentally firing the customs API for EU-domestic labels."""
        with patch("karrio.mappers.gls.proxy.lib.request") as mock_req:
            mock_req.return_value = ShipmentResponse
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(mock_req.call_count, 1)
            self.assertEqual(
                mock_req.call_args[1]["url"],
                f"{gateway.settings.shipment_api_url}/rs/shipments",
            )

    def test_multi_piece_response_bundles_labels(self):
        with (
            patch("karrio.mappers.gls.proxy.lib.request") as mock_req,
            patch(
                "karrio.providers.gls.shipment.create.lib.bundle_base64",
                return_value="BUNDLED_LABEL",
            ) as mock_bundle,
        ):
            mock_req.return_value = MultiPieceShipmentResponse
            details, _ = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            mock_bundle.assert_called_once_with(["LABEL_A", "LABEL_B"], "PDF")
            self.assertEqual(details.docs.label, "BUNDLED_LABEL")
            self.assertEqual(details.meta["tracking_numbers"], ["601079500843", "601079500844"])
            self.assertEqual(details.meta["track_ids"], ["TRACK_A", "TRACK_B"])


if __name__ == "__main__":
    unittest.main()

# ---------------------------------------------------------------------------
# Test payloads
# ---------------------------------------------------------------------------
ShipmentCancelPayload = {"shipment_identifier": "ZHO9AXAC"}

ShipmentPayload = {
    "shipper": {
        "company_name": "Test Shipper Company",
        "address_line1": "Main Street",
        "address_line2": "123",
        "city": "Berlin",
        "postal_code": "12345",
        "country_code": "DE",
        "person_name": "John Doe",
        "phone_number": "+49301234567",
        "email": "shipper@example.com",
    },
    "recipient": {
        "company_name": "Test Recipient Company",
        "address_line1": "Market Street",
        "address_line2": "456",
        "city": "Munich",
        "postal_code": "54321",
        "country_code": "DE",
        "person_name": "Jane Smith",
        "phone_number": "+49891234567",
        "email": "recipient@example.com",
    },
    "parcels": [
        {
            "weight": 5.5,
            "length": 30,
            "width": 20,
            "height": 15,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "service": "gls_parcel",
    "reference": "TEST123",
}

IntlShipmentPayload = {
    "shipper": {
        "company_name": "Test Shipper Company",
        "address_line1": "Main Street",
        "address_line2": "123",
        "city": "Berlin",
        "postal_code": "12345",
        "country_code": "DE",
        "person_name": "John Doe",
        "phone_number": "+49301234567",
        "email": "shipper@example.com",
        "federal_tax_id": "DE123456789",
    },
    "recipient": {
        "company_name": "UK Importer Ltd",
        "address_line1": "Baker Street",
        "address_line2": "221B",
        "city": "London",
        "postal_code": "NW1 6XE",
        "country_code": "GB",
        "person_name": "Jane Smith",
        "phone_number": "+442071234567",
        "email": "recipient@example.co.uk",
    },
    "parcels": [
        {
            "weight": 2.5,
            "length": 30,
            "width": 20,
            "height": 15,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "service": "gls_parcel",
    "reference": "INTL-001",
    "options": {"currency": "EUR"},
    "customs": {
        "incoterm": "DDP",
        "invoice": "INV-2026-0001",
        "invoice_date": "2026-05-26",
        "commodities": [
            {
                "title": "Cotton t-shirts",
                "description": "Cotton T-shirts",
                "quantity": 2,
                "weight": 1.0,
                "weight_unit": "KG",
                "value_amount": 50.0,
                "value_currency": "EUR",
                "hs_code": "6109.10.00",
                "origin_country": "DE",
            }
        ],
        "duty": {"paid_by": "sender", "currency": "EUR"},
        "options": {"shipper_eori": "DE123456789012345"},
    },
}

# ---------------------------------------------------------------------------
# Expected wire payloads (full ShipIT request shape)
#
# DefaultShipmentRequest is the baseline emitted for a ShipmentPayload with no
# options. Per-option requests extend it via dict-merge so the diff between
# variants is obvious — e.g. SaturdayPlusShopReturnRequest only differs in
# the Shipment.Service[] array. `ShippingDate` uses ``mock.ANY`` whenever
# the caller didn't pin one, because it falls back to today's date.
# ---------------------------------------------------------------------------
DefaultConsigneeAddress = {
    "City": "Munich",
    "ContactPerson": "Jane Smith",
    "CountryCode": "DE",
    "FixedLinePhonenumber": "+49891234567",
    "Name1": "Test Recipient Company",
    "Name2": "Jane Smith",
    "Street": "Market Street",
    "StreetNumber": "456",
    "ZIPCode": "54321",
    "eMail": "recipient@example.com",
}

DefaultShipperAlternativeAddress = {
    "City": "Berlin",
    "ContactPerson": "John Doe",
    "CountryCode": "DE",
    "FixedLinePhonenumber": "+49301234567",
    "Name1": "Test Shipper Company",
    "Name2": "John Doe",
    "Street": "Main Street",
    "StreetNumber": "123",
    "ZIPCode": "12345",
    "eMail": "shipper@example.com",
}

DefaultUnit = {"ShipmentUnitReference": ["TEST123"], "Weight": 5.5}

DefaultShipment = {
    "Consignee": {"Address": DefaultConsigneeAddress},
    "Identifier": "KARRIO",
    "Middleware": "JTLviaGLS",
    "Product": "PARCEL",
    "ShipmentReference": ["TEST123"],
    "ShipmentUnit": [DefaultUnit],
    "Shipper": {
        "AlternativeShipperAddress": DefaultShipperAlternativeAddress,
        "ContactID": "TEST_CONTACT_ID",
    },
    "ShippingDate": mock.ANY,
}

DefaultShipmentRequest = {
    "PrintingOptions": {"ReturnLabels": {"LabelFormat": "PDF", "TemplateSet": "NONE"}},
    "Shipment": DefaultShipment,
}


def _with_services(shipment_services=None, unit_services=None, **overrides):
    """Build a DefaultShipmentRequest variant with the named overrides.

    `shipment_services` / `unit_services` are the option-driven Service[]
    arrays to attach (mirroring the wire shape exactly). `overrides` are
    Shipment-level keys (e.g. ShippingDate) to replace.
    """
    shipment = {**DefaultShipment, **overrides}
    if shipment_services is not None:
        shipment["Service"] = shipment_services
    if unit_services is not None:
        shipment["ShipmentUnit"] = [{**DefaultUnit, "Service": unit_services}]
    return {**DefaultShipmentRequest, "Shipment": shipment}


MultiPieceRequest = {
    **DefaultShipmentRequest,
    "Shipment": {
        **DefaultShipment,
        "ShipmentUnit": [
            {"ShipmentUnitReference": ["TEST123"], "Weight": 2.0},
            {"ShipmentUnitReference": ["TEST123"], "Weight": 3.5},
            {"ShipmentUnitReference": ["TEST123"], "Weight": 1.2},
        ],
    },
}

ShopReturnRequest = _with_services(
    shipment_services=[{"ShopReturn": {"NumberOfLabels": 1, "ServiceName": "service_shopreturn"}}],
)

PickAndReturnRequest = _with_services(
    ShippingDate="2026-05-10",
    shipment_services=[{"PickAndReturn": {"PickupDate": "2026-05-10", "ServiceName": "service_pickandreturn"}}],
)

FlagOptionsRequest = _with_services(
    shipment_services=[
        {"Service": {"ServiceName": "service_Saturday"}},
        {"Service": {"ServiceName": "service_flexdelivery"}},
        {"Service": {"ServiceName": "service_addresseeonly"}},
        {"Service": {"ServiceName": "service_signature"}},
    ],
)

DepositRequest = _with_services(
    shipment_services=[
        {
            "Deposit": {
                "ServiceName": "service_deposit",
                "PlaceOfDeposit": "Behind the garage",
            }
        }
    ],
)

ShopDeliveryRequest = _with_services(
    shipment_services=[
        {
            "ShopDelivery": {
                "ServiceName": "service_shopdelivery",
                "ParcelShopID": "DE-0142-BERLIN",
            }
        }
    ],
)

IdentPinRequest = _with_services(
    shipment_services=[
        {
            "IdentPin": {
                "ServiceName": "service_identpin",
                "PIN": "1234",
                "Birthdate": "1980-02-03",
            }
        }
    ],
)

CashRequest = _with_services(
    unit_services=[
        {
            "Cash": {
                "ServiceName": "service_cash",
                "Amount": 75.5,
                "Currency": "EUR",
                "Reason": "Order #12345",
            }
        }
    ],
)


TimeDefiniteRequest = _with_services(
    shipment_services=[{"Service": {"ServiceName": "service_0800"}}],
)

_INSURANCE_UNIT_ENTRY = {
    "AddonLiability": {
        "ServiceName": "service_addonliability",
        "Amount": 250.0,
        "Currency": "EUR",
    }
}

InsuranceRequest = _with_services(unit_services=[_INSURANCE_UNIT_ENTRY])

LimitedQuantityRequest = _with_services(
    unit_services=[
        {
            "LimitedQuantities": {
                "ServiceName": "service_limitedquantities",
                "Weight": 0.5,
            }
        }
    ],
)

_MULTIPIECE_INSURANCE_UNIT_ENTRY = {
    "AddonLiability": {
        "ServiceName": "service_addonliability",
        "Amount": 100.0,
        "Currency": "EUR",
    }
}

MultiPieceInsuranceRequest = {
    **DefaultShipmentRequest,
    "Shipment": {
        **DefaultShipment,
        "ShipmentUnit": [
            {
                "ShipmentUnitReference": ["TEST123"],
                "Weight": 2.0,
                "Service": [_MULTIPIECE_INSURANCE_UNIT_ENTRY],
            },
            {
                "ShipmentUnitReference": ["TEST123"],
                "Weight": 3.0,
                "Service": [_MULTIPIECE_INSURANCE_UNIT_ENTRY],
            },
        ],
    },
}

SaturdayPlusShopReturnRequest = _with_services(
    shipment_services=[
        {"Service": {"ServiceName": "service_Saturday"}},
        {"ShopReturn": {"ServiceName": "service_shopreturn", "NumberOfLabels": 1}},
    ],
)

MutualExclusionRequest = _with_services(
    ShippingDate="2026-05-22",
    shipment_services=[
        {"PickAndReturn": {"PickupDate": "2026-05-22", "ServiceName": "service_pickandreturn"}},
    ],
)

# ---------------------------------------------------------------------------
# Expected customs payloads
#
# IntlCustomsConsignment is the full /customs-consignments body the connector
# builds for the IntlShipmentPayload (DE → GB, DDP, one cotton-t-shirt line
# item, EUR currency). `parcelNumbers` is intentionally absent — the proxy
# stamps it from the shipment response on the second leg.
# ---------------------------------------------------------------------------
IntlCustomsConsignment = {
    "customerReference": "INTL-001",
    "exporter": {
        "address": {
            "city1": "Berlin",
            "countryCode": "DE",
            "name1": "Test Shipper Company",
            "name2": "John Doe",
            "postcode": "12345",
            "street1": "Main Street",
        },
        "contactPerson": {
            "emailAddress": "shipper@example.com",
            "name": "John Doe",
            "phoneCountryPrefix": "+49",
            "phoneNumber": "301234567",
        },
        "eoriNumber": "DE123456789012345",
        "isCommercial": True,
        "taxId": "DE123456789",
    },
    "glsIncotermCode": "10",
    "importer": {
        "address": {
            "city1": "London",
            "countryCode": "GB",
            "name1": "UK Importer Ltd",
            "name2": "Jane Smith",
            "postcode": "NW1 6XE",
            "street1": "Baker Street",
        },
        "contactPerson": {
            "emailAddress": "recipient@example.co.uk",
            "name": "Jane Smith",
            "phoneCountryPrefix": "+44",
            "phoneNumber": "2071234567",
        },
        "isCommercial": True,
    },
    "invoice": {
        "invoiceDate": "2026-05-26",
        "invoiceNumber": "INV-2026-0001",
        "totalGoodsValue": {"amount": 100.0, "currency": "EUR"},
    },
    "lineItems": [
        {
            "commodityCode": "61091000",
            "countryOfOrigin": "DE",
            "goodsDescription": "Cotton T-shirts",
            "grossWeight": {"amount": 2.0, "unit": "KGM"},
            "netWeight": {"amount": 2.0, "unit": "KGM"},
            "quantity": {"amount": 2.0, "unit": "PCE"},
            "statisticalQuantity": 2.0,
            "valueInInvoiceCurrency": 100.0,
        }
    ],
    "totalGrossWeight": {"amount": 2.0, "unit": "KGM"},
}

# ---------------------------------------------------------------------------
# Carrier response fixtures
# ---------------------------------------------------------------------------
ShipmentResponse = """{
  "CreatedShipment": {
    "ShipmentReference": ["TEST123"],
    "ParcelData": [
      {
        "TrackID": "ZHO9AXAC",
        "ParcelNumber": "601079500843",
        "RoutingInfo": {
          "Tour": "2807",
          "InboundSortingFlag": "1",
          "FinalLocationCode": "DE 801",
          "HubLocation": "R83",
          "LastRoutingDate": "2025-10-29"
        },
        "HandlingInformation": "S"
      }
    ],
    "PrintData": [
      {
        "Data": "JVBERi0xLjQKJeLjz9MK",
        "LabelFormat": "PDF"
      }
    ],
    "CustomerID": "2760322938",
    "PickupLocation": "DE 600"
  }
}"""

MultiPieceShipmentResponse = """{
  "CreatedShipment": {
    "ShipmentReference": ["TEST123"],
    "ParcelData": [
      {"TrackID": "TRACK_A", "ParcelNumber": "601079500843"},
      {"TrackID": "TRACK_B", "ParcelNumber": "601079500844"}
    ],
    "PrintData": [
      {"Data": "LABEL_A", "LabelFormat": "PDF"},
      {"Data": "LABEL_B", "LabelFormat": "PDF"}
    ],
    "CustomerID": "2760322938",
    "PickupLocation": "DE 600"
  }
}"""

IntlShipmentResponse = """{
  "CreatedShipment": {
    "ShipmentReference": ["INTL-001"],
    "ParcelData": [
      {
        "TrackID": "GBINTL01",
        "ParcelNumber": "601079500999"
      }
    ],
    "PrintData": [
      {
        "Data": "JVBERi0xLjQKJeLjz9MK",
        "LabelFormat": "PDF"
      }
    ],
    "CustomerID": "2760322938",
    "PickupLocation": "DE 600"
  }
}"""

CustomsConsignmentResponse = """{
  "consignmentId": "CC-2026-0001",
  "status": "ACCEPTED"
}"""

ErrorResponse = """{
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid request parameters",
      "field": "shipment.recipient.postalCode"
    }
  ]
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "gls",
        "carrier_name": "gls",
        "tracking_number": "601079500843",
        "shipment_identifier": "ZHO9AXAC",
        "label_type": "PDF",
        "docs": {"label": "JVBERi0xLjQKJeLjz9MK"},
        "meta": {
            "customer_id": "2760322938",
            "pickup_location": "DE 600",
            "shipment_references": ["TEST123"],
            "tracking_numbers": ["601079500843"],
            "track_ids": ["ZHO9AXAC"],
        },
    },
    [],
]

ParsedShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "gls",
            "carrier_name": "gls",
            "code": "VALIDATION_ERROR",
            "message": "Invalid request parameters",
            "details": {"field": "shipment.recipient.postalCode"},
        }
    ],
]
