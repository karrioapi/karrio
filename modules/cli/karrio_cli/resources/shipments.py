import typer
import karrio_cli.common.utils as utils
import typing
import datetime

app = typer.Typer()


@app.command("list")
def list_shipments(
    address: typing.Optional[str] = None,
    carrier_name: typing.Optional[str] = None,
    created_after: typing.Optional[datetime.datetime] = None,
    created_before: typing.Optional[datetime.datetime] = None,
    has_manifest: typing.Optional[bool] = None,
    has_tracker: typing.Optional[bool] = None,
    id: typing.Optional[str] = None,
    keyword: typing.Optional[str] = None,
    meta_key: typing.Optional[str] = None,
    meta_value: typing.Optional[str] = None,
    metadata_key: typing.Optional[str] = None,
    metadata_value: typing.Optional[str] = None,
    option_key: typing.Optional[str] = None,
    option_value: typing.Optional[str] = None,
    reference: typing.Optional[str] = None,
    service: typing.Optional[str] = None,
    status: typing.Optional[str] = None,
    tracking_number: typing.Optional[str] = None,
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
    List all shipments with optional filters and pagination.

    Examples:
    ```terminal
    # Get all shipments and display as a table
    kcli shipments list --limit 10 | jq -r '.results[] | [.id, .status, .carrier_name, .tracking_number] | @tsv' | column -t -s $'\t'
    ```

    ```terminal
    # Get pending shipments and extract specific fields
    kcli shipments list --status pending --limit 5 | jq '.results[] | {id, status, carrier: .carrier_name, tracking: .tracking_number}'
    ```
    """
    params = {
        "address": address,
        "carrier_name": carrier_name,
        "created_after": created_after.isoformat() if created_after else None,
        "created_before": created_before.isoformat() if created_before else None,
        "has_manifest": has_manifest,
        "has_tracker": has_tracker,
        "id": id,
        "keyword": keyword,
        "meta_key": meta_key,
        "meta_value": meta_value,
        "metadata_key": metadata_key,
        "metadata_value": metadata_value,
        "option_key": option_key,
        "option_value": option_value,
        "reference": reference,
        "service": service,
        "status": status,
        "tracking_number": tracking_number,
        "limit": limit,
        "offset": offset,
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    utils.make_get_request(
        "v1/shipments", params=params, pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("retrieve")
def retrieve_shipment(
    shipment_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Retrieve a shipment by ID.

    Example:
    ```terminal
    kcli shipments retrieve shp_123456789 | jq '{id, status, carrier: .carrier_name, tracking: .tracking_number, created: .created_at}'
    ```
    """
    utils.make_get_request(
        f"v1/shipments/{shipment_id}", pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("buy-label")
def buy_label(
    shipment_id: str,
    selected_rate_id: str = typer.Option(..., help="The ID of the selected rate"),
    label_type: str = typer.Option("PDF", help="The type of label to generate"),
    property: typing.List[str] = typer.Option(
        [],
        "--property",
        "-d",
        help="Set nested properties (e.g. -d payment[paid_by]=sender)",
    ),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Purchase a label for a shipment.

    Example:
    ```terminal
    kcli shipments buy-label shp_123456789 \
        --selected-rate-id rate_987654321 \
        --label-type PDF \
        -d payment[paid_by]=sender \
        -d payment[currency]=USD \
        -d reference=order_12345 \
        -d metadata[customer_id]=cust_9876 | jq '{id, status, label: .label_url, tracking: .tracking_number}'
    ```
    """
    payload = {
        "selected_rate_id": selected_rate_id,
        "label_type": label_type,
    }

    try:
        nested_properties = utils.parse_nested_properties(property)
        payload.update(nested_properties)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    utils.make_post_request(
        f"v1/shipments/{shipment_id}/purchase",
        payload=payload,
        pretty_print=pretty,
        line_numbers=line_numbers,
    )


@app.command("cancel")
def cancel_shipment(
    shipment_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Cancel a shipment.

    Example:
    ```terminal
    kcli shipments cancel shp_123456789 | jq '{id, status, message: .cancellation.message}'
    ```
    """
    utils.make_post_request(
        f"v1/shipments/{shipment_id}/cancel",
        payload={},
        pretty_print=pretty,
        line_numbers=line_numbers,
    )


@app.command("fetch-rates")
def fetch_rates(
    shipment_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Fetch rates for a shipment.

    Example:

    ```terminal
    kcli shipments fetch-rates shp_123456789 | jq '.[] | {carrier: .carrier_name, service: .service, total_charge: .total_charge}'
    ```
    """
    utils.make_post_request(
        f"v1/shipments/{shipment_id}/rates",
        payload={},
        pretty_print=pretty,
        line_numbers=line_numbers,
    )
