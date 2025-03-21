import typer
import commands.sdk as sdk
import commands.docs as docs
import commands.login as login
import commands.codegen as codegen
import commands.carrier as carrier
import commands.plugin as plugin
import resources.shipments as shipments
import resources.orders as orders
import resources.trackers as trackers

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
