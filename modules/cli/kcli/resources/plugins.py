import typer
import karrio.references as references
import typing

app = typer.Typer()

@app.command("list")
def list_plugins(
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    List all plugins with short description and active status.
    """
    plugins = references.collect_plugins_data()
    registry = references.Registry()
    results = []
    for plugin_id, plugin in plugins.items():
        enabled = registry.get(f"{plugin_id.upper()}_ENABLED", True)
        results.append({
            "id": plugin_id,
            "label": plugin.get("label", ""),
            "status": plugin.get("status", ""),
            "enabled": enabled,
            "description": plugin.get("description", ""),
        })
    if pretty:
        import json
        typer.echo(json.dumps(results, indent=2))
    else:
        try:
            from tabulate import tabulate
            table = [
                [i, plugin['id'], plugin['label'], plugin['status'], 'ENABLED' if plugin['enabled'] else 'DISABLED']
                for i, plugin in enumerate(results, 1)
            ]
            headers = ['#', 'ID', 'Label', 'Status', 'Enabled']
            typer.echo(tabulate(table, headers=headers, tablefmt='github'))
        except ImportError:
            for i, plugin in enumerate(results, 1):
                line = f"{i}. {plugin['id']} - {plugin['label']} ({'ENABLED' if plugin['enabled'] else 'DISABLED'}) - {plugin['status']}"
                if line_numbers:
                    typer.echo(f"{i}: {line}")
                else:
                    typer.echo(line)

@app.command("show")
def show_plugin(
    plugin_id: str,
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Pretty print the output"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers in pretty print"),
):
    """
    Show full details for a plugin by ID.
    """
    details = references.get_plugin_details(plugin_id)
    if not details:
        typer.echo(f"Plugin '{plugin_id}' not found.", err=True)
        raise typer.Exit(code=1)
    import json
    if pretty:
        typer.echo(json.dumps(details, indent=2))
    else:
        for i, (k, v) in enumerate(details.items(), 1):
            line = f"{k}: {v}"
            if line_numbers:
                typer.echo(f"{i}: {line}")
            else:
                typer.echo(line)

@app.command("enable")
def enable_plugin(
    plugin_id: str,
):
    """
    Enable a plugin by updating the Django Constance env var associated.
    """
    registry = references.Registry()
    key = f"{plugin_id.upper()}_ENABLED"
    try:
        registry[key] = True
        typer.echo(f"Plugin '{plugin_id}' enabled.")
    except Exception as e:
        typer.echo(f"Failed to enable plugin '{plugin_id}': {e}", err=True)
        raise typer.Exit(code=1)

@app.command("disable")
def disable_plugin(
    plugin_id: str,
):
    """
    Disable a plugin by updating the Django Constance env var associated.
    """
    registry = references.Registry()
    key = f"{plugin_id.upper()}_ENABLED"
    try:
        registry[key] = False
        typer.echo(f"Plugin '{plugin_id}' disabled.")
    except Exception as e:
        typer.echo(f"Failed to disable plugin '{plugin_id}': {e}", err=True)
        raise typer.Exit(code=1)
