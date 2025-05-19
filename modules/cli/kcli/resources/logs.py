import typer
import kcli.common.utils as utils
import typing
import datetime

app = typer.Typer()


@app.command("list")
def list_logs(
    entity_id: typing.Optional[str] = None,
    method: typing.Optional[str] = None,
    status_code: typing.Optional[str] = None,
    created_after: typing.Optional[datetime.datetime] = None,
    created_before: typing.Optional[datetime.datetime] = None,
    limit: int = typer.Option(20, help="Number of results to return per page"),
    offset: int = typer.Option(
        0, help="The initial index from which to return the results"
    ),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    List all logs with optional filters and pagination.

    Examples:
    # Get all logs and display as a table
    ./bin/cli logs list --limit 10 | jq -r '.logs.edges[].node | [.id, .method, .status_code, .path] | @tsv' | column -t -s $'\t'

    # Get logs for a specific entity
    ./bin/cli logs list --entity-id shp_123456789 --limit 5 | jq '.logs.edges[].node | {id, method, status_code, path}'
    """
    params = {
        "entity_id": entity_id,
        "method": method,
        "status_code": status_code,
        "created_after": created_after.isoformat() if created_after else None,
        "created_before": created_before.isoformat() if created_before else None,
        "first": limit,
        "offset": offset,
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    utils.make_graphql_request(
        "get_logs",
        {"filter": params},
        pretty_print=pretty,
        line_numbers=line_numbers
    )


@app.command("retrieve")
def retrieve_log(
    log_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Retrieve a log by ID.

    Example:
    ./bin/cli logs retrieve 123 | jq '{id, method, status_code, path, response_ms, requested_at}'
    """
    utils.make_graphql_request(
        "get_log",
        {"id": int(log_id)},
        pretty_print=pretty,
        line_numbers=line_numbers
    )
