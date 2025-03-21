import typer
from . import commands
from .commands import sdk, docs, login, codegen, carrier, plugin
from .resources import shipments, orders, trackers

app = typer.Typer()

# Add login commands directly to the main app
app.command()(login.login)
app.command()(login.logout)
app.command()(login.status)

# Add resource-specific commands as sub-typers
app.add_typer(
    shipments.app,
    name="shipments",
    help="Manage shipments.",
)

app.add_typer(
    orders.app,
    name="orders",
    help="Manage orders.",
)

app.add_typer(
    trackers.app,
    name="trackers",
    help="Manage trackers.",
)

app.add_typer(
    docs.docs,
    name="docs",
    help="Generate documentation based on carriers metadata.",
)

app.add_typer(
    sdk.app,
    name="sdk",
    help="SDK-related commands.",
)

app.add_typer(
    codegen.app,
    name="codegen",
    help="Code generation utilities.",
)

# Add our new carrier and plugin commands
app.add_typer(
    carrier.app,
    name="carrier",
    help="Carrier integration management commands.",
)

app.add_typer(
    plugin.app,
    name="plugin",
    help="Plugin management commands.",
)

if __name__ == "__main__":
    app()
