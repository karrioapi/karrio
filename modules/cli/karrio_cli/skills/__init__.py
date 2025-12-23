"""Karrio CLI Skills Registry.

This module provides access to AI skills that can be loaded for
various Karrio development tasks.

Available Skills:
- carrier-integration: Comprehensive carrier integration development

Usage:
    from karrio_cli.skills import get_skill, list_skills, SKILL_REGISTRY
    
    # List all skills
    skills = list_skills()
    
    # Get full skill with metadata, instructions, and examples
    skill = get_skill("carrier-integration")
    
    # Get specific example
    example = get_skill_example("carrier-integration", "lib_reference")
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

SKILLS_DIR = Path(__file__).parent


# Skill registry for quick reference and validation
SKILL_REGISTRY = {
    "carrier-integration": {
        "description": "Comprehensive carrier integration development skill",
        "features": [
            "rating", "shipping", "tracking", "pickup", "manifest",
            "document", "address", "duties", "insurance", "webhook", "oauth"
        ],
        "examples": [
            "lib_reference",
            "models_reference",
            "rate_implementation",
            "tracking_implementation",
            "shipment_implementation",
            "pickup_implementation",
            "webhook_oauth_implementation",
            "manifest_document_address_implementation",
            "duties_insurance_implementation",
            "error_proxy_settings_patterns",
            "units_template",
        ],
        "lib_utilities": {
            "data_parsing": ["to_dict", "to_dict_safe", "to_json", "to_object", "to_element", "to_xml"],
            "string_manipulation": ["text", "join", "to_snake_case", "to_slug"],
            "number_formatting": ["to_int", "to_decimal", "to_money", "format_decimal", "to_list"],
            "date_time": ["fdate", "ftime", "fdatetime", "ftimestamp", "fiso_timestamp", "to_date"],
            "address": ["to_address", "to_zip5", "to_zip4", "to_country_name", "to_state_name"],
            "shipping": ["to_packages", "to_services", "to_shipping_options", "to_customs_info", "to_commodities"],
            "multi_piece": ["to_multi_piece_rates", "to_multi_piece_shipment"],
            "http": ["request", "to_query_string", "run_concurently", "run_asynchronously"],
            "documents": ["image_to_pdf", "bundle_pdfs", "bundle_base64", "zpl_to_pdf", "encode_base64"],
            "utilities": ["failsafe", "identity", "sort_events", "to_buffer", "decode"]
        }
    }
}


# Skill identifiers
CARRIER_INTEGRATION_SKILL = "carrier-integration"


def list_skills() -> List[Dict[str, Any]]:
    """List all available skills.
    
    Returns:
        List of skill metadata dictionaries.
    """
    skills = []
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and (skill_dir / "skill.json").exists():
            with open(skill_dir / "skill.json") as f:
                metadata = json.load(f)
                metadata["path"] = str(skill_dir)
                skills.append(metadata)
    return skills


def get_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific skill by name.
    
    Args:
        skill_name: The skill name (e.g., 'carrier-integration')
        
    Returns:
        Skill metadata and content, or None if not found.
    """
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        return None
    
    skill_json = skill_dir / "skill.json"
    if not skill_json.exists():
        return None
    
    with open(skill_json) as f:
        metadata = json.load(f)
    
    # Load instructions
    instructions_file = skill_dir / "instructions.md"
    if instructions_file.exists():
        metadata["instructions"] = instructions_file.read_text()
    
    # Load examples
    examples_dir = skill_dir / "examples"
    if examples_dir.exists():
        metadata["examples"] = {}
        for example_file in examples_dir.glob("*.py"):
            metadata["examples"][example_file.stem] = example_file.read_text()
    
    # Add registry info
    if skill_name in SKILL_REGISTRY:
        metadata["registry"] = SKILL_REGISTRY[skill_name]
    
    metadata["path"] = str(skill_dir)
    return metadata


def get_skill_instructions(skill_name: str) -> Optional[str]:
    """Get the instructions for a skill.
    
    Args:
        skill_name: The skill name
        
    Returns:
        Instructions markdown content, or None if not found.
    """
    skill = get_skill(skill_name)
    return skill.get("instructions") if skill else None


def get_skill_examples(skill_name: str) -> Dict[str, str]:
    """Get all examples for a skill.
    
    Args:
        skill_name: The skill name
        
    Returns:
        Dictionary mapping example names to their content.
    """
    skill = get_skill(skill_name)
    return skill.get("examples", {}) if skill else {}


def get_skill_example(skill_name: str, example_name: str) -> Optional[str]:
    """Get a specific example from a skill.
    
    Args:
        skill_name: The skill name
        example_name: The example name (without .py extension)
        
    Returns:
        Example content, or None if not found.
    """
    examples = get_skill_examples(skill_name)
    return examples.get(example_name)


def get_skill_summary(skill_name: str) -> Optional[str]:
    """Get a concise summary of a skill.
    
    Args:
        skill_name: The skill name
        
    Returns:
        Formatted summary string, or None if not found.
    """
    skill = get_skill(skill_name)
    if not skill:
        return None
    
    registry_info = SKILL_REGISTRY.get(skill_name, {})
    
    lines = [
        f"# {skill.get('display_title', skill_name)}",
        f"Version: {skill.get('version', 'unknown')}",
        "",
        skill.get('description', 'No description available.'),
    ]
    
    if registry_info.get("features"):
        lines.extend([
            "",
            f"## Supported Features ({len(registry_info['features'])})",
            ", ".join(registry_info['features']),
        ])
    
    if registry_info.get("examples"):
        lines.extend([
            "",
            f"## Examples ({len(registry_info['examples'])})",
            ", ".join(registry_info['examples']),
        ])
    
    if registry_info.get("lib_utilities"):
        lines.extend([
            "",
            "## karrio.lib Utilities Categories",
            ", ".join(registry_info['lib_utilities'].keys()),
        ])
    
    if skill.get("capabilities"):
        lines.extend([
            "",
            f"## Capabilities ({len(skill['capabilities'])})",
            ", ".join(skill['capabilities'][:10]) + ("..." if len(skill['capabilities']) > 10 else ""),
        ])
    
    return "\n".join(lines)


def get_lib_utilities_reference(category: Optional[str] = None) -> Dict[str, List[str]]:
    """Get karrio.lib utilities reference.
    
    Args:
        category: Optional category to filter (e.g., 'data_parsing', 'address')
        
    Returns:
        Dictionary of utility categories and their functions.
    """
    lib_utils = SKILL_REGISTRY.get("carrier-integration", {}).get("lib_utilities", {})
    
    if category:
        return {category: lib_utils.get(category, [])}
    
    return lib_utils


__all__ = [
    "list_skills",
    "get_skill",
    "get_skill_instructions",
    "get_skill_examples",
    "get_skill_example",
    "get_skill_summary",
    "get_lib_utilities_reference",
    "SKILL_REGISTRY",
    "CARRIER_INTEGRATION_SKILL",
]
