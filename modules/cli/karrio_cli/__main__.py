import typer
import karrio_cli.commands.sdk as sdk
import karrio_cli.resources.logs as logs
import karrio_cli.commands.login as login
import karrio_cli.resources.orders as orders
import karrio_cli.resources.events as events
import karrio_cli.commands.codegen as codegen
import karrio_cli.resources.trackers as trackers
import karrio_cli.resources.carriers as carriers
import karrio_cli.resources.shipments as shipments
import karrio_cli.resources.connections as connections

try:
    import google.adk
    import karrio_cli.ai.commands as agent
    has_ai_dep = True
except ImportError:
    has_ai_dep = False

try:
    import karrio
    import karrio_cli.commands.plugins as plugins
    has_sdk_dep = True
except ImportError:
    has_sdk_dep = False

app = typer.Typer()

# Add login commands directly to the main app
app.command()(login.login)
app.command()(login.logout)
app.command()(login.status)

# Add resource-specific commands as sub-typers
app.add_typer(
    carriers.app,
    name="carriers",
    help="Manage carriers.",
)

app.add_typer(
    connections.app,
    name="connections",
    help="Manage carrier connections.",
)

app.add_typer(
    shipments.app,
    name="shipments",
    help="Manage shipments.",
)

app.add_typer(
    trackers.app,
    name="trackers",
    help="Manage trackers.",
)

app.add_typer(
    orders.app,
    name="orders",
    help="Manage orders.",
)

app.add_typer(
    logs.app,
    name="logs",
    help="View API request logs.",
)

app.add_typer(
    events.app,
    name="events",
    help="View system events.",
)

if has_sdk_dep:
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

if has_sdk_dep:
    app.add_typer(
        plugins.app,
        name="plugins",
        help="Manage plugins.",
    )

if has_ai_dep:
    app.add_typer(
        agent.app,
        name="agent",
        help="Karrio AI agent.",
    )

if __name__ == "__main__":
    app()
