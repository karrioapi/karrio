import typer
import kcli.commands.sdk as sdk
import kcli.commands.docs as docs
import kcli.commands.login as login
import kcli.commands.codegen as codegen
import kcli.resources.shipments as shipments
import kcli.resources.orders as orders
import kcli.resources.trackers as trackers

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

if __name__ == "__main__":
    app()
