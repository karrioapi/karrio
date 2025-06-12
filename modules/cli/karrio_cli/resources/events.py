import typer
import karrio_cli.common.utils as utils
import typing
import datetime

app = typer.Typer()


@app.command("list")
def list_events(
    type: typing.Optional[str] = typer.Option(
        None,
        help="Event type (e.g. shipment_created, order_created, tracker_created)",
        autocompletion=lambda: [
            "all",
            "batch_completed",
            "batch_failed",
            "batch_queued",
            "batch_running",
            "order_cancelled",
            "order_created",
            "order_delivered",
            "order_fulfilled",
            "order_updated",
            "shipment_cancelled",
            "shipment_delivery_failed",
            "shipment_fulfilled",
            "shipment_needs_attention",
            "shipment_out_for_delivery",
            "shipment_purchased",
            "tracker_created",
            "tracker_updated",
        ]
    ),
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
    List all events with optional filters and pagination.

    Examples:
    ```terminal
    # Get all events and display as a table
    kcli events list --limit 10 | jq -r ".events.edges[].node | [.id, .type, .created_at] | @tsv" | column -t -s $"\t"
    ```

    ```terminal
    # Get events of a specific type
    kcli events list --type shipment_purchased --limit 5 | jq ".events.edges[].node | {id, type, created_at, data}"
    ```

    Example Output:
    ```json
    {
      "events": {
        "edges": [
          {
            "node": {
              "id": "evt_123456789",
              "type": "shipment_purchased",
              "data": {
                "shipment_id": "shp_123456789",
                "status": "purchased"
              },
              "test_mode": false,
              "pending_webhooks": 0,
              "created_at": "2024-03-20T10:30:00Z"
            }
          }
        ],
        "page_info": {
          "count": 1,
          "has_next_page": false,
          "has_previous_page": false,
          "start_cursor": "YXJyYXljb25uZWN0aW9uOjA=",
          "end_cursor": "YXJyYXljb25uZWN0aW9uOjA="
        }
      }
    }
    ```
    """
    params = {
        "type": [type] if type else None,
        "created_after": created_after.isoformat() if created_after else None,
        "created_before": created_before.isoformat() if created_before else None,
        "first": limit,
        "offset": offset,
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    utils.make_graphql_request(
        "get_events",
        {"filter": params},
        pretty_print=pretty,
        line_numbers=line_numbers
    )


@app.command("retrieve")
def retrieve_event(
    event_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Retrieve an event by ID.

    Example:
    ```terminal
    kcli events retrieve evt_123456789 | jq "{id, type, created_at, data}"
    ```

    Example Output:
    ```json
    {
      "event": {
        "id": "evt_123456789",
        "type": "shipment_purchased",
        "data": {
          "shipment_id": "shp_123456789",
          "status": "purchased"
        },
        "test_mode": false,
        "pending_webhooks": 0,
        "created_at": "2024-03-20T10:30:00Z"
      }
    }
    ```
    """
    utils.make_graphql_request(
        "get_event",
        {"id": event_id},
        pretty_print=pretty,
        line_numbers=line_numbers
    )
