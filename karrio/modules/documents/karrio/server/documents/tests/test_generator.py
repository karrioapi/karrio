import json
import base64
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
from karrio.server.documents.models import DocumentTemplate
import karrio.server.manager.models as manager_models
import karrio.server.orders.models as order_models


class TestDocumentGenerator(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.template = DocumentTemplate.objects.create(
            **{
                "name": "Test Generator Template",
                "slug": "test_generator",
                "template": SIMPLE_HTML_TEMPLATE,
                "description": "A test template for generation",
                "related_object": "shipment",
                "metadata": {"doc_type": "invoice"},
                "options": {"page_size": "A4"},
                "created_by": self.user,
            }
        )

    def test_generate_document_with_template_id(self):
        """Test document generation using template_id"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template_id": self.template.id,
            "data": {
                "title": "Test Invoice",
                "shipment": {
                    "tracking_number": "TEST123456",
                    "service": "Standard",
                    "status": "delivered",
                },
            },
            "doc_name": "test_invoice.pdf",
            "doc_format": "PDF",
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        # Debug information if test fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")
            print(f"Response data: {response_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)
        self.assertEqual(response_data["doc_name"], "test_invoice.pdf")
        self.assertEqual(response_data["doc_format"], "PDF")

        # Verify the doc_file is a valid base64 string
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b'%PDF'))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")

    def test_generate_document_with_inline_template(self):
        """Test document generation using inline template"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template": SIMPLE_HTML_TEMPLATE,
            "data": {
                "title": "Inline Template Test",
                "order": {
                    "order_id": "ORD-001",
                    "order_date": "2023-12-01",
                },
            },
            "doc_name": "inline_test.pdf",
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        # Debug information if test fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")
            print(f"Response data: {response_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)
        self.assertEqual(response_data["doc_name"], "inline_test.pdf")

        # Verify the doc_file is a valid base64 string and PDF
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b'%PDF'))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")

    def test_generate_document_missing_template(self):
        """Test error when neither template nor template_id is provided"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "data": {"title": "No Template Test"},
            "doc_name": "no_template.pdf",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("template or template_id is required", str(response.content))

    def test_generate_document_with_metadata_and_options(self):
        """Test document generation with metadata and options"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template_id": self.template.id,
            "data": {
                "title": "Metadata Test",
                "shipment": {"tracking_number": "META123"},
            },
            "options": {
                "prefetch": {
                    "current_date": "{{ utils.datetime.now().strftime('%Y-%m-%d') }}",
                    "tracking_url": "https://track.example.com/{{ shipment.tracking_number }}",
                }
            },
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        # Debug information if test fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")
            print(f"Response data: {response_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)

        # Verify the doc_file is a valid base64 string and PDF
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b'%PDF'))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")


class TestDocumentPrinters(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.template = DocumentTemplate.objects.create(
            **{
                "name": "Printer Test Template",
                "slug": "printer_test",
                "template": SIMPLE_HTML_TEMPLATE,
                "description": "A test template for printing",
                "related_object": "shipment",
                "created_by": self.user,
            }
        )

    def test_template_docs_printer(self):
        """Test template document printing endpoint"""
        url = f"/documents/templates/{self.template.id}.{self.template.slug}"
        response = self.client.get(url, {"title": "Printed Document"})

        # Debug information if test fails
        if response.status_code != status.HTTP_200_OK:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response["Content-Type"].startswith("application/pdf"))

        # Verify we got a valid PDF - handle streaming content
        if hasattr(response, 'streaming_content'):
            content = b''.join(response.streaming_content)
        else:
            content = response.content
        self.assertGreater(len(content), 0)
        self.assertTrue(content.startswith(b'%PDF'))

    def test_template_docs_printer_with_download(self):
        """Test template document printing with download flag"""
        url = f"/documents/templates/{self.template.id}.{self.template.slug}"
        response = self.client.get(url, {"download": "true", "title": "Download Test"})

        # Debug information if test fails
        if response.status_code != status.HTTP_200_OK:
            print(f"Response status: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"Response content: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attachment", response.get("Content-Disposition", ""))

        # Verify we got a valid PDF - handle streaming content
        if hasattr(response, 'streaming_content'):
            content = b''.join(response.streaming_content)
        else:
            content = response.content
        self.assertGreater(len(content), 0)
        self.assertTrue(content.startswith(b'%PDF'))


class TestDocumentGeneratorIntegration(APITestCase):
    """Integration tests for the document generator with real data"""

    def setUp(self) -> None:
        super().setUp()
        self.invoice_template = DocumentTemplate.objects.create(
            **{
                "name": "Invoice Template",
                "slug": "invoice",
                "template": INVOICE_HTML_TEMPLATE,
                "description": "Invoice template for testing",
                "related_object": "shipment",
                "metadata": {"doc_type": "commercial_invoice"},
                "created_by": self.user,
            }
        )

    def test_shipment_context_generation(self):
        """Test document generation with shipment context"""
        # Create address instances
        recipient = manager_models.Address.objects.create(
            person_name="John Doe",
            address_line1="123 Main St",
            city="Test City",
            country_code="CA",
            postal_code="12345",
            created_by=self.user,
        )

        shipper = manager_models.Address.objects.create(
            person_name="Shipper Inc",
            address_line1="456 Business Ave",
            city="Ship City",
            country_code="CA",
            postal_code="67890",
            created_by=self.user,
        )

        # Create a test shipment
        shipment = manager_models.Shipment.objects.create(
            recipient=recipient,
            shipper=shipper,
            test_mode=True,
            status="shipped",
            tracking_number="TRACK123456",
            selected_rate={
                "service": "express",
                "carrier_id": "test_carrier",
                "carrier_name": "Test Carrier",
                "currency": "USD",
                "total_charge": 10.00,
                "test_mode": True,
            },
            created_by=self.user,
        )

        # Create and set parcels
        parcel = manager_models.Parcel.objects.create(
            weight=2.5,
            weight_unit="KG",
            dimension_unit="CM",
            width=20,
            height=15,
            length=30,
            created_by=self.user,
        )
        shipment.parcels.set([parcel])

        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template_id": self.invoice_template.id,
            "data": {"shipments": str(shipment.id)},
            "doc_name": "shipment_invoice.pdf",
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        # Debug information if test fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")
            print(f"Response data: {response_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)
        self.assertEqual(response_data["doc_name"], "shipment_invoice.pdf")

        # Verify the doc_file is a valid base64 string and PDF
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b'%PDF'))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")


# Test Data and Fixtures
SIMPLE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title | default('Simple Test Document') }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .content { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title | default('Simple Test Document') }}</h1>
    </div>

    <div class="content">
        {% if shipment %}
        <p><strong>Tracking Number:</strong> {{ shipment.tracking_number }}</p>
        <p><strong>Service:</strong> {{ shipment.service }}</p>
        <p><strong>Status:</strong> {{ shipment.status }}</p>
        {% endif %}

        {% if order %}
        <p><strong>Order ID:</strong> {{ order.order_id }}</p>
        <p><strong>Order Date:</strong> {{ order.order_date }}</p>
        {% endif %}

        <p>Generated at: {{ utils.datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}</p>
    </div>
</body>
</html>
"""

INVOICE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Commercial Invoice</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .addresses { display: table; width: 100%; margin-bottom: 30px; }
        .address { display: table-cell; width: 50%; vertical-align: top; padding: 10px; }
        .invoice-details { margin-bottom: 30px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total { text-align: right; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>COMMERCIAL INVOICE</h1>
        {% if metadata and metadata.doc_type %}
        <p>Document Type: {{ metadata.doc_type }}</p>
        {% endif %}
    </div>

    <div class="addresses">
        {% if shipment %}
        <div class="address">
            <h3>Ship From:</h3>
            <p>{{ shipment.shipper.person_name or shipment.shipper.company_name }}</p>
            <p>{{ shipment.shipper.address_line1 }}</p>
            {% if shipment.shipper.address_line2 %}
            <p>{{ shipment.shipper.address_line2 }}</p>
            {% endif %}
            <p>{{ shipment.shipper.city }}, {{ shipment.shipper.state_code }} {{ shipment.shipper.postal_code }}</p>
            <p>{{ shipment.shipper.country_code }}</p>
        </div>

        <div class="address">
            <h3>Ship To:</h3>
            <p>{{ shipment.recipient.person_name or shipment.recipient.company_name }}</p>
            <p>{{ shipment.recipient.address_line1 }}</p>
            {% if shipment.recipient.address_line2 %}
            <p>{{ shipment.recipient.address_line2 }}</p>
            {% endif %}
            <p>{{ shipment.recipient.city }}, {{ shipment.recipient.state_code }} {{ shipment.recipient.postal_code }}</p>
            <p>{{ shipment.recipient.country_code }}</p>
        </div>
        {% endif %}
    </div>

    {% if shipment %}
    <div class="invoice-details">
        <table>
            <tr>
                <th>Tracking Number</th>
                <td>{{ shipment.tracking_number }}</td>
                <th>Service</th>
                <td>{{ shipment.service }}</td>
            </tr>
            <tr>
                <th>Status</th>
                <td>{{ shipment.status }}</td>
                <th>Created Date</th>
                <td>{{ shipment.created_at }}</td>
            </tr>
        </table>
    </div>
    {% endif %}

    {% if line_items %}
    <h3>Items</h3>
    <table>
        <thead>
            <tr>
                <th>SKU</th>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in line_items %}
            <tr>
                <td>{{ item.sku }}</td>
                <td>{{ item.title }}</td>
                <td>{{ item.quantity }}</td>
                <td>${{ "%.2f"|format(item.unit_price|float) }}</td>
                <td>${{ "%.2f"|format((item.unit_price|float) * (item.quantity|int)) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endif %}

    <p style="text-align: center; margin-top: 40px;">
        Generated by Karrio on {{ utils.datetime.now().strftime('%Y-%m-%d') }}
    </p>
</body>
</html>
"""

# Sample base64 encoded PDF (minimal valid PDF)
SAMPLE_PDF_BASE64 = "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPD4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQo+PgplbmRvYmoKeHJlZgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmCjAwMDAwMDAwMDkgMDAwMDAgbgowMDAwMDAwMDU4IDAwMDAwIG4KMDAwMDAwMDExNSAwMDAwMCBuCnRyYWlsZXIKPDwKL1NpemUgNAovUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKMTc4CiUlRU9G"

# Sample base64 encoded ZIP file (for testing multi-document bundling)
SAMPLE_ZIP_BASE64 = """UEsDBBQAAAAIAKOOdU8e6yR4HQAAAB8AAAANAAAAdGVzdC1kb2MxLnBkZitIQ1BQ0KdJI5tT37IM5rK/ZIHYsyeCOYhNnwKNOkKjDqN9rCE9C/qzlvggwAEw2TnZ+UpJOZn5eUrJOcY5QCOjkWRzQpOy"""
