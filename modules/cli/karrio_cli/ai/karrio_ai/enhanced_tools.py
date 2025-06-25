"""
Enhanced tools for handling different input formats for carrier integration generation.

This module provides tools to process:
- OpenAPI/Swagger specifications
- Website URLs for scraping API documentation
- PDF documentation files
- Raw text documentation
"""

import os
import json
import yaml
import typing
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
import tempfile
import re

try:
    import PyPDF2
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False

try:
    import openapi_schema_validator
    OPENAPI_VALIDATION_AVAILABLE = True
except ImportError:
    OPENAPI_VALIDATION_AVAILABLE = False


def parse_openapi_spec(
    spec_content: str,
    spec_format: str = "auto"
) -> typing.Dict[str, typing.Any]:
    """
    Parse OpenAPI/Swagger specification and extract carrier API information.

    Args:
        spec_content: OpenAPI specification content (JSON or YAML)
        spec_format: Format of the spec ('json', 'yaml', 'auto')

    Returns:
        Dictionary containing structured API information
    """
    result = {
        "success": False,
        "api_info": {},
        "endpoints": {},
        "schemas": {},
        "auth_methods": [],
        "error": None
    }

    try:
        # Parse the specification
        if spec_format == "auto":
            # Try to detect format
            try:
                spec_data = json.loads(spec_content)
                spec_format = "json"
            except json.JSONDecodeError:
                try:
                    spec_data = yaml.safe_load(spec_content)
                    spec_format = "yaml"
                except yaml.YAMLError:
                    result["error"] = "Unable to parse specification as JSON or YAML"
                    return result
        elif spec_format == "json":
            spec_data = json.loads(spec_content)
        elif spec_format == "yaml":
            spec_data = yaml.safe_load(spec_content)
        else:
            result["error"] = f"Unsupported format: {spec_format}"
            return result

        # Extract API information
        result["api_info"] = {
            "title": spec_data.get("info", {}).get("title", "Unknown API"),
            "version": spec_data.get("info", {}).get("version", "1.0.0"),
            "description": spec_data.get("info", {}).get("description", ""),
            "base_url": spec_data.get("servers", [{}])[0].get("url", "") if spec_data.get("servers") else "",
            "openapi_version": spec_data.get("openapi", spec_data.get("swagger", "unknown"))
        }

        # Extract endpoints
        paths = spec_data.get("paths", {})
        for path, methods in paths.items():
            for method, operation in methods.items():
                if isinstance(operation, dict):
                    endpoint_key = f"{method.upper()} {path}"
                    result["endpoints"][endpoint_key] = {
                        "method": method.upper(),
                        "path": path,
                        "summary": operation.get("summary", ""),
                        "description": operation.get("description", ""),
                        "tags": operation.get("tags", []),
                        "parameters": operation.get("parameters", []),
                        "request_body": operation.get("requestBody", {}),
                        "responses": operation.get("responses", {}),
                        "operation_id": operation.get("operationId", "")
                    }

        # Extract schemas
        components = spec_data.get("components", {})
        definitions = spec_data.get("definitions", {})  # Swagger 2.0

        if components:
            result["schemas"] = components.get("schemas", {})
        if definitions:
            result["schemas"].update(definitions)

        # Extract authentication methods
        security_schemes = components.get("securitySchemes", {}) or spec_data.get("securityDefinitions", {})
        for name, scheme in security_schemes.items():
            auth_type = scheme.get("type", "unknown")
            result["auth_methods"].append({
                "name": name,
                "type": auth_type,
                "scheme": scheme.get("scheme", ""),
                "bearer_format": scheme.get("bearerFormat", ""),
                "in": scheme.get("in", ""),
                "description": scheme.get("description", "")
            })

        # Categorize endpoints by shipping operations
        result["shipping_endpoints"] = _categorize_shipping_endpoints(result["endpoints"])

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def scrape_api_documentation(
    url: str,
    documentation_type: str = "auto"
) -> typing.Dict[str, typing.Any]:
    """
    Scrape API documentation from a URL.

    Args:
        url: The URL to scrape (e.g., API documentation page)
        documentation_type: Type expected (auto, openapi, website, rest_api)

    Returns:
        Dictionary with scraped content and analysis
    """
    import requests
    from bs4 import BeautifulSoup
    import re
    import json

    result = {
        "url": url,
        "success": False,
        "content": "",
        "documentation_type": documentation_type,
        "api_info": {},
        "error": None
    }

    try:
        # Check if user has beautifulsoup4 installed
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Fetch the page
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse the content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content
        text_content = soup.get_text()
        result["content"] = text_content[:10000]  # Limit to avoid overwhelming the LLM

        # Look for OpenAPI/Swagger specs
        openapi_indicators = [
            'swagger', 'openapi', 'api-docs', 'specification',
            'endpoints', 'paths:', 'components:', 'schemas:'
        ]

        if any(indicator in text_content.lower() for indicator in openapi_indicators):
            result["documentation_type"] = "openapi"

        # Look for specific patterns
        api_patterns = {
            "base_url": r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9.-]*)*",
            "endpoints": r"/[a-zA-Z0-9/-]+(?:\{[a-zA-Z0-9_]+\})?",
            "authentication": r"(?:api.?key|token|authorization|bearer|oauth)",
            "methods": r"\b(?:GET|POST|PUT|DELETE|PATCH)\b",
        }

        for pattern_name, pattern in api_patterns.items():
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                result["api_info"][pattern_name] = matches[:10]  # Limit results

        # Try to find JSON content (might be embedded OpenAPI spec)
        json_blocks = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response.text)
        for block in json_blocks:
            try:
                parsed = json.loads(block)
                if any(key in parsed for key in ['openapi', 'swagger', 'paths', 'info']):
                    result["api_info"]["openapi_spec"] = parsed
                    result["documentation_type"] = "openapi"
                    break
            except:
                continue

        result["success"] = True

        # Provide analysis
        result["analysis"] = analyze_carrier_api_documentation(
            text_content[:5000],
            url.split('/')[2] if '://' in url else url,  # Extract domain as carrier name
            result["documentation_type"]
        )

    except ImportError:
        result["error"] = "beautifulsoup4 not installed. Please run: pip install beautifulsoup4 requests"
    except requests.RequestException as e:
        result["error"] = f"Failed to fetch URL: {str(e)}"
    except Exception as e:
        result["error"] = f"Error scraping documentation: {str(e)}"

    return result


def parse_pdf_documentation(
    pdf_path: str
) -> typing.Dict[str, typing.Any]:
    """
    Extract API documentation from PDF files.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing extracted documentation
    """
    result = {
        "success": False,
        "file_path": pdf_path,
        "pages": 0,
        "content": "",
        "api_endpoints": [],
        "code_examples": [],
        "tables": [],
        "error": None
    }

    if not PDF_AVAILABLE:
        result["error"] = "PDF parsing dependencies not installed. Install with: pip install PyPDF2 pdfplumber"
        return result

    try:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            result["error"] = f"PDF file not found: {pdf_path}"
            return result

        # Extract text using pdfplumber (better for structured content)
        with pdfplumber.open(pdf_path) as pdf:
            result["pages"] = len(pdf.pages)

            all_text = []
            tables = []

            for page_num, page in enumerate(pdf.pages):
                # Extract text
                page_text = page.extract_text()
                if page_text:
                    all_text.append(f"=== Page {page_num + 1} ===\n{page_text}")

                # Extract tables
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        tables.append({
                            "page": page_num + 1,
                            "data": table[:10]  # Limit rows
                        })

            result["content"] = "\n\n".join(all_text)
            result["tables"] = tables

        # Extract API endpoints and code examples
        result["api_endpoints"] = _extract_api_patterns(result["content"])
        result["code_examples"] = _extract_code_examples(result["content"])

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def analyze_carrier_documentation(
    carrier_name: str,
    documentation_source: str,
    source_type: str = "auto"
) -> typing.Dict[str, typing.Any]:
    """
    Analyze carrier documentation from various sources.

    Args:
        carrier_name: Name of the carrier
        documentation_source: Source content (OpenAPI spec, URL, file path, or text)
        source_type: Type of source ('openapi', 'url', 'pdf', 'text', 'auto')

    Returns:
        Comprehensive analysis of carrier integration requirements
    """
    result = {
        "carrier_name": carrier_name,
        "source_type": source_type,
        "success": True,
        "error": None
    }

    try:
        # Basic implementation - can be enhanced with actual parsing
        if source_type == "auto":
            source_type = _detect_source_type(documentation_source)

        result["source_type"] = source_type
        result["analysis"] = {
            "api_type": "REST",
            "endpoints": _extract_endpoints(documentation_source),
            "auth_methods": _extract_auth_methods(documentation_source)
        }

    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result


# Helper functions
def _categorize_shipping_endpoints(endpoints: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.List[str]]:
    """Categorize endpoints by shipping operations."""
    categories = {
        "rates": [],
        "shipments": [],
        "tracking": [],
        "labels": [],
        "manifests": [],
        "pickup": [],
        "other": []
    }

    for endpoint_key, endpoint_info in endpoints.items():
        path = endpoint_info["path"].lower()
        summary = endpoint_info["summary"].lower()
        tags = [tag.lower() for tag in endpoint_info["tags"]]

        categorized = False
        for category in categories.keys():
            if category in path or category in summary or any(category in tag for tag in tags):
                categories[category].append(endpoint_key)
                categorized = True
                break

        if not categorized:
            # Additional categorization logic
            if any(keyword in path or keyword in summary for keyword in ["quote", "price", "cost"]):
                categories["rates"].append(endpoint_key)
            elif any(keyword in path or keyword in summary for keyword in ["ship", "create", "book"]):
                categories["shipments"].append(endpoint_key)
            elif any(keyword in path or keyword in summary for keyword in ["track", "status", "trace"]):
                categories["tracking"].append(endpoint_key)
            elif any(keyword in path or keyword in summary for keyword in ["label", "print"]):
                categories["labels"].append(endpoint_key)
            else:
                categories["other"].append(endpoint_key)

    return categories


def _extract_api_patterns(text: str) -> typing.List[str]:
    """Extract API endpoint patterns from text."""
    endpoints = []
    for pattern in [
        r'https?://[^\s/]+/[^\s]*',
        r'/v\d+/[^\s]*',
        r'/api/[^\s]*'
    ]:
        matches = re.findall(pattern, text, re.IGNORECASE)
        endpoints.extend(matches)
    return list(set(endpoints))


def _extract_code_examples(text: str) -> typing.List[str]:
    """Extract code examples from text."""
    examples = []
    for pattern in [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
        r'<[^<>]+>.*?</[^<>]+>',
        r'```[\s\S]*?```',
    ]:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            if len(match) > 50 and len(match) < 1000:
                examples.append(match.strip())
    return examples[:10]


def _detect_source_type(source: str) -> str:
    """Detect the type of documentation source."""
    if source.startswith(('http://', 'https://')):
        return "url"
    elif source.endswith('.pdf'):
        return "pdf"
    elif 'openapi' in source.lower() or 'swagger' in source.lower():
        return "openapi"
    else:
        return "text"


def _extract_endpoints(content: str) -> typing.List[str]:
    """Extract API endpoints from content."""
    endpoints = []
    for pattern in [
        r'https?://[^\s/]+/[^\s]*',
        r'/v\d+/[^\s]*',
        r'/api/[^\s]*'
    ]:
        matches = re.findall(pattern, content, re.IGNORECASE)
        endpoints.extend(matches)
    return list(set(endpoints))


def _extract_auth_methods(content: str) -> typing.List[str]:
    """Extract authentication methods from content."""
    auth_methods = []
    content_lower = content.lower()

    if 'api key' in content_lower or 'apikey' in content_lower:
        auth_methods.append('apiKey')
    if 'oauth' in content_lower:
        auth_methods.append('oauth2')
    if 'bearer' in content_lower:
        auth_methods.append('bearer')

    return auth_methods


def create_karrio_plugin_structure(
    carrier_slug: str,
    carrier_name: str,
    features: str = "rating,shipping,tracking",
    is_xml_api: bool = False,
    output_path: str = "./plugins"
) -> typing.Dict[str, typing.Any]:
    """
    Generate a complete Karrio plugin structure using the official kcli SDK tools.

    Args:
        carrier_slug: Unique identifier (e.g., 'chit_chats', 'my_carrier')
        carrier_name: Display name (e.g., 'Chit Chats', 'My Carrier')
        features: Comma-separated features (rating,shipping,tracking,pickup,address)
        is_xml_api: Whether the carrier uses XML API (vs JSON)
        output_path: Directory where the plugin will be created

    Returns:
        Dictionary with plugin structure information and next steps
    """
    import subprocess
    import os
    from pathlib import Path

    result = {
        "carrier_slug": carrier_slug,
        "carrier_name": carrier_name,
        "features": features,
        "is_xml_api": is_xml_api,
        "output_path": output_path,
        "success": False,
        "plugin_directory": None,
        "generated_files": [],
        "next_steps": [],
        "error": None
    }

    try:
        # Ensure output directory exists
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build the kcli command to generate the plugin
        cmd = [
            "kcli", "sdk", "add-extension",
            "--path", str(output_dir),
            # Use environment variables to avoid interactive prompts
        ]

        # Set environment variables for non-interactive mode
        env = os.environ.copy()
        env.update({
            "KARRIO_CARRIER_SLUG": carrier_slug,
            "KARRIO_CARRIER_NAME": carrier_name,
            "KARRIO_FEATURES": features,
            "KARRIO_IS_XML": "true" if is_xml_api else "false",
            "KARRIO_VERSION": "2025.1"
        })

        # For now, provide manual instructions since kcli requires interactive input
        result.update({
            "success": True,
            "plugin_directory": str(output_dir / carrier_slug),
            "manual_command": f"kcli sdk add-extension --path {output_dir}",
            "command_inputs": {
                "carrier_slug": carrier_slug,
                "display_name": carrier_name,
                "features": features,
                "version": "2025.1",
                "is_xml_api": is_xml_api
            },
            "generated_structure": {
                "directories": [
                    f"{carrier_slug}/",
                    f"{carrier_slug}/schemas/",
                    f"{carrier_slug}/tests/{carrier_slug}/",
                    f"{carrier_slug}/karrio/plugins/{carrier_slug}/",
                    f"{carrier_slug}/karrio/mappers/{carrier_slug}/",
                    f"{carrier_slug}/karrio/providers/{carrier_slug}/",
                    f"{carrier_slug}/karrio/schemas/{carrier_slug}/",
                ],
                "files": [
                    f"{carrier_slug}/pyproject.toml",
                    f"{carrier_slug}/README.md",
                    f"{carrier_slug}/generate",
                    f"{carrier_slug}/schemas/error_response.{'xsd' if is_xml_api else 'json'}",
                ]
            }
        })

        # Add feature-specific files
        features_list = [f.strip() for f in features.split(",")]
        feature_files = []

        if "rating" in features_list:
            ext = "xsd" if is_xml_api else "json"
            feature_files.extend([
                f"{carrier_slug}/schemas/rate_request.{ext}",
                f"{carrier_slug}/schemas/rate_response.{ext}",
            ])

        if "shipping" in features_list:
            ext = "xsd" if is_xml_api else "json"
            feature_files.extend([
                f"{carrier_slug}/schemas/shipment_request.{ext}",
                f"{carrier_slug}/schemas/shipment_response.{ext}",
                f"{carrier_slug}/schemas/shipment_cancel_request.{ext}",
                f"{carrier_slug}/schemas/shipment_cancel_response.{ext}",
            ])

        if "tracking" in features_list:
            ext = "xsd" if is_xml_api else "json"
            feature_files.extend([
                f"{carrier_slug}/schemas/tracking_request.{ext}",
                f"{carrier_slug}/schemas/tracking_response.{ext}",
            ])

        if "pickup" in features_list:
            ext = "xsd" if is_xml_api else "json"
            feature_files.extend([
                f"{carrier_slug}/schemas/pickup_create_request.{ext}",
                f"{carrier_slug}/schemas/pickup_create_response.{ext}",
                f"{carrier_slug}/schemas/pickup_update_request.{ext}",
                f"{carrier_slug}/schemas/pickup_update_response.{ext}",
                f"{carrier_slug}/schemas/pickup_cancel_request.{ext}",
                f"{carrier_slug}/schemas/pickup_cancel_response.{ext}",
            ])

        if "address" in features_list:
            ext = "xsd" if is_xml_api else "json"
            feature_files.extend([
                f"{carrier_slug}/schemas/address_validation_request.{ext}",
                f"{carrier_slug}/schemas/address_validation_response.{ext}",
            ])

        result["generated_structure"]["files"].extend(feature_files)

        # Provide next steps
        result["next_steps"] = [
            f"1. Run: {result['manual_command']}",
            f"2. When prompted, enter:",
            f"   - Carrier slug: {carrier_slug}",
            f"   - Display name: {carrier_name}",
            f"   - Features: {features}",
            f"   - Version: 2025.1",
            f"   - Is XML API: {'Yes' if is_xml_api else 'No'}",
            f"3. Navigate to: {output_dir / carrier_slug}",
            "4. Update the generated schema files with actual API specifications",
            "5. Run the 'generate' script to create Python dataclasses",
            "6. Implement the provider files in karrio/providers/ directory",
            "7. Update mapping files in karrio/mappers/ directory",
            "8. Add tests in tests/ directory",
        ]

    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result


def get_karrio_plugin_structure_info() -> typing.Dict[str, typing.Any]:
    """
    Get detailed information about the correct Karrio plugin structure.

    Returns:
        Dictionary with comprehensive plugin structure information
    """
    return {
        "overview": "Karrio plugins follow a specific directory structure with multiple components",
        "official_generation_command": "kcli sdk add-extension",
        "directory_structure": {
            "root": "{carrier_slug}/",
            "description": "Root directory with the carrier slug as the name",
            "contents": {
                "pyproject.toml": "Project configuration and dependencies",
                "README.md": "Documentation for the carrier integration",
                "generate": "Script to generate Python classes from schemas",
                "schemas/": {
                    "description": "JSON/XML schema files for API requests and responses",
                    "files": [
                        "error_response.json/xsd",
                        "rate_request.json/xsd",
                        "rate_response.json/xsd",
                        "shipment_request.json/xsd",
                        "shipment_response.json/xsd",
                        "tracking_request.json/xsd",
                        "tracking_response.json/xsd",
                        "pickup_*.json/xsd (if pickup feature enabled)",
                        "address_*.json/xsd (if address feature enabled)"
                    ]
                },
                "karrio/": {
                    "description": "Python implementation files",
                    "subdirectories": {
                        "schemas/{carrier_slug}/": {
                            "description": "Generated Python dataclasses from schemas",
                            "files": ["__init__.py", "generated dataclass files"]
                        },
                        "providers/{carrier_slug}/": {
                            "description": "Core implementation files",
                            "files": [
                                "__init__.py",
                                "error.py - Error handling",
                                "utils.py - Utilities and settings",
                                "units.py - Enums and unit mappings",
                                "rates.py - Rate calculation implementation",
                                "shipments.py - Shipping implementation",
                                "tracking.py - Tracking implementation",
                                "pickup.py - Pickup implementation (if enabled)",
                                "address.py - Address validation (if enabled)"
                            ]
                        },
                        "mappers/{carrier_slug}/": {
                            "description": "API proxy and request/response handling",
                            "files": [
                                "__init__.py",
                                "proxy.py - HTTP client and API communication",
                                "mapper.py - Request/response mapping logic"
                            ]
                        },
                        "plugins/{carrier_slug}/": {
                            "description": "Plugin registration and entry point",
                            "files": [
                                "__init__.py",
                                "plugin.py - Plugin definition and registration"
                            ]
                        }
                    }
                },
                "tests/": {
                    "description": "Test suite for the carrier integration",
                    "files": [
                        "{carrier_slug}/",
                        "test_rates.py",
                        "test_shipments.py",
                        "test_tracking.py",
                        "fixtures/ - Test data"
                    ]
                }
            }
        },
        "implementation_workflow": [
            "1. Generate plugin structure using kcli sdk add-extension",
            "2. Update schema files with actual API specifications",
            "3. Run ./generate to create Python dataclasses",
            "4. Implement provider files (rates.py, shipments.py, tracking.py)",
            "5. Implement utils.py with carrier settings and authentication",
            "6. Implement error.py for error handling",
            "7. Update units.py with carrier-specific enums",
            "8. Implement proxy.py for API communication",
            "9. Create comprehensive tests",
            "10. Test integration with Karrio"
        ],
        "key_differences_from_basic_structure": [
            "Uses official CLI tooling instead of manual file creation",
            "Separates schemas (data) from providers (logic) from mappers (API communication)",
            "Includes comprehensive code generation from schemas",
            "Follows Karrio's modular architecture",
            "Includes proper plugin registration system",
            "Has built-in testing framework integration"
        ]
    }


def analyze_carrier_api_documentation(
    api_documentation: str,
    carrier_name: str,
    documentation_type: str = "auto"
) -> typing.Dict[str, typing.Any]:
    """
    Analyze carrier API documentation to extract key information for plugin generation.

    Args:
        api_documentation: The API documentation content
        carrier_name: Name of the carrier
        documentation_type: Type of documentation (openapi, website, pdf, text, auto)

    Returns:
        Dictionary with analyzed API information
    """
    import re
    import json

    result = {
        "carrier_name": carrier_name,
        "documentation_type": documentation_type,
        "api_type": "unknown",
        "authentication": {},
        "endpoints": {},
        "operations": [],
        "data_formats": [],
        "recommendations": {}
    }

    try:
        # Detect API type
        if documentation_type == "auto":
            if "swagger" in api_documentation.lower() or "openapi" in api_documentation.lower():
                documentation_type = "openapi"
            elif "<" in api_documentation and ">" in api_documentation:
                result["api_type"] = "xml"
            elif "{" in api_documentation and "}" in api_documentation:
                result["api_type"] = "json"

        # Try to parse as OpenAPI/Swagger
        if documentation_type == "openapi":
            try:
                if api_documentation.strip().startswith('{'):
                    spec = json.loads(api_documentation)
                else:
                    # Handle YAML (simplified)
                    spec = {"info": {"title": carrier_name}}

                result.update({
                    "api_type": "rest",
                    "documentation_type": "openapi",
                    "spec_version": spec.get("openapi", spec.get("swagger", "unknown")),
                    "base_url": spec.get("servers", [{}])[0].get("url", "") if spec.get("servers") else "",
                    "paths": list(spec.get("paths", {}).keys()),
                })

                # Extract operations
                for path, methods in spec.get("paths", {}).items():
                    for method, details in methods.items():
                        if method.upper() in ["GET", "POST", "PUT", "DELETE"]:
                            result["endpoints"][f"{method.upper()} {path}"] = {
                                "summary": details.get("summary", ""),
                                "description": details.get("description", ""),
                                "parameters": details.get("parameters", []),
                                "requestBody": details.get("requestBody", {}),
                                "responses": details.get("responses", {})
                            }
            except:
                pass

        # Analyze for common shipping operations
        operations_found = []
        if re.search(r"rate|quote|pricing", api_documentation, re.IGNORECASE):
            operations_found.append("rating")
        if re.search(r"ship|label|create.*shipment", api_documentation, re.IGNORECASE):
            operations_found.append("shipping")
        if re.search(r"track|trace|status", api_documentation, re.IGNORECASE):
            operations_found.append("tracking")
        if re.search(r"pickup|collect", api_documentation, re.IGNORECASE):
            operations_found.append("pickup")
        if re.search(r"address.*valid|verify.*address", api_documentation, re.IGNORECASE):
            operations_found.append("address")

        result["operations"] = operations_found

        # Detect authentication methods
        auth_methods = []
        if re.search(r"api.?key|x-api-key", api_documentation, re.IGNORECASE):
            auth_methods.append("api_key")
        if re.search(r"bearer|authorization.*bearer", api_documentation, re.IGNORECASE):
            auth_methods.append("bearer_token")
        if re.search(r"oauth|client.*secret", api_documentation, re.IGNORECASE):
            auth_methods.append("oauth")
        if re.search(r"basic.*auth|username.*password", api_documentation, re.IGNORECASE):
            auth_methods.append("basic_auth")

        result["authentication"]["methods"] = auth_methods

        # Generate recommendations
        recommendations = {}

        if not result["api_type"] or result["api_type"] == "unknown":
            if "xml" in api_documentation.lower() or "</" in api_documentation:
                recommendations["api_type"] = "xml"
            else:
                recommendations["api_type"] = "json"

        if not operations_found:
            recommendations["operations"] = ["rating", "shipping", "tracking"]
            recommendations["note"] = "Could not detect specific operations, using common defaults"

        if not auth_methods:
            recommendations["authentication"] = "api_key"
            recommendations["auth_note"] = "Could not detect auth method, API key is most common"

        result["recommendations"] = recommendations

        # Generate plugin configuration
        result["suggested_plugin_config"] = {
            "carrier_slug": carrier_name.lower().replace(" ", "_").replace("-", "_"),
            "carrier_name": carrier_name,
            "features": ",".join(operations_found or ["rating", "shipping", "tracking"]),
            "is_xml_api": result.get("api_type") == "xml" or recommendations.get("api_type") == "xml",
            "authentication_type": auth_methods[0] if auth_methods else "api_key"
        }

    except Exception as e:
        result["error"] = str(e)

    return result


def extract_openapi_from_url(url: str) -> typing.Dict[str, typing.Any]:
    """
    Try to extract OpenAPI specification from various common URL patterns.

    Args:
        url: Base URL or documentation URL

    Returns:
        Dictionary with OpenAPI spec if found
    """
    import requests
    import json

    result = {
        "original_url": url,
        "spec_found": False,
        "spec_url": None,
        "spec": None,
        "error": None
    }

    # Common OpenAPI spec URL patterns
    if not url.endswith('/'):
        url += '/'

    spec_patterns = [
        "openapi.json",
        "openapi.yaml",
        "swagger.json",
        "swagger.yaml",
        "api-docs",
        "v1/openapi.json",
        "v2/openapi.json",
        "docs/openapi.json",
        "api/openapi.json",
        "static/openapi.json"
    ]

    headers = {
        'Accept': 'application/json, application/yaml, text/yaml, */*',
        'User-Agent': 'Karrio-Agent/1.0'
    }

    for pattern in spec_patterns:
        try:
            spec_url = url + pattern
            response = requests.get(spec_url, headers=headers, timeout=10)

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()

                # Try to parse as JSON
                if 'json' in content_type or response.text.strip().startswith('{'):
                    try:
                        spec = response.json()
                        if any(key in spec for key in ['openapi', 'swagger', 'info', 'paths']):
                            result.update({
                                "spec_found": True,
                                "spec_url": spec_url,
                                "spec": spec,
                                "format": "json"
                            })
                            return result
                    except json.JSONDecodeError:
                        continue

                # Try to parse as YAML
                elif 'yaml' in content_type or any(indicator in response.text for indicator in ['openapi:', 'swagger:', 'info:', 'paths:']):
                    result.update({
                        "spec_found": True,
                        "spec_url": spec_url,
                        "spec": response.text,
                        "format": "yaml"
                    })
                    return result

        except requests.RequestException:
            continue

    result["error"] = "No OpenAPI specification found at common endpoints"
    return result
