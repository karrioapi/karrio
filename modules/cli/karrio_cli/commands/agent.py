import os
import sys
import typer
import subprocess
from dotenv import load_dotenv

app = typer.Typer()

@app.command()
def web():
    """
    Launches the Karrio AI agent web UI.
    This function loads environment variables, and then uses the `adk` command-line
    tool to start the agent's web UI.
    """
    # Load environment variables from .env file in the parent directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
    else:
        # Create a dummy .env if it doesn't exist
        with open(dotenv_path, 'w') as f:
            f.write('GOOGLE_API_KEY=YOUR_API_KEY_HERE\n')
            f.write('GOOGLE_GENAI_USE_VERTEXAI=FALSE\n')
        print(f"Created a sample .env file at {dotenv_path}. Please update it with your Google API Key.")


    # The `adk` command expects to be run from the parent of the agent module
    agent_module_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # The agent module is 'karrio_cli.ai'
    # ADK needs a python-importable path.
    agent_module = 'karrio_cli.ai'

    command = [
        "adk",
        "web",
        agent_module,
    ]

    try:
        # Run the adk command
        print(f"Running agent from: {agent_module_parent_dir}")
        print(f"Using agent module: {agent_module}")
        subprocess.run(command, check=True, cwd=agent_module_parent_dir)
    except FileNotFoundError:
        print("Error: 'adk' command not found.")
        print("Please ensure the Google Agent Development Kit is installed ('pip install karrio-cli[dev]') and in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running agent: {e}")
        sys.exit(1)

if __name__ == '__main__':
    app()
