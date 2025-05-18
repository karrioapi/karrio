import typer
import kcli.common.utils as utils
import typing

app = typer.Typer()

@app.command("list")
def list_carriers(
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    List all carriers.
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
    """
    utils.make_get_request(
        f"v1/carriers/{carrier_name}", pretty_print=pretty, line_numbers=line_numbers
    )
