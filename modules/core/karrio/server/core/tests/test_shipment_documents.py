"""Tests for shipment_documents_accessor decorator.

These tests verify that shipping_documents are correctly built
from label, invoice, and extra_documents (return labels, COD docs, etc.)
without requiring the full Django setup.
"""

import unittest
from unittest.mock import MagicMock


class TestShipmentDocumentsAccessor(unittest.TestCase):
    """Tests for shipment_documents_accessor decorator."""

    def setUp(self):
        from karrio.server.core.validators import shipment_documents_accessor

        self.shipment_documents_accessor = shipment_documents_accessor

    def _make_decorated_class(self, include_base64=False):
        """Create a minimal decorated class for testing."""

        class FakeSerializer:
            def to_representation(self, instance):
                return {"id": "test"}

        if include_base64:
            return self.shipment_documents_accessor(include_base64=True)(
                FakeSerializer
            )
        else:
            return self.shipment_documents_accessor(FakeSerializer)

    def _make_instance(self, **kwargs):
        """Create a mock shipment instance with given attributes."""
        instance = MagicMock()
        # Set defaults
        instance.label = None
        instance.label_type = None
        instance.label_url = None
        instance.invoice = None
        instance.invoice_url = None
        instance.extra_documents = None
        # Override with provided values
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def test_label_only(self):
        cls = self._make_decorated_class()
        serializer = cls()
        instance = self._make_instance(
            label="base64_label_content",
            label_type="PDF",
            label_url="https://example.com/label.pdf",
        )

        result = serializer.to_representation(instance)

        self.assertEqual(len(result["shipping_documents"]), 1)
        doc = result["shipping_documents"][0]
        self.assertEqual(doc["category"], "label")
        self.assertEqual(doc["format"], "PDF")
        self.assertEqual(doc["url"], "https://example.com/label.pdf")
        self.assertIsNone(doc["base64"])  # include_base64=False

    def test_label_with_base64(self):
        cls = self._make_decorated_class(include_base64=True)
        serializer = cls()
        instance = self._make_instance(
            label="base64_label_content",
            label_type="PDF",
        )

        result = serializer.to_representation(instance)

        doc = result["shipping_documents"][0]
        self.assertEqual(doc["base64"], "base64_label_content")

    def test_label_and_invoice(self):
        cls = self._make_decorated_class(include_base64=True)
        serializer = cls()
        instance = self._make_instance(
            label="base64_label",
            label_type="ZPL",
            invoice="base64_invoice",
            invoice_url="https://example.com/invoice.pdf",
        )

        result = serializer.to_representation(instance)

        self.assertEqual(len(result["shipping_documents"]), 2)
        self.assertEqual(result["shipping_documents"][0]["category"], "label")
        self.assertEqual(result["shipping_documents"][0]["format"], "ZPL")
        self.assertEqual(result["shipping_documents"][1]["category"], "invoice")
        self.assertEqual(result["shipping_documents"][1]["base64"], "base64_invoice")

    def test_label_with_return_label_extra_document(self):
        """Verify return label from extra_documents appears in shipping_documents."""
        cls = self._make_decorated_class(include_base64=True)
        serializer = cls()
        instance = self._make_instance(
            label="base64_label",
            label_type="PDF",
            extra_documents=[
                {
                    "category": "return_label",
                    "format": "PDF",
                    "base64": "base64_return_label",
                    "print_format": "910-300-710",
                    "url": None,
                }
            ],
        )

        result = serializer.to_representation(instance)

        self.assertEqual(len(result["shipping_documents"]), 2)
        label_doc = result["shipping_documents"][0]
        return_doc = result["shipping_documents"][1]

        self.assertEqual(label_doc["category"], "label")
        self.assertEqual(return_doc["category"], "return_label")
        self.assertEqual(return_doc["format"], "PDF")
        self.assertEqual(return_doc["base64"], "base64_return_label")

    def test_extra_documents_without_base64_flag(self):
        """Extra documents base64 should be None when include_base64=False."""
        cls = self._make_decorated_class(include_base64=False)
        serializer = cls()
        instance = self._make_instance(
            label="base64_label",
            label_type="PDF",
            extra_documents=[
                {
                    "category": "return_label",
                    "format": "PDF",
                    "base64": "base64_return_label",
                }
            ],
        )

        result = serializer.to_representation(instance)

        return_doc = result["shipping_documents"][1]
        self.assertEqual(return_doc["category"], "return_label")
        self.assertIsNone(return_doc["base64"])

    def test_multiple_extra_documents(self):
        """Verify both return_label and cod_document appear in shipping_documents."""
        cls = self._make_decorated_class(include_base64=True)
        serializer = cls()
        instance = self._make_instance(
            label="base64_label",
            label_type="PDF",
            invoice="base64_invoice",
            extra_documents=[
                {
                    "category": "return_label",
                    "format": "PDF",
                    "base64": "base64_return",
                },
                {
                    "category": "cod_document",
                    "format": "PDF",
                    "base64": "base64_cod",
                },
            ],
        )

        result = serializer.to_representation(instance)

        self.assertEqual(len(result["shipping_documents"]), 4)
        categories = [d["category"] for d in result["shipping_documents"]]
        self.assertEqual(categories, ["label", "invoice", "return_label", "cod_document"])

    def test_empty_extra_documents(self):
        cls = self._make_decorated_class()
        serializer = cls()
        instance = self._make_instance(
            label="base64_label",
            label_type="PDF",
            extra_documents=[],
        )

        result = serializer.to_representation(instance)

        self.assertEqual(len(result["shipping_documents"]), 1)
        self.assertEqual(result["shipping_documents"][0]["category"], "label")

    def test_no_documents(self):
        cls = self._make_decorated_class()
        serializer = cls()
        instance = self._make_instance()

        result = serializer.to_representation(instance)

        self.assertEqual(result["shipping_documents"], [])


if __name__ == "__main__":
    unittest.main()
