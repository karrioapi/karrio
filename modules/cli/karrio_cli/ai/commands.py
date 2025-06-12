import os
import sys
import typer
import subprocess
import decouple
from pathlib import Path

app = typer.Typer()

# Find the workspace root (where .env should be located)
# Work relative to current working directory instead of going up levels
current_file = Path(__file__).resolve()
current_working_dir = Path.cwd()  # This will be the patch directory
workspace_root = current_working_dir  # Use current directory as workspace root

# Look for .env files in multiple locations (prioritizing current working directory)
env_locations = [
    workspace_root / ".env",  # Current working directory .env (patch/.env)
    current_file.parent / ".env",  # Local AI directory .env
    workspace_root / ".env.local",  # Alternative naming in current dir
]

# Find the first existing .env file
env_file = None
for location in env_locations:
    if location.exists():
        env_file = location
        break

# Configure decouple to use the found .env file or system environment
if env_file:
    config = decouple.Config(decouple.RepositoryEnv(str(env_file)))
    print(f"Loading environment from: {env_file}")
else:
    config = decouple.AutoConfig()  # Use AutoConfig instead of RepositoryEnv without source
    print("No .env file found, using system environment variables only")

@app.command()
def web():
    """
    Launches the Karrio AI agent web UI.
    This function loads environment variables, and then uses the `adk` command-line
    tool to start the agent's web UI.
    """
    # Load environment variables using python-decouple
    google_api_key = config('GOOGLE_API_KEY', default='YOUR_API_KEY_HERE')
    google_genai_use_vertexai = config('GOOGLE_GENAI_USE_VERTEXAI', default='FALSE')

    # Verify API key is properly set
    if google_api_key == 'YOUR_API_KEY_HERE':
        print("❌ Error: GOOGLE_API_KEY not found!")
        print(f"📍 Searched for .env files in:")
        for location in env_locations:
            exists = "✅" if location.exists() else "❌"
            print(f"   {exists} {location}")
        print("\n💡 To fix this:")
        print(f"   1. Create a .env file in: {workspace_root}")
        print("   2. Add your Google API key: GOOGLE_API_KEY=your_actual_api_key_here")
        print("   3. Get an API key from: https://console.cloud.google.com/apis/credentials")
        sys.exit(1)
    else:
        # Mask the API key for security when displaying
        masked_key = google_api_key[:8] + "..." + google_api_key[-4:] if len(google_api_key) > 12 else "***"
        print(f"✅ Google API Key loaded: {masked_key}")

    # Prepare environment for the ADK process
    env = os.environ.copy()  # Copy current environment
    env['GOOGLE_API_KEY'] = google_api_key
    env['GOOGLE_GENAI_USE_VERTEXAI'] = google_genai_use_vertexai

    # Debug: Show environment variables being passed
    print(f"🔧 Environment variables for ADK:")
    print(f"   GOOGLE_API_KEY: {google_api_key[:8]}...{google_api_key[-4:] if len(google_api_key) > 12 else '***'}")
    print(f"   GOOGLE_GENAI_USE_VERTEXAI: {google_genai_use_vertexai}")

    # The `adk` command expects to be run from the parent of the agent module
    agent_module_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # The agent directory path (not module name)
    agent_dir = os.path.join(agent_module_parent_dir, 'ai')

    command = [
        "adk",
        "web",
        agent_dir,
    ]

    try:
        # Run the adk command with explicit environment
        print(f"Running agent from: {agent_module_parent_dir}")
        print(f"Using agent directory: {agent_dir}")
        subprocess.run(command, check=True, cwd=agent_module_parent_dir, env=env)
    except FileNotFoundError:
        print("Error: 'adk' command not found.")
        print("Please ensure the Google Agent Development Kit is installed ('pip install karrio-cli[dev]') and in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running agent: {e}")
        sys.exit(1)

if __name__ == '__main__':
    app()
