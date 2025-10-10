# Shipping Methods API Documentation

## Overview

The Shipping Methods API allows you to create predefined shipping methods with specific carrier configurations and use them to streamline label purchasing. This is particularly useful for standardizing shipping options across your organization or platform.

**Base URL:** `http://localhost:5002/v1`

---

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [List Shipping Methods](#1-list-shipping-methods)
  - [Buy Label with Shipping Method](#2-buy-label-with-shipping-method)
  - [Buy Label for Existing Shipment](#3-buy-label-for-existing-shipment)
- [Complete Examples](#complete-examples)
- [Error Handling](#error-handling)

---

## Authentication

All API requests require authentication using a Bearer token or API key in the Authorization header:

```bash
Authorization: Token YOUR_API_KEY
```

---

## Endpoints

### 1. List Shipping Methods

Retrieve all configured shipping methods.

**Endpoint:** `GET /shipping-methods`

**Query Parameters:**
- `limit` (integer): Number of results per page (default: 25)
- `offset` (integer): Pagination offset
- `search` (string): Search by name, slug, or description
- `created_after` (datetime): Filter by creation date
- `created_before` (datetime): Filter by creation date

#### Request Example

```bash
curl -X GET "http://localhost:5002/v1/shipping-methods?limit=10&offset=0" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

#### Response Example

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "mtd_abc123def456",
      "object_type": "shipping-method",
      "name": "UPS Ground Economy",
      "slug": "ups-ground-economy",
      "description": "Standard UPS ground shipping for domestic shipments",
      "carrier_code": "ups",
      "carrier_service": "ups_standard",
      "carrier_id": "car_ups12345",
      "carrier_options": {
        "insurance": 100,
        "signature_required": false
      },
      "metadata": {
        "department": "fulfillment",
        "priority": "standard"
      },
      "is_active": true,
      "test_mode": false,
      "created_at": "2024-01-15T10:30:00.000000Z"
    },
    {
      "id": "mtd_xyz789ghi012",
      "object_type": "shipping-method",
      "name": "DHL Express Worldwide",
      "slug": "dhl-express-worldwide",
      "description": "Fast international shipping via DHL Express",
      "carrier_code": "dhl_express",
      "carrier_service": "dhl_express_worldwide",
      "carrier_id": "car_dhl67890",
      "carrier_options": {
        "insurance": 500,
        "dhl_paperless_trade": true
      },
      "metadata": {
        "department": "international",
        "priority": "express"
      },
      "is_active": true,
      "test_mode": false,
      "created_at": "2024-01-15T11:45:00.000000Z"
    }
  ]
}
```

---

### 2. Buy Label with Shipping Method

Create a new shipment and immediately purchase a label using a predefined shipping method configuration.

**Endpoint:** `POST /shipping-methods/{method_id}/labels`

**Path Parameters:**
- `method_id` (string, required): The shipping method ID

**Request Body:**

```typescript
{
  "recipient": {
    "address_line1": string,
    "person_name": string,
    "company_name"?: string,
    "phone_number": string,
    "city": string,
    "country_code": string,
    "postal_code": string,
    "residential"?: boolean,
    "state_code"?: string,
    "email"?: string
  },
  "shipper": {
    "address_line1": string,
    "person_name": string,
    "company_name"?: string,
    "phone_number": string,
    "city": string,
    "country_code": string,
    "postal_code": string,
    "residential"?: boolean,
    "state_code"?: string,
    "email"?: string
  },
  "parcels": [
    {
      "weight": number,
      "weight_unit": "KG" | "LB",
      "length"?: number,
      "width"?: number,
      "height"?: number,
      "dimension_unit"?: "CM" | "IN",
      "package_preset"?: string
    }
  ],
  "payment"?: {
    "currency": string,
    "paid_by": "sender" | "recipient"
  },
  "options"?: {
    "insurance"?: number,
    "signature_required"?: boolean,
    "shipping_date"?: string,
    // ... other carrier-specific options
  },
  "customs"?: {
    // For international shipments
    "content_type": string,
    "incoterm": string,
    "items": Array
  }
}
```

#### Example 1: UPS Standard Domestic Shipment

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_ups_standard_123/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "123 Main Street",
      "person_name": "John Doe",
      "company_name": "Acme Corp",
      "phone_number": "555-123-4567",
      "city": "Los Angeles",
      "country_code": "US",
      "postal_code": "90001",
      "state_code": "CA",
      "residential": false,
      "email": "john@acmecorp.com"
    },
    "shipper": {
      "address_line1": "456 Warehouse Blvd",
      "person_name": "Jane Smith",
      "company_name": "Shipper LLC",
      "phone_number": "555-987-6543",
      "city": "New York",
      "country_code": "US",
      "postal_code": "10001",
      "state_code": "NY",
      "residential": false,
      "email": "jane@shipperllc.com"
    },
    "parcels": [
      {
        "weight": 5.5,
        "weight_unit": "LB",
        "length": 12,
        "width": 10,
        "height": 8,
        "dimension_unit": "IN"
      }
    ],
    "payment": {
      "currency": "USD",
      "paid_by": "sender"
    },
    "options": {
      "signature_required": true,
      "insurance": 150
    }
  }'
```

#### Example 2: DHL Express International Shipment

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dhl_express_456/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "Friedrichstraße 123",
      "person_name": "Hans Mueller",
      "company_name": "Deutsche GmbH",
      "phone_number": "+49 30 12345678",
      "city": "Berlin",
      "country_code": "DE",
      "postal_code": "10117",
      "residential": false,
      "email": "hans@deutsche-gmbh.de"
    },
    "shipper": {
      "address_line1": "456 Export Drive",
      "person_name": "Sarah Johnson",
      "company_name": "Global Exports Inc",
      "phone_number": "+1 212-555-0100",
      "city": "New York",
      "country_code": "US",
      "postal_code": "10001",
      "state_code": "NY",
      "residential": false,
      "email": "sarah@globalexports.com"
    },
    "parcels": [
      {
        "weight": 3.5,
        "weight_unit": "KG",
        "length": 40,
        "width": 30,
        "height": 25,
        "dimension_unit": "CM"
      }
    ],
    "payment": {
      "currency": "USD",
      "paid_by": "sender"
    },
    "customs": {
      "content_type": "merchandise",
      "incoterm": "DDP",
      "commercial_invoice": true,
      "items": [
        {
          "description": "Electronic Components",
          "quantity": 10,
          "value_amount": 250.00,
          "value_currency": "USD",
          "weight": 0.35,
          "weight_unit": "KG",
          "origin_country": "US",
          "hs_code": "8542.31.0000"
        }
      ]
    },
    "options": {
      "dhl_paperless_trade": true,
      "insurance": 500
    }
  }'
```

#### Example 3: DHL Parcel DE Domestic (Germany)

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dhl_parcel_de_789/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "Marienplatz 1",
      "person_name": "Anna Schmidt",
      "company_name": "München Tech",
      "phone_number": "+49 89 12345678",
      "city": "München",
      "country_code": "DE",
      "postal_code": "80331",
      "residential": false,
      "email": "anna@muenchen-tech.de"
    },
    "shipper": {
      "address_line1": "Alexanderplatz 5",
      "person_name": "Thomas Weber",
      "company_name": "Berlin Handel",
      "phone_number": "+49 30 98765432",
      "city": "Berlin",
      "country_code": "DE",
      "postal_code": "10178",
      "residential": false,
      "email": "thomas@berlin-handel.de"
    },
    "parcels": [
      {
        "weight": 2.0,
        "weight_unit": "KG",
        "length": 35,
        "width": 25,
        "height": 15,
        "dimension_unit": "CM"
      }
    ],
    "payment": {
      "currency": "EUR",
      "paid_by": "sender"
    },
    "options": {
      "dhl_parcel_de_preferred_day": "2024-02-01",
      "dhl_parcel_de_preferred_location": "Garage"
    }
  }'
```

#### Example 4: DPD Express 12h (European)

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dpd_express_12h/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "Rue de la Paix 12",
      "person_name": "Marie Dubois",
      "company_name": "Paris Commerce SARL",
      "phone_number": "+33 1 42 60 30 30",
      "city": "Paris",
      "country_code": "FR",
      "postal_code": "75002",
      "residential": false,
      "email": "marie@pariscommerce.fr"
    },
    "shipper": {
      "address_line1": "Via Roma 45",
      "person_name": "Giovanni Rossi",
      "company_name": "Milano Export SpA",
      "phone_number": "+39 02 1234567",
      "city": "Milano",
      "country_code": "IT",
      "postal_code": "20121",
      "residential": false,
      "email": "giovanni@milanoexport.it"
    },
    "parcels": [
      {
        "weight": 4.5,
        "weight_unit": "KG",
        "length": 50,
        "width": 40,
        "height": 30,
        "dimension_unit": "CM"
      }
    ],
    "payment": {
      "currency": "EUR",
      "paid_by": "sender"
    },
    "options": {
      "dpd_saturday_delivery": true,
      "insurance": 300
    }
  }'
```

#### Response Example

```json
{
  "id": "shp_abc123xyz789",
  "object_type": "shipment",
  "status": "purchased",
  "carrier_name": "ups",
  "carrier_id": "car_ups12345",
  "tracking_number": "1Z999AA10123456784",
  "tracking_url": "/v1/trackers/ups/1Z999AA10123456784",
  "shipment_identifier": "1Z999AA10123456784",
  "label_type": "PDF",
  "label_url": "https://api.karrio.io/labels/shp_abc123xyz789.pdf",
  "invoice_url": null,
  "selected_rate": {
    "id": "rat_xyz789abc123",
    "object_type": "rate",
    "carrier_name": "ups",
    "carrier_id": "car_ups12345",
    "currency": "USD",
    "service": "ups_standard",
    "total_charge": 42.50,
    "transit_days": 3,
    "estimated_delivery": "2024-01-20",
    "extra_charges": [
      {
        "name": "Base charge",
        "amount": 35.00,
        "currency": "USD"
      },
      {
        "name": "Fuel surcharge",
        "amount": 5.25,
        "currency": "USD"
      },
      {
        "name": "Signature fee",
        "amount": 2.25,
        "currency": "USD"
      }
    ],
    "test_mode": false
  },
  "shipper": {
    "id": "adr_shipper123",
    "address_line1": "456 Warehouse Blvd",
    "person_name": "Jane Smith",
    "company_name": "Shipper LLC",
    "phone_number": "+1 555-987-6543",
    "city": "New York",
    "country_code": "US",
    "postal_code": "10001",
    "state_code": "NY",
    "residential": false,
    "email": "jane@shipperllc.com"
  },
  "recipient": {
    "id": "adr_recipient456",
    "address_line1": "123 Main Street",
    "person_name": "John Doe",
    "company_name": "Acme Corp",
    "phone_number": "+1 555-123-4567",
    "city": "Los Angeles",
    "country_code": "US",
    "postal_code": "90001",
    "state_code": "CA",
    "residential": false,
    "email": "john@acmecorp.com"
  },
  "parcels": [
    {
      "id": "pcl_parcel789",
      "weight": 5.5,
      "weight_unit": "LB",
      "length": 12.0,
      "width": 10.0,
      "height": 8.0,
      "dimension_unit": "IN"
    }
  ],
  "options": {
    "signature_required": true,
    "insurance": 150,
    "shipping_date": "2024-01-17T10:30:00Z"
  },
  "payment": {
    "currency": "USD",
    "paid_by": "sender"
  },
  "service": "ups_standard",
  "carrier_id": "car_ups12345",
  "test_mode": false,
  "created_at": "2024-01-17T10:30:15.123456Z",
  "messages": []
}
```

---

### 3. Buy Label for Existing Shipment

Purchase a label for an existing shipment (in draft status) using a shipping method's configuration.

**Endpoint:** `POST /shipping-methods/{method_id}/shipments/{shipment_id}/labels`

**Path Parameters:**
- `method_id` (string, required): The shipping method ID
- `shipment_id` (string, required): The existing shipment ID

**Request Body:**

```typescript
{
  "label_type"?: "PDF" | "ZPL" | "PNG",
  "options"?: {
    "insurance"?: number,
    "signature_required"?: boolean,
    // ... additional options to override defaults
  },
  "metadata"?: {
    // Custom key-value pairs
  },
  "reference"?: string
}
```

#### Example 1: Purchase Label for Existing UPS Shipment

**Step 1: Create Draft Shipment**

```bash
curl -X POST "http://localhost:5002/v1/shipments" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "789 Oak Avenue",
      "person_name": "Emily Davis",
      "phone_number": "555-111-2222",
      "city": "Chicago",
      "country_code": "US",
      "postal_code": "60601",
      "state_code": "IL"
    },
    "shipper": {
      "address_line1": "456 Warehouse Blvd",
      "person_name": "Jane Smith",
      "phone_number": "555-987-6543",
      "city": "New York",
      "country_code": "US",
      "postal_code": "10001",
      "state_code": "NY"
    },
    "parcels": [
      {
        "weight": 3.5,
        "weight_unit": "LB"
      }
    ],
    "payment": {
      "currency": "USD",
      "paid_by": "sender"
    },
    "carrier_id": "car_ups12345"
  }'
```

**Response:** Returns shipment with `id: "shp_draft123"` and `status: "draft"` with available rates.

**Step 2: Buy Label with Shipping Method**

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_ups_standard_123/shipments/shp_draft123/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "label_type": "PDF",
    "options": {
      "insurance": 200,
      "currency": "USD"
    },
    "metadata": {
      "order_id": "ORD-2024-001",
      "customer_ref": "CUST-12345"
    },
    "reference": "ORDER-2024-001"
  }'
```

#### Example 2: Purchase Label for DHL Express Shipment

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dhl_express_456/shipments/shp_draft456/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "label_type": "PDF",
    "options": {
      "dhl_paperless_trade": true,
      "insurance": 1000,
      "currency": "USD",
      "dhl_saturday_delivery": false
    },
    "metadata": {
      "order_id": "INTL-2024-045",
      "priority": "express"
    }
  }'
```

#### Example 3: Purchase Label for DHL Parcel DE Shipment

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dhl_parcel_de_789/shipments/shp_draft789/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "label_type": "PDF_A4",
    "options": {
      "dhl_parcel_de_preferred_day": "2024-01-25",
      "dhl_parcel_de_preferred_location": "Backyard",
      "dhl_parcel_de_visual_check_of_age": "A16",
      "currency": "EUR"
    },
    "metadata": {
      "channel": "web",
      "warehouse": "DE-BERLIN-01"
    },
    "reference": "DE-SHIP-2024-123"
  }'
```

#### Example 4: Purchase Label for DPD Express Shipment

```bash
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dpd_express_10h/shipments/shp_draft101/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "label_type": "PDF",
    "options": {
      "dpd_saturday_delivery": true,
      "dpd_parcel_shop_delivery": null,
      "currency": "EUR",
      "insurance": 400
    },
    "metadata": {
      "channel": "b2b",
      "priority": "express",
      "delivery_window": "10:00"
    },
    "reference": "DPD-EXPRESS-2024-456"
  }'
```

#### Response Example

```json
{
  "id": "shp_draft123",
  "object_type": "shipment",
  "status": "purchased",
  "carrier_name": "ups",
  "carrier_id": "car_ups12345",
  "tracking_number": "1Z999AA10123456785",
  "tracking_url": "/v1/trackers/ups/1Z999AA10123456785",
  "shipment_identifier": "1Z999AA10123456785",
  "label_type": "PDF",
  "label_url": "https://api.karrio.io/labels/shp_draft123.pdf",
  "selected_rate": {
    "id": "rat_selected789",
    "carrier_name": "ups",
    "carrier_id": "car_ups12345",
    "service": "ups_standard",
    "currency": "USD",
    "total_charge": 38.75,
    "transit_days": 3
  },
  "options": {
    "insurance": 200,
    "signature_required": false,
    "shipping_date": "2024-01-17T10:35:00Z"
  },
  "metadata": {
    "order_id": "ORD-2024-001",
    "customer_ref": "CUST-12345"
  },
  "reference": "ORDER-2024-001",
  "service": "ups_standard",
  "carrier_id": "car_ups12345",
  "test_mode": false,
  "created_at": "2024-01-17T09:15:22.987654Z",
  "messages": []
}
```

---

## Complete Examples

### Scenario 1: E-commerce Platform with Multiple Shipping Options

Create shipping methods for different service levels:

```bash
# 1. Create Economy Shipping Method (UPS Ground)
curl -X POST "http://localhost:5002/graphql" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) { create_shipping_method(input: $data) { shipping_method { id name slug carrier_service } } }",
    "variables": {
      "data": {
        "name": "Economy Shipping",
        "description": "Standard ground shipping, 3-5 business days",
        "carrier_code": "ups",
        "carrier_service": "ups_standard",
        "carrier_id": "car_ups12345",
        "carrier_options": {
          "insurance": 50
        },
        "is_active": true,
        "metadata": {
          "service_level": "economy",
          "max_days": 5
        }
      }
    }
  }'

# 2. Create Express Shipping Method (UPS Next Day)
curl -X POST "http://localhost:5002/graphql" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) { create_shipping_method(input: $data) { shipping_method { id name slug carrier_service } } }",
    "variables": {
      "data": {
        "name": "Express Overnight",
        "description": "Next business day delivery",
        "carrier_code": "ups",
        "carrier_service": "ups_next_day_air",
        "carrier_id": "car_ups12345",
        "carrier_options": {
          "insurance": 100,
          "signature_required": true
        },
        "is_active": true,
        "metadata": {
          "service_level": "express",
          "max_days": 1
        }
      }
    }
  }'

# 3. Create International Shipping Method (DHL Express)
curl -X POST "http://localhost:5002/graphql" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) { create_shipping_method(input: $data) { shipping_method { id name slug carrier_service } } }",
    "variables": {
      "data": {
        "name": "International Express",
        "description": "Fast worldwide shipping via DHL",
        "carrier_code": "dhl_express",
        "carrier_service": "dhl_express_worldwide",
        "carrier_id": "car_dhl67890",
        "carrier_options": {
          "insurance": 500,
          "dhl_paperless_trade": true
        },
        "is_active": true,
        "metadata": {
          "service_level": "international",
          "regions": ["EU", "ASIA", "LATAM"]
        }
      }
    }
  }'
```

### Scenario 2: Multi-Carrier Strategy

Use different carriers for different regions:

```bash
# US Domestic - UPS Ground
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_ups_ground_us/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "123 Main St",
      "person_name": "John Doe",
      "city": "Los Angeles",
      "country_code": "US",
      "postal_code": "90001",
      "state_code": "CA",
      "phone_number": "555-0100"
    },
    "shipper": {
      "address_line1": "456 Warehouse Blvd",
      "person_name": "Jane Smith",
      "city": "New York",
      "country_code": "US",
      "postal_code": "10001",
      "state_code": "NY",
      "phone_number": "555-0200"
    },
    "parcels": [{"weight": 5, "weight_unit": "LB"}],
    "payment": {"currency": "USD", "paid_by": "sender"}
  }'

# Germany Domestic - DHL Parcel DE
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dhl_parcel_de/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "Hauptstraße 10",
      "person_name": "Klaus Müller",
      "city": "Hamburg",
      "country_code": "DE",
      "postal_code": "20095",
      "phone_number": "+49 40 12345678"
    },
    "shipper": {
      "address_line1": "Lagerstraße 5",
      "person_name": "Anna Weber",
      "city": "Berlin",
      "country_code": "DE",
      "postal_code": "10115",
      "phone_number": "+49 30 98765432"
    },
    "parcels": [{"weight": 2, "weight_unit": "KG"}],
    "payment": {"currency": "EUR", "paid_by": "sender"}
  }'

# International - DHL Express
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dhl_express_intl/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "10 Oxford St",
      "person_name": "James Wilson",
      "city": "London",
      "country_code": "GB",
      "postal_code": "W1D 1BS",
      "phone_number": "+44 20 12345678"
    },
    "shipper": {
      "address_line1": "456 Warehouse Blvd",
      "person_name": "Jane Smith",
      "city": "New York",
      "country_code": "US",
      "postal_code": "10001",
      "state_code": "NY",
      "phone_number": "555-0200"
    },
    "parcels": [{"weight": 3.5, "weight_unit": "KG"}],
    "payment": {"currency": "USD", "paid_by": "sender"},
    "customs": {
      "content_type": "merchandise",
      "incoterm": "DDP",
      "items": [{
        "description": "Electronics",
        "quantity": 1,
        "value_amount": 300,
        "value_currency": "USD",
        "weight": 3.5,
        "weight_unit": "KG",
        "origin_country": "US",
        "hs_code": "8517.12.0000"
      }]
    }
  }'

# European Cross-Border - DPD Express 12h
curl -X POST "http://localhost:5002/v1/shipping-methods/mtd_dpd_express_12h/labels" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "address_line1": "Avenue des Champs-Élysées 101",
      "person_name": "Pierre Lefevre",
      "company_name": "Paris Boutique",
      "city": "Paris",
      "country_code": "FR",
      "postal_code": "75008",
      "phone_number": "+33 1 45 62 34 56"
    },
    "shipper": {
      "address_line1": "Breitscheidstraße 25",
      "person_name": "Petra Schmidt",
      "company_name": "Stuttgart Logistics",
      "city": "Stuttgart",
      "country_code": "DE",
      "postal_code": "70174",
      "phone_number": "+49 711 12345678"
    },
    "parcels": [{"weight": 5.5, "weight_unit": "KG"}],
    "payment": {"currency": "EUR", "paid_by": "sender"},
    "options": {
      "dpd_saturday_delivery": false,
      "insurance": 250
    }
  }'
```

---

## Error Handling

### Common Error Codes

| Status Code | Error Type         | Description                                                |
| ----------- | ------------------ | ---------------------------------------------------------- |
| 400         | `bad_request`      | Invalid request parameters or missing required fields      |
| 401         | `unauthorized`     | Missing or invalid authentication token                    |
| 404         | `not_found`        | Shipping method or shipment not found                      |
| 422         | `validation_error` | Validation failed (e.g., invalid address, carrier service) |
| 424         | `carrier_error`    | Carrier API returned an error                              |
| 500         | `server_error`     | Internal server error                                      |

### Error Response Format

```json
{
  "errors": [
    {
      "code": "validation_error",
      "message": "Invalid postal code format",
      "details": {
        "field": "recipient.postal_code",
        "value": "INVALID",
        "constraint": "Must be 5 digits for US addresses"
      }
    }
  ]
}
```

### Carrier Error Response

```json
{
  "errors": [
    {
      "code": "carrier_error",
      "carrier": "ups",
      "message": "Address validation failed",
      "details": "The recipient city does not match the postal code"
    }
  ],
  "messages": [
    {
      "carrier_name": "ups",
      "carrier_id": "car_ups12345",
      "message": "City/State/Zip combination is invalid",
      "code": "INVALID_ADDRESS",
      "details": {}
    }
  ]
}
```

---

## Carrier-Specific Options

### UPS Options

```json
{
  "options": {
    "signature_required": true,
    "insurance": 100,
    "saturday_delivery": true,
    "hold_for_pickup": true,
    "delivery_confirmation": "adult_signature"
  }
}
```

### DHL Express Options

```json
{
  "options": {
    "dhl_paperless_trade": true,
    "dhl_saturday_delivery": true,
    "insurance": 500,
    "dhl_duties_and_taxes_paid": true,
    "dhl_delivery_signature": true
  }
}
```

### DHL Parcel DE Options

```json
{
  "options": {
    "dhl_parcel_de_preferred_day": "2024-01-25",
    "dhl_parcel_de_preferred_location": "Garage",
    "dhl_parcel_de_preferred_neighbour": "Apt 2B",
    "dhl_parcel_de_visual_check_of_age": "A16",
    "dhl_parcel_de_no_neighbour_delivery": true,
    "dhl_parcel_de_named_person_only": true,
    "dhl_parcel_de_additional_insurance": 250
  }
}
```

### DPD Options

```json
{
  "options": {
    "dpd_saturday_delivery": true,
    "dpd_ex_works_delivery": false,
    "dpd_parcel_shop_delivery": "PARCELSHOP_ID_12345",
    "dpd_tyres": false,
    "insurance": 200
  }
}
```

**Available DPD Services:**
- `dpd_cl` - DPD Classic
- `dpd_express_10h` - DPD Express 10:00
- `dpd_express_12h` - DPD Express 12:00
- `dpd_express_18h_guarantee` - DPD Express 18:00 with guarantee

---

## Best Practices

1. **Create Shipping Methods for Common Scenarios**: Pre-configure shipping methods for your most common shipping scenarios (domestic economy, express, international, etc.)

2. **Use Metadata**: Store custom information in the metadata field to track business-specific data (customer segments, fulfillment centers, priority levels)

3. **Handle Errors Gracefully**: Always check for carrier errors and validation issues. Provide clear feedback to users.

4. **Test Mode**: Use `test_mode: true` carrier connections during development to avoid creating real labels and charges.

5. **Address Validation**: Validate addresses before submitting to reduce carrier errors and ensure successful delivery.

6. **Customs Documentation**: Always include complete customs information for international shipments to avoid delays.

7. **Option Overrides**: When buying labels, you can override shipping method options in the request payload for shipment-specific requirements.

---

## Support

For additional support:
- **API Reference**: http://localhost:5002/shipping/redoc
- **Carrier Specs**: `GET http://localhost:5002/v1/carriers`
- **Service References**: `GET http://localhost:5002/v1/references`
- **GraphQL Playground**: http://localhost:5002/graphql

---

*Last Updated: January 2025*
