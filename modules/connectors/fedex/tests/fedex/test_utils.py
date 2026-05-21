import unittest
from unittest import mock

import karrio.providers.fedex.utils as provider_utils


class TestFedExBuildCustomerReference(unittest.TestCase):
    def test_returns_none_for_none_value(self):
        result = provider_utils.build_customer_reference("CUSTOMER_REFERENCE", None)
        self.assertIsNone(result)

    def test_returns_none_for_empty_string(self):
        result = provider_utils.build_customer_reference("CUSTOMER_REFERENCE", "")
        self.assertIsNone(result)

    def test_returns_reference_for_valid_value(self):
        result = provider_utils.build_customer_reference("CUSTOMER_REFERENCE", "Ref-123")
        self.assertIsNotNone(result)
        self.assertEqual(result.customerReferenceType, "CUSTOMER_REFERENCE")
        self.assertEqual(result.value, "Ref-123")

    def test_truncates_customer_reference_to_30_chars(self):
        result = provider_utils.build_customer_reference("CUSTOMER_REFERENCE", "X" * 35)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.value), 30)

    def test_truncates_rma_association_to_20_chars(self):
        result = provider_utils.build_customer_reference("RMA_ASSOCIATION", "R" * 25)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.value), 20)

    def test_preserves_value_at_exact_max_length(self):
        exact_value = "X" * 30
        result = provider_utils.build_customer_reference("CUSTOMER_REFERENCE", exact_value)
        self.assertIsNotNone(result)
        self.assertEqual(result.value, exact_value)

    def test_preserves_value_under_max_length(self):
        result = provider_utils.build_customer_reference("DEPARTMENT_NUMBER", "DEPT-001")
        self.assertIsNotNone(result)
        self.assertEqual(result.value, "DEPT-001")


class TestFedExCollectCustomerReferences(unittest.TestCase):
    def _make_payload(self, reference=None, options=None):
        payload = mock.MagicMock()
        payload.reference = reference
        payload.options = options or {}
        return payload

    def _make_customs(self, invoice=None):
        customs = mock.MagicMock()
        customs.invoice = invoice
        return customs

    def _make_options(self, invoice_number=None):
        options = mock.MagicMock()
        options.invoice_number.state = invoice_number
        return options

    def test_returns_commercial_invoice_and_package_keys(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(),
            self._make_customs(),
            self._make_options(),
        )
        self.assertIn("commercial_invoice", result)
        self.assertIn("package", result)

    def test_empty_references_excluded_when_no_data(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(reference=None),
            self._make_customs(invoice=None),
            self._make_options(invoice_number=None),
        )
        self.assertEqual(result["commercial_invoice"], [])
        self.assertEqual(result["package"], [])

    def test_invoice_number_in_commercial_invoice_from_customs(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(),
            self._make_customs(invoice="INV-123"),
            self._make_options(),
        )
        values = {r.customerReferenceType: r.value for r in result["commercial_invoice"]}
        self.assertIn("INVOICE_NUMBER", values)
        self.assertEqual(values["INVOICE_NUMBER"], "INV-123")

    def test_invoice_number_falls_back_to_options(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(),
            self._make_customs(invoice=None),
            self._make_options(invoice_number="OPT-INV-789"),
        )
        values = {r.customerReferenceType: r.value for r in result["commercial_invoice"]}
        self.assertIn("INVOICE_NUMBER", values)
        self.assertEqual(values["INVOICE_NUMBER"], "OPT-INV-789")

    def test_customs_invoice_takes_priority_over_options(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(),
            self._make_customs(invoice="CUSTOMS-INV"),
            self._make_options(invoice_number="OPT-INV"),
        )
        values = {r.customerReferenceType: r.value for r in result["commercial_invoice"]}
        self.assertEqual(values["INVOICE_NUMBER"], "CUSTOMS-INV")

    def test_customer_reference_in_package_from_payload(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(reference="#MyOrder"),
            self._make_customs(),
            self._make_options(),
        )
        types = [r.customerReferenceType for r in result["package"]]
        self.assertIn("CUSTOMER_REFERENCE", types)

    def test_package_reference_number_is_ignored_for_po_number(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(),
            self._make_customs(),
            self._make_options(),
        )
        types = [r.customerReferenceType for r in result["package"]]
        self.assertNotIn("P_O_NUMBER", types)

    def test_po_number_falls_back_to_options(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(options={"fedex_po_number": "OPT-PO-999"}),
            self._make_customs(),
            self._make_options(),
        )
        values = {r.customerReferenceType: r.value for r in result["package"]}
        self.assertIn("P_O_NUMBER", values)
        self.assertEqual(values["P_O_NUMBER"], "OPT-PO-999")

    def test_invoice_number_excluded_from_package_references(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(),
            self._make_customs(invoice="INV-123"),
            self._make_options(),
        )
        package_types = [r.customerReferenceType for r in result["package"]]
        self.assertNotIn("INVOICE_NUMBER", package_types)

    def test_customer_reference_appears_in_both_commercial_and_package(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(reference="#SharedRef"),
            self._make_customs(),
            self._make_options(),
        )
        commercial_types = [r.customerReferenceType for r in result["commercial_invoice"]]
        package_types = [r.customerReferenceType for r in result["package"]]
        self.assertIn("CUSTOMER_REFERENCE", commercial_types)
        self.assertIn("CUSTOMER_REFERENCE", package_types)

    def test_rma_association_in_package_from_options(self):
        result = provider_utils.collect_customer_references(
            self._make_payload(options={"fedex_rma_association": "RMA-001"}),
            self._make_customs(),
            self._make_options(),
        )
        values = {r.customerReferenceType: r.value for r in result["package"]}
        self.assertIn("RMA_ASSOCIATION", values)
        self.assertEqual(values["RMA_ASSOCIATION"], "RMA-001")


if __name__ == "__main__":
    unittest.main()
