import typer
import karrio_cli.common.utils as utils
import typing

app = typer.Typer()

@app.command("list")
def list_carriers(
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    List all carriers.

    Examples:
    ```terminal
    # Get all carriers and display as a table
    kcli carriers list | jq -r ".results[] | [.name, .display_name, .capabilities[]] | @tsv" | column -t -s $"\t"
    ```

    ```terminal
    # Get carriers and extract specific fields
    kcli carriers list | jq ".results[] | {name, display_name, capabilities}"
    ```

    Example Output:
    ```json
    {
      "count": 3,
      "next": null,
      "previous": null,
      "results": [
        {
          "name": "ups",
          "display_name": "UPS",
          "capabilities": ["rating", "shipping", "tracking"],
          "services": {
            "ups_standard": "11",
            "ups_express": "01",
            "ups_expedited": "02"
          },
          "requirements": ["api_key", "password", "account_number"]
        }
      ]
    }
    ```
    """
    utils.make_get_request(
        "v1/carriers", params=None, pretty_print=pretty, line_numbers=line_numbers
    )

@app.command("retrieve")
def retrieve_carrier(
    carrier_name: str,
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    Retrieve a carrier by name.

    Example:
    ```terminal
    kcli carriers retrieve ups | jq "{name, display_name, capabilities, services: .services | length}"
    ```

    Example Output:
    ```json
    {
      "name": "ups",
      "display_name": "UPS",
      "capabilities": ["rating", "shipping", "tracking"],
      "services": {
        "ups_standard": "11",
        "ups_express": "01",
        "ups_expedited": "02",
        "ups_express_plus": "14",
        "ups_worldwide_express": "07",
        "ups_worldwide_expedited": "08",
        "ups_standard_international": "65"
      },
      "requirements": ["api_key", "password", "account_number"],
      "metadata": {
        "test_mode_supported": true,
        "multi_piece_supported": true
      }
    }
    ```
    """
    utils.make_get_request(
        f"v1/carriers/{carrier_name}", pretty_print=pretty, line_numbers=line_numbers
    )
