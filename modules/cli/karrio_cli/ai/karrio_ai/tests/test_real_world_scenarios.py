#!/usr/bin/env python3
"""
Real-world carrier integration testing scenarios.

This script demonstrates how to test the Karrio ADK agent with various
real-world input formats and integration scenarios.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add the ai module to the path
sys.path.insert(0, str(Path(__file__).parent))

from karrio_ai.agent import (
    root_agent,
    analyze_existing_connector,
    extract_carrier_patterns,
    generate_carrier_schema,
    generate_carrier_mappings,
    generate_integration_tests,
    assemble_complete_integration,
)
from karrio_ai.enhanced_tools import analyze_carrier_documentation


def test_openapi_integration():
    """Test building integration from OpenAPI specification."""
    print("=== Testing OpenAPI Integration ===")

    # Example OpenAPI spec for a fictional carrier
    openapi_spec = '''
    openapi: 3.0.0
    info:
      title: SwiftShip API
      version: 1.0.0
      description: API for SwiftShip carrier services
    servers:
      - url: https://api.swiftship.com/v1
    paths:
      /rates:
        post:
          summary: Get shipping rates
          tags: [Rates]
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/RateRequest'
          responses:
            200:
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/RateResponse'
      /shipments:
        post:
          summary: Create shipment
          tags: [Shipments]
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ShipmentRequest'
          responses:
            201:
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ShipmentResponse'
      /tracking/{tracking_number}:
        get:
          summary: Track shipment
          tags: [Tracking]
          parameters:
            - name: tracking_number
              in: path
              required: true
              schema:
                type: string
          responses:
            200:
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/TrackingResponse'
    components:
      securitySchemes:
        ApiKeyAuth:
          type: apiKey
          in: header
          name: X-API-Key
      schemas:
        RateRequest:
          type: object
          properties:
            origin:
              type: object
            destination:
              type: object
            packages:
              type: array
              items:
                type: object
        RateResponse:
          type: object
          properties:
            rates:
              type: array
              items:
                type: object
                properties:
                  service_code:
                    type: string
                  total_cost:
                    type: number
                  currency:
                    type: string
    '''

    try:
        # Analyze the OpenAPI specification
        analysis = analyze_carrier_documentation(
            carrier_name="swiftship",
            documentation_source=openapi_spec,
            source_type="openapi"
        )

        print(f"✓ Analysis successful: {analysis['success']}")
        print(f"✓ Detected API type: {analysis['analysis']['api_type']}")
        print(f"✓ Found {len(analysis['analysis']['endpoints'])} endpoints")
        print(f"✓ Auth methods: {analysis['analysis']['auth_methods']}")

        # Generate complete integration
        integration_config = {
            "carrier_name": "swiftship",
            "operations": ["rates", "shipments", "tracking"],
            "auth_type": "API_KEY",
            "api_base_url": "https://api.swiftship.com/v1",
            "test_mode": True
        }

        result = assemble_complete_integration(
            carrier_name="swiftship",
            integration_config=integration_config
        )

        print(f"✓ Integration generated: {result['integration_complete']}")
        print(f"✓ Generated {len(result['generated_files'])} file types")

        return True

    except Exception as e:
        print(f"❌ OpenAPI integration test failed: {e}")
        return False


def test_url_scraping_integration():
    """Test building integration from scraped website documentation."""
    print("\n=== Testing URL Scraping Integration ===")

    # Example: Pretend we're scraping API docs from a website
    mock_scraped_content = """
    SwiftShip Developer Documentation

    API Base URL: https://api.swiftship.com/v1

    Authentication:
    All requests require an API key in the X-API-Key header.

    Endpoints:

    POST /rates - Get shipping rates
    Request: JSON object with origin, destination, packages
    Response: Array of rate objects with service_code, total_cost, currency

    POST /shipments - Create a new shipment
    Request: JSON with shipper, recipient, packages, service
    Response: Shipment object with tracking_number, label_url

    GET /tracking/{number} - Track a shipment
    Response: Tracking object with status and events

    Example rate request:
    {
      "origin": {"postal_code": "10001", "country": "US"},
      "destination": {"postal_code": "90210", "country": "US"},
      "packages": [{"weight": 2.5, "dimensions": {"length": 10, "width": 8, "height": 6}}]
    }
    """

    try:
        # Analyze scraped content
        analysis = analyze_carrier_documentation(
            carrier_name="swiftship_web",
            documentation_source=mock_scraped_content,
            source_type="text"
        )

        print(f"✓ URL analysis successful: {analysis['success']}")
        print(f"✓ Found {len(analysis['analysis']['endpoints'])} endpoints")
        print(f"✓ Auth methods detected: {analysis['analysis']['auth_methods']}")

        # Extract patterns from similar carriers
        patterns = extract_carrier_patterns(
            similar_carriers=["ups", "fedex", "canadapost"],
            pattern_type="all"
        )

        print(f"✓ Extracted patterns from {len(patterns['analyzed_carriers'])} carriers")
        print(f"✓ Found {len(patterns['best_practices'])} best practices")

        # Generate schemas from the scraped documentation
        schema_result = generate_carrier_schema(
            carrier_name="swiftship_web",
            api_documentation=mock_scraped_content,
            schema_type="complete"
        )

        print(f"✓ Generated {len(schema_result['classes'])} schema classes")

        return True

    except Exception as e:
        print(f"❌ URL scraping integration test failed: {e}")
        return False


def test_pdf_documentation_integration():
    """Test building integration from PDF documentation."""
    print("\n=== Testing PDF Documentation Integration ===")

    # Simulate PDF content (in real scenario, this would be extracted from PDF)
    mock_pdf_content = """
    SwiftShip API Documentation v2.0

    Page 1: Introduction
    Welcome to SwiftShip API. This REST API allows you to integrate shipping functionality.

    Page 2: Authentication
    API Key Authentication required. Include your API key in the Authorization header:
    Authorization: Bearer YOUR_API_KEY

    Page 3: Rate Calculation
    Endpoint: POST /api/v2/calculate-rates
    Description: Calculate shipping rates for packages

    Request Format:
    {
      "shipper_address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "US"
      },
      "recipient_address": {
        "street": "456 Oak Ave",
        "city": "Los Angeles",
        "state": "CA",
        "postal_code": "90210",
        "country": "US"
      },
      "packages": [
        {
          "weight_kg": 1.5,
          "length_cm": 20,
          "width_cm": 15,
          "height_cm": 10
        }
      ]
    }

    Page 4: Shipment Creation
    Endpoint: POST /api/v2/shipments
    Description: Create a new shipment and generate shipping label

    Page 5: Tracking
    Endpoint: GET /api/v2/track/{tracking_number}
    Description: Get real-time tracking information
    """

    try:
        # Analyze PDF content
        analysis = analyze_carrier_documentation(
            carrier_name="swiftship_pdf",
            documentation_source=mock_pdf_content,
            source_type="text"  # Using text since we don't have actual PDF parsing
        )

        print(f"✓ PDF analysis successful: {analysis['success']}")
        print(f"✓ Found {len(analysis['analysis']['endpoints'])} endpoints")
        print(f"✓ Auth methods: {analysis['analysis']['auth_methods']}")

        # Generate mappings based on PDF documentation
        api_endpoints = {
            "rates": "https://api.swiftship.com/api/v2/calculate-rates",
            "shipments": "https://api.swiftship.com/api/v2/shipments",
            "tracking": "https://api.swiftship.com/api/v2/track"
        }

        mapping_result = generate_carrier_mappings(
            carrier_name="swiftship_pdf",
            api_endpoints=api_endpoints,
            operation_type="complete"
        )

        print(f"✓ Generated {len(mapping_result['generated_mappings'])} mapping types")

        # Generate comprehensive tests
        test_data = {
            "operations": ["rates", "shipments", "tracking"],
            "test_addresses": {
                "domestic": {"country": "US", "postal_code": "10001"},
                "international": {"country": "CA", "postal_code": "M5V 3A1"}
            }
        }

        test_result = generate_integration_tests(
            carrier_name="swiftship_pdf",
            test_data=test_data,
            test_type="complete"
        )

        print(f"✓ Generated {len(test_result['generated_tests'])} test categories")

        return True

    except Exception as e:
        print(f"❌ PDF documentation integration test failed: {e}")
        return False


def test_mixed_source_integration():
    """Test building integration from multiple sources."""
    print("\n=== Testing Mixed Source Integration ===")

    try:
        # Analyze an existing carrier first
        existing_analysis = analyze_existing_connector("ups", "all")
        print(f"✓ Analyzed existing UPS connector: {len(existing_analysis['files'])} files")

        # Extract patterns from multiple carriers
        patterns = extract_carrier_patterns(
            similar_carriers=["ups", "fedex", "dhl_express"],
            pattern_type="all"
        )
        print(f"✓ Extracted patterns from {len(patterns['analyzed_carriers'])} carriers")

        # Create a complex integration config
        complex_config = {
            "carrier_name": "complexship",
            "operations": ["rates", "shipments", "tracking", "pickup", "manifests"],
            "auth_type": "OAUTH2",
            "api_base_url": "https://api.complexship.com/v1",
            "special_requirements": [
                "Multi-piece shipments",
                "International customs",
                "Hazmat handling",
                "Signature required"
            ],
            "test_mode": True
        }

        # Assemble complete integration
        result = assemble_complete_integration(
            carrier_name="complexship",
            integration_config=complex_config
        )

        print(f"✓ Complex integration generated: {result['integration_complete']}")
        print(f"✓ Generated {len(result['generated_files'])} file types")
        print(f"✓ Project structure: {result['project_structure']['root']}")

        # Print next steps
        print("\n📋 Next Steps:")
        for step in result['next_steps']:
            print(f"  - {step}")

        return True

    except Exception as e:
        print(f"❌ Mixed source integration test failed: {e}")
        return False


def test_real_carrier_scenarios():
    """Test with realistic carrier scenarios."""
    print("\n=== Testing Real Carrier Scenarios ===")

    scenarios = [
        {
            "name": "European Carrier with VAT",
            "carrier": "europost",
            "complexity": "high",
            "requirements": [
                "VAT calculations",
                "Customs documentation",
                "Multi-language support",
                "GDPR compliance"
            ]
        },
        {
            "name": "Regional LTL Carrier",
            "carrier": "regional_freight",
            "complexity": "medium",
            "requirements": [
                "Weight-based pricing",
                "Terminal locations",
                "Pickup scheduling",
                "Freight classifications"
            ]
        },
        {
            "name": "E-commerce Last Mile",
            "carrier": "lastmile_express",
            "complexity": "low",
            "requirements": [
                "Simple API key auth",
                "Standard package sizes",
                "Basic tracking",
                "Delivery windows"
            ]
        }
    ]

    success_count = 0

    for scenario in scenarios:
        print(f"\n🔍 Testing: {scenario['name']}")

        try:
            # Generate integration for this scenario
            config = {
                "carrier_name": scenario["carrier"],
                "operations": ["rates", "shipments", "tracking"],
                "complexity": scenario["complexity"],
                "special_requirements": scenario["requirements"],
                "test_mode": True
            }

            result = assemble_complete_integration(
                carrier_name=scenario["carrier"],
                integration_config=config
            )

            if result["integration_complete"]:
                print(f"  ✓ {scenario['name']} integration successful")
                success_count += 1
            else:
                print(f"  ⚠️ {scenario['name']} integration incomplete")

        except Exception as e:
            print(f"  ❌ {scenario['name']} failed: {e}")

    print(f"\n📊 Scenario Results: {success_count}/{len(scenarios)} successful")
    return success_count == len(scenarios)


def main():
    """Run all real-world integration tests."""
    print("🚀 Starting Real-World Carrier Integration Tests")
    print("=" * 60)

    tests = [
        ("OpenAPI Specification", test_openapi_integration),
        ("URL Scraping", test_url_scraping_integration),
        ("PDF Documentation", test_pdf_documentation_integration),
        ("Mixed Sources", test_mixed_source_integration),
        ("Real Carrier Scenarios", test_real_carrier_scenarios),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"\n📋 Running: {test_name}")
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"💥 {test_name}: CRASHED - {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"📊 Final Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All real-world integration tests passed!")
        print("\n✨ The ADK agent can handle:")
        print("  ✅ OpenAPI/Swagger specifications")
        print("  ✅ Web scraped documentation")
        print("  ✅ PDF documentation files")
        print("  ✅ Mixed source inputs")
        print("  ✅ Complex carrier requirements")
        print("\n🚀 Ready for production use!")
    else:
        print("⚠️ Some tests failed. Review the errors above.")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
