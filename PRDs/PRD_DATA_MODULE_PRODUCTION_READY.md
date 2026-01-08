# Product Requirements Document: Data Module Production Readiness

**Project**: Karrio Data Module Production-Ready Enhancement
**Version**: 1.0
**Date**: 2026-01-03
**Status**: Planning
**Owner**: Engineering Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Success Criteria](#goals--success-criteria)
4. [Feature Requirements](#feature-requirements)
   - [4.1 Ratesheet CSV Import](#41-ratesheet-csv-import)
   - [4.2 Sample CSV Download API](#42-sample-csv-download-api)
   - [4.3 Improved Batch Shipment Processing](#43-improved-batch-shipment-processing)
5. [Technical Architecture](#technical-architecture)
6. [API Design](#api-design)
7. [Database Changes](#database-changes)
8. [Testing Strategy](#testing-strategy)
9. [Implementation Plan](#implementation-plan)
10. [Risk Assessment](#risk-assessment)

---

## Executive Summary

This document outlines the requirements for making the Karrio Data Module (`modules/data`) production-ready. The data module currently provides:

- **Batch Operations**: Create shipments, trackers, and orders in bulk
- **Data Import/Export**: CSV/XLS/XLSX file import and export for resources
- **Data Templates**: Custom field mappings for import/export operations

**Current State**: The module is functional but lacks:
- Comprehensive test coverage
- Ratesheet CSV import capability for the rate sheet editor
- Sample CSV download endpoints for all supported import types
- Robust retry mechanisms and efficient queuing for batch shipment processing

**This PRD addresses**:
1. **Ratesheet CSV Import**: Enable importing carrier rate sheets from CSV files (like `services.csv`) directly into the ratesheet editor
2. **Sample CSV Downloads**: API endpoints to download sample CSV templates with all supported fields
3. **Comprehensive Testing**: Full test coverage for all batch APIs (shipments, trackers, orders)
4. **Improved Batch Processing**: Enhanced retry logic and efficient queuing for label generation

---

## Problem Statement

### Current Limitations

1. **No Ratesheet CSV Import**
   - Users must manually enter rate data in the ratesheet editor
   - Existing CSV files like `dhl_parcel_de/services.csv` and `landmark/services.csv` cannot be imported
   - No way to bulk-load rate data from carrier contracts

2. **No Sample CSV Templates**
   - Users don't know the expected CSV format for imports
   - No documentation of all supported fields
   - Error-prone manual CSV creation

3. **Minimal Test Coverage**
   - `modules/data/karrio/server/data/tests.py` is essentially empty
   - No tests for batch operations (shipments, trackers, orders)
   - No tests for import/export functionality
   - No tests for GraphQL mutations

4. **Basic Batch Processing**
   - No retry mechanism for failed label purchases
   - Sequential processing without priority queuing
   - Limited error recovery options

### Impact

- **User Experience**: Manual data entry is time-consuming and error-prone
- **Reliability**: Untested code leads to production bugs
- **Scalability**: Basic batch processing limits throughput for large operations
- **Adoption**: Lack of sample templates creates friction for new users

---

## Goals & Success Criteria

### Primary Goals

| Goal | Success Criteria |
|------|-----------------|
| Ratesheet CSV Import | Users can import CSV files to populate rate sheets with services, zones, and rates |
| Sample CSV Downloads | All resource types have downloadable sample CSVs with full field documentation |
| Comprehensive Testing | 90%+ test coverage for data module APIs and batch operations |
| Improved Batch Processing | Configurable retries, priority queuing, and proper error handling |

### Key Metrics

- **Test Coverage**: >= 90% line coverage for `modules/data/`
- **Import Success Rate**: >= 99% for valid CSV files
- **Batch Processing Throughput**: Support 1000+ shipments per batch operation
- **Retry Success Rate**: >= 80% recovery rate for transient failures

---

## Feature Requirements

### 4.1 Ratesheet CSV Import

#### Overview

Enable importing carrier rate sheet data from CSV files directly into the ratesheet editor. This supports the existing CSV format used by carrier connectors.

#### CSV Format Specification

Based on existing formats (`dhl_parcel_de/services.csv`, `landmark/services.csv`):

```csv
service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,cost,currency,transit_days,domicile,international
V01PAK,DHL Paket,Germany,DE,0.01,31.5,120,60,60,0.0,0.0,EUR,,true,false
V54EPAK,DHL EuroPaket,Europe,"AT,BE,BG,HR",0.01,31.5,120,60,60,0.0,0.0,EUR,,false,true
```

#### Supported Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `service_code` | string | Yes | Unique service identifier |
| `service_name` | string | Yes | Human-readable service name |
| `zone_label` | string | Yes | Zone name/label |
| `country_codes` | string | Yes | Comma-separated ISO country codes |
| `postal_codes` | string | No | Comma-separated postal codes or ranges |
| `cities` | string | No | Comma-separated city names |
| `min_weight` | float | No | Minimum weight in kg (default: 0) |
| `max_weight` | float | No | Maximum weight in kg |
| `max_length` | float | No | Maximum length in cm |
| `max_width` | float | No | Maximum width in cm |
| `max_height` | float | No | Maximum height in cm |
| `rate` | float | Yes | Sell price for this service-zone |
| `cost` | float | No | Cost of goods sold (COGS) |
| `currency` | string | Yes | ISO currency code |
| `transit_days` | int | No | Estimated transit days |
| `transit_time` | float | No | Estimated transit time in hours |
| `domicile` | bool | No | Domestic delivery support |
| `international` | bool | No | International delivery support |

#### Import Logic

1. **Parse CSV** into rows
2. **Group by service_code** to identify unique services
3. **Extract unique zones** from zone_label + country_codes combinations
4. **Create ServiceLevel** records for each unique service
5. **Create shared zones** at RateSheet level
6. **Create service_rates** mappings for service-zone combinations
7. **Link zones to services** via zone_ids

#### API Endpoint

```
POST /api/v1/rate-sheets/{id}/import
Content-Type: multipart/form-data

Parameters:
- data_file: CSV file
- merge_strategy: "replace" | "merge" (default: "merge")
```

#### GraphQL Mutation

```graphql
mutation ImportRateSheetCSV($input: ImportRateSheetCSVInput!) {
  importRateSheetCSV(input: $input) {
    rateSheet {
      id
      services { id serviceCode serviceName }
      zones
      serviceRates
    }
    errors { field messages }
  }
}

input ImportRateSheetCSVInput {
  id: String!
  dataFile: Upload!
  mergeStrategy: MergeStrategy
}

enum MergeStrategy {
  REPLACE
  MERGE
}
```

#### Validation Rules

- Service code must be unique within the rate sheet
- Country codes must be valid ISO 3166-1 alpha-2 codes
- Currency must be valid ISO 4217 code
- Rate must be >= 0
- Weight values must be positive if provided
- Dimension values must be positive if provided

---

### 4.2 Sample CSV Download API

#### Overview

Provide API endpoints to download sample CSV files for all supported import types with full field documentation.

#### Supported Resource Types

| Resource Type | Endpoint | Description |
|--------------|----------|-------------|
| `shipments` | `/api/v1/data/samples/shipments.csv` | Shipment import template |
| `trackers` | `/api/v1/data/samples/trackers.csv` | Tracker import template |
| `orders` | `/api/v1/data/samples/orders.csv` | Order import template |
| `ratesheets` | `/api/v1/data/samples/ratesheets.csv` | Ratesheet import template |

#### Sample CSV Content

Each sample CSV should include:
1. **Header row** with all supported field names
2. **Comment row** (prefixed with #) describing each field
3. **Example data row** showing valid values
4. **Optional data row** showing nullable/optional fields

**Example: shipments.csv**
```csv
shipper_name,shipper_company,shipper_address1,shipper_address2,shipper_city,shipper_state,shipper_postal_code,shipper_country,shipper_phone,shipper_email,shipper_residential,recipient_name,recipient_company,recipient_address1,recipient_address2,recipient_city,recipient_state,recipient_postal_code,recipient_country,recipient_phone,recipient_email,recipient_residential,parcel_weight,parcel_weight_unit,parcel_length,parcel_width,parcel_height,parcel_dimension_unit,parcel_package_preset,service,reference,options
# Required: name,Optional: company,Required: address,Optional: address2,Required: city,Required: state,Required: postal,Required: country (ISO),Optional: phone,Optional: email,Optional: true/false,Required: name,Optional: company,Required: address,Optional: address2,Required: city,Required: state,Required: postal,Required: country (ISO),Optional: phone,Optional: email,Optional: true/false,Required: weight,Required: KG/LB,Optional: length,Optional: width,Optional: height,Optional: CM/IN,Optional: preset code,Optional: service code,Optional: reference,Optional: JSON options
John Doe,Acme Inc,123 Main St,Suite 100,New York,NY,10001,US,+1234567890,john@example.com,false,Jane Smith,Tech Corp,456 Oak Ave,,Los Angeles,CA,90001,US,+0987654321,jane@example.com,true,2.5,KG,30,20,15,CM,,fedex_ground,ORDER-123,"{""signature_required"": true}"
```

**Example: ratesheets.csv**
```csv
service_code,service_name,zone_label,country_codes,postal_codes,cities,min_weight,max_weight,max_length,max_width,max_height,rate,cost,currency,transit_days,transit_time,domicile,international
# Required: unique code,Required: display name,Required: zone name,Required: ISO codes (comma-sep),Optional: postal codes,Optional: cities,Optional: min kg,Optional: max kg,Optional: max cm,Optional: max cm,Optional: max cm,Required: sell price,Optional: COGS,Required: ISO currency,Optional: days,Optional: hours,Optional: true/false,Optional: true/false
EXPRESS,Express Delivery,Domestic,US,,,0.01,30,120,60,60,15.99,12.50,USD,2,,true,false
STANDARD,Standard Delivery,Europe,"DE,FR,IT,ES",,,0.01,31.5,100,50,50,8.99,6.00,EUR,5,,false,true
```

#### API Design

```
GET /api/v1/data/samples/{resource_type}.{format}

Parameters:
- resource_type: shipments | trackers | orders | ratesheets
- format: csv | xlsx | xls

Response:
- Content-Type: text/csv | application/vnd.ms-excel | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- Content-Disposition: attachment; filename="sample_{resource_type}.{format}"
```

#### Implementation

Create a new resource module `modules/data/karrio/server/data/resources/samples.py`:

```python
SHIPMENT_SAMPLE_HEADERS = {
    "shipper_name": "Shipper name (Required)",
    "shipper_company": "Shipper company (Optional)",
    # ... all fields from DEFAULT_HEADERS in shipments.py
}

RATESHEET_SAMPLE_HEADERS = {
    "service_code": "Service code (Required, unique)",
    "service_name": "Service name (Required)",
    "zone_label": "Zone label (Required)",
    "country_codes": "Country codes (Required, comma-separated ISO)",
    # ... all supported fields
}

def get_sample_dataset(resource_type: str) -> tablib.Dataset:
    """Generate sample dataset with headers, comments, and example data."""
    pass
```

---

### 4.3 Improved Batch Shipment Processing

#### Overview

Enhance the batch shipment processing system with:
- Configurable retry mechanism for failed operations
- Priority-based queuing system
- Efficient label generation when services are specified
- Detailed progress tracking and error reporting

#### Current Implementation Issues

From `modules/data/karrio/server/events/task_definitions/data/shipments.py`:

```python
@utils.error_wrapper
def process_shipment(shipment):
    preferred_service = shipment.options.get("preferred_service")
    should_purchase = any(preferred_service or "")
    # ... no retry logic, no error recovery
```

**Problems**:
1. No retry for transient failures (network issues, rate limits)
2. No priority queue (all shipments processed equally)
3. No batching of carrier API calls
4. No detailed status tracking per resource

#### Enhanced Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Batch Operation Created                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Resource Validation Phase                     │
│  - Validate all shipments                                        │
│  - Group by carrier for efficient API calls                      │
│  - Assign priority based on service type                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Priority Queue System                        │
│  - High: Express/priority services                               │
│  - Medium: Standard services with preferred_service              │
│  - Low: Draft shipments (rate fetch only)                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing with Retries                       │
│  - Retry config: max_retries=3, backoff=exponential              │
│  - Transient errors: retry with backoff                          │
│  - Permanent errors: mark failed, continue                       │
│  - Rate limits: queue delay + retry                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Status Tracking & Callbacks                   │
│  - Per-resource status updates                                   │
│  - Webhook notifications on completion                           │
│  - Detailed error messages per resource                          │
└─────────────────────────────────────────────────────────────────┘
```

#### Resource Status Enhancement

```python
class ResourceStatus(lib.StrEnum):
    queued = "queued"           # Initial state
    processing = "processing"   # Currently being processed
    retrying = "retrying"       # Failed, scheduled for retry
    created = "created"         # Successfully created (draft)
    purchased = "purchased"     # Label purchased successfully
    has_errors = "has_errors"   # Permanent failure
    incomplete = "incomplete"   # Partial success
    processed = "processed"     # Fully processed
```

#### Retry Configuration

```python
@dataclass
class RetryConfig:
    max_retries: int = 3
    initial_delay: float = 1.0  # seconds
    max_delay: float = 60.0     # seconds
    exponential_base: float = 2.0
    retryable_errors: List[str] = field(default_factory=lambda: [
        "rate_limit_exceeded",
        "timeout",
        "connection_error",
        "service_unavailable",
    ])
```

#### Enhanced Task Definition

```python
# modules/data/karrio/server/events/task_definitions/data/shipments.py

from karrio.server.core.logging import logger
import karrio.server.core.utils as utils

@dataclass
class ProcessingResult:
    resource_id: str
    status: str
    error: Optional[dict] = None
    retry_count: int = 0
    tracking_number: Optional[str] = None

@utils.error_wrapper
def process_shipments_batch(
    shipment_ids: List[str],
    retry_config: Optional[RetryConfig] = None,
) -> List[ProcessingResult]:
    """
    Process shipments with retry logic and priority queuing.

    Args:
        shipment_ids: List of shipment IDs to process
        retry_config: Optional retry configuration

    Returns:
        List of processing results for each shipment
    """
    config = retry_config or RetryConfig()
    results = []

    # Group shipments by carrier for efficient API calls
    shipments = models.Shipment.objects.filter(
        id__in=shipment_ids,
        status="draft"
    ).select_related('shipper', 'recipient')

    # Sort by priority (express services first)
    prioritized = sorted(
        shipments,
        key=lambda s: get_shipment_priority(s),
        reverse=True
    )

    for shipment in prioritized:
        result = process_single_shipment_with_retry(shipment, config)
        results.append(result)

        # Update batch operation progress
        update_batch_progress(shipment.meta.get("batch_id"), result)

    return results

def process_single_shipment_with_retry(
    shipment: models.Shipment,
    config: RetryConfig,
) -> ProcessingResult:
    """Process a single shipment with retry logic."""
    retry_count = 0
    last_error = None

    while retry_count <= config.max_retries:
        try:
            result = process_shipment(shipment)
            return ProcessingResult(
                resource_id=shipment.id,
                status="purchased" if result.tracking_number else "created",
                tracking_number=result.tracking_number,
                retry_count=retry_count,
            )
        except Exception as e:
            last_error = e
            error_code = getattr(e, 'code', 'unknown')

            if error_code not in config.retryable_errors:
                # Permanent error, don't retry
                break

            retry_count += 1
            if retry_count <= config.max_retries:
                delay = min(
                    config.initial_delay * (config.exponential_base ** retry_count),
                    config.max_delay
                )
                logger.info(
                    "Retrying shipment processing",
                    shipment_id=shipment.id,
                    retry_count=retry_count,
                    delay=delay,
                )
                time.sleep(delay)

    return ProcessingResult(
        resource_id=shipment.id,
        status="has_errors",
        error=lib.to_dict(last_error),
        retry_count=retry_count,
    )

def get_shipment_priority(shipment: models.Shipment) -> int:
    """Determine processing priority for a shipment."""
    preferred_service = shipment.options.get("preferred_service", "")

    # Express/priority services get highest priority
    if any(kw in preferred_service.lower() for kw in ["express", "priority", "next_day"]):
        return 100

    # Shipments with preferred_service specified get medium priority
    if preferred_service:
        return 50

    # Draft shipments (rate fetch only) get lowest priority
    return 10
```

#### Batch Operation Status Updates

```python
def update_batch_progress(batch_id: str, result: ProcessingResult):
    """Update batch operation with individual resource result."""
    if not batch_id:
        return

    batch = models.BatchOperation.objects.filter(pk=batch_id).first()
    if not batch:
        return

    resources = list(batch.resources or [])

    # Find and update the resource
    for i, resource in enumerate(resources):
        if resource.get("id") == result.resource_id:
            resources[i] = {
                "id": result.resource_id,
                "status": result.status,
                "errors": result.error,
                "tracking_number": result.tracking_number,
                "retry_count": result.retry_count,
            }
            break

    # Calculate overall batch status
    statuses = [r.get("status") for r in resources]
    if all(s in ["purchased", "created", "processed"] for s in statuses):
        batch_status = "completed"
    elif any(s == "has_errors" for s in statuses):
        batch_status = "completed_with_errors"
    elif any(s in ["queued", "processing", "retrying"] for s in statuses):
        batch_status = "running"
    else:
        batch_status = "running"

    batch.resources = resources
    batch.status = batch_status
    batch.save(update_fields=["resources", "status"])
```

---

## Technical Architecture

### Module Structure

```
modules/data/
├── karrio/
│   └── server/
│       ├── data/
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── filters.py
│       │   ├── models.py
│       │   ├── signals.py
│       │   ├── urls.py
│       │   ├── migrations/
│       │   ├── resources/
│       │   │   ├── __init__.py
│       │   │   ├── orders.py
│       │   │   ├── shipments.py
│       │   │   ├── trackers.py
│       │   │   ├── ratesheets.py      # NEW: Ratesheet import resource
│       │   │   └── samples.py         # NEW: Sample CSV generation
│       │   ├── serializers/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── batch.py
│       │   │   ├── batch_orders.py
│       │   │   ├── batch_shipments.py
│       │   │   ├── batch_trackers.py
│       │   │   ├── data.py
│       │   │   └── ratesheets.py      # NEW: Ratesheet CSV serializer
│       │   ├── views/
│       │   │   ├── __init__.py
│       │   │   ├── batch.py
│       │   │   ├── batch_order.py
│       │   │   ├── batch_shipment.py
│       │   │   ├── batch_tracking.py
│       │   │   ├── data.py
│       │   │   └── samples.py         # NEW: Sample download views
│       │   └── tests/                 # NEW: Test directory
│       │       ├── __init__.py
│       │       ├── test_batch_shipments.py
│       │       ├── test_batch_trackers.py
│       │       ├── test_batch_orders.py
│       │       ├── test_data_import.py
│       │       ├── test_data_export.py
│       │       ├── test_ratesheet_import.py
│       │       ├── test_samples.py
│       │       └── fixtures.py
│       ├── events/
│       │   └── task_definitions/
│       │       └── data/
│       │           ├── __init__.py
│       │           ├── batch.py
│       │           └── shipments.py   # ENHANCED: Retry logic
│       └── graph/
│           └── schemas/
│               └── data/
│                   ├── __init__.py
│                   ├── inputs.py
│                   ├── mutations.py   # ENHANCED: Ratesheet import
│                   └── types.py
```

---

## API Design

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/data/samples/{type}.{format}` | Download sample CSV template |
| `POST` | `/api/v1/rate-sheets/{id}/import` | Import CSV to rate sheet |
| `POST` | `/api/v1/batches/shipments` | Create shipment batch (existing) |
| `POST` | `/api/v1/batches/trackers` | Create tracker batch (existing) |
| `POST` | `/api/v1/batches/orders` | Create order batch (existing) |
| `POST` | `/api/v1/batches/data/import` | Import data file (existing) |
| `GET` | `/api/v1/batches/data/export/{type}.{format}` | Export data file (existing) |
| `GET` | `/api/v1/batches/{id}` | Get batch operation status (existing) |

### GraphQL Schema Additions

```graphql
# New Mutations
extend type Mutation {
  importRateSheetCSV(input: ImportRateSheetCSVInput!): ImportRateSheetCSVMutation
}

# New Types
type ImportRateSheetCSVMutation {
  rateSheet: RateSheetType
  importSummary: ImportSummary
  errors: [ErrorType]
}

type ImportSummary {
  servicesCreated: Int!
  servicesUpdated: Int!
  zonesCreated: Int!
  ratesCreated: Int!
  warnings: [String]
}

input ImportRateSheetCSVInput {
  id: String!
  dataFile: Upload!
  mergeStrategy: MergeStrategy
}

enum MergeStrategy {
  REPLACE  # Clear existing and import new
  MERGE    # Add new, update existing by service_code
}

# New Queries
extend type Query {
  sampleCSVFields(resourceType: ResourceType!): [SampleFieldType]
}

type SampleFieldType {
  name: String!
  label: String!
  required: Boolean!
  description: String
  example: String
}

enum ResourceType {
  SHIPMENTS
  TRACKERS
  ORDERS
  RATESHEETS
}
```

---

## Database Changes

No new database tables required. The existing models are sufficient:

- `BatchOperation`: Stores batch operation status and resources
- `DataTemplate`: Stores custom field mappings
- `RateSheet`: Stores rate sheet configuration (zones, services, service_rates)
- `ServiceLevel`: Stores service definitions

### Model Enhancements

Update `BatchOperation.resources` JSON structure to include enhanced status tracking:

```python
# Current structure
resources = [
    {"id": "shp_xxx", "status": "queued"}
]

# Enhanced structure
resources = [
    {
        "id": "shp_xxx",
        "status": "purchased",
        "tracking_number": "1Z999AA...",
        "retry_count": 1,
        "errors": None,
        "processed_at": "2026-01-03T10:30:00Z"
    }
]
```

---

## Testing Strategy

### Test Structure

Create comprehensive tests in `modules/data/karrio/server/data/tests/`:

```
tests/
├── __init__.py
├── fixtures.py              # Shared test data and helpers
├── test_batch_shipments.py  # Batch shipment API tests
├── test_batch_trackers.py   # Batch tracker API tests
├── test_batch_orders.py     # Batch order API tests
├── test_data_import.py      # CSV/XLS import tests
├── test_data_export.py      # CSV/XLS export tests
├── test_ratesheet_import.py # Ratesheet CSV import tests
├── test_samples.py          # Sample CSV download tests
└── test_graphql.py          # GraphQL mutation tests
```

### Test Cases

#### Batch Shipments Tests (`test_batch_shipments.py`)

```python
from django.test import TestCase
from unittest import mock
from karrio.server.data.serializers import BatchShipmentData
from karrio.server.core.tests import APITestCase

class TestBatchShipmentAPI(APITestCase):
    """Test batch shipment creation API."""

    def test_create_batch_shipments(self):
        """Test creating a batch of shipments."""
        response = self.client.post(
            "/api/v1/batches/shipments",
            data=BATCH_SHIPMENT_DATA,
            content_type="application/json",
        )
        print(response)
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            response.data,
            {
                "id": mock.ANY,
                "status": "queued",
                "resource_type": "shipments",
                "resources": mock.ANY,
                "created_at": mock.ANY,
                "updated_at": mock.ANY,
                "test_mode": True,
            }
        )

    def test_create_batch_with_invalid_shipment(self):
        """Test batch creation fails with invalid shipment data."""
        invalid_data = {"shipments": [{"shipper": {}}]}  # Missing required fields
        response = self.client.post(
            "/api/v1/batches/shipments",
            data=invalid_data,
            content_type="application/json",
        )
        print(response)
        self.assertEqual(response.status_code, 400)

    def test_batch_shipment_with_preferred_service(self):
        """Test batch shipment with preferred_service triggers label purchase."""
        data = {
            "shipments": [{
                **VALID_SHIPMENT,
                "options": {"preferred_service": "fedex_ground"}
            }]
        }
        response = self.client.post(
            "/api/v1/batches/shipments",
            data=data,
            content_type="application/json",
        )
        print(response)
        self.assertResponseNoErrors(response)

    def test_batch_operation_status_tracking(self):
        """Test batch operation status updates during processing."""
        # Create batch
        response = self.client.post(
            "/api/v1/batches/shipments",
            data=BATCH_SHIPMENT_DATA,
            content_type="application/json",
        )
        batch_id = response.data["id"]

        # Check status
        status_response = self.client.get(f"/api/v1/batches/{batch_id}")
        print(status_response)
        self.assertResponseNoErrors(status_response)
        self.assertIn(status_response.data["status"], ["queued", "running", "completed"])
```

#### Ratesheet Import Tests (`test_ratesheet_import.py`)

```python
import io
from django.test import TestCase
from karrio.server.core.tests import APITestCase
from karrio.server.providers.models import RateSheet

class TestRateSheetCSVImport(APITestCase):
    """Test ratesheet CSV import functionality."""

    def setUp(self):
        super().setUp()
        self.rate_sheet = RateSheet.objects.create(
            name="Test Rate Sheet",
            slug="test_rate_sheet",
            carrier_name="generic",
            created_by=self.user,
        )

    def test_import_valid_csv(self):
        """Test importing a valid CSV file."""
        csv_content = """service_code,service_name,zone_label,country_codes,rate,currency,transit_days
EXPRESS,Express Delivery,Domestic,US,15.99,USD,2
STANDARD,Standard Delivery,Europe,"DE,FR,IT",8.99,EUR,5"""

        csv_file = io.StringIO(csv_content)
        csv_file.name = "rates.csv"

        response = self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": csv_file},
            format="multipart",
        )
        print(response)
        self.assertResponseNoErrors(response)

        # Verify services were created
        self.rate_sheet.refresh_from_db()
        self.assertEqual(self.rate_sheet.services.count(), 2)

    def test_import_csv_with_merge_strategy(self):
        """Test importing with merge strategy preserves existing data."""
        # First import
        csv1 = """service_code,service_name,zone_label,country_codes,rate,currency
EXPRESS,Express,US,US,15.99,USD"""
        self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": io.StringIO(csv1), "merge_strategy": "merge"},
            format="multipart",
        )

        # Second import with merge
        csv2 = """service_code,service_name,zone_label,country_codes,rate,currency
STANDARD,Standard,US,US,9.99,USD"""
        response = self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": io.StringIO(csv2), "merge_strategy": "merge"},
            format="multipart",
        )
        print(response)

        # Both services should exist
        self.rate_sheet.refresh_from_db()
        self.assertEqual(self.rate_sheet.services.count(), 2)

    def test_import_csv_with_replace_strategy(self):
        """Test importing with replace strategy clears existing data."""
        # First import
        csv1 = """service_code,service_name,zone_label,country_codes,rate,currency
EXPRESS,Express,US,US,15.99,USD"""
        self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": io.StringIO(csv1)},
            format="multipart",
        )

        # Second import with replace
        csv2 = """service_code,service_name,zone_label,country_codes,rate,currency
STANDARD,Standard,US,US,9.99,USD"""
        response = self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": io.StringIO(csv2), "merge_strategy": "replace"},
            format="multipart",
        )
        print(response)

        # Only the new service should exist
        self.rate_sheet.refresh_from_db()
        self.assertEqual(self.rate_sheet.services.count(), 1)
        self.assertEqual(self.rate_sheet.services.first().service_code, "STANDARD")

    def test_import_invalid_country_codes(self):
        """Test import fails with invalid country codes."""
        csv_content = """service_code,service_name,zone_label,country_codes,rate,currency
EXPRESS,Express,Invalid,XX,15.99,USD"""

        response = self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": io.StringIO(csv_content)},
            format="multipart",
        )
        print(response)
        self.assertEqual(response.status_code, 400)

    def test_import_missing_required_fields(self):
        """Test import fails with missing required fields."""
        csv_content = """service_code,service_name
EXPRESS,Express"""  # Missing zone_label, country_codes, rate, currency

        response = self.client.post(
            f"/api/v1/rate-sheets/{self.rate_sheet.id}/import",
            data={"data_file": io.StringIO(csv_content)},
            format="multipart",
        )
        print(response)
        self.assertEqual(response.status_code, 400)
```

#### Sample CSV Tests (`test_samples.py`)

```python
from django.test import TestCase
from karrio.server.core.tests import APITestCase

class TestSampleCSVDownload(APITestCase):
    """Test sample CSV download endpoints."""

    def test_download_shipments_sample(self):
        """Test downloading shipments sample CSV."""
        response = self.client.get("/api/v1/data/samples/shipments.csv")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("shipper_name", response.content.decode())

    def test_download_trackers_sample(self):
        """Test downloading trackers sample CSV."""
        response = self.client.get("/api/v1/data/samples/trackers.csv")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn("tracking_number", response.content.decode())

    def test_download_orders_sample(self):
        """Test downloading orders sample CSV."""
        response = self.client.get("/api/v1/data/samples/orders.csv")
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_download_ratesheets_sample(self):
        """Test downloading ratesheets sample CSV."""
        response = self.client.get("/api/v1/data/samples/ratesheets.csv")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn("service_code", response.content.decode())
        self.assertIn("zone_label", response.content.decode())

    def test_download_xlsx_format(self):
        """Test downloading sample in XLSX format."""
        response = self.client.get("/api/v1/data/samples/shipments.xlsx")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    def test_invalid_resource_type(self):
        """Test error for invalid resource type."""
        response = self.client.get("/api/v1/data/samples/invalid.csv")
        print(response)
        self.assertEqual(response.status_code, 404)
```

#### Data Import/Export Tests (`test_data_import.py`, `test_data_export.py`)

```python
import io
from django.test import TestCase
from karrio.server.core.tests import APITestCase

class TestDataImport(APITestCase):
    """Test data import functionality."""

    def test_import_shipments_csv(self):
        """Test importing shipments from CSV."""
        csv_content = """Shipper name,Shipper Company,Shipper address 1,Shipper city,Shipper state,Shipper postal code,Shipper country,Recipient name,Recipient Company,Recipient address 1,Recipient city,Recipient state,Recipient postal code,Recipient country,Parcel weight,Parcel weight unit
John Doe,Acme Inc,123 Main St,New York,NY,10001,US,Jane Smith,Tech Corp,456 Oak Ave,Los Angeles,CA,90001,US,2.5,KG"""

        csv_file = io.StringIO(csv_content)
        csv_file.name = "shipments.csv"

        response = self.client.post(
            "/api/v1/batches/data/import",
            data={
                "resource_type": "shipments",
                "data_file": csv_file,
            },
            format="multipart",
        )
        print(response)
        self.assertEqual(response.status_code, 202)

    def test_import_trackers_csv(self):
        """Test importing trackers from CSV."""
        csv_content = """Tracking Number,Carrier
1Z999AA10123456784,ups"""

        csv_file = io.StringIO(csv_content)
        csv_file.name = "trackers.csv"

        response = self.client.post(
            "/api/v1/batches/data/import",
            data={
                "resource_type": "trackers",
                "data_file": csv_file,
            },
            format="multipart",
        )
        print(response)
        self.assertEqual(response.status_code, 202)


class TestDataExport(APITestCase):
    """Test data export functionality."""

    def test_export_shipments_csv(self):
        """Test exporting shipments to CSV."""
        # Create some shipments first
        self._create_test_shipment()

        response = self.client.get("/api/v1/batches/data/export/shipments.csv")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_export_with_filters(self):
        """Test exporting with query filters."""
        response = self.client.get(
            "/api/v1/batches/data/export/shipments.csv?status=purchased"
        )
        print(response)
        self.assertEqual(response.status_code, 200)
```

### Test Commands

```bash
# Run all data module tests
karrio test karrio.server.data.tests

# Run specific test file
karrio test karrio.server.data.tests.test_batch_shipments

# Run with coverage
karrio test karrio.server.data.tests --with-coverage
```

---

## Implementation Plan

### Phase 1: Test Infrastructure (Week 1)

| Task | Description | Priority |
|------|-------------|----------|
| 1.1 | Create test directory structure | High |
| 1.2 | Create `fixtures.py` with test data | High |
| 1.3 | Implement `test_batch_shipments.py` | High |
| 1.4 | Implement `test_batch_trackers.py` | High |
| 1.5 | Implement `test_batch_orders.py` | High |

### Phase 2: Sample CSV Downloads (Week 2)

| Task | Description | Priority |
|------|-------------|----------|
| 2.1 | Create `resources/samples.py` module | High |
| 2.2 | Define sample headers for all resource types | High |
| 2.3 | Implement `views/samples.py` endpoints | High |
| 2.4 | Add URL routes for sample downloads | High |
| 2.5 | Implement `test_samples.py` tests | High |

### Phase 3: Ratesheet CSV Import (Weeks 3-4)

| Task | Description | Priority |
|------|-------------|----------|
| 3.1 | Create `resources/ratesheets.py` module | High |
| 3.2 | Implement CSV parsing logic | High |
| 3.3 | Implement zone extraction and deduplication | High |
| 3.4 | Implement service creation logic | High |
| 3.5 | Implement service_rates mapping | High |
| 3.6 | Add merge/replace strategies | Medium |
| 3.7 | Create REST endpoint for import | High |
| 3.8 | Create GraphQL mutation | High |
| 3.9 | Implement `test_ratesheet_import.py` | High |

### Phase 4: Improved Batch Processing (Weeks 5-6)

| Task | Description | Priority |
|------|-------------|----------|
| 4.1 | Implement `RetryConfig` dataclass | High |
| 4.2 | Implement exponential backoff logic | High |
| 4.3 | Implement priority queue sorting | Medium |
| 4.4 | Update `process_shipments_batch` | High |
| 4.5 | Update `process_single_shipment_with_retry` | High |
| 4.6 | Implement batch progress tracking | High |
| 4.7 | Add tests for retry logic | High |
| 4.8 | Add tests for priority queuing | Medium |

### Phase 5: Import/Export Tests & Polish (Week 7)

| Task | Description | Priority |
|------|-------------|----------|
| 5.1 | Implement `test_data_import.py` | High |
| 5.2 | Implement `test_data_export.py` | High |
| 5.3 | Implement `test_graphql.py` | Medium |
| 5.4 | Documentation updates | Medium |
| 5.5 | Code review and cleanup | High |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CSV parsing edge cases (quotes, special chars) | Medium | Medium | Use robust CSV parser, extensive test coverage |
| Retry logic causing duplicate operations | Low | High | Implement idempotency checks |
| Large batch operations timing out | Medium | Medium | Implement chunking and progress tracking |
| GraphQL file upload issues | Low | Medium | Test with various file sizes and types |
| Zone deduplication conflicts | Medium | Low | Use deterministic zone ID generation |
| Breaking existing import formats | Low | High | Maintain backward compatibility with existing headers |

---

## Appendix

### A. Existing CSV Formats Reference

**DHL Parcel DE (`services.csv`)**:
```csv
service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,currency,transit_days,domicile,international
V01PAK,DHL Paket,Germany,DE,0.01,31.5,120,60,60,0.0,EUR,,true,false
```

**Landmark (`services.csv`)**:
```csv
service_code,service_name,zone_label,country_codes,rate,currency,transit_days
LGINTSTD,MaxiPak Scan DDP,United States,US,5.71,GBP,7
LGINTSTD,MaxiPak Scan DDP,EU Zone 1,"AT,BE,CZ,DE,DK,FR,IE,LU,NL,PL",4.33,GBP,8
```

### B. SDK Models Reference

From `modules/sdk/karrio/core/models.py`:

- `ServiceLevel`: Service definition with zones, surcharges, weight/dimension limits
- `ServiceZone`: Zone with rate, weight constraints, and location matching
- `SharedZone`: Shared zone definition at RateSheet level
- `SharedSurcharge`: Shared surcharge definition at RateSheet level
- `ServiceRate`: Service-zone rate mapping
- `RateSheet`: Complete rate configuration

### C. Server Models Reference

From `modules/core/karrio/server/providers/models/sheet.py`:

- `RateSheet` model with:
  - `zones`: JSONField for shared zone definitions
  - `surcharges`: JSONField for shared surcharge definitions
  - `service_rates`: JSONField for service-zone mappings
  - `services`: ManyToManyField to ServiceLevel
