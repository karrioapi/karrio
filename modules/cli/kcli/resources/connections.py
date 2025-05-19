import typer
import kcli.common.utils as utils
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
    """
    utils.make_delete_request(
        f"v1/connections/{connection_id}", pretty_print=pretty, line_numbers=line_numbers
    )
