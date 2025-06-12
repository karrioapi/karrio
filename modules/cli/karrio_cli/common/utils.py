import json
import enum
import pydoc
import typer
import requests
import importlib
import karrio_cli.commands.login as login
from rich.syntax import Syntax
from rich.console import Console
from .queries import GET_LOGS, GET_LOG, GET_EVENTS, GET_EVENT

DEFAULT_FEATURES = [
    "tracking",
    "rating",
    "shipping",
]

console = Console()

# GraphQL Queries
GET_EVENTS = """
query get_events($filter: EventFilter) {
    events(filter: $filter) {
        page_info {
            count
            has_next_page
            has_previous_page
            start_cursor
            end_cursor
        }
        edges {
            node {
                id
                type
                data
                test_mode
                pending_webhooks
                created_at
            }
        }
    }
}
"""

GET_EVENT = """
query get_event($id: String!) {
    event(id: $id) {
        id
        type
        data
        test_mode
        pending_webhooks
        created_at
    }
}
"""

def parse_json_or_xml_string(value: str):
    """Parse a string that might be JSON or XML."""
    if not value or not isinstance(value, str):
        return value

    # Try to parse as JSON first
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        # If not JSON, return as is (could be XML or other format)
        return value


def parse_records(records):
    """Parse record data and response fields."""
    if not records:
        return records

    return [
        {
            **record,
            "record": {
                **record["record"],
                "data": parse_json_or_xml_string(record["record"].get("data")),
                "response": parse_json_or_xml_string(record["record"].get("response")),
            } if record.get("record") else record["record"]
        }
        for record in records
    ]


def parse_log_response(data):
    """Parse log response data, including nested records."""
    if not data:
        return data

    # Handle logs list response
    if "logs" in data:
        edges = data["logs"].get("edges", [])
        for edge in edges:
            node = edge.get("node", {})
            if node:
                node["response"] = parse_json_or_xml_string(node.get("response"))
                node["data"] = parse_json_or_xml_string(node.get("data"))
                node["records"] = parse_records(node.get("records", []))
        return data

    # Handle single log response
    if "log" in data:
        log = data["log"]
        if log:
            log["response"] = parse_json_or_xml_string(log.get("response"))
            log["data"] = parse_json_or_xml_string(log.get("data"))
            log["records"] = parse_records(log.get("records", []))
        return data

    return data


def format_json_output(data, pretty_print=False, line_numbers=False):
    json_str = json.dumps(data, default=str, indent=2)
    if pretty_print:
        syntax = Syntax(json_str, "json", theme="ansi_light", line_numbers=line_numbers)
        console.print(syntax)
    else:
        typer.echo(json_str)


def get_api_url_and_headers():
    host, api_key = login.get_host_and_key()
    headers = {"Authorization": f"Token {api_key}"} if api_key else {}
    return host, headers


def make_request(
    method,
    endpoint: str,
    payload: dict = None,
    params: dict = None,
    pretty_print: bool = False,
    line_numbers: bool = False,
):
    api_url, headers = get_api_url_and_headers()
    url = f"{api_url}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=headers)
        elif method == "PATCH":
            response = requests.patch(url, json=payload, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()

        if response.status_code == 204:  # No Content
            return None

        data = response.json()
        format_json_output(data, pretty_print, line_numbers)
        return data
    except requests.RequestException as e:
        error_message = {"error": str(e)}
        format_json_output(error_message, pretty_print, line_numbers)
        return None


def make_get_request(
    endpoint: str,
    params: dict = None,
    pretty_print: bool = False,
    line_numbers: bool = False,
):
    return make_request(
        "GET",
        endpoint,
        params=params,
        pretty_print=pretty_print,
        line_numbers=line_numbers,
    )


def make_post_request(
    endpoint: str, payload: dict, pretty_print: bool = False, line_numbers: bool = False
):
    return make_request(
        "POST",
        endpoint,
        payload=payload,
        pretty_print=pretty_print,
        line_numbers=line_numbers,
    )


def make_patch_request(
    endpoint: str, payload: dict, pretty_print: bool = False, line_numbers: bool = False
):
    return make_request(
        "PATCH",
        endpoint,
        payload=payload,
        pretty_print=pretty_print,
        line_numbers=line_numbers,
    )


def make_delete_request(
    endpoint: str, pretty_print: bool = False, line_numbers: bool = False
):
    return make_request(
        "DELETE", endpoint, pretty_print=pretty_print, line_numbers=line_numbers
    )


def parse_event_response(data):
    """Parse the GraphQL response for events."""
    if "events" in data:
        return {"events": data["events"]}
    elif "event" in data:
        return {"event": data["event"]}
    return data


def make_graphql_request(
    query_name: str,
    variables: dict = None,
    pretty_print: bool = False,
    line_numbers: bool = False,
):
    """
    Make a GraphQL request to the API.

    Args:
        query_name: Name of the query to execute (e.g., 'get_logs', 'get_log', 'get_events', 'get_event')
        variables: Variables to pass to the query
        pretty_print: Whether to pretty print the output
        line_numbers: Whether to show line numbers in pretty print
    """
    api_url, headers = get_api_url_and_headers()
    url = f"{api_url}/graphql"

    # Get the query based on the query name
    query = {
        "get_logs": GET_LOGS,
        "get_log": GET_LOG,
        "get_events": GET_EVENTS,
        "get_event": GET_EVENT,
    }.get(query_name)

    if not query:
        raise ValueError(f"Unknown query: {query_name}")

    payload = {
        "query": query,
        "variables": variables or {}
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Check for GraphQL errors
        if "errors" in data:
            error_message = {"error": data["errors"]}
            format_json_output(error_message, pretty_print, line_numbers)
            return None

        # Extract and parse the data from the response
        if query_name.startswith("get_event"):
            result = parse_event_response(data.get("data", {}))
        else:
            result = parse_log_response(data.get("data", {}))

        format_json_output(result, pretty_print, line_numbers)
        return result

    except requests.RequestException as e:
        error_message = {"error": str(e)}
        format_json_output(error_message, pretty_print, line_numbers)
        return None


def gen(entity):
    return pydoc.render_doc(entity, renderer=pydoc.plaintext)


def format_dimension(code, dim):
    return (
        f"| `{ code }` "
        f'| { f" x ".join([str(d) for d in dim.values() if isinstance(d, float)]) } '
        f'| { f" x ".join([k for k in dim.keys() if isinstance(dim[k], float)]) }'
    )


def instantiate_tree(cls, indent=0, alias=""):
    tree = f"{alias}{cls.__name__}(\n"
    indent += 1
    items = cls.__annotations__.items() if hasattr(cls, "__annotations__") else []

    for name, typ in items:
        if typ.__name__ == "Optional" and hasattr(typ, "__args__"):
            typ = typ.__args__[0]
        if typ.__name__ == "List" and hasattr(typ, "__args__"):
            typ = typ.__args__[0]
            if hasattr(typ, "__annotations__"):
                tree += (
                    " " * indent * 4
                    + f"{name}=[\n"
                    + " " * (indent + 1) * 4
                    + f"{instantiate_tree(typ, indent + 1, alias=alias)}\n"
                    + " " * indent * 4
                    + "],\n"
                )
            else:
                tree += " " * indent * 4 + f"{name}=[],\n"
        elif hasattr(typ, "__annotations__"):
            tree += (
                " " * indent * 4
                + f"{name}={instantiate_tree(typ, indent, alias=alias)},\n"
            )
        else:
            tree += " " * indent * 4 + f"{name}=None,\n"

    tree += " " * (indent - 1) * 4 + ")"
    return tree


def instantiate_class_from_module(
    module_name: str,
    class_name: str,
    module_alias: str = "",
):
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    alias = f"{module_alias}." if module_alias != "" else ""

    return instantiate_tree(cls, alias=alias)


def parse_nested_properties(properties: list[str]) -> dict:
    """
    Parse a list of nested properties into a dictionary.

    Example input: ["payment[paid_by]=sender", "metadata[key1]=value1"]
    """
    result = {}

    def set_nested(d, path, value):
        keys = path.split("[")
        for i, key in enumerate(keys):
            key = key.rstrip("]")
            if i == len(keys) - 1:
                d[key] = value
            else:
                d = d.setdefault(key, {})

    for prop in properties:
        if "=" not in prop:
            raise ValueError(
                f"Invalid property format: {prop}. Use 'key=value' or 'nested[key]=value'."
            )
        path, value = prop.split("=", 1)
        set_nested(result, path, value)

    return result
