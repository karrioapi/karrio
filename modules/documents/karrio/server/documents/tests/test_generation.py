import json
from unittest.mock import patch

from django.test import TestCase
from karrio.server.documents.generator import Documents, TemplateRenderingError
from karrio.server.settings.constance import DEFAULT_COMMERCIAL_INVOICE_TEMPLATE
from rest_framework import status
from rest_framework.test import APIClient


class DocumentGenerationErrorHandlingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Mock authentication for testing
        with patch("karrio.server.core.views.api.APIView.permission_classes", []):
            pass

    def test_template_with_undefined_variable_returns_error(self):
        """Test that template with undefined variables returns proper error message"""
        template = "<div>{{ shipment.shipper.address_line1 }}</div>"
        data = {
            "template": template,
            "doc_format": "html",
            "doc_name": "Test Document",
            "data": {
                "object": {"id": "test123"},
                # Note: no shipment data provided, so shipment.shipper.address_line1 will be undefined
            },
        }

        # Mock the permission check
        with patch("karrio.server.core.views.api.APIView.check_permissions"):
            response = self.client.post(
                "/v1/documents/generate", data=json.dumps(data), content_type="application/json"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.json())
        self.assertIn("Template variable error", response.json()["errors"][0]["message"])
        self.assertIn("shipment", response.json()["errors"][0]["message"])

    def test_template_syntax_error_returns_error(self):
        """Test that template with syntax errors returns proper error message"""
        template = "<div>{{ unclosed_tag</div>"  # Missing closing }}
        data = {"template": template, "doc_format": "html", "doc_name": "Test Document", "data": {"test": "data"}}

        with patch("karrio.server.core.views.api.APIView.check_permissions"):
            response = self.client.post(
                "/v1/documents/generate", data=json.dumps(data), content_type="application/json"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.json())
        self.assertIn("Template syntax error", response.json()["errors"][0]["message"])

    def test_missing_template_returns_error(self):
        """Test that missing template returns proper error message"""
        data = {
            "doc_format": "html",
            "doc_name": "Test Document",
            "data": {"test": "data"},
            # Note: no template or template_id provided
        }

        with patch("karrio.server.core.views.api.APIView.check_permissions"):
            response = self.client.post(
                "/v1/documents/generate", data=json.dumps(data), content_type="application/json"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.json())
        self.assertEqual(response.json()["errors"][0]["message"], "template or template_id is required")

    def test_template_rendering_error_direct(self):
        """Test TemplateRenderingError class directly"""
        try:
            # Test with a template that has undefined variables
            Documents.generate(template="<div>{{ undefined_var.nested.property }}</div>", data={"some_data": "test"})
            self.fail("Should have raised TemplateRenderingError")
        except TemplateRenderingError as e:
            self.assertIn("Template variable error", e.message)
            self.assertIn("undefined_var", e.message)
            self.assertIn("Available variables", e.message)
        except Exception as e:
            self.fail(f"Should have raised TemplateRenderingError, got {type(e).__name__}: {e}")


class DocumentGenerationContextTest(TestCase):
    """Test that data contexts are properly handled"""

    def test_generic_context_fallback(self):
        """Test that generic context fallback works for arbitrary data"""
        template = "<div>{{ custom_field }}</div>"
        data = {"custom_field": "test value"}

        try:
            result = Documents.generate(template, data=data)
            self.assertIsNotNone(result)
        except TemplateRenderingError as e:
            # Should work for simple templates
            if "PDF generation error" not in e.message:
                self.fail(f"Template rendering failed: {e.message}")

    def test_inline_shipment_context_renders_single_page(self):
        """An inline template with related_object='shipment' + a provided
        shipments_context must render that context directly (exposing
        `shipment` as a top-level variable) and must NOT append the generic
        fallback page that would otherwise raise on `shipment`."""
        template = "<div>{{ shipment.tracking_number }} - {{ shipment.shipper.city }}</div>"
        data = {
            "shipments_context": [
                {
                    "shipment": {"tracking_number": "TRK123", "shipper": {"city": "Berlin"}},
                    "line_items": [],
                    "carrier": {},
                    "orders": [],
                }
            ]
        }

        with patch("karrio.server.documents.generator.weasyprint.HTML") as mock_html:
            Documents.generate(template, data=data, related_object="shipment")

            # Exactly one page rendered (no generic fallback context appended).
            self.assertEqual(mock_html.call_count, 1)
            rendered = mock_html.call_args.kwargs["string"]
            self.assertIn("TRK123 - Berlin", rendered)

    def test_inline_shipment_context_without_related_object_appends_generic(self):
        """Regression guard: WITHOUT related_object, the generic fallback page is
        appended and a shipment template raises an undefined-variable error.
        This is exactly why the admin preview passes related_object='shipment'."""
        template = "<div>{{ shipment.tracking_number }}</div>"
        data = {
            "shipments_context": [
                {"shipment": {"tracking_number": "TRK123"}, "line_items": [], "carrier": {}, "orders": []}
            ]
        }

        with self.assertRaises(TemplateRenderingError) as ctx:
            Documents.generate(template, data=data)  # related_object defaults to None

        self.assertIn("Template variable error", ctx.exception.message)

    def test_default_invoice_template_renders_multipage_multipackage(self):
        """The default commercial-invoice template must render a large multi-item
        (15 commodities), multi-piece (3 parcels) shipment: every line item is
        emitted, identity fields (Tax ID / VAT / EORI) surface, and the totals
        reflect the package count and summed parcel weight."""
        commodities = [
            {
                "title": f"Industrial Component {i}",
                "description": f"Precision machined part series {i}",
                "hs_code": f"84{i:02d}900000",
                "sku": f"PART-{i:04d}-SS",
                "quantity": (i % 4) + 1,
                "value_amount": round(19.5 * i, 2),
                "value_currency": "EUR",
                "origin_country": "DE" if i % 2 else "IT",
            }
            for i in range(1, 16)
        ]
        parcels = [
            {"weight": 4.2, "weight_unit": "KG"},
            {"weight": 3.8, "weight_unit": "KG"},
            {"weight": 5.1, "weight_unit": "KG"},
        ]
        data = {
            "shipments_context": [
                {
                    "shipment": {
                        "tracking_number": "JJD000390007310899999",
                        "service": "dhl_parcel_de_europaket",
                        "shipper": {
                            "company_name": "JTL Outfitters GmbH",
                            "city": "Düsseldorf",
                            "country_code": "DE",
                            "federal_tax_id": "DE811234567",
                        },
                        "recipient": {
                            "company_name": "COFIEM Electronics SARL",
                            "city": "Trévoux",
                            "country_code": "FR",
                            "federal_tax_id": "FR62381834050",
                        },
                        "customs": {
                            "incoterm": "DDP",
                            "content_type": "merchandise",
                            "options": {
                                "vat_registration_number": "DE811234567",
                                "eori_number": "DE123456789012345",
                            },
                            "commodities": commodities,
                        },
                        "options": {"currency": "EUR"},
                        "parcels": parcels,
                    },
                    "line_items": [],
                    "carrier": {},
                    "orders": [],
                }
            ]
        }

        with patch("karrio.server.documents.generator.weasyprint.HTML") as mock_html:
            Documents.generate(DEFAULT_COMMERCIAL_INVOICE_TEMPLATE, data=data, related_object="shipment")

        rendered = mock_html.call_args.kwargs["string"]

        # Every one of the 15 line items is emitted (by SKU).
        for i in range(1, 16):
            self.assertIn(f"PART-{i:04d}-SS", rendered)

        # Identity fields surface when present.
        self.assertIn("DE811234567", rendered)  # shipper tax id / VAT
        self.assertIn("DE123456789012345", rendered)  # EORI
        self.assertIn("FR62381834050", rendered)  # consignee tax id

        # Multi-piece totals: 3 packages and the summed parcel weight (13.10 KG).
        expected_subtotal = sum((i % 4 + 1) * round(19.5 * i, 2) for i in range(1, 16))
        self.assertIn("Total Packages", rendered)
        self.assertIn("13.10 KG", rendered)
        self.assertIn(f"{expected_subtotal:.2f} EUR", rendered)
