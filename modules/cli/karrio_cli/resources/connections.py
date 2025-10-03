import typer
import karrio_cli.common.utils as utils
import typing

app = typer.Typer()

@app.command("list")
def list_connections(
    carrier_name: typing.Optional[str] = None,
    system_only: bool = typer.Option(False, "--system-only", help="Filter for system connections only"),
    limit: int = typer.Option(20, help="Number of results to return per page"),
    offset: int = typer.Option(0, help="The initial index from which to return the results"),
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    List all carrier connections with optional filters and pagination.

    Examples:
    ```terminal
    # Get all connections and display as a table
    kcli connections list | jq -r ".results[] | [.id, .carrier_name, .test_mode] | @tsv" | column -t -s $"\t"
    ```

    ```terminal
    # Get connections for a specific carrier
    kcli connections list --carrier-name ups | jq ".results[] | {id, carrier_name, test_mode}"
    ```

    Example Output:
    ```json
    {
      "count": 2,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": "conn_123456789",
          "carrier_name": "ups",
          "test_mode": true,
          "active": true,
          "capabilities": ["rating", "shipping", "tracking"],
          "metadata": {}
        }
      ]
    }
    ```
    """
    params = {
        "carrier_name": carrier_name,
        "system_only": system_only,
        "limit": limit,
        "offset": offset,
    }
    params = {k: v for k, v in params.items() if v is not None}
    utils.make_get_request(
        "v1/connections", params=params, pretty_print=pretty, line_numbers=line_numbers
    )

@app.command("retrieve")
def retrieve_connection(
    connection_id: str,
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    Retrieve a carrier connection by ID.

    Example:
    ```terminal
    kcli connections retrieve conn_123456789 | jq "{id, carrier_name, test_mode, active}"
    ```

    Example Output:
    ```json
    {
      "id": "conn_123456789",
      "carrier_name": "ups",
      "test_mode": true,
      "active": true,
      "capabilities": ["rating", "shipping", "tracking"],
      "credentials": {
        "api_key": "YOUR_API_KEY",
        "password": "YOUR_PASSWORD",
        "account_number": "YOUR_ACCOUNT"
      },
      "metadata": {}
    }
    ```
    """
    utils.make_get_request(
        f"v1/connections/{connection_id}", pretty_print=pretty, line_numbers=line_numbers
    )

@app.command("create")
def create_connection(
    property: typing.List[str] = typer.Option(
        [], "--property", "-d", help="Set nested properties (e.g. -d carrier_name=ups -d credentials[api_key]=xxx)"
    ),
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    Create a new carrier connection.

    Example:
    ```terminal
    kcli connections create \\
        -d carrier_name=ups \\
        -d test_mode=true \\
        -d credentials[api_key]=YOUR_API_KEY \\
        -d credentials[password]=YOUR_PASSWORD \\
        -d credentials[account_number]=YOUR_ACCOUNT | jq "{id, carrier_name, test_mode}"
    ```

    Example Output:
    ```json
    {
      "id": "conn_123456789",
      "carrier_name": "ups",
      "test_mode": true,
      "active": true,
      "capabilities": ["rating", "shipping", "tracking"],
      "credentials": {
        "api_key": "YOUR_API_KEY",
        "password": "YOUR_PASSWORD",
        "account_number": "YOUR_ACCOUNT"
      }
    }
    ```
    """
    try:
        payload = utils.parse_nested_properties(property)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)
    utils.make_post_request(
        "v1/connections", payload=payload, pretty_print=pretty, line_numbers=line_numbers
    )

@app.command("update")
def update_connection(
    connection_id: str,
    property: typing.List[str] = typer.Option(
        [], "--property", "-d", help="Set nested properties (e.g. -d credentials[api_key]=newvalue)"
    ),
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    Update a carrier connection by ID.

    Example:
    ```terminal
    kcli connections update conn_123456789 \\
        -d test_mode=false \\
        -d credentials[api_key]=NEW_API_KEY | jq "{id, carrier_name, test_mode}"
    ```

    Example Output:
    ```json
    {
      "id": "conn_123456789",
      "carrier_name": "ups",
      "test_mode": false,
      "active": true,
      "credentials": {
        "api_key": "NEW_API_KEY",
        "password": "YOUR_PASSWORD",
        "account_number": "YOUR_ACCOUNT"
      }
    }
    ```
    """
    try:
        payload = utils.parse_nested_properties(property)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)
    utils.make_patch_request(
        f"v1/connections/{connection_id}", payload=payload, pretty_print=pretty, line_numbers=line_numbers
    )

@app.command("delete")
def delete_connection(
    connection_id: str,
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    Delete a carrier connection by ID.

    Example:
    ```terminal
    kcli connections delete conn_123456789 | jq "{message: \"Connection deleted successfully\"}"
    ```

    Example Output:
    ```json
    {
      "message": "Connection deleted successfully"
    }
    ```
    """
    utils.make_delete_request(
        f"v1/connections/{connection_id}", pretty_print=pretty, line_numbers=line_numbers
    )
