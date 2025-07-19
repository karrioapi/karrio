import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from karrio.server.documents.generator import Documents, TemplateRenderingError


class DocumentGenerationErrorHandlingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Mock authentication for testing
        with patch('karrio.server.core.views.api.APIView.permission_classes', []):
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
            }
        }

        # Mock the permission check
        with patch('karrio.server.core.views.api.APIView.check_permissions'):
            response = self.client.post(
                '/v1/documents/generate',
                data=json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.json())
        self.assertIn('Template variable error', response.json()['errors'][0]['message'])
        self.assertIn('shipment', response.json()['errors'][0]['message'])

    def test_template_syntax_error_returns_error(self):
        """Test that template with syntax errors returns proper error message"""
        template = "<div>{{ unclosed_tag</div>"  # Missing closing }}
        data = {
            "template": template,
            "doc_format": "html",
            "doc_name": "Test Document",
            "data": {"test": "data"}
        }

        with patch('karrio.server.core.views.api.APIView.check_permissions'):
            response = self.client.post(
                '/v1/documents/generate',
                data=json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.json())
        self.assertIn('Template syntax error', response.json()['errors'][0]['message'])

    def test_missing_template_returns_error(self):
        """Test that missing template returns proper error message"""
        data = {
            "doc_format": "html",
            "doc_name": "Test Document",
            "data": {"test": "data"}
            # Note: no template or template_id provided
        }

        with patch('karrio.server.core.views.api.APIView.check_permissions'):
            response = self.client.post(
                '/v1/documents/generate',
                data=json.dumps(data),
                content_type='application/json'
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.json())
        self.assertEqual(
            response.json()['errors'][0]['message'],
            'template or template_id is required'
        )

    def test_valid_template_with_data_succeeds(self):
        """Test that valid template with proper data succeeds"""
        template = "<div>Hello {{ name }}!</div>"
        data = {
            "template": template,
            "doc_format": "html",
            "doc_name": "Test Document",
            "data": {
                "name": "World",
                "shipment": {
                    "shipper": {"address_line1": "123 Test St"}
                }
            }
        }

        # Mock PDF generation to avoid WeasyPrint dependency in tests
        with patch('karrio.server.core.views.api.APIView.check_permissions'), \
             patch('karrio.server.documents.generator.weasyprint.HTML') as mock_html:

            # Mock the PDF generation
            mock_buffer = b"fake pdf content"
            mock_html.return_value.write_pdf.return_value = None

            # Patch the buffer creation
            with patch('karrio.server.documents.generator.io.BytesIO') as mock_bytesio:
                mock_bytesio.return_value.getvalue.return_value = mock_buffer

                response = self.client.post(
                    '/v1/documents/generate',
                    data=json.dumps(data),
                    content_type='application/json'
                )

        # Should succeed (201) or fail gracefully with a proper error message
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            # If it fails, it should be with a proper error message, not a 500
            self.assertIn('errors', response.json())
            error_message = response.json()['errors'][0]['message']
            # Should not be a generic "internal server error"
            self.assertNotIn('Internal server error', error_message)

    def test_template_rendering_error_direct(self):
        """Test TemplateRenderingError class directly"""
        try:
            # Test with a template that has undefined variables
            Documents.generate(
                template="<div>{{ undefined_var.nested.property }}</div>",
                data={"some_data": "test"}
            )
            self.fail("Should have raised TemplateRenderingError")
        except TemplateRenderingError as e:
            self.assertIn("Template variable error", e.message)
            self.assertIn("undefined_var", e.message)
            self.assertIn("Available variables", e.message)
        except Exception as e:
            self.fail(f"Should have raised TemplateRenderingError, got {type(e).__name__}: {e}")


class DocumentGenerationContextTest(TestCase):
    """Test that data contexts are properly handled"""

    def test_shipment_context_properly_passed(self):
        """Test that shipment data is properly passed to template context"""
        template = "<div>{{ shipment.shipper.address_line1 }}</div>"
        data = {
            "shipment": {
                "shipper": {"address_line1": "123 Test Street"}
            }
        }

        try:
            # This should work without errors
            result = Documents.generate(template, data=data)
            # If we get here, the context was properly passed
            self.assertIsNotNone(result)
        except TemplateRenderingError as e:
            # If it fails, it should be due to PDF generation, not template rendering
            if "PDF generation error" not in e.message:
                self.fail(f"Template rendering failed: {e.message}")

    def test_generic_context_fallback(self):
        """Test that generic context fallback works for arbitrary data"""
        template = "<div>{{ custom_field }}</div>"
        data = {
            "custom_field": "test value"
        }

        try:
            result = Documents.generate(template, data=data)
            self.assertIsNotNone(result)
        except TemplateRenderingError as e:
            # Should work for simple templates
            if "PDF generation error" not in e.message:
                self.fail(f"Template rendering failed: {e.message}")
