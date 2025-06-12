import os
import typing
from pathlib import Path
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import FunctionTool
from google.adk import Agent as BaseAgent

# Import the RAG system
from .rag_system import get_rag_system, search_implementation_patterns

# Get the workspace root directory - resolve relative to this file's location
WORKSPACE_ROOT = Path(__file__).resolve().parents[5]  # Use resolve() for consistent path handling
CONNECTORS_DIR = WORKSPACE_ROOT / "modules" / "connectors"
SDK_DIR = WORKSPACE_ROOT / "modules" / "sdk"
CLI_TEMPLATES_DIR = WORKSPACE_ROOT / "modules" / "cli" / "karrio_cli" / "templates"

# Initialize RAG system
RAG_SYSTEM = get_rag_system(WORKSPACE_ROOT)


# Tool Functions for Connector Generation
def analyze_existing_connector(
    carrier_name: str,
    analysis_type: str = "structure"
) -> typing.Dict[str, typing.Any]:
    """
    Analyze an existing connector to understand patterns and structure using RAG system.

    Args:
        carrier_name: Name of the carrier (e.g., 'ups', 'fedex', 'canadapost')
        analysis_type: Type of analysis ('structure', 'mappings', 'schemas', 'tests', 'all')

    Returns:
        Dictionary containing comprehensive analysis results with patterns
    """
    connector_path = CONNECTORS_DIR / carrier_name

    if not connector_path.exists():
        return {"error": f"Connector {carrier_name} not found"}

    # Use RAG system for comprehensive analysis
    analysis = RAG_SYSTEM.analyze_carrier_structure(carrier_name)
    analysis["analysis_type"] = analysis_type
    analysis["path"] = str(connector_path)

    try:
        # Add traditional directory analysis if requested
        if analysis_type in ["structure", "all"]:
            analysis["directory_structure"] = _analyze_directory_structure(connector_path)

        # Get patterns from RAG system
        if analysis_type in ["mappings", "all"]:
            mapping_patterns = RAG_SYSTEM.search_patterns(
                pattern_type="mapping",
                carrier_name=carrier_name
            )
            analysis["mapping_patterns"] = [
                {
                    "description": p.description,
                    "code_example": p.code_example[:500],  # Truncate for brevity
                    "confidence": p.confidence_score
                }
                for p in mapping_patterns
            ]

        if analysis_type in ["schemas", "all"]:
            schema_patterns = RAG_SYSTEM.search_patterns(
                pattern_type="schema",
                carrier_name=carrier_name
            )
            analysis["schema_patterns"] = [
                {
                    "description": p.description,
                    "code_example": p.code_example[:500],
                    "confidence": p.confidence_score
                }
                for p in schema_patterns
            ]

        if analysis_type in ["auth", "all"]:
            auth_patterns = RAG_SYSTEM.search_patterns(
                pattern_type="auth",
                carrier_name=carrier_name
            )
            analysis["auth_patterns"] = [
                {
                    "description": p.description,
                    "code_example": p.code_example[:500],
                    "confidence": p.confidence_score
                }
                for p in auth_patterns
            ]

        # Add implementation examples
        if analysis_type in ["examples", "all"]:
            rate_examples = RAG_SYSTEM.get_implementation_examples("rate", [carrier_name])
            shipment_examples = RAG_SYSTEM.get_implementation_examples("shipment", [carrier_name])

            analysis["implementation_examples"] = {
                "rate_operations": [
                    {
                        "file": ex.file_path,
                        "function": ex.content.split('\n')[0] if ex.content else "",
                        "lines": f"{ex.start_line}-{ex.end_line}"
                    }
                    for ex in rate_examples[:3]
                ],
                "shipment_operations": [
                    {
                        "file": ex.file_path,
                        "function": ex.content.split('\n')[0] if ex.content else "",
                        "lines": f"{ex.start_line}-{ex.end_line}"
                    }
                    for ex in shipment_examples[:3]
                ]
            }

    except Exception as e:
        analysis["error"] = str(e)

    return analysis


def extract_carrier_patterns(
    similar_carriers: typing.Optional[typing.List[str]] = None,
    pattern_type: str = "api_structure"
) -> typing.Dict[str, typing.Any]:
    """
    Extract common patterns from similar carriers using RAG system for new integration.

    Args:
        similar_carriers: List of similar carriers to analyze
        pattern_type: Type of patterns to extract ('auth', 'mapping', 'schema', 'error_handling', 'all')

    Returns:
        Dictionary containing extracted patterns with code examples and similarities
    """
    if similar_carriers is None:
        # Use RAG system to find default similar carriers
        similar_carriers = ["ups", "fedex", "canadapost", "dhl_express", "usps"]

    patterns = {
        "pattern_type": pattern_type,
        "analyzed_carriers": similar_carriers,
        "common_patterns": {},
        "variations": {},
        "code_examples": {},
        "best_practices": [],
        "analysis": {}
    }

    try:
        # Extract patterns using RAG system
        all_patterns = []

        for carrier in similar_carriers:
            if pattern_type == "all":
                # Get all pattern types for comprehensive analysis
                carrier_patterns = {
                    "auth": RAG_SYSTEM.search_patterns("auth", carrier_name=carrier, limit=3),
                    "mapping": RAG_SYSTEM.search_patterns("mapping", carrier_name=carrier, limit=3),
                    "schema": RAG_SYSTEM.search_patterns("schema", carrier_name=carrier, limit=3),
                    "error_handling": RAG_SYSTEM.search_patterns("error_handling", carrier_name=carrier, limit=3)
                }
            else:
                carrier_patterns = RAG_SYSTEM.search_patterns(pattern_type, carrier_name=carrier, limit=5)

            patterns["common_patterns"][carrier] = carrier_patterns

            # Collect all patterns for similarity analysis
            if isinstance(carrier_patterns, dict):
                for pt, pt_patterns in carrier_patterns.items():
                    all_patterns.extend(pt_patterns)
            else:
                all_patterns.extend(carrier_patterns)

        # Analyze pattern similarities and extract common approaches
        patterns["similarities"] = _analyze_pattern_similarities(all_patterns)

        # Extract best practices based on confidence scores
        high_confidence_patterns = [p for p in all_patterns if p.confidence_score > 0.6]
        patterns["best_practices"] = [
            {
                "description": p.description,
                "carrier": p.carrier_name,
                "code_snippet": p.code_example[:300],
                "confidence": p.confidence_score
            }
            for p in sorted(high_confidence_patterns, key=lambda x: x.confidence_score, reverse=True)[:10]
        ]

        # Generate code examples for common patterns
        if pattern_type in ["mapping", "all"]:
            patterns["code_examples"]["rate_mapping"] = _extract_rate_mapping_examples(similar_carriers)
            patterns["code_examples"]["shipment_mapping"] = _extract_shipment_mapping_examples(similar_carriers)

        if pattern_type in ["auth", "all"]:
            patterns["code_examples"]["authentication"] = _extract_auth_examples(similar_carriers)

        if pattern_type in ["schema", "all"]:
            patterns["code_examples"]["schema_definitions"] = _extract_schema_examples(similar_carriers)

        # Add comprehensive analysis
        patterns["analysis"] = {
            "total_patterns_found": len(all_patterns),
            "carriers_with_patterns": len(set(p.carrier_name for p in all_patterns)),
            "most_common_pattern_types": [pt for pt, count in
                                        sorted([(pt, sum(1 for p in all_patterns if p.pattern_type == pt))
                                               for pt in set(p.pattern_type for p in all_patterns)],
                                              key=lambda x: x[1], reverse=True)[:3]],
            "avg_confidence": sum(p.confidence_score for p in all_patterns) / len(all_patterns) if all_patterns else 0
        }

    except Exception as e:
        patterns["error"] = str(e)

    return patterns


def generate_carrier_schema(
    carrier_name: str,
    api_documentation: str,
    schema_type: str = "complete"
) -> typing.Dict[str, typing.Any]:
    """
    Generate Python schemas from carrier API documentation.

    Args:
        carrier_name: Name of the new carrier
        api_documentation: API documentation or JSON schema
        schema_type: Type of schema generation ('rates', 'shipments', 'tracking', 'complete')

    Returns:
        Dictionary containing generated schema code
    """
    result = {
        "carrier": carrier_name,
        "schema_type": schema_type,
        "generated_schemas": {},
        "imports": [],
        "classes": []
    }

    try:
        # Try to import codegen, but handle gracefully if not available
        try:
            from karrio_cli.commands.codegen import transform_content
            codegen_available = True
        except ImportError:
            codegen_available = False

        # Use existing codegen transform functionality if available
        # Temporarily disable codegen until we can debug the integration properly
        use_codegen = False  # Set to False to always use fallback

        if use_codegen and codegen_available and api_documentation.strip().startswith('{'):
            # Assume JSON schema input
            # This would integrate with existing quicktype/codegen pipeline
            transformed = transform_content(api_documentation, append_type_suffix=True)
            result["generated_schemas"][schema_type] = transformed
            result["classes"] = _extract_class_names(transformed)
        else:
            # Enhanced fallback: Generate comprehensive schema structure
            schemas_generated = []

            if schema_type in ["rates", "complete"]:
                rate_schema = _generate_rate_schema(carrier_name)
                schemas_generated.extend(rate_schema["classes"])
                result["generated_schemas"]["rates"] = rate_schema["code"]

            if schema_type in ["shipments", "complete"]:
                shipment_schema = _generate_shipment_schema(carrier_name)
                schemas_generated.extend(shipment_schema["classes"])
                result["generated_schemas"]["shipments"] = shipment_schema["code"]

            if schema_type in ["tracking", "complete"]:
                tracking_schema = _generate_tracking_schema(carrier_name)
                schemas_generated.extend(tracking_schema["classes"])
                result["generated_schemas"]["tracking"] = tracking_schema["code"]

            # If specific schema type, generate that
            if schema_type not in ["rates", "shipments", "tracking", "complete"]:
                basic_schema = _generate_basic_schema(carrier_name, schema_type)
                schemas_generated.extend(basic_schema["classes"])
                result["generated_schemas"][schema_type] = basic_schema["code"]

            result["classes"] = schemas_generated

        # Generate appropriate imports
        result["imports"] = [
            "import attr",
            "import jstruct",
            "import typing",
            "from karrio.core.models import *",
            "from karrio.core.utils import *"
        ]

    except Exception as e:
        result["error"] = str(e)

    return result


def generate_carrier_mappings(
    carrier_name: str,
    api_endpoints: typing.Dict[str, str],
    operation_type: str = "complete"
) -> typing.Dict[str, typing.Any]:
    """
    Generate mapping files for carrier API operations.

    Args:
        carrier_name: Name of the carrier
        api_endpoints: Dictionary of API endpoints
        operation_type: Type of operations ('rates', 'shipments', 'tracking', 'complete')

    Returns:
        Dictionary containing generated mapping code
    """
    result = {
        "carrier": carrier_name,
        "operation_type": operation_type,
        "generated_mappings": {},
        "endpoints": api_endpoints
    }

    try:
        # Generate mappings based on existing templates
        templates_path = CLI_TEMPLATES_DIR

        if operation_type in ["rates", "complete"]:
            result["generated_mappings"]["rates"] = _generate_rates_mapping(
                carrier_name, api_endpoints.get("rates", ""), templates_path
            )

        if operation_type in ["shipments", "complete"]:
            result["generated_mappings"]["shipments"] = _generate_shipments_mapping(
                carrier_name, api_endpoints.get("shipments", ""), templates_path
            )

        if operation_type in ["tracking", "complete"]:
            result["generated_mappings"]["tracking"] = _generate_tracking_mapping(
                carrier_name, api_endpoints.get("tracking", ""), templates_path
            )

    except Exception as e:
        result["error"] = str(e)

    return result


def generate_integration_tests(
    carrier_name: str,
    test_data: typing.Dict[str, typing.Any],
    test_type: str = "complete"
) -> typing.Dict[str, typing.Any]:
    """
    Generate comprehensive tests for carrier integration.

    Args:
        carrier_name: Name of the carrier
        test_data: Test data and configurations
        test_type: Type of tests ('unit', 'integration', 'complete')

    Returns:
        Dictionary containing generated test code
    """
    result = {
        "carrier": carrier_name,
        "test_type": test_type,
        "generated_tests": {},
        "test_files": []
    }

    try:
        # Generate different types of tests
        if test_type in ["unit", "complete"]:
            result["generated_tests"]["unit"] = _generate_unit_tests(
                carrier_name, test_data
            )

        if test_type in ["integration", "complete"]:
            result["generated_tests"]["integration"] = _generate_integration_tests(
                carrier_name, test_data
            )

        # Generate test fixtures
        result["generated_tests"]["fixtures"] = _generate_test_fixtures(
            carrier_name, test_data
        )

    except Exception as e:
        result["error"] = str(e)

    return result


def assemble_complete_integration(
    carrier_name: str,
    integration_config: typing.Dict[str, typing.Any]
) -> typing.Dict[str, typing.Any]:
    """
    Assemble a complete carrier integration with all components using official Karrio tools.

    Args:
        carrier_name: Name of the carrier
        integration_config: Complete integration configuration

    Returns:
        Dictionary containing the complete integration structure with proper instructions
    """
    from .enhanced_tools import create_karrio_plugin_structure, get_karrio_plugin_structure_info

    result = {
        "carrier": carrier_name,
        "integration_complete": False,
        "official_structure": True,
        "generation_method": "kcli_sdk_tools",
        "next_steps": []
    }

    try:
        # Get carrier slug from config or generate it
        carrier_slug = integration_config.get("carrier_slug",
                                           carrier_name.lower().replace(" ", "_").replace("-", "_"))

        # Determine features and API type from config
        features = integration_config.get("features", "rating,shipping,tracking")
        is_xml_api = integration_config.get("is_xml_api", False)
        output_path = integration_config.get("output_path", "./plugins")

        # Generate plugin structure using official tools
        plugin_result = create_karrio_plugin_structure(
            carrier_slug=carrier_slug,
            carrier_name=carrier_name,
            features=features,
            is_xml_api=is_xml_api,
            output_path=output_path
        )

        # Get structure information
        structure_info = get_karrio_plugin_structure_info()

        result.update({
            "plugin_generation": plugin_result,
            "structure_info": structure_info,
            "integration_complete": plugin_result["success"],
            "carrier_slug": carrier_slug,
            "features": features,
            "is_xml_api": is_xml_api,
        })

        if plugin_result["success"]:
            result["next_steps"] = [
                "🚀 OFFICIAL KARRIO PLUGIN GENERATION:",
                "",
                "1. **Generate Plugin Structure:**",
                f"   Run: {plugin_result['manual_command']}",
                "",
                "2. **When prompted, enter:**",
                f"   • Carrier slug: {carrier_slug}",
                f"   • Display name: {carrier_name}",
                f"   • Features: {features}",
                "   • Version: 2025.1",
                f"   • Is XML API: {'Yes' if is_xml_api else 'No'}",
                "",
                "3. **Implementation Steps:**",
                "   • Update schema files with actual API specifications",
                "   • Run ./generate to create Python dataclasses",
                "   • Implement provider files (rates.py, shipments.py, tracking.py)",
                "   • Configure utils.py with carrier settings and authentication",
                "   • Implement error.py for error handling",
                "   • Update units.py with carrier-specific enums",
                "   • Implement proxy.py for API communication",
                "   • Create comprehensive tests",
                "",
                "4. **File Structure Created:**",
            ] + [f"   {file}" for file in plugin_result["generated_structure"]["files"][:10]]

            if len(plugin_result["generated_structure"]["files"]) > 10:
                result["next_steps"].append(f"   ... and {len(plugin_result['generated_structure']['files']) - 10} more files")

    except Exception as e:
        result["error"] = str(e)
        result["integration_complete"] = False

    return result


# Helper functions (simplified for brevity)
def _analyze_directory_structure(path: Path) -> typing.Dict[str, typing.Any]:
    """Analyze directory structure of a connector."""
    structure = {"directories": [], "files": []}
    try:
        for item in path.rglob("*"):
            if item.is_dir():
                structure["directories"].append(str(item.relative_to(path)))
            else:
                structure["files"].append(str(item.relative_to(path)))
    except Exception:
        pass
    return structure


def _analyze_mapping_files(path: Path) -> typing.List[str]:
    """Analyze mapping files in a connector."""
    mappings = []
    try:
        for py_file in path.glob("*.py"):
            mappings.append(py_file.name)
    except Exception:
        pass
    return mappings


def _analyze_schema_files(path: Path) -> typing.List[str]:
    """Analyze schema files in a connector."""
    schemas = []
    try:
        for py_file in path.rglob("*.py"):
            schemas.append(str(py_file.relative_to(path)))
    except Exception:
        pass
    return schemas


def _analyze_test_files(path: Path) -> typing.List[str]:
    """Analyze test files in a connector."""
    tests = []
    try:
        for py_file in path.glob("*.py"):
            tests.append(py_file.name)
    except Exception:
        pass
    return tests


def _extract_class_names(content: str) -> typing.List[str]:
    """Extract class names from Python code."""
    import re
    return re.findall(r"class\s+(\w+)", content)


def _generate_rates_mapping(carrier_name: str, endpoint: str, templates_path: Path) -> str:
    """Generate rates mapping code."""
    # This would use the existing rates.py template
    return f"# Generated rates mapping for {carrier_name}\n# Endpoint: {endpoint}"


def _generate_shipments_mapping(carrier_name: str, endpoint: str, templates_path: Path) -> str:
    """Generate shipments mapping code."""
    # This would use the existing shipments.py template
    return f"# Generated shipments mapping for {carrier_name}\n# Endpoint: {endpoint}"


def _generate_tracking_mapping(carrier_name: str, endpoint: str, templates_path: Path) -> str:
    """Generate tracking mapping code."""
    # This would use the existing tracking.py template
    return f"# Generated tracking mapping for {carrier_name}\n# Endpoint: {endpoint}"


def _generate_unit_tests(carrier_name: str, test_data: typing.Dict[str, typing.Any]) -> str:
    """Generate unit tests."""
    return f"# Generated unit tests for {carrier_name}"


def _generate_integration_tests(carrier_name: str, test_data: typing.Dict[str, typing.Any]) -> str:
    """Generate integration tests."""
    return f"# Generated integration tests for {carrier_name}"


def _generate_test_fixtures(carrier_name: str, test_data: typing.Dict[str, typing.Any]) -> str:
    """Generate test fixtures."""
    return f"# Generated test fixtures for {carrier_name}"


def _generate_project_structure(carrier_name: str) -> typing.Dict[str, typing.Any]:
    """Generate complete project structure."""
    return {
        "root": f"modules/connectors/{carrier_name}",
        "directories": [
            "karrio/providers",
            "karrio/mappers",
            "karrio/schemas",
            "tests",
            "schemas"
        ],
        "files": [
            "pyproject.toml",
            "README.md",
            "generate"
        ]
    }


def _generate_file(carrier_name: str, file_type: str, config: typing.Dict[str, typing.Any]) -> str:
    """Generate individual file content."""
    return f"# Generated {file_type} for {carrier_name}"


def _analyze_pattern_similarities(patterns: typing.List) -> typing.Dict[str, typing.Any]:
    """Analyze similarities between patterns from different carriers."""
    if not patterns:
        return {"common_approaches": [], "unique_implementations": []}

    # Simple analysis based on common keywords
    common_keywords = {}
    for pattern in patterns:
        if hasattr(pattern, 'code_example'):
            words = pattern.code_example.lower().split()
            for word in words:
                if len(word) > 3 and word.isalpha():  # Filter meaningful words
                    common_keywords[word] = common_keywords.get(word, 0) + 1

    # Find most common approaches
    sorted_keywords = sorted(common_keywords.items(), key=lambda x: x[1], reverse=True)

    return {
        "common_approaches": [kw for kw, count in sorted_keywords[:10] if count > 1],
        "pattern_frequency": dict(sorted_keywords[:20]),
        "total_patterns_analyzed": len(patterns)
    }


def _extract_rate_mapping_examples(carriers: typing.List[str]) -> typing.List[typing.Dict[str, str]]:
    """Extract rate mapping examples from carriers."""
    examples = []
    for carrier in carriers:
        rate_examples = RAG_SYSTEM.get_implementation_examples("parse_rate_response", [carrier])
        for ex in rate_examples[:2]:  # Limit to 2 per carrier
            examples.append({
                "carrier": carrier,
                "function_name": ex.content.split('\n')[0] if ex.content else "",
                "file_path": ex.file_path,
                "code_snippet": ex.content[:400]
            })
    return examples


def _extract_shipment_mapping_examples(carriers: typing.List[str]) -> typing.List[typing.Dict[str, str]]:
    """Extract shipment mapping examples from carriers."""
    examples = []
    for carrier in carriers:
        shipment_examples = RAG_SYSTEM.get_implementation_examples("shipment_request", [carrier])
        for ex in shipment_examples[:2]:
            examples.append({
                "carrier": carrier,
                "function_name": ex.content.split('\n')[0] if ex.content else "",
                "file_path": ex.file_path,
                "code_snippet": ex.content[:400]
            })
    return examples


def _extract_auth_examples(carriers: typing.List[str]) -> typing.List[typing.Dict[str, str]]:
    """Extract authentication examples from carriers."""
    examples = []
    for carrier in carriers:
        auth_patterns = RAG_SYSTEM.search_patterns("auth", carrier_name=carrier, limit=2)
        for pattern in auth_patterns:
            examples.append({
                "carrier": carrier,
                "description": pattern.description,
                "code_snippet": pattern.code_example[:400],
                "confidence": pattern.confidence_score
            })
    return examples


def _extract_schema_examples(carriers: typing.List[str]) -> typing.List[typing.Dict[str, str]]:
    """Extract schema definition examples from carriers."""
    examples = []
    for carrier in carriers:
        schema_patterns = RAG_SYSTEM.search_patterns("schema", carrier_name=carrier, limit=2)
        for pattern in schema_patterns:
            examples.append({
                "carrier": carrier,
                "description": pattern.description,
                "code_snippet": pattern.code_example[:400],
                "confidence": pattern.confidence_score
            })
    return examples


def _generate_rate_schema(carrier_name: str) -> typing.Dict[str, typing.Any]:
    """Generate rate-specific schemas."""
    code = f"""# Generated rate schemas for {carrier_name}
import attr
import jstruct
import typing

@attr.s(auto_attribs=True)
class {carrier_name.title()}RateRequestType:
    \"\"\"Rate request schema for {carrier_name}.\"\"\"
    origin: typing.Optional[str] = None
    destination: typing.Optional[str] = None
    packages: typing.List[typing.Dict[str, typing.Any]] = jstruct.JList[dict]
    services: typing.Optional[typing.List[str]] = jstruct.JList[str]

@attr.s(auto_attribs=True)
class {carrier_name.title()}RateType:
    \"\"\"Individual rate schema for {carrier_name}.\"\"\"
    service_code: typing.Optional[str] = None
    service_name: typing.Optional[str] = None
    total_cost: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    delivery_days: typing.Optional[int] = None

@attr.s(auto_attribs=True)
class {carrier_name.title()}RateResponseType:
    \"\"\"Rate response schema for {carrier_name}.\"\"\"
    rates: typing.List[{carrier_name.title()}RateType] = jstruct.JList[{carrier_name.title()}RateType]
    status: typing.Optional[str] = None
"""

    classes = [
        f"{carrier_name.title()}RateRequestType",
        f"{carrier_name.title()}RateType",
        f"{carrier_name.title()}RateResponseType"
    ]

    return {"code": code, "classes": classes}


def _generate_shipment_schema(carrier_name: str) -> typing.Dict[str, typing.Any]:
    """Generate shipment-specific schemas."""
    code = f"""# Generated shipment schemas for {carrier_name}
import attr
import jstruct
import typing

@attr.s(auto_attribs=True)
class {carrier_name.title()}ShipmentRequestType:
    \"\"\"Shipment request schema for {carrier_name}.\"\"\"
    shipper: typing.Optional[typing.Dict[str, typing.Any]] = None
    recipient: typing.Optional[typing.Dict[str, typing.Any]] = None
    packages: typing.List[typing.Dict[str, typing.Any]] = jstruct.JList[dict]
    service: typing.Optional[str] = None

@attr.s(auto_attribs=True)
class {carrier_name.title()}ShipmentResponseType:
    \"\"\"Shipment response schema for {carrier_name}.\"\"\"
    tracking_number: typing.Optional[str] = None
    label_url: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    status: typing.Optional[str] = None
"""

    classes = [
        f"{carrier_name.title()}ShipmentRequestType",
        f"{carrier_name.title()}ShipmentResponseType"
    ]

    return {"code": code, "classes": classes}


def _generate_tracking_schema(carrier_name: str) -> typing.Dict[str, typing.Any]:
    """Generate tracking-specific schemas."""
    code = f"""# Generated tracking schemas for {carrier_name}
import attr
import jstruct
import typing

@attr.s(auto_attribs=True)
class {carrier_name.title()}TrackingRequestType:
    \"\"\"Tracking request schema for {carrier_name}.\"\"\"
    tracking_numbers: typing.List[str] = jstruct.JList[str]

@attr.s(auto_attribs=True)
class {carrier_name.title()}TrackingEventType:
    \"\"\"Tracking event schema for {carrier_name}.\"\"\"
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None
    location: typing.Optional[str] = None
    status: typing.Optional[str] = None
    description: typing.Optional[str] = None

@attr.s(auto_attribs=True)
class {carrier_name.title()}TrackingResponseType:
    \"\"\"Tracking response schema for {carrier_name}.\"\"\"
    tracking_number: typing.Optional[str] = None
    status: typing.Optional[str] = None
    events: typing.List[{carrier_name.title()}TrackingEventType] = jstruct.JList[{carrier_name.title()}TrackingEventType]
"""

    classes = [
        f"{carrier_name.title()}TrackingRequestType",
        f"{carrier_name.title()}TrackingEventType",
        f"{carrier_name.title()}TrackingResponseType"
    ]

    return {"code": code, "classes": classes}


def _generate_basic_schema(carrier_name: str, schema_type: str) -> typing.Dict[str, typing.Any]:
    """Generate basic schema for any type."""
    code = f"""# Generated schema for {carrier_name} - {schema_type}
import attr
import jstruct
import typing

@attr.s(auto_attribs=True)
class {carrier_name.title()}{schema_type.title()}ResponseType:
    \"\"\"Generated schema for {carrier_name} {schema_type} response.\"\"\"
    status: typing.Optional[str] = None
    data: typing.Optional[typing.Dict[str, typing.Any]] = None
    # Add more fields based on API documentation
"""

    classes = [f"{carrier_name.title()}{schema_type.title()}ResponseType"]

    return {"code": code, "classes": classes}


# Import enhanced tools
from .enhanced_tools import (
    create_karrio_plugin_structure,
    get_karrio_plugin_structure_info,
    analyze_carrier_api_documentation,
    scrape_api_documentation,
    extract_openapi_from_url
)

# Create FunctionTool instances
analyze_existing_connector_tool = FunctionTool(analyze_existing_connector)
extract_carrier_patterns_tool = FunctionTool(extract_carrier_patterns)
generate_carrier_schema_tool = FunctionTool(generate_carrier_schema)
generate_carrier_mappings_tool = FunctionTool(generate_carrier_mappings)
generate_integration_tests_tool = FunctionTool(generate_integration_tests)
assemble_complete_integration_tool = FunctionTool(assemble_complete_integration)

# Enhanced tools for proper plugin generation
create_plugin_structure_tool = FunctionTool(create_karrio_plugin_structure)
get_plugin_structure_info_tool = FunctionTool(get_karrio_plugin_structure_info)
analyze_api_documentation_tool = FunctionTool(analyze_carrier_api_documentation)
scrape_api_documentation_tool = FunctionTool(scrape_api_documentation)
extract_openapi_from_url_tool = FunctionTool(extract_openapi_from_url)

# Specialized Sub-Agents
schema_agent = Agent(
    name="schema_agent",
    model="gemini-1.5-flash",
    description="Specialized agent for generating Python schemas from carrier API documentation",
    instruction="""
    You are a specialized agent for generating Python dataclasses and schemas from carrier API documentation.

    Your expertise includes:
    - Converting JSON schemas to Python dataclasses with proper typing
    - Using attrs and jstruct decorators for serialization
    - Following Karrio's schema conventions
    - Handling complex nested types and optional fields
    - Generating appropriate imports and type hints

    When generating schemas:
    1. Always use attrs with auto_attribs=True
    2. Use jstruct decorators for JSON serialization
    3. Append 'Type' suffix to class names unless they already end with 'Type'
    4. Use typing module for all type annotations
    5. Handle Optional, List, Union, and Dict types properly
    6. Generate proper default values using jstruct helpers

    You work with the main integration agent to ensure schema compatibility.
    """,
    tools=[generate_carrier_schema_tool],
)

mapping_agent = Agent(
    name="mapping_agent",
    model="gemini-1.5-flash",
    description="Specialized agent for generating API request/response mappings",
    instruction="""
    You are a specialized agent for generating carrier API mappings and transformations.

    Your expertise includes:
    - Creating request/response mapping functions
    - Handling API authentication and headers
    - Converting between Karrio models and carrier-specific formats
    - Error handling and validation
    - Rate, shipment, and tracking API mappings

    When generating mappings:
    1. Follow Karrio's mapping patterns from existing connectors
    2. Use proper error handling with Karrio's error models
    3. Implement proper request/response transformations
    4. Handle carrier-specific authentication methods
    5. Support all required operations (rates, shipments, tracking)
    6. Include proper logging and debugging information

    You integrate with the schema agent for data models and the integration agent for final assembly.
    """,
    tools=[generate_carrier_mappings_tool, extract_carrier_patterns_tool],
)

integration_agent = Agent(
    name="integration_agent",
    model="gemini-1.5-flash",
    description="Main integration agent that orchestrates complete carrier integration using official Karrio tools",
    instruction="""
    You are the main integration agent responsible for orchestrating complete carrier integrations using official Karrio CLI tools.

    IMPORTANT: You must use the official Karrio plugin generation workflow:
    1. Use `kcli sdk add-extension` command to generate proper plugin structure
    2. Guide users through the official workflow, not manual file creation
    3. Provide accurate structure information based on real Karrio templates

    Your capabilities include:
    - Creating plugin structures using official CLI tools (create_plugin_structure_tool)
    - Analyzing carrier API documentation to determine plugin configuration (analyze_api_documentation_tool)
    - Providing accurate plugin structure information (get_plugin_structure_info_tool)
    - Coordinating with specialized sub-agents for implementation details
    - Ensuring proper Karrio project structure conventions

    When a user asks to build a carrier integration:
    1. If they provide a URL, use scrape_api_documentation_tool or extract_openapi_from_url_tool to fetch the API docs
    2. If they provide API documentation directly, analyze it using analyze_api_documentation_tool
    3. Use the official plugin generation tools to create proper structure
    4. Provide step-by-step instructions using kcli commands
    5. Guide them through the implementation workflow
    6. Ensure they understand the proper file structure and implementation pattern

    You ensure 95%+ completion by:
    - Using official Karrio tooling and templates
    - Following the proper provider/mapper/schema separation
    - Including all necessary components for production use
    - Providing accurate implementation guidance based on real Karrio patterns
    """,
    tools=[
        analyze_existing_connector_tool,
        extract_carrier_patterns_tool,
        assemble_complete_integration_tool,
        create_plugin_structure_tool,
        get_plugin_structure_info_tool,
        analyze_api_documentation_tool,
        scrape_api_documentation_tool,
        extract_openapi_from_url_tool
    ],
)

testing_agent = Agent(
    name="testing_agent",
    model="gemini-1.5-flash",
    description="Specialized agent for generating comprehensive test suites",
    instruction="""
    You are a specialized agent for generating comprehensive test suites for carrier integrations.

    Your expertise includes:
    - Creating unit tests for individual components
    - Generating integration tests for end-to-end workflows
    - Building test fixtures and mock data
    - Testing error handling and edge cases
    - Performance and reliability testing

    When generating tests:
    1. Create tests for all major functionality (rates, shipments, tracking)
    2. Include both positive and negative test cases
    3. Generate realistic test data and fixtures
    4. Test error handling and validation
    5. Follow pytest conventions and best practices
    6. Include integration tests with mock API responses
    7. Generate performance benchmarks where appropriate

    You work with the integration agent to ensure complete test coverage.
    """,
    tools=[generate_integration_tests_tool],
)

# Main Karrio Integration Agent - Orchestrates sub-agents
root_agent = SequentialAgent(
    name="karrio_integration_agent",
    description="Advanced Karrio shipping carrier integration agent with multi-agent architecture and RAG capabilities",
    sub_agents=[schema_agent, mapping_agent, integration_agent, testing_agent],
)
