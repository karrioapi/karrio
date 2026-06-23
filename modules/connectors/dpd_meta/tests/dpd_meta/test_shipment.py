"""DPD Meta carrier shipment tests."""

import logging
import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dpd_meta.units as provider_units
import karrio.sdk as karrio

from .fixture import gateway, gateway_with_depot

logger = logging.getLogger(__name__)


class TestDPDGroupShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), [ShipmentRequest])

    def test_create_shipment(self):
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment?LabelPrintFormat=PDF",
            )

    def test_create_shipment_request_includes_sending_depot(self):
        request = gateway_with_depot.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = lib.to_dict(request.serialize())
        # shipment carries the 7-digit GeoRouting code (BU code + depot)
        self.assertEqual(serialized[0]["sendingDepot"], "0010998")

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_create_multiparcel_shipment_request_rounds_weight_to_10g(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**MultiparcelRoundingPayload))
        serialized = lib.to_dict(request.serialize())
        self.assertEqual(serialized[0]["shipmentInfos"]["weight"], "240")
        self.assertNotIn("dimensions", serialized[0]["shipmentInfos"])
        self.assertEqual(serialized[0]["parcel"][0]["parcelInfos"]["weight"], "120")
        self.assertEqual(serialized[0]["parcel"][1]["parcelInfos"]["weight"], "120")

    def test_create_shipment_request_b2c_recipient_name_mapping(self):
        payload = dict(
            ShipmentPayload,
            recipient=dict(
                ShipmentPayload["recipient"],
                company_name="",
                person_name="Max Mustermann",
            ),
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        receiver_address = lib.to_dict(request.serialize())[0]["receiver"]["address"]
        self.assertEqual(receiver_address["name1"], "Max Mustermann")
        self.assertEqual(receiver_address.get("name2", ""), "")

    def test_create_shipment_request_b2c_classic_product_code(self):
        payload = dict(ShipmentPayload, service="dpd_meta_b2c_classic")
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        self.assertEqual(lib.to_dict(request.serialize())[0]["shipmentInfos"]["productCode"], "327")

    def test_create_shipment_request_b2c_small_product_code(self):
        payload = dict(ShipmentPayload, service="dpd_meta_b2c_small")
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        self.assertEqual(lib.to_dict(request.serialize())[0]["shipmentInfos"]["productCode"], "328")

    def test_create_shipment_request_includes_phone_numbers(self):
        # Phone numbers are transmitted like any other carrier; recipient-phone
        # privacy is handled centrally by the generic suppress_recipient_phone
        # option at the SDK seam, not by a DPD-specific gate.
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = lib.to_dict(request.serialize())[0]
        self.assertEqual(serialized["sender"]["contact"]["phone1"], "+49301234567")
        self.assertEqual(serialized["receiver"]["contact"]["phone1"], "+33123456789")


class TestResolveProductCode(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def _options(self, data: dict):
        return lib.to_shipping_options(data, initializer=provider_units.shipping_options_initializer)

    # Single-option cells (11 tests)

    def test_cod_classic(self):
        self.assertEqual(provider_units.resolve_product_code("101", self._options({"cash_on_delivery": 100})), "109")

    def test_cod_b2c_classic(self):
        self.assertEqual(provider_units.resolve_product_code("327", self._options({"cash_on_delivery": 100})), "329")

    def test_cod_b2c_small(self):
        self.assertEqual(provider_units.resolve_product_code("328", self._options({"cash_on_delivery": 100})), "330")

    def test_saturday_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_saturday_delivery": True})), "103"
        )

    def test_saturday_b2c_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_saturday_delivery": True})), "358"
        )

    def test_small_parcel_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_small_parcel": True})), "136"
        )

    def test_small_parcel_b2c_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_small_parcel": True})), "328"
        )

    def test_ex_works_classic(self):
        self.assertEqual(provider_units.resolve_product_code("101", self._options({"dpd_meta_ex_works": True})), "105")

    def test_pudo_b2c_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_parcel_shop_id": "DE40501"})), "337"
        )

    def test_pudo_b2c_small(self):
        self.assertEqual(
            provider_units.resolve_product_code("328", self._options({"dpd_meta_parcel_shop_id": "DE40501"})), "338"
        )

    def test_pass_through_no_options(self):
        self.assertEqual(provider_units.resolve_product_code("101", self._options({})), "101")

    # Dual-option triples (2 tests)

    def test_dual_b2c_classic_cod_small(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "327", self._options({"cash_on_delivery": 100, "dpd_meta_small_parcel": True})
            ),
            "330",
        )

    def test_dual_b2c_classic_pudo_small(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "327", self._options({"dpd_meta_parcel_shop_id": "DE40501", "dpd_meta_small_parcel": True})
            ),
            "338",
        )

    # Precedence tests (3 tests)

    def test_precedence_cod_over_saturday(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "101", self._options({"cash_on_delivery": 100, "saturday_delivery": True})
            ),
            "109",
        )

    def test_precedence_cod_over_pudo(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "327", self._options({"cash_on_delivery": 100, "dpd_meta_parcel_shop_id": "X"})
            ),
            "329",
        )

    def test_precedence_small_over_exw(self):
        # Phase 1: (101, exw, small) is now a documented dual-option triple -> 138.
        # The triple takes precedence over the single-option small-parcel branch.
        self.assertEqual(
            provider_units.resolve_product_code(
                "101", self._options({"dpd_meta_small_parcel": True, "dpd_meta_ex_works": True})
            ),
            "138",
        )

    # Edge cases (4 tests)

    def test_zero_cod_is_falsy(self):
        self.assertEqual(provider_units.resolve_product_code("101", self._options({"cash_on_delivery": 0.0})), "101")

    def test_empty_pudo_id_is_falsy(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_parcel_shop_id": ""})), "101"
        )

    def test_express_pass_through_with_cod(self):
        self.assertEqual(provider_units.resolve_product_code("350", self._options({"cash_on_delivery": 100})), "350")

    def test_unknown_service_pass_through(self):
        self.assertEqual(provider_units.resolve_product_code("dpd_meta_classic", self._options({})), "dpd_meta_classic")

    def test_resolve_pudo_id_emits_on_pudo_code(self):
        opts = self._options({"dpd_meta_parcel_shop_id": "X"})
        self.assertEqual(provider_units.resolve_pudo_id(opts, "337"), "X")
        self.assertEqual(provider_units.resolve_pudo_id(opts, "338"), "X")

    def test_resolve_pudo_id_none_on_non_pudo_code(self):
        opts = self._options({"dpd_meta_parcel_shop_id": "X"})
        self.assertIsNone(provider_units.resolve_pudo_id(opts, "101"))
        self.assertIsNone(provider_units.resolve_pudo_id(self._options({}), "337"))

    # Phase 1 — productCode swap + alias rewire tests

    def test_food_classic(self):
        self.assertEqual(provider_units.resolve_product_code("101", self._options({"dpd_meta_food": True})), "383")

    def test_food_express_18(self):
        self.assertEqual(provider_units.resolve_product_code("155", self._options({"dpd_meta_food": True})), "378")

    def test_food_express_12(self):
        self.assertEqual(provider_units.resolve_product_code("225", self._options({"dpd_meta_food": True})), "379")

    def test_exchange_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_exchange_service": True})),
            "113",
        )

    def test_dual_classic_exchange_small(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options({"dpd_meta_exchange_service": True, "dpd_meta_small_parcel": True}),
            ),
            "142",
        )

    def test_dual_classic_exw_small(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "101", self._options({"dpd_meta_ex_works": True, "dpd_meta_small_parcel": True})
            ),
            "138",
        )

    def test_express_18_exw(self):
        self.assertEqual(provider_units.resolve_product_code("155", self._options({"dpd_meta_ex_works": True})), "158")

    def test_express_12_saturday(self):
        self.assertEqual(
            provider_units.resolve_product_code("225", self._options({"dpd_meta_saturday_delivery": True})),
            "228",
        )

    def test_express_12_exw(self):
        self.assertEqual(provider_units.resolve_product_code("225", self._options({"dpd_meta_ex_works": True})), "231")

    def test_dual_express_12_exw_saturday(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "225",
                self._options({"dpd_meta_ex_works": True, "dpd_meta_saturday_delivery": True}),
            ),
            "234",
        )

    def test_express_830_exw(self):
        self.assertEqual(provider_units.resolve_product_code("350", self._options({"dpd_meta_ex_works": True})), "351")

    # Alias rewires — these resolve at ShippingService.map level, not in resolve_product_code
    #
    # Non-Bronze services (118/365/366/378/379/383) have their ShippingService aliases
    # commented out for the Bronze certification demo (SHIP2-1194).  value_or_key falls
    # back to the input key string when the member is absent; the routing maps
    # (FOOD_PRODUCT_CODE_MAP, EXCHANGE_PRODUCT_CODE_MAP) operate on ShippingOption state
    # and are unaffected.  Uncomment the enum members once these products are in scope.
    def test_alias_food_resolves_to_key_when_hidden(self):
        # dpd_meta_food alias commented out → value_or_key returns input key
        code = provider_units.ShippingService.map("dpd_meta_food").value_or_key
        self.assertEqual(code, "dpd_meta_food")

    def test_alias_shop_return_resolves_to_332(self):
        code = provider_units.ShippingService.map("dpd_meta_shop_return").value_or_key
        self.assertEqual(code, "332")

    def test_alias_tyres_resolves_to_key_when_hidden(self):
        # dpd_meta_classic_tyres alias commented out → falls back to key
        code = provider_units.ShippingService.map("dpd_meta_classic_tyres").value_or_key
        self.assertEqual(code, "dpd_meta_classic_tyres")

    def test_alias_tyres_b2c_resolves_to_key_when_hidden(self):
        # dpd_meta_classic_tyres_b2c alias commented out → falls back to key
        code = provider_units.ShippingService.map("dpd_meta_classic_tyres_b2c").value_or_key
        self.assertEqual(code, "dpd_meta_classic_tyres_b2c")

    def test_alias_shop2shop_resolves_to_345(self):
        code = provider_units.ShippingService.map("dpd_meta_shop2shop_domestic").value_or_key
        self.assertEqual(code, "345")

    def test_b2c_classic_routes_to_small_parcel_when_flagged(self):
        # Shop2Home / Shop2Shop / Klein Paket / size variants no longer have
        # alias service codes. Rate sheets reference dpd_meta_b2c_classic
        # directly; XS/S parcel sizes set dpd_meta_small_parcel to route to 328.
        self.assertEqual(provider_units.ShippingService.map("dpd_meta_b2c_classic").value_or_key, "327")
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_small_parcel": True})),
            "328",
        )

    def test_exchange_inbound_resolves_to_key_when_hidden(self):
        # dpd_meta_classic_exchange_inbound alias commented out → falls back to key
        code = provider_units.ShippingService.map("dpd_meta_classic_exchange_inbound").value_or_key
        self.assertEqual(code, "dpd_meta_classic_exchange_inbound")

    def test_food_time_variants_resolve_to_key_when_hidden(self):
        # dpd_meta_food_1200 / dpd_meta_food_1800 aliases commented out → fall back to keys
        self.assertEqual(provider_units.ShippingService.map("dpd_meta_food_1200").value_or_key, "dpd_meta_food_1200")
        self.assertEqual(provider_units.ShippingService.map("dpd_meta_food_1800").value_or_key, "dpd_meta_food_1800")

    def test_parcelshop_resolves_to_337(self):
        # Direct rate-sheet path: parcelshop = 337. Booking requires a
        # parcel_shop_id option (resolve_pudo_id surfaces it for codes 337/338).
        self.assertEqual(provider_units.ShippingService.map("dpd_meta_parcelshop").value_or_key, "337")

    # Limited Quantity (ADR-LQ) — April 2026 PDF additions.
    def test_lq_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_hazardous_limited_quantities": True})),
            "793",
        )

    def test_lq_b2c_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_hazardous_limited_quantities": True})),
            "794",
        )

    def test_lq_shop_return(self):
        self.assertEqual(
            provider_units.resolve_product_code("332", self._options({"dpd_meta_hazardous_limited_quantities": True})),
            "447",
        )

    def test_lq_express_12(self):
        self.assertEqual(
            provider_units.resolve_product_code("225", self._options({"dpd_meta_hazardous_limited_quantities": True})),
            "797",
        )

    def test_lq_express_18(self):
        self.assertEqual(
            provider_units.resolve_product_code("155", self._options({"dpd_meta_hazardous_limited_quantities": True})),
            "799",
        )

    def test_dual_classic_exw_lq(self):
        # 101 + ex_works + LQ → 704 (PDF-documented triple).
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options({"dpd_meta_ex_works": True, "dpd_meta_hazardous_limited_quantities": True}),
            ),
            "704",
        )

    def test_hazardous_beats_lq(self):
        # Mutually exclusive in practice; full hazardous wins if both are set.
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options({"dpd_meta_dangerous_goods": True, "dpd_meta_hazardous_limited_quantities": True}),
            ),
            "102",
        )

    # Precedence sanity — food beats exw beats small
    def test_food_beats_other_singles(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options(
                    {
                        "dpd_meta_food": True,
                        "dpd_meta_ex_works": True,
                        "dpd_meta_small_parcel": True,
                    }
                ),
            ),
            "383",  # food wins; no (101, food, *) triple matches
        )

    # Phase 2 — hazardous (dangerous goods) precedence

    def test_hazardous_classic(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_dangerous_goods": True})),
            "102",
        )

    def test_dual_classic_exw_hazardous(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options({"dpd_meta_dangerous_goods": True, "dpd_meta_ex_works": True}),
            ),
            "106",
        )

    def test_hazardous_beats_exchange(self):
        # Single-option precedence: hazardous > exchange. No (101, hazardous, exchange) triple defined.
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options({"dpd_meta_dangerous_goods": True, "dpd_meta_exchange_service": True}),
            ),
            "102",
        )

    def test_food_beats_hazardous(self):
        # food still highest.
        self.assertEqual(
            provider_units.resolve_product_code(
                "101",
                self._options({"dpd_meta_food": True, "dpd_meta_dangerous_goods": True}),
            ),
            "383",
        )

    # Phase 3 — id_check (PersonalDeliveryType=s2) precedence

    def test_id_check_express_18(self):
        self.assertEqual(
            provider_units.resolve_product_code("155", self._options({"dpd_meta_id_check": True})),
            "168",
        )

    def test_id_check_express_12(self):
        self.assertEqual(
            provider_units.resolve_product_code("225", self._options({"dpd_meta_id_check": True})),
            "249",
        )

    def test_dual_express_18_exw_id_check(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "155",
                self._options({"dpd_meta_id_check": True, "dpd_meta_ex_works": True}),
            ),
            "171",
        )

    def test_dual_express_12_exw_id_check(self):
        self.assertEqual(
            provider_units.resolve_product_code(
                "225",
                self._options({"dpd_meta_id_check": True, "dpd_meta_ex_works": True}),
            ),
            "255",
        )

    def test_food_beats_id_check(self):
        # food highest precedence; even with id_check set, food still wins.
        self.assertEqual(
            provider_units.resolve_product_code(
                "155",
                self._options({"dpd_meta_food": True, "dpd_meta_id_check": True}),
            ),
            "378",
        )

    def test_id_check_beats_saturday(self):
        # Single-option precedence: id_check above saturday.
        self.assertEqual(
            provider_units.resolve_product_code(
                "225",
                self._options({"dpd_meta_id_check": True, "dpd_meta_saturday_delivery": True}),
            ),
            "249",
        )

    # Phase 5 — country allowlist guard for 103 (Saturday Classic) and 358 (Saturday B2C)

    def test_country_guard_103_de_falls_back(self):
        # DE is not in 103's allowlist (NL, BE, PL, CZ, FR) → fall back to 101.
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_saturday_delivery": True}), "DE"),
            "101",
        )

    def test_country_guard_103_fr_passes(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_saturday_delivery": True}), "FR"),
            "103",
        )

    def test_country_guard_103_nl_passes(self):
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_saturday_delivery": True}), "NL"),
            "103",
        )

    def test_country_guard_358_de_falls_back(self):
        # DE is not in 358's allowlist (NL, BE, BG) → fall back to 327.
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_saturday_delivery": True}), "DE"),
            "327",
        )

    def test_country_guard_358_nl_passes(self):
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_saturday_delivery": True}), "NL"),
            "358",
        )

    def test_country_guard_358_bg_passes(self):
        self.assertEqual(
            provider_units.resolve_product_code("327", self._options({"dpd_meta_saturday_delivery": True}), "BG"),
            "358",
        )

    def test_country_guard_backwards_compat_no_country_arg(self):
        # When recipient_country is omitted (legacy callers), no guard applied —
        # current behaviour preserved.
        self.assertEqual(
            provider_units.resolve_product_code("101", self._options({"dpd_meta_saturday_delivery": True})),
            "103",
        )


class TestDPDMetaShipmentIntegration(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_create_shipment_request_with_cod(self):
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_classic",
            options={"cash_on_delivery": 100.0, "currency": "EUR"},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        self.assertDictEqual(lib.to_dict(request.serialize())[0], ShipmentRequestWithCOD)

    def test_create_shipment_request_with_pudo(self):
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_b2c_classic",
            options={"dpd_meta_parcel_shop_id": "DE40501", "dpd_meta_notification_email": "test@example.com"},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        self.assertDictEqual(lib.to_dict(request.serialize())[0], ShipmentRequestWithPUDO)

    def test_pudo_id_not_emitted_on_non_pudo_service(self):
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_classic",
            options={"dpd_meta_parcel_shop_id": "DE40501"},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())[0]
        self.assertEqual(request_dict["shipmentInfos"]["productCode"], "101")
        self.assertNotIn("pudoId", request_dict["receiver"])

    def test_user_reference_goes_to_customer_reference_numbers(self):
        """Regression: payload.reference must NOT leak into shipmentInfos.shipmentId
        (BU-API enforces mpsId == 25 alphanumeric); it belongs in customerReferenceNumbers."""
        payload = dict(ShipmentPayload, service="dpd_meta_classic", reference="ORDER-1234")
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())[0]
        self.assertNotIn("shipmentId", request_dict["shipmentInfos"])
        self.assertEqual(request_dict.get("customerReferenceNumbers"), ["ORDER-1234"])

    def test_pudo_auto_fallback_to_recipient_email(self):
        """PUDO shipments auto-fallback to recipient.email when no explicit
        dpd_meta_notification_email is set — required by DPD SOAP parcelShopNotification."""
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_b2c_classic",
            recipient=dict(ShipmentPayload["recipient"], email="anna@example.com"),
            options={"dpd_meta_parcel_shop_id": "PS0001"},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())[0]
        messages = request_dict["parcel"][0]["messages"]
        self.assertListEqual(
            messages,
            ShipmentRequestPUDOAutoFallbackMessages,
        )

    def test_senderparcelrefs_suppressed_when_value_is_karrio_autofill(self):
        """karrio core auto-fills parcel.reference_number from the parcel id
        (`pcl_<hex>` -> `<hex>`). That cryptic value must NOT leak into
        senderParcelRefs."""
        payload = dict(
            ShipmentPayload,
            parcels=[
                dict(
                    ShipmentPayload["parcels"][0],
                    id="pcl_a0590914ba1c",
                    reference_number="a0590914ba1c",
                )
            ],
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertNotIn("senderParcelRefs", serialized["parcel"][0])

    def test_senderparcelrefs_kept_when_user_supplied(self):
        """A meaningful (non-autofill) reference_number must still be sent."""
        payload = dict(
            ShipmentPayload,
            parcels=[dict(ShipmentPayload["parcels"][0], reference_number="JTL-PARCEL-001")],
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertEqual(serialized["parcel"][0]["senderParcelRefs"], ["JTL-PARCEL-001"])

    def test_customs_skipped_for_eu_internal_cross_border(self):
        """EU member-state to EU member-state: no customs block even if user supplies it."""
        payload = dict(
            ShipmentPayload,
            customs={
                "content_type": "merchandise",
                "incoterm": "DDP",
                "commodities": [
                    {"description": "Item", "quantity": 1, "value_amount": 50.0, "weight": 1.0, "weight_unit": "KG"}
                ],
            },
        )
        # Default fixture is DE → FR (both EU). Customs must NOT emit.
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertNotIn("international", serialized)
        self.assertNotIn("cifcost", serialized.get("shipmentInfos", {}))

    def test_customs_emitted_for_non_eu_cross_border(self):
        """EU member-state to non-EU country: customs block emits."""
        payload = dict(
            ShipmentPayload,
            recipient=dict(ShipmentPayload["recipient"], country_code="GB"),
            customs={
                "content_type": "merchandise",
                "incoterm": "DDP",
                "commodities": [
                    {"description": "Item", "quantity": 1, "value_amount": 50.0, "weight": 1.0, "weight_unit": "KG"}
                ],
            },
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertIn("international", serialized)

    def test_create_shipment_request_b2c_emits_email_message_from_recipient(self):
        """B2C product codes auto-promote recipient.email to predict notification."""
        payload = dict(ShipmentPayload, service="dpd_meta_b2c_classic")
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        messages = serialized["parcel"][0].get("messages") or []
        email_msgs = [m for m in messages if m.get("messageType") == "EMAIL"]
        self.assertEqual(len(email_msgs), 1)
        self.assertEqual(email_msgs[0]["messageDestination"], ShipmentPayload["recipient"]["email"])

    def test_create_shipment_request_classic_does_not_emit_email_message(self):
        """Non-B2C product codes do NOT auto-promote recipient.email."""
        payload = dict(ShipmentPayload, service="dpd_meta_classic")
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        messages = serialized["parcel"][0].get("messages") or []
        email_msgs = [m for m in messages if m.get("messageType") == "EMAIL"]
        self.assertEqual(len(email_msgs), 0)

    def test_address_fields_truncated_to_maxlength(self):
        """Regression: sender/receiver address fields exceeding DPD maxLength must be
        truncated to prevent cvc-maxLength-valid SOAP faults from the BU-API."""
        long_company = "A" * 75  # 75 chars — DPD maxLength for name1/companyName is 35
        long_street = "B" * 61  # 61 chars — DPD maxLength for street is 35
        payload = dict(
            ShipmentPayload,
            shipper=dict(
                ShipmentPayload["shipper"],
                company_name=long_company,
                address_line1=long_street,
            ),
            recipient=dict(
                ShipmentPayload["recipient"],
                company_name=long_company,
                address_line1=long_street,
            ),
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        request_dict = lib.to_dict(request.serialize())[0]
        sender_addr = request_dict["sender"]["address"]
        receiver_addr = request_dict["receiver"]["address"]
        self.assertEqual(len(sender_addr["name1"]), 35)
        self.assertEqual(len(sender_addr["street"]), 35)
        self.assertEqual(len(receiver_addr["name1"]), 35)
        self.assertEqual(len(receiver_addr["street"]), 35)

    def test_create_shipment_request_hazardous_emits_block(self):
        """parcel.hazardous block is populated when dpd_meta_dangerous_goods=True;
        productCode auto-resolves to 102 (D + HAZ)."""
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_classic",
            options={
                "dpd_meta_dangerous_goods": True,
                "dpd_meta_dg_un_number": "1234",
                "dpd_meta_dg_hazard_class": "3",
                "dpd_meta_dg_packing_group": "II",
                "dpd_meta_dg_description": "Flammable liquid",
                "dpd_meta_dg_weight": 2.5,
            },
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertEqual(serialized["shipmentInfos"]["productCode"], "102")
        parcel = serialized["parcel"][0]
        self.assertIn("hazardous", parcel)
        # DPD META-API requires hazardous as an array of HazardousType.
        self.assertIsInstance(parcel["hazardous"], list)
        self.assertEqual(len(parcel["hazardous"]), 1)
        haz = parcel["hazardous"][0]
        self.assertEqual(haz["identificationUnNo"], "1234")
        self.assertEqual(haz["classCode"], "3")
        self.assertEqual(haz["packingGroup"], "II")
        self.assertEqual(haz["description"], "Flammable liquid")
        self.assertEqual(haz["substanceWeight"], "2500")

    def test_create_shipment_request_no_hazardous_when_off(self):
        payload = dict(ShipmentPayload, service="dpd_meta_classic", options={})
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        parcel = serialized["parcel"][0]
        self.assertNotIn("hazardous", parcel)

    def test_create_shipment_request_id_check_emits_person_block(self):
        """id_check=true emits Shipment.person.PersonalDeliveryType="s2" and
        auto-resolves productCode to 168 on Express 18:00."""
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_express_18",
            options={"dpd_meta_id_check": True},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertEqual(serialized["shipmentInfos"]["productCode"], "168")
        self.assertIn("person", serialized)
        self.assertEqual(serialized["person"]["personalDeliveryType"], "s2")

    def test_create_shipment_request_no_person_when_id_check_off(self):
        payload = dict(ShipmentPayload, service="dpd_meta_express_18", options={})
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertNotIn("person", serialized)

    def test_create_shipment_request_cod_emits_mps_complete_delivery(self):
        """COD shipments must serialize mpsCompleteDelivery="s2" at the top level."""
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_classic",
            options={"cash_on_delivery": 100.0, "currency": "EUR"},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertEqual(serialized.get("mpsCompleteDelivery"), "s2")

    def test_create_shipment_request_no_mps_when_no_cod(self):
        payload = dict(ShipmentPayload, service="dpd_meta_classic", options={})
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertNotIn("mpsCompleteDelivery", serialized)

    def test_create_shipment_request_de_saturday_falls_back_to_101(self):
        """Country allowlist guard: DE→DE saturday must NOT emit 103 (DPD only
        accepts 103 in NL/BE/PL/CZ/FR). Must fall back to 101."""
        payload = dict(
            ShipmentPayload,
            service="dpd_meta_classic",
            recipient=dict(ShipmentPayload["recipient"], country_code="DE"),
            options={"dpd_meta_saturday_delivery": True},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = lib.to_dict(request.serialize())[0]
        self.assertEqual(serialized["shipmentInfos"]["productCode"], "101")


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "Main Street",
        "street_number": "42",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "person_name": "John Sender",
        "company_name": "Sender Corp",
        "phone_number": "+49301234567",
        "email": "sender@example.com",
    },
    "recipient": {
        "address_line1": "Secondary Road",
        "street_number": "88",
        "city": "Paris",
        "postal_code": "75001",
        "country_code": "FR",
        "person_name": "Jane Receiver",
        "company_name": "Receiver Inc",
        "phone_number": "+33123456789",
        "email": "receiver@example.com",
    },
    "parcels": [
        {
            "weight": 3.0,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Electronic equipment",
        }
    ],
    "service": "dpd_meta_classic",
    "reference": "SHIP123456",
}

ShipmentRequest = {
    # DE shipper: the proxy resolves the depot serving the sender zip code.
    "sendingDepot": "[DEPOT]",
    "customerReferenceNumbers": ["SHIP123456"],
    "numberOfParcels": "1",
    "parcel": [
        {
            "parcelContent": "Electronic equipment",
            "parcelInfos": {
                "dimensions": {"height": 15, "length": 30, "width": 20},
                "weight": "3000",
            },
        }
    ],
    "receiver": {
        "address": {
            "city": "Paris",
            "companyName": "Receiver Inc",
            "country": "FR",
            "houseNumber": "88",
            "name1": "Receiver Inc",
            "name2": "Jane Receiver",
            "street": "Secondary Road",
            "zipCode": "75001",
        },
        "contact": {"email": "receiver@example.com", "phone1": "+33123456789"},
    },
    "sender": {
        "address": {
            "city": "Berlin",
            "companyName": "Sender Corp",
            "country": "DE",
            "houseNumber": "42",
            "name1": "Sender Corp",
            "name2": "John Sender",
            "street": "Main Street",
            "zipCode": "10115",
        },
        "contact": {"email": "sender@example.com", "phone1": "+49301234567"},
    },
    "shipmentInfos": {
        "productCode": "101",
        "weight": "3000",
    },
}

ShipmentResponse = """{
  "shipmentId": "SHIP123456",
  "parcelIds": ["0987654321"],
  "networkShipmentId": "NET123456",
  "networkParcelIds": ["0987654321"],
  "parcelBarcodes": [
    {
      "parcel": "0987654321",
      "barcode": "0987654321000",
      "reference": "REF001"
    }
  ],
  "label": {
    "base64Data": "JVBERi0xLjQKJeLjz9MNCg==",
    "media-type": "application/pdf"
  }
}"""

ErrorResponse = """{
  "errorCode": "ERR001",
  "errorMessage": "Invalid shipment data",
  "errorOrigin": "META-API"
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "dpd_meta",
        "carrier_name": "dpd_meta",
        "tracking_number": "0987654321",
        "shipment_identifier": "SHIP123456",
        "label_type": "PDF",
        "docs": {"label": "JVBERi0xLjQKJeLjz9MNCg=="},
        "meta": {
            "network_shipment_id": "NET123456",
            "network_parcel_ids": ["0987654321"],
            "parcel_barcodes": [
                {
                    "parcel": "0987654321",
                    "barcode": "0987654321000",
                    "reference": "REF001",
                }
            ],
            "tracking_numbers": ["0987654321"],
            "tracking_url": "https://www.dpdgroup.com/tracking?parcelNumber=0987654321",
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_meta",
            "carrier_name": "dpd_meta",
            "code": "ERR001",
            "message": "Error Code ERR001: Invalid shipment data",
            "details": {"errorOrigin": "META-API"},
        }
    ],
]

MultiparcelRoundingPayload = {
    "shipper": {
        "address_line1": "Main Street",
        "street_number": "42",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "person_name": "John Sender",
        "company_name": "Sender Corp",
        "phone_number": "+49301234567",
        "email": "sender@example.com",
    },
    "recipient": {
        "address_line1": "Secondary Road",
        "street_number": "88",
        "city": "Hamburg",
        "postal_code": "20095",
        "country_code": "DE",
        "person_name": "Jane Receiver",
        "company_name": "Receiver Inc",
        "phone_number": "+49401234567",
        "email": "receiver@example.com",
    },
    "parcels": [
        {
            "weight": 0.115,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
        {
            "weight": 0.115,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
    ],
    "service": "dpd_meta_classic",
    "reference": "MULTI001",
}

ShipmentRequestWithCOD = {
    "sendingDepot": "[DEPOT]",
    "customerReferenceNumbers": ["SHIP123456"],
    "mpsCompleteDelivery": "s2",
    "numberOfParcels": "1",
    "parcel": [
        {
            "cod": {
                "amount": {
                    "amount": 100.0,
                    "currency": "EUR",
                },
                "collectType": "s0",
            },
            "parcelContent": "Electronic equipment",
            "parcelInfos": {
                "dimensions": {"height": 15, "length": 30, "width": 20},
                "weight": "3000",
            },
        }
    ],
    "receiver": {
        "address": {
            "city": "Paris",
            "companyName": "Receiver Inc",
            "country": "FR",
            "houseNumber": "88",
            "name1": "Receiver Inc",
            "name2": "Jane Receiver",
            "street": "Secondary Road",
            "zipCode": "75001",
        },
        "contact": {"email": "receiver@example.com", "phone1": "+33123456789"},
    },
    "sender": {
        "address": {
            "city": "Berlin",
            "companyName": "Sender Corp",
            "country": "DE",
            "houseNumber": "42",
            "name1": "Sender Corp",
            "name2": "John Sender",
            "street": "Main Street",
            "zipCode": "10115",
        },
        "contact": {"email": "sender@example.com", "phone1": "+49301234567"},
    },
    "shipmentInfos": {
        "productCode": "109",
        "weight": "3000",
    },
}

ShipmentRequestWithPUDO = {
    "customerReferenceNumbers": ["SHIP123456"],
    "numberOfParcels": "1",
    "parcel": [
        {
            "messages": [
                {
                    "messageDestination": "test@example.com",
                    "messageLanguage": "EN",
                    "messageType": "EMAIL",
                }
            ],
            "parcelContent": "Electronic equipment",
            "parcelInfos": {
                "dimensions": {"height": 15, "length": 30, "width": 20},
                "weight": "3000",
            },
        }
    ],
    "receiver": {
        "address": {
            "city": "Paris",
            "companyName": "Receiver Inc",
            "country": "FR",
            "houseNumber": "88",
            "name1": "Receiver Inc",
            "name2": "Jane Receiver",
            "street": "Secondary Road",
            "zipCode": "75001",
        },
        "contact": {"email": "receiver@example.com", "phone1": "+33123456789"},
        "pudoId": "DE40501",
    },
    "sender": {
        "address": {
            "city": "Berlin",
            "companyName": "Sender Corp",
            "country": "DE",
            "houseNumber": "42",
            "name1": "Sender Corp",
            "name2": "John Sender",
            "street": "Main Street",
            "zipCode": "10115",
        },
        "contact": {"email": "sender@example.com", "phone1": "+49301234567"},
    },
    "shipmentInfos": {
        "productCode": "337",
        "weight": "3000",
    },
    "sendingDepot": "[DEPOT]",
}

ShipmentRequestPUDOAutoFallbackMessages = [
    {
        "messageDestination": "anna@example.com",
        "messageLanguage": "EN",
        "messageType": "EMAIL",
    }
]
