"""Tests for /references and /carriers endpoint i18n translation support.

Verifies that the references and carriers endpoints return translated strings
when a language is specified via query param or Accept-Language header.
"""

from django.contrib.auth import get_user_model
from karrio.server.user.models import Token
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestReferencesTranslation(APITestCase):
    """Test that GET /api/references returns translated values."""

    def setUp(self):
        self.maxDiff = None
        self.user = get_user_model().objects.create_superuser("admin@example.com", "test")
        self.token = Token.objects.create(user=self.user, test_mode=False)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_references_default_english(self):
        """Test that references returns English values by default."""
        response = self.client.get("/v1/references?reduced=false")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("carriers", data)
        self.assertIn("service_names", data)
        self.assertIn("option_names", data)
        self.assertIn("options", data)
        self.assertIn("connection_fields", data)
        self.assertIn("carrier_capabilities", data)
        self.assertIn("integration_status", data)
        self.assertIn("shipment_statuses", data)
        self.assertIn("pickup_statuses", data)
        self.assertIn("tracking_statuses", data)
        self.assertIn("tracking_reasons", data)
        self.assertIn("rate_charge_labels", data)
        self.assertIn("rate_first_mile", data)
        self.assertIn("rate_last_mile", data)
        self.assertIn("rate_form_factor", data)

    def test_references_status_and_reason_labels_default_english(self):
        """Test that status and reason references expose human-readable English labels."""
        response = self.client.get("/v1/references?reduced=false")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data.get("shipment_statuses", {}).get("needs_attention"), "Needs Attention")
        self.assertEqual(data.get("pickup_statuses", {}).get("picked_up"), "Picked Up")
        self.assertEqual(data.get("tracking_statuses", {}).get("return_to_sender"), "Return To Sender")
        self.assertEqual(
            data.get("tracking_reasons", {}).get("carrier_address_not_found"),
            "Carrier Address Not Found",
        )

    def test_references_default_rate_labels(self):
        """Test that rate-related reference labels are exposed in English by default."""
        response = self.client.get("/v1/references?reduced=false")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data.get("rate_charge_labels", {}).get("base_charge"), "Base Charge")
        self.assertEqual(data.get("rate_first_mile", {}).get("pick_up"), "Pick Up")
        self.assertEqual(data.get("rate_last_mile", {}).get("service_point"), "Service Point")
        self.assertEqual(data.get("rate_form_factor", {}).get("envelope"), "Envelope")

    def test_references_status_and_reason_labels_with_lang(self):
        """Test that translated references endpoint includes status and reason dictionaries."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        for key in (
            "shipment_statuses",
            "pickup_statuses",
            "tracking_statuses",
            "tracking_reasons",
        ):
            self.assertIn(key, data)
            self.assertIsInstance(data[key], dict)
            self.assertGreater(len(data[key]), 0, f"{key} should not be empty")

    def test_references_status_and_reason_labels_german_values(self):
        """Test that German references return translated status and reason labels."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data.get("shipment_statuses", {}).get("created"), "Erstellt")
        self.assertEqual(
            data.get("shipment_statuses", {}).get("needs_attention"),
            "Aufmerksamkeit erforderlich",
        )
        self.assertEqual(data.get("pickup_statuses", {}).get("scheduled"), "Geplant")
        self.assertEqual(
            data.get("tracking_statuses", {}).get("return_to_sender"),
            "Rücksendung an Absender",
        )
        self.assertEqual(
            data.get("tracking_reasons", {}).get("carrier_address_not_found"),
            "Adresse durch Zusteller nicht gefunden",
        )
        self.assertEqual(
            data.get("tracking_reasons", {}).get("customs_delay"),
            "Verzögerung beim Zoll",
        )

    def test_references_german_rate_labels(self):
        """Test that rate-related reference labels are translated for German locale."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data.get("rate_charge_labels", {}).get("base_charge"), "Grundpreis")
        self.assertEqual(data.get("rate_charge_labels", {}).get("fuel_surcharge"), "Kraftstoffzuschlag")
        self.assertEqual(data.get("rate_first_mile", {}).get("pick_up"), "Abholung")
        self.assertEqual(
            data.get("rate_first_mile", {}).get("pick_up_and_drop_off"),
            "Abholung und Abgabe",
        )
        self.assertEqual(data.get("rate_last_mile", {}).get("service_point"), "Servicestelle")
        self.assertEqual(data.get("rate_last_mile", {}).get("po_box"), "Postfach")
        self.assertEqual(data.get("rate_form_factor", {}).get("envelope"), "Umschlag")
        self.assertEqual(data.get("rate_form_factor", {}).get("pallet"), "Palette")

    def test_references_german_service_names(self):
        """Test that DHL Express service names are translated to German."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        dhl_services = data.get("service_names", {}).get("dhl_express", {})
        self.assertIn("dhl_express_worldwide", dhl_services)
        self.assertEqual(
            dhl_services["dhl_express_worldwide"],
            "DHL Express Weltweit",
        )

    def test_references_capabilities_are_strings(self):
        """Test that carrier capabilities are returned as string lists."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        capabilities = data.get("carrier_capabilities", {})
        self.assertGreater(len(capabilities), 0, "No carrier capabilities returned")

        for carrier_id, caps in capabilities.items():
            self.assertIsInstance(caps, list, f"Capabilities for '{carrier_id}' is not a list")
            for cap in caps:
                self.assertIsInstance(cap, str, f"Capability for '{carrier_id}' is not a string")
                self.assertGreater(len(cap), 0, f"Empty capability for '{carrier_id}'")

    def test_references_german_connection_field_labels(self):
        """Test that connection fields include translated German labels."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        connection_fields = data.get("connection_fields", {})

        checked = 0
        for carrier_id, fields in connection_fields.items():
            for field_name, field_data in fields.items():
                self.assertIn(
                    "label",
                    field_data,
                    f"Field '{field_name}' for carrier '{carrier_id}' missing 'label'",
                )
                self.assertGreater(
                    len(field_data["label"]),
                    0,
                    f"Empty label for '{field_name}' on '{carrier_id}'",
                )
                checked += 1
        self.assertGreater(checked, 0, "No connection fields were validated")

    def test_references_german_option_labels(self):
        """Test that shipping options include translated German labels."""
        response = self.client.get("/v1/references?reduced=false&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        options = data.get("options", {})

        checked = 0
        for carrier_id, carrier_options in options.items():
            for option_code, option_data in carrier_options.items():
                self.assertIn(
                    "label",
                    option_data,
                    f"Option '{option_code}' for carrier '{carrier_id}' missing 'label'",
                )
                self.assertGreater(
                    len(option_data["label"]),
                    0,
                    f"Empty label for '{option_code}' on '{carrier_id}'",
                )
                checked += 1
        self.assertGreater(checked, 0, "No shipping options were validated")

    def test_references_invalid_lang_returns_400(self):
        """Test that an unsupported language code returns 400."""
        response = self.client.get("/v1/references?reduced=false&lang=xyz")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)
        self.assertIn("xyz", data["error"])

    def test_references_reduced_mode(self):
        """Test that reduced mode still returns translatable fields."""
        response = self.client.get("/v1/references?reduced=true&lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("carriers", data)

    def test_references_accept_language_header(self):
        """Test that Accept-Language header is used when no ?lang= param."""
        response = self.client.get(
            "/v1/references?reduced=false",
            HTTP_ACCEPT_LANGUAGE="de",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        dhl_services = data.get("service_names", {}).get("dhl_express", {})
        self.assertEqual(
            dhl_services.get("dhl_express_worldwide"),
            "DHL Express Weltweit",
        )

    def test_references_lang_param_overrides_header(self):
        """Test that ?lang= param takes priority over Accept-Language header."""
        # Request with ?lang=en but Accept-Language: de — English should win
        response_en = self.client.get(
            "/v1/references?reduced=false&lang=en",
            HTTP_ACCEPT_LANGUAGE="de",
        )
        self.assertEqual(response_en.status_code, status.HTTP_200_OK)

        # Request with Accept-Language: de (no ?lang=) — German should be used
        response_de = self.client.get(
            "/v1/references?reduced=false",
            HTTP_ACCEPT_LANGUAGE="de",
        )
        self.assertEqual(response_de.status_code, status.HTTP_200_OK)

        # DHL Express service should differ between en and de
        en_data = response_en.json()
        de_data = response_de.json()
        en_service = en_data.get("service_names", {}).get("dhl_express", {}).get("dhl_express_worldwide", "")
        de_service = de_data.get("service_names", {}).get("dhl_express", {}).get("dhl_express_worldwide", "")
        self.assertNotEqual(
            en_service,
            de_service,
            "Expected different translations when ?lang=en overrides Accept-Language: de",
        )


class TestCarriersTranslation(APITestCase):
    """Test that GET /v1/carriers returns translated values when lang is specified."""

    def setUp(self):
        self.maxDiff = None
        self.user = get_user_model().objects.create_superuser("admin@example.com", "test")
        self.token = Token.objects.create(user=self.user, test_mode=False)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_carriers_list_default(self):
        """Test that /v1/carriers returns carrier list without lang."""
        response = self.client.get("/v1/carriers")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "No carriers returned")

        carrier = data[0]
        self.assertIn("carrier_name", carrier)
        self.assertIn("shipping_options", carrier)
        self.assertIn("connection_fields", carrier)

    def test_carriers_list_with_lang(self):
        """Test that /v1/carriers?lang=de returns translated labels."""
        response = self.client.get("/v1/carriers?lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_carriers_connection_field_labels(self):
        """Test that carrier connection fields have translated labels."""
        response = self.client.get("/v1/carriers?lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        checked = 0
        for carrier in data:
            for field_name, field_data in carrier.get("connection_fields", {}).items():
                self.assertIn(
                    "label",
                    field_data,
                    f"Field '{field_name}' for '{carrier['carrier_name']}' missing 'label'",
                )
                self.assertGreater(
                    len(field_data["label"]),
                    0,
                    f"Empty label for '{field_name}' on '{carrier['carrier_name']}'",
                )
                checked += 1
        self.assertGreater(checked, 0, "No connection fields were validated")

    def test_carriers_option_labels(self):
        """Test that carrier shipping options have translated labels."""
        response = self.client.get("/v1/carriers?lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        checked = 0
        for carrier in data:
            for option_code, option_data in carrier.get("shipping_options", {}).items():
                self.assertIn(
                    "label",
                    option_data,
                    f"Option '{option_code}' for '{carrier['carrier_name']}' missing 'label'",
                )
                self.assertGreater(
                    len(option_data["label"]),
                    0,
                    f"Empty label for '{option_code}' on '{carrier['carrier_name']}'",
                )
                checked += 1
        self.assertGreater(checked, 0, "No shipping options were validated")

    def test_carriers_option_labels_no_carrier_prefix(self):
        """Test that DHL Parcel DE option labels have carrier prefix stripped."""
        response = self.client.get("/v1/carriers/dhl_parcel_de?lang=en")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        prefix = "Dhl Parcel De "
        checked = 0
        for option_code, option_data in data.get("shipping_options", {}).items():
            label = option_data.get("label", "")
            if option_code.startswith("dhl_parcel_de_"):
                self.assertFalse(
                    label.startswith(prefix),
                    f"Option label '{label}' still has carrier prefix '{prefix}'",
                )
                checked += 1
        self.assertGreater(checked, 0, "No DHL option labels were checked for prefix")

    def test_carriers_invalid_lang_returns_400(self):
        """Test that an unsupported language code returns 400."""
        response = self.client.get("/v1/carriers?lang=xyz")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)
        self.assertIn("xyz", data["error"])

    def test_carriers_detail_with_lang(self):
        """Test that /v1/carriers/<name>?lang=de returns translated details."""
        list_response = self.client.get("/v1/carriers")
        carriers = list_response.json()
        if not carriers:
            self.skipTest("No carriers available")

        carrier_name = carriers[0]["carrier_name"]
        response = self.client.get(f"/v1/carriers/{carrier_name}?lang=de")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["carrier_name"], carrier_name)

        for _field_name, field_data in data.get("connection_fields", {}).items():
            self.assertIn("label", field_data)

        for _option_code, option_data in data.get("shipping_options", {}).items():
            self.assertIn("label", option_data)

    def test_carriers_unknown_returns_404(self):
        """Test that requesting an unknown carrier returns 404."""
        response = self.client.get("/v1/carriers/nonexistent_carrier")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_carriers_accept_language_header(self):
        """Test that Accept-Language header works for /v1/carriers."""
        response = self.client.get(
            "/v1/carriers",
            HTTP_ACCEPT_LANGUAGE="de",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_carriers_detail_accept_language_header(self):
        """Test that Accept-Language header works for /v1/carriers/<name>."""
        list_response = self.client.get("/v1/carriers")
        carriers = list_response.json()
        if not carriers:
            self.skipTest("No carriers available")

        carrier_name = carriers[0]["carrier_name"]
        response = self.client.get(
            f"/v1/carriers/{carrier_name}",
            HTTP_ACCEPT_LANGUAGE="de",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["carrier_name"], carrier_name)

        for _field_name, field_data in data.get("connection_fields", {}).items():
            self.assertIn("label", field_data)
