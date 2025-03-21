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


@app.command()
def create_plugin(
    plugin_name: Optional[str]=typer.Option(None, prompt=True, help="Name of the plugin (e.g., address_validator)"),
    display_name: Optional[str]=typer.Option(None, prompt=True, help="Display name of the plugin (e.g., \"Address Validator\")"),
    description: Optional[str]=typer.Option(None, prompt=True, help="Brief description of what the plugin does"),
    author: Optional[str]=typer.Option(None, prompt=True, help="Plugin author name"),
    version: str=typer.Option("0.1.0", prompt=True, help="Initial plugin version"),
    carrier_integration: Optional[str]=typer.Option(None, prompt=True, help="Carrier to integrate with (leave empty if not carrier-specific)"),
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
    
    # Create README.md, setup.py and other files here...
    # (Simplified for the example)
    
    typer.echo(f"\n✅ Plugin {display_name} created successfully at {plugin_dir}")
    typer.echo("\nNext steps:")
    typer.echo(f"1. Implement your plugin logic in {plugin_dir}/src/karrio/plugins/{plugin_name}/plugin.py")
    typer.echo(f"2. Add tests in {plugin_dir}/tests/")
    typer.echo(f"3. Install your plugin with: pip install -e {plugin_dir}")
    typer.echo("4. Use your plugin in your Karrio application")


@app.command()
def create_carrier(
    carrier_name: Optional[str]=typer.Option(None, prompt=True, help="The slug name for the carrier (e.g., fedex_custom)"),
    display_name: Optional[str]=typer.Option(None, prompt=True, help="The display name for the carrier (e.g., \"FedEx Custom\")"),
    dry_run: bool=typer.Option(False, "--dry-run", help="Run in dry-run mode without making changes"),
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Create a new carrier integration with the specified name and display name."""
    karrio_root = find_karrio_root()
    if not karrio_root:
        typer.echo("Error: Could not find Karrio root directory.")
        typer.echo("Please make sure you're within a Karrio project or specify the path.")
        sys.exit(1)
    
    if no_prompt and (carrier_name is None or display_name is None):
        typer.echo("Error: carrier_name and display_name are required when --no-prompt is used")
        sys.exit(1)
    
    # Create carrier directory structure
    carrier_slug = carrier_name.strip().lower()
    carrier_dir = karrio_root / "modules" / "connectors" / carrier_slug
    
    # Templates directory
    templates_dir = karrio_root / "templates" / "carrier"
    
    if dry_run:
        typer.echo(f"Would create carrier '{display_name}' with slug '{carrier_slug}' at {carrier_dir}")
        return
    
    # Create directories
    typer.echo(f"Creating carrier integration for {display_name} ({carrier_slug})...")
    
    # Create main directories
    carrier_dir.mkdir(exist_ok=True, parents=True)
    (carrier_dir / "karrio" / "providers" / carrier_slug).mkdir(exist_ok=True, parents=True)
    (carrier_dir / "karrio" / "mappers" / carrier_slug).mkdir(exist_ok=True, parents=True)
    (carrier_dir / "tests").mkdir(exist_ok=True, parents=True)
    (carrier_dir / "schemas").mkdir(exist_ok=True, parents=True)
    
    # Create __init__.py file
    init_content = f"from karrio.providers.{carrier_slug}.rate import rate_request, parse_rate_response\n"
    init_content += f"from karrio.providers.{carrier_slug}.error import parse_error_response\n"
    init_content += f"from karrio.providers.{carrier_slug}.utils import create_xml_request_header, create_xml_response_header\n\n"
    init_content += "__all__ = [\n"
    init_content += "    \"rate_request\",\n"
    init_content += "    \"parse_rate_response\",\n"
    init_content += "    \"parse_error_response\",\n"
    init_content += "    \"create_xml_request_header\",\n"
    init_content += "    \"create_xml_response_header\",\n"
    init_content += "]\n"
    
    with open(carrier_dir / "__init__.py", "w") as f:
        f.write(init_content)
    
    # Create setup.py
    setup_content = "from setuptools import setup, find_namespace_packages\n\n"
    setup_content += "# Read README.md\n"
    setup_content += "with open(\"README.md\", \"r\", encoding=\"utf-8\") as fh:\n"
    setup_content += "    long_description = fh.read()\n\n"
    setup_content += "setup(\n"
    setup_content += f"    name=f\"karrio.{carrier_slug}\",\n"
    setup_content += "    version=\"2024.3\",\n"
    setup_content += "    author=\"Karrio Team\",\n"
    setup_content += "    author_email=\"hello@karrio.io\",\n"
    setup_content += f"    description=\"Karrio {display_name} carrier integration\",\n"
    setup_content += "    long_description=long_description,\n"
    setup_content += "    long_description_content_type=\"text/markdown\",\n"
    setup_content += "    url=\"https://karrio.io\",\n"
    setup_content += "    project_urls={\n"
    setup_content += "        \"Bug Tracker\": \"https://github.com/karrioapi/karrio/issues\",\n"
    setup_content += "    },\n"
    setup_content += "    classifiers=[\n"
    setup_content += "        \"Programming Language :: Python :: 3\",\n"
    setup_content += "        \"License :: OSI Approved :: MIT License\",\n"
    setup_content += "        \"Operating System :: OS Independent\",\n"
    setup_content += "    ],\n"
    setup_content += "    packages=find_namespace_packages(include=[\"karrio.*\"]),\n"
    setup_content += "    python_requires=\">=3.8\",\n"
    setup_content += "    install_requires=[\n"
    setup_content += "        \"karrio\",\n"
    setup_content += "    ],\n"
    setup_content += ")\n"
    
    with open(carrier_dir / "setup.py", "w") as f:
        f.write(setup_content)
    
    # Create README.md
    readme_content = f"# {display_name} Integration\n\n"
    readme_content += f"This package provides integration with {display_name} API services.\n\n"
    readme_content += "## Installation\n\n"
    readme_content += "```bash\n"
    readme_content += "pip install -e .\n"
    readme_content += "```\n\n"
    readme_content += "## Features\n\n"
    readme_content += "- Rating\n"
    readme_content += "- Shipping\n"
    readme_content += "- Tracking\n\n"
    readme_content += "## Configuration\n\n"
    readme_content += f"Add your {display_name} credentials to the settings:\n\n"
    readme_content += "```python\n"
    readme_content += "settings = {\n"
    readme_content += "    \"api_key\": \"your_api_key\",\n"
    readme_content += "    \"password\": \"your_password\",\n"
    readme_content += "    \"account_number\": \"your_account\",\n"
    readme_content += "    \"test_mode\": True,\n"
    readme_content += "}\n"
    readme_content += "```\n"
    
    with open(carrier_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    # Copy template files
    for template_file in ['settings.py', 'rate.py', 'error.py', 'utils.py', 'ship.py']:
        source_path = templates_dir / template_file
        if source_path.exists():
            if template_file == 'settings.py':
                dest_path = carrier_dir / "karrio" / "mappers" / carrier_slug / template_file
            else:
                dest_path = carrier_dir / "karrio" / "providers" / carrier_slug / template_file
            
            # Create parent directories if they don't exist
            dest_path.parent.mkdir(exist_ok=True, parents=True)
            
            # Read template content
            with open(source_path, "r") as src:
                content = src.read()
            
            # Replace placeholders
            content = content.replace("[CARRIER_NAME]", display_name)
            content = content.replace("[carrier_slug]", carrier_slug)
            content = content.replace("[carrier_domain]", f"{carrier_slug}.com")
            
            # Write to destination
            with open(dest_path, "w") as dst:
                dst.write(content)
            
            typer.echo(f"Created {template_file} for {carrier_slug}")
    
    # Create generate script
    generate_content = "#!/bin/bash\n\n"
    generate_content += "# Generate Python types from JSON schema\n"
    generate_content += "echo \"Generating Python types from schemas...\"\n\n"
    generate_content += "# TODO: Add schema generation commands here\n\n"
    generate_content += "echo \"Python types generation complete!\"\n"
    
    with open(carrier_dir / "generate", "w") as f:
        f.write(generate_content)
    
    # Make the generate script executable
    os.chmod(carrier_dir / "generate", 0o755)
    
    # Create a test file
    test_file = carrier_dir / "tests" / f"test_{carrier_slug}.py"
    test_content = "import unittest\n"
    test_content += "from datetime import datetime\n"
    test_content += "from karrio.core.models import (\n"
    test_content += "    RateRequest, TrackingRequest, ShipmentRequest,\n"
    test_content += "    Address, Parcel\n"
    test_content += ")\n\n\n"
    test_content += f"class Test{display_name.replace(' ', '')}(unittest.TestCase):\n"
    test_content += f"    \"\"\"Test {display_name} carrier integration.\"\"\"\n\n"
    test_content += "    def setUp(self):\n"
    test_content += "        self.settings = {\n"
    test_content += "            \"api_key\": \"test_api_key\",\n"
    test_content += "            \"password\": \"test_password\",\n"
    test_content += "            \"account_number\": \"test_account\",\n"
    test_content += "            \"test_mode\": True,\n"
    test_content += "        }\n\n"
    test_content += "    def test_rate_request(self):\n"
    test_content += "        \"\"\"Test rate request.\"\"\"\n"
    test_content += "        request = RateRequest(\n"
    test_content += "            shipper=Address(\n"
    test_content += "                address_line1=\"123 Main St\",\n"
    test_content += "                city=\"San Francisco\",\n"
    test_content += "                state_code=\"CA\",\n"
    test_content += "                postal_code=\"94105\",\n"
    test_content += "                country_code=\"US\",\n"
    test_content += "            ),\n"
    test_content += "            recipient=Address(\n"
    test_content += "                address_line1=\"456 Market St\",\n"
    test_content += "                city=\"Los Angeles\",\n"
    test_content += "                state_code=\"CA\",\n"
    test_content += "                postal_code=\"90001\",\n"
    test_content += "                country_code=\"US\",\n"
    test_content += "            ),\n"
    test_content += "            parcels=[\n"
    test_content += "                Parcel(\n"
    test_content += "                    weight=10.0,\n"
    test_content += "                    weight_unit=\"LB\",\n"
    test_content += "                )\n"
    test_content += "            ],\n"
    test_content += "            date=datetime.now(),\n"
    test_content += "        )\n"
    test_content += "        \n"
    test_content += "        # Skip actual test for now\n"
    test_content += "        self.assertTrue(True)\n\n\n"
    test_content += "if __name__ == \"__main__\":\n"
    test_content += "    unittest.main()\n"
    
    with open(test_file, "w") as f:
        f.write(test_content)
    
    typer.echo(f"\n✅ Successfully created carrier integration: {display_name} ({carrier_slug})")
    typer.echo(f"Carrier created at: {carrier_dir}")
    typer.echo("\nNext steps:")
    typer.echo("1. Update the carrier's API configuration in settings.py")
    typer.echo("2. Customize the API endpoints in the provider files")
    typer.echo("3. Update the template files to match your carrier's API")
    typer.echo("4. Run the generate script to update the generated code")


if __name__ == "__main__":
    app()
