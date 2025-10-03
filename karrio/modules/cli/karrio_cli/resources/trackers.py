import typer
import typing
import datetime
import karrio_cli.common.utils as utils

app = typer.Typer()


@app.command("list")
def list_trackers(
    carrier_name: typing.Optional[str] = None,
    tracking_number: typing.Optional[str] = None,
    status: typing.Optional[str] = None,
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
    List all trackers with optional filters and pagination.

    Examples:
    ```terminal
    # Get all trackers and display as a table
    kcli trackers list --limit 10 | jq -r ".results[] | [.id, .tracking_number, .carrier_name, .status] | @tsv" | column -t -s $"\t"
    ```

    ```terminal
    # Get in-transit trackers and extract specific fields
    kcli trackers list --status in_transit --limit 5 | jq ".results[] | {id, tracking: .tracking_number, carrier: .carrier_name, status}"
    ```

    Example Output:
    ```json
    {
      "count": 10,
      "next": "/v1/trackers?limit=10&offset=10",
      "previous": null,
      "results": [
        {
          "id": "trk_123456789",
          "tracking_number": "1Z999AA1234567890",
          "carrier_name": "ups",
          "status": "in_transit",
          "created_at": "2024-03-20T10:30:00Z",
          "events": [
            {
              "date": "2024-03-20T10:30:00Z",
              "description": "Package picked up",
              "location": "San Francisco, CA",
              "code": "PU"
            }
          ],
          "metadata": {}
        }
      ]
    }
    ```
    """
    params = {
        "carrier_name": carrier_name,
        "tracking_number": tracking_number,
        "status": status,
        "created_after": created_after.isoformat() if created_after else None,
        "created_before": created_before.isoformat() if created_before else None,
        "limit": limit,
        "offset": offset,
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    utils.make_get_request(
        "v1/trackers", params=params, pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("retrieve")
def retrieve_tracker(
    tracker_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Retrieve a tracker by ID.

    Example:
    ```terminal
    kcli trackers retrieve trk_123456789 | jq "{id, tracking: .tracking_number, carrier: .carrier_name, status, last_event: .events[-1].description}"
    ```

    Example Output:
    ```json
    {
      "id": "trk_123456789",
      "tracking_number": "1Z999AA1234567890",
      "carrier_name": "ups",
      "status": "delivered",
      "created_at": "2024-03-19T15:45:00Z",
      "events": [
        {
          "date": "2024-03-20T14:30:00Z",
          "description": "Package delivered",
          "location": "New York, NY",
          "code": "DL"
        }
      ],
      "metadata": {
        "order_id": "ORD12345"
      }
    }
    ```
    """
    utils.make_get_request(
        f"v1/trackers/{tracker_id}", pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("create")
def create_tracker(
    tracking_number: str = typer.Option(..., help="The tracking number"),
    carrier_name: str = typer.Option(..., help="The carrier name"),
    account_number: typing.Optional[str] = typer.Option(
        None, help="The account number"
    ),
    reference: typing.Optional[str] = typer.Option(
        None, help="A reference for the tracker"
    ),
    property: typing.List[str] = typer.Option(
        [],
        "--property",
        "-d",
        help="Set nested properties (e.g. -d info[customer_name]=John Doe)",
    ),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Create a new tracker.

    Example:
    ```terminal
    kcli trackers create --tracking-number 1Z999AA1234567890 --carrier-name ups \\
        -d info[customer_name]="John Doe" \\
        -d info[order_id]=ORD12345 \\
        -d metadata[source]=website | jq "{id, tracking: .tracking_number, carrier: .carrier_name, status}"
    ```

    Example Output:
    ```json
    {
      "id": "trk_123456789",
      "tracking_number": "1Z999AA1234567890",
      "carrier_name": "ups",
      "status": "unknown",
      "created_at": "2024-03-20T10:30:00Z",
      "info": {
        "customer_name": "John Doe",
        "order_id": "ORD12345"
      },
      "metadata": {
        "source": "website"
      }
    }
    ```
    """
    payload = {
        "tracking_number": tracking_number,
        "carrier_name": carrier_name,
        "account_number": account_number,
        "reference": reference,
    }

    try:
        nested_properties = utils.parse_nested_properties(property)
        payload.update(nested_properties)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    utils.make_post_request(
        "v1/trackers", payload=payload, pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("update")
def update_tracker(
    tracker_id: str,
    property: typing.List[str] = typer.Option(
        [],
        "--property",
        "-d",
        help="Set nested properties (e.g. -d info[customer_name]=John Doe)",
    ),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Update an existing tracker.

    Example:
    ```terminal
    kcli trackers update trk_123456789 \\
        -d info[note]="Package delayed" \\
        -d metadata[status]=delayed | jq "{id, tracking: .tracking_number, status, note: .info.note}"
    ```

    Example Output:
    ```json
    {
      "id": "trk_123456789",
      "tracking_number": "1Z999AA1234567890",
      "status": "in_transit",
      "info": {
        "note": "Package delayed"
      },
      "metadata": {
        "status": "delayed"
      }
    }
    ```
    """
    payload = {}

    try:
        nested_properties = utils.parse_nested_properties(property)
        payload.update(nested_properties)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    utils.make_patch_request(
        f"v1/trackers/{tracker_id}",
        payload=payload,
        pretty_print=pretty,
        line_numbers=line_numbers,
    )


@app.command("delete")
def delete_tracker(
    tracker_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Delete a tracker.

    Example:
    ```terminal
    kcli trackers delete trk_123456789 | jq "{message: \"Tracker deleted successfully\"}"
    ```

    Example Output:
    ```json
    {
      "message": "Tracker deleted successfully"
    }
    ```
    """
    utils.make_delete_request(
        f"v1/trackers/{tracker_id}", pretty_print=pretty, line_numbers=line_numbers
    )
