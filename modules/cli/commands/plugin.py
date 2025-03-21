import os
import sys
import shutil
import typer
from typing import Optional, Dict, Any
from pathlib import Path

# Import shared utilities
from .carrier import find_karrio_root

app = typer.Typer(help="Plugin management commands")


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


@app.command()
def create_plugin_interactive():
    """Create a new plugin interactively with prompts for all required information."""
    plugin_name = typer.prompt("Enter the plugin name (e.g., address_validator)")
    display_name = typer.prompt("Enter the display name (e.g., \"Address Validator\")")
    description = typer.prompt("Enter a brief description of what the plugin does")
    author = typer.prompt("Enter the plugin author name")
    version = typer.prompt("Enter the initial plugin version", default="0.1.0")
    carrier_integration = typer.prompt("Enter a carrier to integrate with (leave empty if not carrier-specific)", default="")
    
    # Call the main create_plugin function with the gathered inputs
    create_plugin(
        plugin_name=plugin_name,
        display_name=display_name,
        description=description,
        author=author,
        version=version,
        carrier_integration=carrier_integration if carrier_integration else None
    ) 
