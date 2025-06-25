#!/usr/bin/env python3
"""
Real integration test to evaluate how close we are to 95% completion.

This test simulates building a complete carrier integration and
evaluates the quality and completeness of generated components.
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


def test_real_world_integration():
    """Test building a complete integration for a hypothetical carrier."""
    print("=== Testing Real-World Integration Generation ===")

    # Simulate a new carrier - "SwiftShip"
    carrier_config = {
        "name": "swiftship",
        "display_name": "SwiftShip Express",
        "api_type": "REST",
        "auth_type": "API_KEY",
        "base_url": "https://api.swiftship.com/v2",
        "operations": ["rates", "shipments", "tracking"],
        "countries": ["US", "CA", "MX"],
        "test_mode_supported": True
    }

    # Sample API documentation
    api_docs = {
        "rate_request": {
            "endpoint": "/rates/quote",
            "method": "POST",
            "schema": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "object",
                        "properties": {
                            "postal_code": {"type": "string"},
                            "country_code": {"type": "string"}
                        }
                    },
                    "destination": {
                        "type": "object",
                        "properties": {
                            "postal_code": {"type": "string"},
                            "country_code": {"type": "string"}
                        }
                    },
                    "packages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "weight": {"type": "number"},
                                "length": {"type": "number"},
                                "width": {"type": "number"},
                                "height": {"type": "number"}
                            }
                        }
                    }
                }
            }
        },
        "rate_response": {
            "schema": {
                "type": "object",
                "properties": {
                    "rates": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "service_code": {"type": "string"},
                                "service_name": {"type": "string"},
                                "total_cost": {"type": "number"},
                                "currency": {"type": "string"},
                                "delivery_days": {"type": "integer"},
                                "surcharges": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "amount": {"type": "number"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    results = {}

    try:
        # Step 1: Analyze similar carriers
        print("\n1. Analyzing similar carriers...")
        similar_analysis = analyze_existing_connector("fedex", "all")
        results["similar_analysis"] = {
            "success": "error" not in similar_analysis,
            "files_found": len(similar_analysis.get("files", [])),
            "patterns_found": len(similar_analysis.get("patterns", []))
        }
        print(f"✓ Found {results['similar_analysis']['files_found']} files and {results['similar_analysis']['patterns_found']} patterns")

        # Step 2: Extract patterns from multiple carriers
        print("\n2. Extracting patterns from similar carriers...")
        patterns = extract_carrier_patterns(
            similar_carriers=["fedex", "ups", "canadapost"],
            pattern_type="all"
        )
        results["pattern_extraction"] = {
            "success": "error" not in patterns,
            "carriers_analyzed": len(patterns.get("analyzed_carriers", [])),
            "best_practices": len(patterns.get("best_practices", [])),
            "code_examples": len(patterns.get("code_examples", {}))
        }
        print(f"✓ Analyzed {results['pattern_extraction']['carriers_analyzed']} carriers, found {results['pattern_extraction']['best_practices']} best practices")

        # Step 3: Generate schemas
        print("\n3. Generating schemas...")
        rate_schema = generate_carrier_schema(
            carrier_name="swiftship",
            api_documentation=json.dumps(api_docs["rate_response"]["schema"]),
            schema_type="rates"
        )
        results["schema_generation"] = {
            "success": "error" not in rate_schema,
            "classes_generated": len(rate_schema.get("classes", [])),
            "imports_needed": len(rate_schema.get("imports", []))
        }
        print(f"✓ Generated {results['schema_generation']['classes_generated']} classes with {results['schema_generation']['imports_needed']} imports")

        # Step 4: Generate mappings
        print("\n4. Generating mappings...")
        mappings = generate_carrier_mappings(
            carrier_name="swiftship",
            api_endpoints={
                "rates": "https://api.swiftship.com/v2/rates/quote",
                "shipments": "https://api.swiftship.com/v2/shipments/create",
                "tracking": "https://api.swiftship.com/v2/tracking/status"
            },
            operation_type="complete"
        )
        results["mapping_generation"] = {
            "success": "error" not in mappings,
            "mappings_generated": len(mappings.get("generated_mappings", {})),
            "endpoints_covered": len(mappings.get("endpoints", {}))
        }
        print(f"✓ Generated {results['mapping_generation']['mappings_generated']} mappings for {results['mapping_generation']['endpoints_covered']} endpoints")

        # Step 5: Generate tests
        print("\n5. Generating tests...")
        test_data = {
            "operations": ["rates", "shipments", "tracking"],
            "test_addresses": {
                "domestic": {"country": "US", "postal_code": "90210"},
                "international": {"country": "CA", "postal_code": "M5V 3A1"}
            },
            "test_packages": [
                {"weight": 5.0, "length": 10, "width": 8, "height": 6},
                {"weight": 25.0, "length": 20, "width": 16, "height": 12}
            ]
        }
        tests = generate_integration_tests(
            carrier_name="swiftship",
            test_data=test_data,
            test_type="complete"
        )
        results["test_generation"] = {
            "success": "error" not in tests,
            "test_categories": len(tests.get("generated_tests", {})),
            "test_files": len(tests.get("test_files", []))
        }
        print(f"✓ Generated {results['test_generation']['test_categories']} test categories")

        # Step 6: Assemble complete integration
        print("\n6. Assembling complete integration...")
        integration = assemble_complete_integration(
            carrier_name="swiftship",
            integration_config=carrier_config
        )
        results["integration_assembly"] = {
            "success": "error" not in integration and integration.get("integration_complete", False),
            "files_generated": len(integration.get("generated_files", {})),
            "next_steps": len(integration.get("next_steps", []))
        }
        print(f"✓ Integration complete: {results['integration_assembly']['success']}")
        print(f"✓ Generated {results['integration_assembly']['files_generated']} file types")

        return results

    except Exception as e:
        print(f"❌ Real-world integration test failed: {e}")
        return {"error": str(e)}


def evaluate_completion_percentage(results):
    """Evaluate how close we are to 95% completion."""
    print("\n=== Completion Evaluation ===")

    if "error" in results:
        print(f"❌ Integration failed: {results['error']}")
        return 0

    # Define completion criteria and weights
    criteria = {
        "similar_analysis": {"weight": 10, "max_score": 100},
        "pattern_extraction": {"weight": 15, "max_score": 100},
        "schema_generation": {"weight": 20, "max_score": 100},
        "mapping_generation": {"weight": 25, "max_score": 100},
        "test_generation": {"weight": 15, "max_score": 100},
        "integration_assembly": {"weight": 15, "max_score": 100}
    }

    total_score = 0
    max_possible = sum(c["weight"] for c in criteria.values())

    for criterion, config in criteria.items():
        if criterion in results:
            result = results[criterion]

            # Calculate success score for this criterion
            if result["success"]:
                if criterion == "similar_analysis":
                    score = min(100, (result["files_found"] / 400) * 100)  # Expect ~400 files for major carriers
                elif criterion == "pattern_extraction":
                    score = min(100, (result["best_practices"] / 10) * 50 + (result["code_examples"] / 5) * 50)
                elif criterion == "schema_generation":
                    score = min(100, (result["classes_generated"] / 3) * 100)  # Expect ~3 main classes
                elif criterion == "mapping_generation":
                    score = min(100, (result["mappings_generated"] / 3) * 100)  # rates, shipments, tracking
                elif criterion == "test_generation":
                    score = min(100, (result["test_categories"] / 3) * 100)  # unit, integration, fixtures
                elif criterion == "integration_assembly":
                    score = 100 if result["success"] else 0
                else:
                    score = 100
            else:
                score = 0

            weighted_score = (score / 100) * config["weight"]
            total_score += weighted_score

            print(f"{criterion}: {score:.1f}% (weight: {config['weight']}%, contribution: {weighted_score:.1f}%)")
        else:
            print(f"{criterion}: 0% (missing)")

    completion_percentage = (total_score / max_possible) * 100
    print(f"\n🎯 Overall Completion: {completion_percentage:.1f}%")

    if completion_percentage >= 95:
        print("🎉 Excellent! Ready for production use.")
    elif completion_percentage >= 85:
        print("✅ Good! Minor improvements needed.")
    elif completion_percentage >= 70:
        print("⚠️  Decent progress, but needs significant improvements.")
    else:
        print("❌ Major work needed to reach production readiness.")

    return completion_percentage


def identify_improvement_areas(results, completion_percentage):
    """Identify specific areas that need improvement."""
    print(f"\n=== Improvement Recommendations ===")

    improvements = []

    # Check each area and suggest improvements
    if "similar_analysis" in results and results["similar_analysis"]["files_found"] < 300:
        improvements.append("📁 Enhance connector analysis depth - currently analyzing fewer files than expected")

    if "pattern_extraction" in results and results["pattern_extraction"]["best_practices"] < 5:
        improvements.append("🧩 Improve pattern extraction - need more comprehensive best practice identification")

    if "schema_generation" in results and results["schema_generation"]["classes_generated"] < 2:
        improvements.append("📋 Enhance schema generation - should generate multiple related classes")

    if "mapping_generation" in results and results["mapping_generation"]["mappings_generated"] < 3:
        improvements.append("🔄 Complete mapping generation - need all operation types (rates, shipments, tracking)")

    if "test_generation" in results and results["test_generation"]["test_categories"] < 3:
        improvements.append("🧪 Expand test coverage - need unit, integration, and fixture generation")

    # Add priority improvements based on completion percentage
    if completion_percentage < 95:
        improvements.extend([
            "🚀 Implement actual file generation (currently just generates descriptions)",
            "🔧 Add validation of generated code syntax and imports",
            "📚 Enhance schema generation with actual API documentation parsing",
            "🎯 Implement carrier-specific customizations based on API characteristics",
            "🔍 Add comprehensive error handling and validation",
            "📈 Include performance optimization and caching",
            "🧩 Add support for complex authentication methods (OAuth, certificates)",
            "🌐 Support for international shipping requirements",
            "📊 Add real-time API testing and validation"
        ])

    if improvements:
        print("Priority improvements needed:")
        for i, improvement in enumerate(improvements[:5], 1):  # Show top 5
            print(f"{i}. {improvement}")
    else:
        print("🎉 No major improvements needed - ready for production!")

    return improvements


def main():
    """Run the real-world integration test and evaluation."""
    print("🚀 Starting Real-World Integration Test")
    print("=" * 60)

    # Run the complete integration test
    results = test_real_world_integration()

    # Evaluate completion percentage
    completion_percentage = evaluate_completion_percentage(results)

    # Identify improvement areas
    improvements = identify_improvement_areas(results, completion_percentage)

    print(f"\n" + "=" * 60)
    print(f"📊 FINAL ASSESSMENT: {completion_percentage:.1f}% Complete")
    print(f"🎯 Target: 95% for production readiness")
    print(f"📈 Gap: {max(0, 95 - completion_percentage):.1f}% remaining")

    if completion_percentage >= 95:
        print("🎉 READY FOR PRODUCTION! 🎉")
    else:
        print(f"⚠️  Need {95 - completion_percentage:.1f}% more to reach production readiness")

    return completion_percentage >= 95


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
