import typer
import karrio_cli.common.utils as utils
import typing
import datetime

app = typer.Typer()


@app.command("list")
def list_orders(
    created_after: typing.Optional[datetime.datetime] = None,
    created_before: typing.Optional[datetime.datetime] = None,
    status: typing.Optional[str] = None,
    reference: typing.Optional[str] = None,
    metadata_key: typing.Optional[str] = None,
    metadata_value: typing.Optional[str] = None,
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
    List all orders with optional filters and pagination.

    Examples:
    ```terminal
    # Get all orders and display as a table
    kcli orders list --limit 15 | jq -r ".results[] | [.id, .status, .created_at, .total_charge.amount] | @tsv" | column -t -s $"\t"
    ```

    ```terminal
    # Get pending orders and extract specific fields
    kcli orders list --status pending --limit 5 | jq ".results[] | {id, status, created: .created_at, total: .total_charge.amount}"
    ```

    Example Output:
    ```json
    {
      "count": 15,
      "next": "/v1/orders?limit=15&offset=15",
      "previous": null,
      "results": [
        {
          "id": "ord_123456789",
          "status": "pending",
          "created_at": "2024-03-20T10:30:00Z",
          "total_charge": {
            "amount": 25.50,
            "currency": "USD"
          },
          "line_items": [],
          "metadata": {}
        }
      ]
    }
    ```
    """
    params = {
        "created_after": created_after.isoformat() if created_after else None,
        "created_before": created_before.isoformat() if created_before else None,
        "status": status,
        "reference": reference,
        "metadata_key": metadata_key,
        "metadata_value": metadata_value,
        "limit": limit,
        "offset": offset,
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    utils.make_get_request(
        "v1/orders", params=params, pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("retrieve")
def retrieve_order(
    order_id: str,
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Retrieve an order by ID.

    Example:
    ```terminal
    kcli orders retrieve ord_987654321 | jq "{id, status, created: .created_at, total: .total_charge.amount, items: .line_items | length}"
    ```
    """
    utils.make_get_request(
        f"v1/orders/{order_id}", pretty_print=pretty, line_numbers=line_numbers
    )


@app.command("cancel")
def cancel_order(
    order_id: str,
    property: typing.List[str] = typer.Option(
        [],
        "--property",
        "-d",
        help="Set nested properties (e.g. -d reason=customer_request)",
    ),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print the output"
    ),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-n", help="Show line numbers in pretty print"
    ),
):
    """
    Cancel an order.

    Example:
    ```terminal
    kcli orders cancel ord_987654321 -d reason=customer_request | jq "{id, status, cancel_reason: .cancellation.reason}"
    ```
    """
    payload = {}

    try:
        nested_properties = utils.parse_nested_properties(property)
        payload.update(nested_properties)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

    utils.make_post_request(
        f"v1/orders/{order_id}/cancel",
        payload=payload,
        pretty_print=pretty,
        line_numbers=line_numbers,
    )
