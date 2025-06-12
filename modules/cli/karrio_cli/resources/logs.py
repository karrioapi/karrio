import typer
import karrio_cli.common.utils as utils
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
    ```terminal
    # Get all logs and display as a table
    kcli logs list --limit 10 | jq -r ".logs.edges[].node | [.id, .method, .status_code, .path] | @tsv" | column -t -s $"\t"
    ```

    ```terminal
    # Get logs for a specific entity
    kcli logs list --entity-id shp_123456789 --limit 5 | jq ".logs.edges[].node | {id, method, status_code, path}"
    ```

    Example Output:
    ```json
    {
      "logs": {
        "edges": [
          {
            "node": {
              "id": "123",
              "method": "POST",
              "status_code": 200,
              "path": "/v1/shipments",
              "request": {
                "headers": {},
                "body": {}
              },
              "response": {
                "headers": {},
                "body": {}
              },
              "response_ms": 245,
              "requested_at": "2024-03-20T10:30:00Z"
            }
          }
        ],
        "pageInfo": {
          "hasNextPage": true,
          "hasPreviousPage": false,
          "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
          "endCursor": "YXJyYXljb25uZWN0aW9uOjk="
        }
      }
    }
    ```
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
    ```terminal
    kcli logs retrieve 123 | jq "{id, method, status_code, path, response_ms, requested_at}"
    ```

    Example Output:
    ```json
    {
      "log": {
        "id": "123",
        "method": "POST",
        "status_code": 200,
        "path": "/v1/shipments",
        "request": {
          "headers": {
            "Content-Type": "application/json",
            "Authorization": "Token <redacted>"
          },
          "body": {
            "shipment_id": "shp_123456789"
          }
        },
        "response": {
          "headers": {
            "Content-Type": "application/json"
          },
          "body": {
            "id": "shp_123456789",
            "status": "created"
          }
        },
        "response_ms": 245,
        "requested_at": "2024-03-20T10:30:00Z"
      }
    }
    ```
    """
    utils.make_graphql_request(
        "get_log",
        {"id": int(log_id)},
        pretty_print=pretty,
        line_numbers=line_numbers
    )
