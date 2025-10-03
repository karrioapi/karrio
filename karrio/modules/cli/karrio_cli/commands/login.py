import os
import typer
import requests

app = typer.Typer()

DEFAULT_HOST = "http://localhost:5002"


def get_config():
    config_file = os.path.expanduser("~/.karrio/config")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return dict(line.strip().split("=") for line in f)
    return {}


def get_host_and_key():
    config = get_config()
    host = os.environ.get("KARRIO_HOST") or config.get("KARRIO_HOST") or DEFAULT_HOST
    api_key = os.environ.get("KARRIO_API_KEY") or config.get("KARRIO_API_KEY")
    return host, api_key


@app.command()
def login(
    host: str = typer.Option(
        DEFAULT_HOST,
        prompt="Enter the Karrio host URL",
        help="The URL of the Karrio instance",
    ),
    api_key: str = typer.Option(
        ...,
        prompt="Enter your Karrio API key",
        hide_input=True,
        help="Your Karrio API key",
    ),
):
    """
    Configure a connection to a Karrio instance.

    Example:
    ```terminal
    kcli login --host http://localhost:5002 --api-key your_api_key_here | jq '{message: "Login successful", host: .host}'
    ```
    """
    if not host:
        host = DEFAULT_HOST

    try:
        # Validate the connection
        headers = {"Authorization": f"Token {api_key}"}
        response = requests.get(f"{host}", headers=headers)
        response.raise_for_status()

        # Save the configuration
        config_dir = os.path.expanduser("~/.karrio")
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, "config")

        with open(config_file, "w") as f:
            f.write(f"KARRIO_HOST={host}\n")
            f.write(f"KARRIO_API_KEY={api_key}\n")

        typer.echo(f"Successfully logged in to Karrio instance at {host}")
        typer.echo(f"Configuration saved to {config_file}")

    except requests.RequestException as e:
        typer.echo(f"Error connecting to Karrio instance: {str(e)}", err=True)
    except IOError as e:
        typer.echo(f"Error saving configuration: {str(e)}", err=True)


@app.command()
def logout():
    """
    Remove the saved Karrio configuration.

    Example:
    ```terminal
    kcli logout | jq '{message: "Logout successful"}'
    ```
    """
    config_file = os.path.expanduser("~/.karrio/config")
    try:
        os.remove(config_file)
        typer.echo("Successfully logged out. Karrio configuration removed.")
    except FileNotFoundError:
        typer.echo("No saved Karrio configuration found.")
    except IOError as e:
        typer.echo(f"Error removing configuration: {str(e)}", err=True)


@app.command()
def status():
    """
    Check the current login status and connection to Karrio.

    Example:
    ```terminal
    kcli status | jq '{status: "Connected", host: .host, api_key: "********"}'
    ```
    """
    host, api_key = get_host_and_key()

    if api_key:
        try:
            headers = {"Authorization": f"Token {api_key}"}
            response = requests.get(f"{host}", headers=headers)
            response.raise_for_status()

            # Display connection status
            typer.echo(f"Connected to Karrio instance at {host}")

            # Display API metadata if available
            try:
                metadata = response.json()
                typer.echo("\nAPI Metadata:")
                for key, value in metadata.items():
                    typer.echo(f"  {key}: {value}")
            except ValueError:
                typer.echo("\nNo API metadata available")

            # Display API key source
            if os.environ.get("KARRIO_API_KEY"):
                typer.echo("\nUsing API key from environment variable")
            elif os.path.exists(os.path.expanduser("~/.karrio/config")):
                typer.echo("\nUsing API key from config file")

        except requests.RequestException as e:
            typer.echo(f"Error connecting to Karrio instance: {str(e)}", err=True)
    else:
        typer.echo(
            "Not logged in. Use 'karrio login' to configure the connection or set KARRIO_API_KEY environment variable."
        )


if __name__ == "__main__":
    app()
