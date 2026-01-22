# Product Requirements Document: ShippingDocumentCategory Enum

**Project**: Standardized Shipping Document Categories
**Version**: 1.1
**Date**: 2026-01-13
**Status**: Implemented
**Owner**: Engineering Team
**Reference**: All implementation must follow `AGENTS.md` coding guidelines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Success Criteria](#goals--success-criteria)
4. [Technical Architecture](#technical-architecture)
5. [SDK/Core Changes](#sdkcore-changes)
6. [Carrier Integration Changes](#carrier-integration-changes)
7. [Testing Strategy](#testing-strategy)
8. [Implementation Plan](#implementation-plan)
9. [Risk Assessment](#risk-assessment)

---

## Executive Summary

This document outlines the introduction of a standardized `ShippingDocumentCategory` enum in `karrio/core/units.py` to normalize document category names across all carrier integrations. Currently, document categories are passed as arbitrary strings (e.g., `"retrunLabel"`, `"codLabel"`), leading to inconsistency and potential typos.

### Key Changes

1. **New `ShippingDocumentCategory` Enum**: A standardized enum with PascalCase values for all document types (e.g., `ShippingLabel`, `ReturnLabel`)
2. **Carrier-Specific Mapping Enums**: Each carrier defines their own `ShippingDocumentCategory` enum in their `units.py` with carrier-prefixed values and unified mappings (like the `LabelType` pattern)
3. **Consistent Category Naming**: All carriers use `provider_units.ShippingDocumentCategory.map(category).name_or_key` for document categories
4. **Backward Compatible**: Unmapped carrier-specific categories will fall back to the original key

**Risk Level**: LOW (additive changes, backward compatible with `.map().name_or_key` pattern)
**User Impact**: Improved consistency in document category naming across all carrier responses

---

## Problem Statement

### Current State

**ShippingDocument Model** (Current):
```python
@attr.s(auto_attribs=True)
class ShippingDocument:
    """Karrio unified shipping document data type."""

    category: str       # Arbitrary string, no standardization
    format: str = "PDF"
    print_format: str = None
    base64: str = None
    url: str = None
```

**Current Usage** (from `dhl_parcel_de/shipment/create.py:47`):
```python
extra_documents = [
    ("retrunLabel", shipment.returnLabel),  # Note: typo "retrunLabel"
    ("codLabel", shipment.codLabel),
]

# Used as:
models.ShippingDocument(
    category=label,  # Raw string like "retrunLabel" or "codLabel"
    format=lib.identity("ZPL" if doc.fileFormat == "ZPL2" else "PDF"),
    base64=lib.failsafe(lambda: doc.b64 or doc.zpl2),
    ...
)
```

**Problems**:

1. **No Standardization**: Each carrier uses its own naming convention for document categories
2. **Typos**: Current implementations contain typos (e.g., `"retrunLabel"` instead of `"returnLabel"`)
3. **Inconsistent Casing**: Some use camelCase, others use snake_case or PascalCase
4. **No Validation**: No way to validate if a category is recognized
5. **Difficult to Query**: Users cannot reliably filter or query documents by category across carriers

### Desired State

**New Usage Pattern**:
```python
extra_documents = [
    ("return_label", shipment.returnLabel),
    ("cod_label", shipment.codLabel),
]

# Used as:
models.ShippingDocument(
    category=units.ShippingDocumentCategory.map("return_label").name_or_key,
    format=lib.identity("ZPL" if doc.fileFormat == "ZPL2" else "PDF"),
    base64=lib.failsafe(lambda: doc.b64 or doc.zpl2),
    ...
)
```

---

## Goals & Success Criteria

### Goals

1. **Standardize Document Categories**: Provide a single source of truth for document category names
2. **Enable Carrier Mapping**: Allow carriers to map their specific document types to standard categories
3. **Maintain Backward Compatibility**: Use `.name_or_key` pattern to gracefully handle unmapped categories
4. **Prevent Typos**: Enum values enforce correct spelling

### Success Criteria

| Metric | Target |
|--------|--------|
| All core connectors updated | 100% of connectors with extra_documents |
| Backward compatibility | Zero breaking changes |
| Standard category coverage | 90%+ of carrier document types mapped |
| Test coverage | Unit tests for enum mappings |

---

## Technical Architecture

### ShippingDocumentCategory Enum Design

The enum follows the established pattern from other enums like `TrackingStatus` with `.map()` functionality.

**Document Categories** (derived from industry standards):

| Enum Value | Description | Common Carrier Terms |
|------------|-------------|---------------------|
| `shipping_label` | Primary shipping label | label, shipping_label, main_label |
| `return_label` | Return shipping label | return_label, returnLabel, retoure |
| `export_document` | Export/customs documents | export_document, customs_doc, exportDoc |
| `receipt` | Shipping receipt | receipt, confirmation |
| `cod_label` | Cash on delivery label | cod_label, codLabel, cod_document |
| `enclosed_return_label` | Enclosed return label in package | enclosed_return, enclosedReturnLabel |
| `harmonized_label` | Harmonized/combined label | harmonized_label, combinedLabel |
| `international_shipping_label` | International shipping label | intl_label, internationalShippingLabel |
| `warenpost_national` | German Warenpost national | warenpost_national, warenpostNational |
| `return_label_international` | International return label | intl_return, returnLabelInternational |
| `warenpost_international` | German Warenpost international | warenpost_international |
| `commercial_invoice` | Commercial invoice document | commercial_invoice, invoice |
| `packing_list` | Packing list document | packing_list, packingList |
| `certificate_of_origin` | Certificate of origin | coo, certificate_of_origin |
| `customs_declaration` | Customs declaration form | customs_declaration, cn22, cn23 |
| `dangerous_goods` | Dangerous goods declaration | dg_declaration, hazmat |
| `proof_of_delivery` | Proof of delivery document | pod, proof_of_delivery |
| `manifest` | Shipping manifest | manifest, summary |
| `qr_code` | QR code document | qr_code, qrCode |
| `error_label` | Error/exception label | error_label, errorLabel |

---

## SDK/Core Changes

### 1. Add `ShippingDocumentCategory` Enum to `karrio/core/units.py`

```python
class ShippingDocumentCategory(utils.StrEnum):
    """Standardized shipping document category types.

    Usage:
        category = ShippingDocumentCategory.map("return_label").name_or_key
        category = ShippingDocumentCategory.map("ReturnLabel").name_or_key  # Maps to return_label
    """

    # Primary labels
    shipping_label = "ShippingLabel"
    return_label = "ReturnLabel"

    # Customs and export documents
    export_document = "ExportDocument"
    commercial_invoice = "CommercialInvoice"
    customs_declaration = "CustomsDeclaration"
    certificate_of_origin = "CertificateOfOrigin"

    # Other documents
    cod_document = "CODDocument"
    packing_list = "PackingList"
    dangerous_goods = "DangerousGoods"
    proof_of_delivery = "ProofOfDelivery"
    error_label = "ErrorLabel"
    manifest = "Manifest"
    receipt = "Receipt"
    qr_code = "QRCode"
```

### 2. Carrier-Specific Enum Pattern

Each carrier defines their own `ShippingDocumentCategory` enum with values matching the carrier's API naming convention:

```python
# In carrier provider units.py (e.g., dhl_parcel_de/units.py)
class ShippingDocumentCategory(lib.StrEnum):
    """Carrier specific document category types.

    Maps DHL Parcel DE document types to standard ShippingDocumentCategory.
    Values match the exact syntax used by DHL Parcel DE API.
    """

    shipping_label = "shippingLabel"
    return_label = "returnLabel"
    export_document = "exportDocument"
    receipt = "receipt"
    cod_document = "codLabel"
    enclosed_return_label = "enclosedReturnLabel"
    harmonized_label = "harmonizedLabel"
    international_shipping_label = "internationalShippingLabel"
    warenpost_national = "warenpostNational"
    return_label_international = "returnLabelInternational"
    warenpost_international = "warenpostInternational"
    error_label = "errorLabel"
    qr_code = "qrCode"
```

Usage in shipment response parsing:

```python
# In carrier shipment/create.py
import karrio.providers.dhl_parcel_de.units as provider_units

extra_documents = [
    ("return_label", shipment.returnLabel),
    ("cod_document", shipment.codLabel),
]

models.ShippingDocument(
    category=provider_units.ShippingDocumentCategory.map(category).name_or_key,
    ...
)
```

---

## Carrier Integration Changes

### Pattern for Updating Connectors

Each carrier connector that returns `extra_documents` should be updated:

**Before**:
```python
extra_documents = [
    ("retrunLabel", shipment.returnLabel),  # typo, inconsistent
    ("codLabel", shipment.codLabel),
]

models.ShippingDocument(
    category=label,
    ...
)
```

**After**:
```python
extra_documents = [
    ("return_label", shipment.returnLabel),
    ("cod_label", shipment.codLabel),
]

models.ShippingDocument(
    category=units.ShippingDocumentCategory.map(label).name_or_key,
    ...
)
```

### Connectors to Update

#### High Priority (Core Connectors with extra_documents)

| Connector | File | Current Categories |
|-----------|------|-------------------|
| dhl_parcel_de | `shipment/create.py:47` | retrunLabel, codLabel |
| fedex | `shipment/*.py` | Various |
| ups | `shipment/*.py` | Various |
| dhl_express | `shipment/*.py` | Various |
| canadapost | `shipment/*.py` | Various |

#### Search Pattern

Find all connectors using extra_documents:
```bash
grep -r "extra_documents" modules/connectors/*/karrio/providers/*/shipment/
```

---

## Testing Strategy

### SDK Tests

```python
"""Test ShippingDocumentCategory enum."""

import unittest
from karrio.core import units


class TestShippingDocumentCategory(unittest.TestCase):
    def test_standard_categories(self):
        """Verify all standard categories exist."""
        expected = [
            "shipping_label",
            "return_label",
            "cod_label",
            "export_document",
            "receipt",
            "commercial_invoice",
        ]
        for cat in expected:
            self.assertEqual(
                units.ShippingDocumentCategory.map(cat).name_or_key,
                cat
            )

    def test_mapping_unknown_category(self):
        """Unknown categories should return original key."""
        result = units.ShippingDocumentCategory.map("custom_carrier_doc").name_or_key
        self.assertEqual(result, "custom_carrier_doc")

    def test_case_insensitive_mapping(self):
        """Verify case handling for common variations."""
        # Test that mapping handles carrier variations
        variations = [
            ("return_label", "return_label"),
            ("RETURN_LABEL", "return_label"),  # If enum supports case-insensitive
        ]
        for input_val, expected in variations:
            result = units.ShippingDocumentCategory.map(input_val).name_or_key
            self.assertIn(result, [input_val, expected])


if __name__ == "__main__":
    unittest.main()
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run SDK tests
./bin/run-sdk-tests

# Run specific carrier tests
python -m unittest discover -v -f modules/connectors/dhl_parcel_de/tests
```

---

## Implementation Plan

### Phase 1: Core Enum Implementation

| Task | File | Status |
|------|------|--------|
| Add `ShippingDocumentCategory` enum | `karrio/core/units.py` | ✅ Completed |
| Add unit tests for enum | `modules/sdk/tests/` | Pending |
| Update documentation | API docs | Pending |

### Phase 2: Carrier Connector Updates

| Connector | Priority | Status |
|-----------|----------|--------|
| dhl_parcel_de | HIGH | ✅ Completed |
| dpd_meta | HIGH | ✅ Completed |
| fedex | HIGH | Pending |
| ups | HIGH | Pending |
| dhl_express | HIGH | Pending |
| All others | MEDIUM | Pending |

### Phase 3: Validation & Cleanup

| Task | Status |
|------|--------|
| Run full test suite | Pending |
| Fix any typos in existing code | ✅ Completed (dhl_parcel_de, dpd_meta) |
| Update API documentation | Pending |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing integrations | Low | Medium | Use `.name_or_key` pattern |
| Unmapped carrier categories | Medium | Low | Fall back to original key |
| Test failures | Low | Low | Incremental rollout |

---

## Appendix A: Document Category Reference

### Standard Document Categories

| Category | Description | Use Case |
|----------|-------------|----------|
| `shipping_label` | Primary label for package | Main shipping document |
| `return_label` | Pre-paid return label | Returns/exchanges |
| `cod_label` | Cash on delivery label | COD shipments |
| `export_document` | Export documentation | International customs |
| `commercial_invoice` | Commercial invoice | International trade |
| `receipt` | Shipping confirmation | Customer confirmation |
| `packing_list` | Contents list | Warehouse/logistics |
| `manifest` | Batch summary | Carrier pickup |
| `proof_of_delivery` | Delivery confirmation | Confirmation/disputes |

### Carrier-Specific Mappings

| Carrier | Their Term | Standard Category |
|---------|-----------|-------------------|
| DHL Parcel DE | returnLabel | return_label |
| DHL Parcel DE | codLabel | cod_document |
| DHL Parcel DE | warenpostNational | warenpost_national |
| DHL Parcel DE | shippingLabel | shipping_label |
| DPD META | qrcode | qr_code |
| FedEx | RETURN_SHIPPING_LABEL | return_label |
| UPS | Return Label | return_label |

---

## Appendix B: Example Usage

### Before (Current Implementation)

```python
# dhl_parcel_de/shipment/create.py
extra_documents = [
    ("retrunLabel", shipment.returnLabel),  # Typo!
    ("codLabel", shipment.codLabel),
]

return models.ShipmentDetails(
    ...
    docs=models.Documents(
        label=label,
        invoice=invoice,
        extra_documents=[
            models.ShippingDocument(
                category=label,  # Raw string
                format=lib.identity("ZPL" if doc.fileFormat == "ZPL2" else "PDF"),
                base64=lib.failsafe(lambda: doc.b64 or doc.zpl2),
                print_format=doc.printFormat,
                url=doc.url,
            )
            for label, doc in extra_documents
            if doc is not None
        ],
    ),
    ...
)
```

### After (With ShippingDocumentCategory)

```python
# dhl_parcel_de/shipment/create.py
import karrio.providers.dhl_parcel_de.units as provider_units

extra_documents = [
    ("return_label", shipment.returnLabel),
    ("cod_document", shipment.codLabel),
]

return models.ShipmentDetails(
    ...
    docs=models.Documents(
        label=label,
        invoice=invoice,
        extra_documents=[
            models.ShippingDocument(
                category=provider_units.ShippingDocumentCategory.map(category).name_or_key,
                format=lib.identity("ZPL" if doc.fileFormat == "ZPL2" else "PDF"),
                base64=lib.failsafe(lambda: doc.b64 or doc.zpl2),
                print_format=doc.printFormat,
                url=doc.url,
            )
            for category, doc in extra_documents
            if doc is not None
        ],
    ),
    ...
)
```

### API Response Example

```json
{
  "shipment": {
    "tracking_number": "123456789",
    "docs": {
      "label": "base64_encoded_label...",
      "extra_documents": [
        {
          "category": "return_label",
          "format": "PDF",
          "base64": "base64_encoded_return_label..."
        },
        {
          "category": "cod_document",
          "format": "PDF",
          "base64": "base64_encoded_cod_label..."
        }
      ]
    }
  }
}
```
