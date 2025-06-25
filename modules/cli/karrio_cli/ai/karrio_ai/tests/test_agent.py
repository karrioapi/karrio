#!/usr/bin/env python3
"""
Test script for the enhanced Karrio ADK agent with RAG capabilities.

This script tests the multi-agent architecture, RAG system integration,
and tool functions for carrier integration generation.
"""

import sys
import os
import json
from pathlib import Path

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
    RAG_SYSTEM
)


def test_rag_system():
    """Test the RAG system functionality."""
    print("=== Testing RAG System ===")

    try:
        # Test pattern search
        auth_patterns = RAG_SYSTEM.search_patterns("auth", limit=3)
        print(f"Found {len(auth_patterns)} authentication patterns")

        mapping_patterns = RAG_SYSTEM.search_patterns("mapping", limit=3)
        print(f"Found {len(mapping_patterns)} mapping patterns")

        schema_patterns = RAG_SYSTEM.search_patterns("schema", limit=3)
        print(f"Found {len(schema_patterns)} schema patterns")

        # Test carrier similarity
        test_carrier_info = {
            'api_type': 'REST',
            'auth_type': 'API_KEY',
            'operations': ['rates', 'shipments', 'tracking']
        }
        similar_carriers = RAG_SYSTEM.get_similar_carriers(test_carrier_info)
        print(f"Found similar carriers: {similar_carriers}")

        # Test implementation examples
        rate_examples = RAG_SYSTEM.get_implementation_examples("rate")
        print(f"Found {len(rate_examples)} rate implementation examples")

        print("✅ RAG system tests passed")
        return True

    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        return False


def test_analyze_existing_connector():
    """Test the analyze_existing_connector tool."""
    print("\n=== Testing Connector Analysis ===")

    try:
        # Test with UPS connector
        ups_analysis = analyze_existing_connector("ups", "all")

        if "error" in ups_analysis:
            print(f"UPS analysis error: {ups_analysis['error']}")
            return False

        print(f"UPS analysis completed for carrier: {ups_analysis.get('carrier_name', 'unknown')}")
        print(f"Found {len(ups_analysis.get('files', []))} files")
        print(f"Structure components: {ups_analysis.get('structure', {})}")

        if 'mapping_patterns' in ups_analysis:
            print(f"Found {len(ups_analysis['mapping_patterns'])} mapping patterns")

        if 'schema_patterns' in ups_analysis:
            print(f"Found {len(ups_analysis['schema_patterns'])} schema patterns")

        print("✅ Connector analysis tests passed")
        return True

    except Exception as e:
        print(f"❌ Connector analysis test failed: {e}")
        return False


def test_extract_carrier_patterns():
    """Test the extract_carrier_patterns tool."""
    print("\n=== Testing Pattern Extraction ===")

    try:
        # Test pattern extraction from similar carriers
        patterns = extract_carrier_patterns(
            similar_carriers=["ups", "fedex", "canadapost"],
            pattern_type="mapping"
        )

        if "error" in patterns:
            print(f"Pattern extraction error: {patterns['error']}")
            return False

        print(f"Analyzed carriers: {patterns['analyzed_carriers']}")
        print(f"Pattern type: {patterns['pattern_type']}")
        print(f"Found common patterns for {len(patterns['common_patterns'])} carriers")

        if 'best_practices' in patterns:
            print(f"Extracted {len(patterns['best_practices'])} best practices")
            for bp in patterns['best_practices'][:2]:
                print(f"  - {bp['description'][:50]}... (confidence: {bp['confidence']})")

        print("✅ Pattern extraction tests passed")
        return True

    except Exception as e:
        print(f"❌ Pattern extraction test failed: {e}")
        return False


def test_generate_carrier_schema():
    """Test the generate_carrier_schema tool."""
    print("\n=== Testing Schema Generation ===")

    try:
        # Test with sample JSON schema
        sample_json_schema = '''
        {
            "type": "object",
            "properties": {
                "rate_id": {"type": "string"},
                "service_name": {"type": "string"},
                "total_cost": {"type": "number"},
                "currency": {"type": "string"},
                "delivery_days": {"type": "integer"}
            }
        }
        '''

        schema_result = generate_carrier_schema(
            carrier_name="test_carrier",
            api_documentation=sample_json_schema,
            schema_type="rates"
        )

        if "error" in schema_result:
            print(f"Schema generation error: {schema_result['error']}")
            return False

        print(f"Generated schemas for: {schema_result['carrier']}")
        print(f"Schema type: {schema_result['schema_type']}")
        print(f"Found {len(schema_result['classes'])} classes")
        print(f"Required imports: {len(schema_result['imports'])}")

        print("✅ Schema generation tests passed")
        return True

    except Exception as e:
        print(f"❌ Schema generation test failed: {e}")
        return False


def test_generate_carrier_mappings():
    """Test the generate_carrier_mappings tool."""
    print("\n=== Testing Mapping Generation ===")

    try:
        # Test mapping generation
        api_endpoints = {
            "rates": "https://api.testcarrier.com/v1/rates",
            "shipments": "https://api.testcarrier.com/v1/shipments",
            "tracking": "https://api.testcarrier.com/v1/tracking"
        }

        mapping_result = generate_carrier_mappings(
            carrier_name="test_carrier",
            api_endpoints=api_endpoints,
            operation_type="complete"
        )

        if "error" in mapping_result:
            print(f"Mapping generation error: {mapping_result['error']}")
            return False

        print(f"Generated mappings for: {mapping_result['carrier']}")
        print(f"Operation type: {mapping_result['operation_type']}")
        print(f"Generated {len(mapping_result['generated_mappings'])} mapping types")
        print(f"API endpoints: {list(mapping_result['endpoints'].keys())}")

        print("✅ Mapping generation tests passed")
        return True

    except Exception as e:
        print(f"❌ Mapping generation test failed: {e}")
        return False


def test_generate_integration_tests():
    """Test the generate_integration_tests tool."""
    print("\n=== Testing Test Generation ===")

    try:
        # Test test generation
        test_data = {
            "operations": ["rates", "shipments", "tracking"],
            "test_addresses": {
                "domestic": {"country": "US", "postal_code": "10001"},
                "international": {"country": "CA", "postal_code": "M5V 3A1"}
            }
        }

        test_result = generate_integration_tests(
            carrier_name="test_carrier",
            test_data=test_data,
            test_type="complete"
        )

        if "error" in test_result:
            print(f"Test generation error: {test_result['error']}")
            return False

        print(f"Generated tests for: {test_result['carrier']}")
        print(f"Test type: {test_result['test_type']}")
        print(f"Generated {len(test_result['generated_tests'])} test categories")

        print("✅ Test generation tests passed")
        return True

    except Exception as e:
        print(f"❌ Test generation test failed: {e}")
        return False


def test_assemble_complete_integration():
    """Test the assemble_complete_integration tool."""
    print("\n=== Testing Integration Assembly ===")

    try:
        # Test complete integration assembly
        integration_config = {
            "carrier_name": "test_carrier",
            "operations": ["rates", "shipments", "tracking"],
            "auth_type": "API_KEY",
            "api_base_url": "https://api.testcarrier.com/v1",
            "test_mode": True
        }

        assembly_result = assemble_complete_integration(
            carrier_name="test_carrier",
            integration_config=integration_config
        )

        if "error" in assembly_result:
            print(f"Integration assembly error: {assembly_result['error']}")
            return False

        print(f"Assembled integration for: {assembly_result['carrier']}")
        print(f"Integration complete: {assembly_result['integration_complete']}")
        print(f"Generated {len(assembly_result['generated_files'])} file types")
        print(f"Project structure: {assembly_result['project_structure']['root']}")
        print(f"Next steps: {len(assembly_result['next_steps'])} items")

        for step in assembly_result['next_steps']:
            print(f"  - {step}")

        print("✅ Integration assembly tests passed")
        return True

    except Exception as e:
        print(f"❌ Integration assembly test failed: {e}")
        return False


def test_agent_integration():
    """Test the complete agent integration."""
    print("\n=== Testing Agent Integration ===")

    try:
        # Test that all agents are properly configured
        print(f"Root agent: {root_agent.name}")
        print(f"Sub-agents: {len(root_agent.sub_agents)}")

        # Verify agent names
        agent_names = [agent.name for agent in root_agent.sub_agents]
        expected_agents = ["schema_agent", "mapping_agent", "integration_agent", "testing_agent"]

        for expected in expected_agents:
            if expected in agent_names:
                print(f"✅ {expected} is configured")
            else:
                print(f"❌ {expected} is missing")
                return False

        print("✅ Agent integration tests passed")
        return True

    except Exception as e:
        print(f"❌ Agent integration test failed: {e}")
        return False


def run_all_tests():
    """Run all test functions."""
    print("🚀 Starting Karrio ADK Agent Tests")
    print("=" * 50)

    tests = [
        test_rag_system,
        test_analyze_existing_connector,
        test_extract_carrier_patterns,
        test_generate_carrier_schema,
        test_generate_carrier_mappings,
        test_generate_integration_tests,
        test_assemble_complete_integration,
        test_agent_integration
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed! The ADK agent is ready for use.")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
