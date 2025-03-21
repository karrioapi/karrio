import typer
import kcli.utils as utils
import typing
import datetime

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
    # Get all trackers and display as a table
    ./bin/cli trackers list --limit 10 | jq -r '.results[] | [.id, .tracking_number, .carrier_name, .status] | @tsv' | column -t -s $'\t'

    # Get in-transit trackers and extract specific fields
    ./bin/cli trackers list --status in_transit --limit 5 | jq '.results[] | {id, tracking: .tracking_number, carrier: .carrier_name, status}'
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
    ./bin/cli trackers retrieve trk_123456789 | jq '{id, tracking: .tracking_number, carrier: .carrier_name, status, last_event: .events[-1].description}'
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
    ./bin/cli trackers create --tracking-number 1Z999AA1234567890 --carrier-name ups \
        -d info[customer_name]="John Doe" -d info[order_id]=ORD12345 -d metadata[source]=website | jq '{id, tracking: .tracking_number, carrier: .carrier_name, status}'
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
    ./bin/cli trackers update trk_123456789 \
        -d info[note]="Package delayed" -d metadata[status]=delayed | jq '{id, tracking: .tracking_number, status, note: .info.note}'
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
    ./bin/cli trackers delete trk_123456789 | jq '{message: "Tracker deleted successfully"}'
    """
    utils.make_delete_request(
        f"v1/trackers/{tracker_id}", pretty_print=pretty, line_numbers=line_numbers
    )
