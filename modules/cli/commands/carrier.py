import os
import sys
import shutil
import subprocess
import typer
from typing import Optional, List
from pathlib import Path
from enum import Enum
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(help="Carrier integration management commands")


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
def create_carrier(
    carrier_name: str=typer.Argument(..., help="The slug name for the carrier (e.g., fedex_custom)"),
    display_name: str=typer.Argument(..., help="The display name for the carrier (e.g., \"FedEx Custom\")"),
    dry_run: bool=typer.Option(False, "--dry-run", help="Run in dry-run mode without making changes"),
    no_prompt: bool=typer.Option(False, "--no-prompt", help="Skip interactive prompts and use default values")
):
    """Create a new carrier integration with the specified name and display name."""
    ensure_directory_structure()
    
    if not dry_run:
        # Run the carrier creation script
        args = [carrier_name, display_name]
        if no_prompt:
            args.append("--no-prompt")
        run_script("create-carrier.sh", args)


@app.command()
def create_carrier_interactive():
    """Create a new carrier integration interactively with prompts for all required information."""
    ensure_directory_structure()
    
    # Prompt for carrier slug
    carrier_name = typer.prompt("Enter the carrier slug (e.g., fedex_custom)")
    
    # Prompt for display name
    display_name = typer.prompt("Enter the display name (e.g., \"FedEx Custom\")")
    
    # Confirm creation
    if typer.confirm(f"Create carrier integration for '{display_name}' with slug '{carrier_name}'?"):
        # Run the carrier creation script
        args = [carrier_name, display_name]
        run_script("create-carrier.sh", args)
    else:
        typer.echo("Carrier creation cancelled.")


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
