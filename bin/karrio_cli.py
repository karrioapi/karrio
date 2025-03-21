#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import typer
from typing import Optional, List
from pathlib import Path
from enum import Enum

app = typer.Typer(help="Karrio carrier integration CLI tools")


class Feature(str, Enum):
    TRACKING = "tracking"
    RATING = "rating"
    SHIPPING = "shipping"


def find_karrio_root() -> Optional[Path]:
    """Find the Karrio root directory by traversing up from the current directory."""
    current_dir = Path.cwd()
    
    # Try traversing up from current directory
    while current_dir != current_dir.parent:
        if any((current_dir / marker).exists() for marker in ["create-carrier.sh", "requirements.txt", "setup.py"]):
            return current_dir
        current_dir = current_dir.parent
    
    # If not found, try the absolute path
    absolute_path = Path("/Users/shadrackaddo/karrio")
    if any((absolute_path / marker).exists() for marker in ["create-carrier.sh", "requirements.txt", "setup.py"]):
        return absolute_path
    
    return None


def run_script(script_name: str, args: List[str]=None, shell: bool=False):
    """Run a script from the Karrio root directory."""
    karrio_root = find_karrio_root()
    if not karrio_root:
        typer.echo("Error: Could not find Karrio root directory.")
        typer.echo("Please make sure you're within a Karrio project or specify the path.")
        sys.exit(1)
    
    if shell:
        cmd = f"{script_name} {' '.join(args) if args else ''}"
    else:
        script_path = karrio_root / script_name
        if not script_path.exists():
            typer.echo(f"Error: Script {script_name} not found at {script_path}")
            sys.exit(1)
        
        # Make sure the script is executable
        os.chmod(script_path, 0o755)
        
        # Build the command
        cmd = [str(script_path)]
        if args:
            cmd.extend(args)
    
    # Run the command
    try:
        if shell:
            subprocess.run(cmd, cwd=str(karrio_root), shell=True, check=True)
        else:
            subprocess.run(cmd, cwd=str(karrio_root), check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error running {script_name}: {e}")
        sys.exit(e.returncode)


def ensure_directory_structure():
    """Ensure the required directory structure exists."""
    karrio_root = find_karrio_root()
    if not karrio_root:
        return
    
    # Create plugins directory
    plugins_path = karrio_root / "plugins"
    plugins_path.mkdir(exist_ok=True)
    
    # Use existing carriers as templates
    connectors_path = karrio_root / "modules" / "connectors"
    if connectors_path.exists():
        # Look for established carriers to use as templates (e.g., ups, fedex, dhl)
        template_carriers = ["ups", "fedex", "dhl"]
        for carrier in template_carriers:
            carrier_path = connectors_path / carrier
            if carrier_path.exists():
                typer.echo(f"Using {carrier} as template carrier...")
                return
        
        # If none of the preferred carriers exist, use the first available carrier
        for carrier_dir in connectors_path.glob("*"):
            if carrier_dir.is_dir() and not carrier_dir.name.startswith("test"):
                typer.echo(f"Using {carrier_dir.name} as template carrier...")
                return
    
    typer.echo("Warning: No existing carriers found to use as templates.")


@app.command()
def add_extension(
    carrier_slug: str=typer.Option(..., help="Karrio unique carrier_name"),
    display_name: str=typer.Option(..., help="Carrier label used throughout the app"),
    features: str=typer.Option(
        "tracking,rating,shipping",
        help="The carrier features to integrate (comma-separated)"
    ),
    version: str=typer.Option("2024.3", "--version", "-v", help="Extension initial version"),
    is_xml: bool=typer.Option(
        False,
        "--xml/--json",
        "-x/-j",
        help="Specify whether the carrier API data format is XML"
    ),
    no_prompt: bool=typer.Option(
        False,
        "--no-prompt",
        help="Skip interactive prompts and use default values"
    )
):
    """Add a new carrier extension following Karrio's official format."""
    ensure_directory_structure()
    
    karrio_root = find_karrio_root()
    connectors_path = karrio_root / "modules" / "connectors"
    
    # Find a suitable template carrier
    template_carrier = None
    preferred_carriers = ["ups", "fedex", "dhl"]
    
    # First try preferred carriers
    for carrier in preferred_carriers:
        if (connectors_path / carrier).exists():
            template_carrier = carrier
            break
    
    # If no preferred carrier found, use the first available non-test carrier
    if not template_carrier:
        for carrier_dir in connectors_path.glob("*"):
            if carrier_dir.is_dir() and not carrier_dir.name.startswith("test"):
                template_carrier = carrier_dir.name
                break
    
    if not template_carrier:
        typer.echo("Error: No template carrier found in modules/connectors/")
        sys.exit(1)
    
    typer.echo(f"Using {template_carrier} as template for new carrier...")
    
    # Copy template carrier structure
    source_carrier = connectors_path / template_carrier
    new_carrier = connectors_path / carrier_slug
    
    # Copy template carrier files
    if source_carrier.exists() and not new_carrier.exists():
        shutil.copytree(str(source_carrier), str(new_carrier), dirs_exist_ok=True)
        
        # Update package name in setup.py
        setup_py = new_carrier / "setup.py"
        if setup_py.exists():
            with open(setup_py, "r") as f:
                content = f.read()
            content = content.replace(f"karrio.{template_carrier}", f"karrio.{carrier_slug}")
            content = content.replace(f"karrio-{template_carrier}", f"karrio-{carrier_slug}")
            content = content.replace(template_carrier.title(), carrier_slug.title())
            with open(setup_py, "w") as f:
                f.write(content)
        
        # Update package structure
        old_provider = new_carrier / "karrio" / "providers" / template_carrier
        new_provider = new_carrier / "karrio" / "providers" / carrier_slug
        if old_provider.exists():
            old_provider.rename(new_provider)
        
        # Update imports in Python files
        for py_file in new_carrier.rglob("*.py"):
            if py_file.is_file():
                with open(py_file, "r") as f:
                    content = f.read()
                content = content.replace(f"karrio.{template_carrier}", f"karrio.{carrier_slug}")
                content = content.replace(f"providers.{template_carrier}", f"providers.{carrier_slug}")
                with open(py_file, "w") as f:
                    f.write(content)
        
        typer.echo(f"Successfully created carrier extension: {display_name} ({carrier_slug})")
        typer.echo(f"Carrier created at: {new_carrier}")
        typer.echo("\nNext steps:")
        typer.echo("1. Update the carrier's API configuration in settings.py")
        typer.echo("2. Customize the API endpoints in the provider files")
        typer.echo("3. Update the JSON schema files to match your carrier's API")
        typer.echo("4. Run ./generate to update the generated code")


@app.command()
def create_carrier(
    carrier_name: str=typer.Argument(..., help="The slug name for the carrier (e.g., fedex_custom)"),
    display_name: str=typer.Argument(..., help="The display name for the carrier (e.g., \"FedEx Custom\")"),
    dry_run: bool=typer.Option(False, "--dry-run", help="Run in dry-run mode without making changes"),
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Create a new carrier integration with the specified name and display name."""
    ensure_directory_structure()
    
    # First use the official add-extension command
    add_extension(
        carrier_slug=carrier_name,
        display_name=display_name,
        features="tracking,rating,shipping",
        version="2024.3",
        is_xml=False,
        no_prompt=no_prompt
    )
    
    if not dry_run:
        # Additional setup from our improvements
        args = [carrier_name, display_name]
        if no_prompt:
            args.append("--no-prompt")
        run_script("create-carrier.sh", args)


@app.command()
def troubleshoot(
    carrier_name: Optional[str]=typer.Argument(None, help="The name of the carrier to troubleshoot"),
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Diagnose common issues with carrier integrations."""
    ensure_directory_structure()
    
    args = []
    if carrier_name:
        args.append(carrier_name)
    if no_prompt:
        args.append("--no-prompt")
    run_script("troubleshoot-carrier.sh", args)


@app.command()
def start_docs(
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Start the documentation server for carrier integrations."""
    ensure_directory_structure()
    
    args = []
    if no_prompt:
        args.append("--no-prompt")
    run_script("start-docs.sh", args)


@app.command()
def run_tests(
    verbose: bool=typer.Option(True, "--verbose", "-v", help="Run tests in verbose mode"),
    coverage: bool=typer.Option(False, "--coverage", "-c", help="Run tests with coverage"),
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Run tests for carrier integrations."""
    ensure_directory_structure()
    
    args = []
    if verbose:
        args.append("--verbose")
    if coverage:
        args.append("--coverage")
    if no_prompt:
        args.append("--no-prompt")
    run_script("run-all-tests.sh", args)


@app.command()
def generate_api(
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Generate API code from JSON schemas."""
    ensure_directory_structure()
    
    args = []
    if no_prompt:
        args.append("--no-prompt")
    
    # Run the generate script in each carrier directory
    karrio_root = find_karrio_root()
    plugins_path = karrio_root / "plugins"
    for carrier_dir in plugins_path.glob("*"):
        if (carrier_dir / "generate").exists():
            typer.echo(f"Generating API code for {carrier_dir.name}...")
            subprocess.run(["./generate"], cwd=str(carrier_dir), check=True)


@app.command()
def migrate_structure(
    carrier_name: str=typer.Argument(..., help="Name of the carrier to migrate"),
    dry_run: bool=typer.Option(False, "--dry-run", help="Show what would be done without making changes"),
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Migrate a carrier to the new structure."""
    ensure_directory_structure()
    
    args = [carrier_name]
    if dry_run:
        args.append("--dry-run")
    if no_prompt:
        args.append("--no-prompt")
    run_script("migrate-carrier.sh", args)


@app.command()
def create_plugin(
    plugin_name: str=typer.Option(..., prompt=True, help="Name of the plugin (e.g., address_validator)"),
    display_name: str=typer.Option(..., prompt=True, help="Display name of the plugin (e.g., \"Address Validator\")"),
    description: str=typer.Option(..., prompt=True, help="Brief description of what the plugin does"),
    author: str=typer.Option(..., prompt=True, help="Plugin author name"),
    version: str=typer.Option("0.1.0", prompt=True, help="Initial plugin version"),
    carrier_integration: str=typer.Option(None, prompt=True, help="Carrier to integrate with (leave empty if not carrier-specific)"),
):
    """Create a new plugin in the plugins directory."""
    karrio_root = find_karrio_root()
    if not karrio_root:
        typer.echo("Error: Could not find Karrio root directory.")
        typer.echo("Please make sure you're within a Karrio project or specify the path.")
        sys.exit(1)
    
    # Create plugins directory if it doesn't exist
    plugins_dir = karrio_root / "plugins"
    plugins_dir.mkdir(exist_ok=True)
    
    # Create plugin directory
    plugin_dir = plugins_dir / plugin_name
    if plugin_dir.exists():
        if not typer.confirm(f"Plugin directory {plugin_dir} already exists. Overwrite?"):
            typer.echo("Aborting plugin creation.")
            return
        shutil.rmtree(plugin_dir)
    
    plugin_dir.mkdir(exist_ok=True)
    
    # Create basic plugin structure
    (plugin_dir / "src").mkdir(exist_ok=True)
    (plugin_dir / "tests").mkdir(exist_ok=True)
    
    # Create README.md
    with open(plugin_dir / "README.md", "w") as f:
        f.write(f"""# {display_name}

{description}

## Installation

```bash
pip install -e ./plugins/{plugin_name}
```

## Usage

```python
import karrio
from karrio.plugins.{plugin_name} import plugin

# Plugin usage example
# ...
```

## Development

1. Clone the repository
2. Install the plugin in development mode
3. Run tests

```bash
cd plugins/{plugin_name}
pip install -e .
pytest
```
""")

    # Create setup.py
    with open(plugin_dir / "setup.py", "w") as f:
        f.write(f"""from setuptools import setup, find_namespace_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=f"karrio.plugin.{plugin_name}",
    version="{version}",
    author="{author}",
    author_email="author@example.com",
    description="{description}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    project_urls={{
        "Documentation": "https://docs.karrio.io/",
        "Source": "https://github.com/karrioapi/karrio",
    }},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={{"": "src"}},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "karrio",
    ],
    python_requires=">=3.8",
)
""")

    # Create src package structure
    karrio_plugin_dir = plugin_dir / "src" / "karrio" / "plugins" / plugin_name
    karrio_plugin_dir.mkdir(parents=True, exist_ok=True)
    
    # Create basic __init__.py
    with open(karrio_plugin_dir / "__init__.py", "w") as f:
        f.write(f"""\"\"\"
{display_name} plugin for Karrio.

{description}
\"\"\"

__version__ = "{version}"
""")

    # Create plugin.py
    with open(karrio_plugin_dir / "plugin.py", "w") as f:
        f.write(f"""\"\"\"
Main plugin implementation for {display_name}.
\"\"\"

from typing import Dict, Any, Optional
from karrio.core.models import Message


class {plugin_name.replace('_', ' ').title().replace(' ', '')}Plugin:
    \"\"\"
    {display_name} plugin implementation.
    \"\"\"

    def __init__(self, settings: Dict[str, Any]):
        \"\"\"
        Initialize the plugin with settings.
        
        Args:
            settings: Plugin configuration settings
        \"\"\"
        self.settings = settings
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"
        Execute the plugin with the provided data.
        
        Args:
            data: Input data for the plugin
            
        Returns:
            Dict[str, Any]: Result of the plugin execution
        \"\"\"
        # Implement your plugin logic here
        result = {{
            "success": True,
            "data": data,
            "messages": []
        }}
        
        return result
        
    def validate(self, data: Dict[str, Any]) -> Optional[Message]:
        \"\"\"
        Validate the input data.
        
        Args:
            data: Input data to validate
            
        Returns:
            Optional[Message]: Error message if validation fails, None otherwise
        \"\"\"
        # Implement validation logic here
        return None
""")

    # Create test file
    with open(plugin_dir / "tests" / "test_plugin.py", "w") as f:
        f.write(f"""\"\"\"
Tests for the {display_name} plugin.
\"\"\"

import unittest
from karrio.plugins.{plugin_name}.plugin import {plugin_name.replace('_', ' ').title().replace(' ', '')}Plugin


class Test{plugin_name.replace('_', ' ').title().replace(' ', '')}Plugin(unittest.TestCase):
    \"\"\"Test cases for {display_name} plugin.\"\"\"

    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        self.plugin = {plugin_name.replace('_', ' ').title().replace(' ', '')}Plugin(settings={{}})
        
    def test_initialization(self):
        \"\"\"Test plugin initialization.\"\"\"
        self.assertIsNotNone(self.plugin)
        
    def test_execute(self):
        \"\"\"Test plugin execution.\"\"\"
        test_data = {{"test": "data"}}
        result = self.plugin.execute(test_data)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], test_data)


if __name__ == "__main__":
    unittest.main()
""")

    # Create carrier-specific integration if specified
    if carrier_integration:
        # Create carrier integration directory
        carrier_dir = karrio_plugin_dir / "carriers" / carrier_integration
        carrier_dir.mkdir(parents=True, exist_ok=True)
        
        # Create carrier integration file
        with open(carrier_dir / "__init__.py", "w") as f:
            f.write(f"""\"\"\"
{carrier_integration.title()} integration for {display_name} plugin.
\"\"\"

from typing import Dict, Any


def execute(settings: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    Execute the {carrier_integration.title()} integration with the provided data.
    
    Args:
        settings: Plugin configuration settings
        data: Input data for the integration
        
    Returns:
        Dict[str, Any]: Result of the integration execution
    \"\"\"
    # Implement carrier-specific integration logic here
    result = {{
        "carrier": "{carrier_integration}",
        "success": True,
        "data": data,
        "messages": []
    }}
    
    return result
""")

    typer.echo(f"\n✅ Plugin {display_name} created successfully at {plugin_dir}")
    typer.echo("\nNext steps:")
    typer.echo(f"1. Implement your plugin logic in {plugin_dir}/src/karrio/plugins/{plugin_name}/plugin.py")
    typer.echo(f"2. Add tests in {plugin_dir}/tests/")
    typer.echo(f"3. Install your plugin with: pip install -e {plugin_dir}")
    typer.echo("4. Use your plugin in your Karrio application")


if __name__ == "__main__":
    app() 
