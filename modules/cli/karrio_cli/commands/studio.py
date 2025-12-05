import os
import sys
import json
import time
import typer
import uvicorn
import logging
import pathlib
import subprocess
import shutil
import importlib.util
from typing import List, Optional, Tuple, Dict, Any
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import karrio_cli.commands.sdk as sdk_cmd

app = typer.Typer()
studio_api = FastAPI()

# Setup templates
MODULE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = MODULE_DIR / "studio_ui"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

ROOT_DIR = pathlib.Path(os.getenv("KARRIO_ROOT", os.getcwd())).resolve()
CACHE_TTL = 5
EXTENSION_CACHE: Dict[str, Any] = {"timestamp": 0, "data": []}
AI_TOOL_CACHE: Dict[str, Any] = {"timestamp": 0, "tools": []}


def detect_ai_tools(force: bool = False) -> List[Dict[str, Any]]:
    now = time.time()
    if not force and now - AI_TOOL_CACHE["timestamp"] < CACHE_TTL:
        return AI_TOOL_CACHE["tools"]

    tools = []
    cursor_path = shutil.which("cursor-agent")
    claude_path = shutil.which("claude")

    if cursor_path:
        tools.append(
            {
                "id": "cursor-agent",
                "label": "cursor-agent",
                "preferred": True,
                "path": cursor_path,
            }
        )
    if claude_path:
        tools.append(
            {
                "id": "claude",
                "label": "claude",
                "preferred": not bool(cursor_path),
                "path": claude_path,
            }
        )

    AI_TOOL_CACHE["timestamp"] = now
    AI_TOOL_CACHE["tools"] = tools
    return tools


SCRIPT_COMMAND_DEFS = {
    "install_editable": {
        "label": "pip install -e",
        "description": "Install the carrier extension in editable mode.",
        "build": lambda ext: ["pip", "install", "-e", ext["path"]],
    },
    "show_plugin": {
        "label": "Show plugin metadata",
        "description": "Inspect plugin registration via ./bin/cli plugins show.",
        "build": lambda ext: ["./bin/cli", "plugins", "show", ext["id"]],
    },
    "generate_cli": {
        "label": "Run generate script",
        "description": "Re-run ./bin/run-generate-on for this extension.",
        "build": lambda ext: ["./bin/run-generate-on", ext["path"]],
    },
    "run_tests": {
        "label": "Carrier unittest suite",
        "description": "Execute python -m unittest discover -v -f on the carrier tests.",
        "build": lambda ext: [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-v",
            "-f",
            str((ROOT_DIR / ext["path"] / "tests").resolve()),
        ],
    },
}

SCRIPT_COMMANDS_METADATA = [
    {"id": key, "label": value["label"], "description": value["description"]}
    for key, value in SCRIPT_COMMAND_DEFS.items()
]

AI_PROMPT_DEFS = {
    "progress_review": {
        "label": "Review integration progress",
        "description": "Summarize remaining steps based on success criteria.",
        "tags": ["overview", "progress"],
        "template": (
            "Carrier: {name} ({carrier_id})\\n"
            "Path: {path}\\n"
            "Features: {features}\\n"
            "Progress summary:\\n{progress_report}\\n"
            "Using the Karrio Carrier Integration Guide, outline remaining steps "
            "and highlight risks."
        ),
    },
    "tests_debug": {
        "label": "Diagnose carrier tests",
        "description": "Generate a plan for fixing failing unittests.",
        "tags": ["tests", "debug"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Progress summary:\\n{progress_report}\\n"
            "Task: Help me debug carrier tests. Suggest assertions to inspect, "
            "common schema mistakes, and how to align with test templates."
        ),
    },
    "mapping_helper": {
        "label": "Mapping assistant",
        "description": "Guide the provider mapping for rate/shipping APIs.",
        "tags": ["mapping", "schemas"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Progress summary:\\n{progress_report}\\n"
            "Provide step-by-step instructions to map Karrio models to the "
            "carrier schema, referencing generated dataclasses and units."
        ),
    },
    "schema_troubleshoot": {
        "label": "Schema generation troubleshooting",
        "description": "Diagnose ./bin/run-generate-on failures.",
        "tags": ["schemas", "generate"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Describe the schema generation error output or paste logs here.\\n"
            "Task: Inspect the generate script, schema samples, and CLI flags from the "
            "guide and recommend fixes (file edits, camel/snake flags, sample tweaks). "
            "Provide the exact commands to rerun generation afterwards."
        ),
    },
    "snippet_builder": {
        "label": "Request/response snippet builder",
        "description": "Produce provider skeletons for mapping.",
        "tags": ["mapping", "snippets"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Features: {features}\\n"
            "Task: Produce Python snippets showing request builders, proxy calls, "
            "and parse functions using the generated schema modules. Include attr-based "
            "dataclass instantiation, lib.to_object usage, and comments for optional fields."
        ),
    },
    "test_template": {
        "label": "Test template refresher",
        "description": "Regenerate feature unittest files per guide.",
        "tags": ["tests", "templates"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nFeature: <rating/shipping/tracking/etc.>\\n"
            "Path: {path}\\n"
            "Provide the full unittest structure for this feature following the mandatory "
            "4-method pattern (create request, action, parse success, parse error). "
            "Include required print statements, assertListEqual, ANY placeholders, and "
            "payload/response constants."
        ),
    },
    "cli_batch": {
        "label": "CLI command batch runner",
        "description": "Execute repo commands sequentially and report output.",
        "tags": ["cli", "automation"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Run the following commands in order and capture output:\\n"
            "1. ./bin/run-generate-on {path}\\n"
            "2. pip install -e {path}\\n"
            "3. python -m unittest discover -v -f {path}/tests\\n"
            "4. ./bin/cli plugins show {carrier_id}\\n"
            "Highlight failures and list follow-up steps."
        ),
    },
    "metadata_audit": {
        "label": "Metadata / registration audit",
        "description": "Fix cases where plugin isn't listed.",
        "tags": ["metadata", "cli"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Symptoms: describe plugin registration issue.\\n"
            "Task: Inspect karrio/plugins/{carrier_id}/__init__.py, ensure METADATA is "
            "correct, Mapper imports are valid, pip install -e is run, and ./bin/cli "
            "plugins show {carrier_id} works. Provide fixes and verification commands."
        ),
    },
    "deployment_checklist": {
        "label": "Deployment checklist",
        "description": "Final success-criteria audit before release.",
        "tags": ["release", "checklist"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nPath: {path}\\n"
            "Progress summary:\\n{progress_report}\\n"
            "Task: Verify every success criterion (schemas, providers, units, proxy, "
            "metadata, installation, tests, CLI registration, docs). Produce a final QA "
            "checklist and release notes items."
        ),
    },
    "api_troubleshoot": {
        "label": "API troubleshooting",
        "description": "Diagnose carrier API/auth errors.",
        "tags": ["api", "debug"],
        "template": (
            "Carrier: {name} ({carrier_id})\\nEndpoint: <URL>\\n"
            "Request payload snippet: <json>\\nResponse/error: <json/text>\\n"
            "Task: Compare with official docs, inspect proxy headers/auth, suggest "
            "instrumentation (trace modes, logging, retries), and provide patch guidance "
            "for proxy/auth logic."
        ),
    },
    "kickoff_new_integration": {
        "label": "Kick off new integration",
        "description": "Scaffold a brand new carrier connector using the guide.",
        "tags": ["scaffolding", "guide"],
        "template": (
            "Strictly follow the Karrio Carrier Integration Guide at "
            "https://github.com/karrioapi/karrio/raw/refs/heads/main/CARRIER_INTEGRATION_GUIDE.md.\n"
            "Carrier context:\n"
            "- Carrier: {name} ({carrier_id})\n"
            "- Location: {path}\n"
            "- Features: {features}\n"
            "Task:\n"
            "1. Verify environment setup (./bin/activate-env) and CLI usage.\n"
            "2. Ensure schema samples exist or describe how to derive them.\n"
            "3. Build provider logic, units, utils, proxy, metadata, and tests.\n"
            "4. Make sure every success criterion in the guide is satisfied, "
            "including schema generation, plugin registration, installation, and tests.\n"
            "5. Provide a step-by-step plan plus commands to run.\n"
            "Current progress summary:\n{progress_report}"
        ),
    },
    "fix_failing_tests": {
        "label": "Fix failing tests",
        "description": "Diagnose red tests and propose fixes.",
        "tags": ["tests", "debug"],
        "template": (
            "Carrier: {name} ({carrier_id})\nPath: {path}\n"
            "Features: {features}\n"
            "Progress summary:\n{progress_report}\n"
            "Goal: Identify reasons why unittest suites might fail and provide actionable "
            "steps (code snippets, schema adjustments, request mappings) to fix them. "
            "Reference test templates from the guide, ensure print statements precede "
            "assertions, and highlight required assertions."
        ),
    },
    "dpd_group_new": {
        "label": "DPD Group integration prompt",
        "description": "Full instruction set for DPD Group connector.",
        "tags": ["dpd", "scaffolding"],
        "template": (
            "Strictly follow https://github.com/karrioapi/karrio/raw/refs/heads/main/CARRIER_INTEGRATION_GUIDE.md "
            "to build a new dpd_group integration under modules/connectors/dpd_group.\n"
            "Resources:\n"
            "- Docs: https://nst-preprod.dpsin.dpdgroup.com/api/docs/\n"
            "- PREPROD base URL: https://nst-preprod.dpsin.dpdgroup.com/api/v1.1/\n"
            "- PROD base URL: https://shipping.dpdgroup.com/api/v1.1/\n"
            "Success criteria: all required schema files, provider logic, units, proxy, "
            "metadata, and tests must match the guide. Ensure SDK/CLI commands are listed.\n"
            "Current carrier context:\n"
            "- Carrier placeholder: {name} ({carrier_id})\n"
            "- Expected path: modules/connectors/dpd_group\n"
            "- Progress summary:\n{progress_report}\n"
            "Deliverables: actionable checklist + exact CLI commands."
        ),
    },
    "gls_group_new": {
        "label": "GLS Group integration prompt",
        "description": "Full instruction set for GLS Group connector.",
        "tags": ["gls", "scaffolding"],
        "template": (
            "Strictly follow https://github.com/karrioapi/karrio/raw/refs/heads/main/CARRIER_INTEGRATION_GUIDE.md "
            "to build a new gls_group integration under modules/connectors/gls_group.\n"
            "Resources:\n"
            "- Auth docs: https://dev-portal.gls-group.net/docs/authentification-service-v2/1/routes/token/post\n"
            "- Ship docs: https://dev-portal.gls-group.net/docs/shipit-farm/1/routes/rs/shipments/post\n"
            "- Production token: https://api.gls-group.net/oauth2/v2/token\n"
            "- Sandbox token: https://api-sandbox.gls-group.net/oauth2/v2/token\n"
            "Ensure all success criteria (schemas, provider logic, metadata, installation, tests) "
            "are satisfied.\n"
            "Carrier context placeholder: {name} ({carrier_id}) at {path}\n"
            "Progress summary:\n{progress_report}\n"
            "Provide a full implementation plan plus commands."
        ),
    },
    "rate_payload_builder": {
        "label": "Karrio rate payload builder",
        "description": "Produce a sample RateRequest JSON payload for testing.",
        "tags": ["payload", "testing"],
        "template": (
            "Carrier context: {name} ({carrier_id}) at {path}\n"
            "Reference RateRequest in modules/sdk/karrio/core/models.py and payloads such as "
            "modules/connectors/landmark/tests/landmark/test_rate.py.\n"
            "Task: Generate a complete JSON payload for karrio.Rates.create(...) including "
            "shipper, recipient, parcels, services, and options. Return only the JSON body "
            "plus notes about dynamic fields."
        ),
    },
    "carrier_sample_data": {
        "label": "Carrier schema sample builder",
        "description": "Generate request/response samples from carrier schemas.",
        "tags": ["schemas", "samples"],
        "template": (
            "Carrier: {name} ({carrier_id}) at {path}\n"
            "Task: Inspect generated schemas in karrio/schemas/{carrier_id} and produce JSON "
            "samples for key operations (e.g., rate_request, rate_response) similar to "
            "modules/connectors/landmark/tests/landmark/test_rate.py. Label each sample with "
            "its schema."
        ),
    },
}

AI_PROMPTS_METADATA = [
    {
        "id": key,
        "label": value["label"],
        "description": value["description"],
        "tags": ", ".join(value["tags"]),
    }
    for key, value in AI_PROMPT_DEFS.items()
]


def _scan_extensions() -> List[Dict[str, Any]]:
    connectors_dir = ROOT_DIR / "modules" / "connectors"
    plugins_dir = ROOT_DIR / "community" / "plugins"

    extensions: List[Dict[str, Any]] = []

    for base_dir in [connectors_dir, plugins_dir]:
        if not base_dir.exists():
            continue

        for item in base_dir.iterdir():
            if not item.is_dir() or not (item / "pyproject.toml").exists():
                continue

            name = item.name
            relative_path = item.relative_to(ROOT_DIR)
            tests_dir = item / "tests" / name
            features = []
            if tests_dir.exists():
                if (tests_dir / "test_rate.py").exists():
                    features.append("rating")
                if (tests_dir / "test_shipment.py").exists():
                    features.append("shipping")
                if (tests_dir / "test_tracking.py").exists():
                    features.append("tracking")
                if (tests_dir / "test_manifest.py").exists():
                    features.append("manifest")
                if (tests_dir / "test_pickup.py").exists():
                    features.append("pickup")
                if (tests_dir / "test_address.py").exists():
                    features.append("address")

            extensions.append(
                {
                    "id": name,
                    "name": name.replace("_", " ").title(),
                    "path": str(relative_path),
                    "absolute_path": str(item),
                    "features": features or ["rating", "shipping", "tracking"],
                    "type": "connector" if "connectors" in str(base_dir) else "plugin",
                }
            )

    extensions.sort(key=lambda ext: ext["name"].lower())
    return extensions


def get_extensions(force_refresh: bool = False) -> List[Dict[str, Any]]:
    now = time.time()
    if not force_refresh and now - EXTENSION_CACHE["timestamp"] < CACHE_TTL:
        return EXTENSION_CACHE["data"]

    data = _scan_extensions()
    EXTENSION_CACHE["timestamp"] = now
    EXTENSION_CACHE["data"] = data
    return data

@studio_api.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@studio_api.get("/partials/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    extensions = get_extensions()
    connectors_count = sum(1 for e in extensions if e['type'] == 'connector')
    plugins_count = len(extensions) - connectors_count
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "extensions": extensions,
        "connectors_count": connectors_count,
        "plugins_count": plugins_count
    })

@studio_api.get("/api/extensions")
async def list_extensions_sidebar(request: Request):
    extensions = get_extensions()
    return templates.TemplateResponse(
        "sidebar_extensions.html",
        {"request": request, "extensions": extensions},
    )

@studio_api.get("/partials/new-extension", response_class=HTMLResponse)
async def new_extension_form(request: Request):
    return templates.TemplateResponse("new_extension.html", {"request": request})

@studio_api.post("/api/extensions", response_class=HTMLResponse)
async def create_extension(
    request: Request,
    display_name: str = Form(...),
    carrier_slug: str = Form(...),
    type: str = Form(...),
    features: List[str] = Form(...),
    is_xml_api: bool = Form(False)
):
    try:
        root_dir = pathlib.Path(os.getcwd())
        path = "modules/connectors" if type == "connector" else "community/plugins"
        version = "2025.5" # Default version
        
        # Call the SDK command logic
        sdk_cmd._add_extension(
            id=carrier_slug.lower(),
            name=display_name,
            feature=",".join(features),
            version=version,
            is_xml_api=is_xml_api,
            path=path
        )

        get_extensions(force_refresh=True)
        
        # Return a success toast and redirect to dashboard
        response = await dashboard(request)
        response.headers["HX-Trigger"] = json.dumps(
            {
                "notify": {"message": "Extension created successfully!", "type": "success"},
                "refreshExtensions": True,
            }
        )
        return response
        
    except Exception as e:
        logging.error(f"Failed to create extension: {e}")
        # Return error toast (using HX-Trigger with error)
        return HTMLResponse(
            status_code=200,  # HTMX handles 200 best for swapping
            content=f"<div class='p-4 bg-red-50 text-red-600 rounded'>Error: {str(e)}</div>",
            headers={
                "HX-Trigger": json.dumps(
                    {"notify": {"message": "Failed to create extension", "type": "error"}}
                )
            },
        )


def _format_progress_report(items: List[Dict[str, Any]]) -> str:
    return "\n".join(
        f"{'✅' if item['status'] else '⚠️'} {item['label']}: {item['detail']}"
        for item in items
    )


def _evaluate_extension(ext: Dict[str, Any]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []

    def add(label: str, detail: str, status: bool):
        items.append({"label": label, "detail": detail, "status": status})

    root = ROOT_DIR / ext["path"]
    carrier_id = ext["id"]

    generate_script = root / "generate"
    add("Generate script", "generate file present", generate_script.exists())

    schemas_dir = root / "schemas"
    schema_files = (
        [f for f in schemas_dir.glob("*") if f.is_file()] if schemas_dir.exists() else []
    )
    add("Schema samples", f"{len(schema_files)} files in schemas/", len(schema_files) >= 2)

    generated_dir = root / "karrio" / "schemas" / carrier_id
    generated_files = (
        [f for f in generated_dir.glob("*.py")] if generated_dir.exists() else []
    )
    add("Generated dataclasses", f"{len(generated_files)} python files", len(generated_files) > 0)

    providers_dir = root / "karrio" / "providers" / carrier_id
    provider_files = (
        [f for f in providers_dir.glob("*.py")] if providers_dir.exists() else []
    )
    add("Provider logic", f"{len(provider_files)} modules", len(provider_files) > 0)

    tests_dir = root / "tests" / carrier_id
    test_files = (
        [f for f in tests_dir.glob("test_*.py")] if tests_dir.exists() else []
    )
    add("Carrier tests", f"{len(test_files)} test files", len(test_files) > 0)

    plugin_file = root / "karrio" / "plugins" / carrier_id / "__init__.py"
    metadata_ok = False
    if plugin_file.exists():
        try:
            spec = importlib.util.spec_from_file_location(
                f"studio_plugin_{carrier_id}", plugin_file
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)  # type: ignore
                metadata_ok = hasattr(module, "METADATA")
        except Exception:
            metadata_ok = False
    add("Plugin metadata import", f"karrio.plugins.{carrier_id}", metadata_ok)

    passed = sum(1 for item in items if item["status"])
    total = len(items)
    score = int(round((passed / total) * 100)) if total else 0

    return {
        "items": items,
        "score": score,
        "passed": passed,
        "total": total,
        "report": _format_progress_report(items),
    }

def get_extension_details(id: str) -> Optional[Tuple[Dict[str, Any], List[str]]]:
    lookup = id.strip().lower()
    extensions = get_extensions()
    ext = next((e for e in extensions if e["id"].lower() == lookup), None)
    if ext is None:
        extensions = get_extensions(force_refresh=True)
        ext = next((e for e in extensions if e["id"].lower() == lookup), None)
    if not ext:
        return None

    ext_path = ROOT_DIR / ext["path"]
    schema_dir = ext_path / "schemas"
    schemas: List[str] = []
    if schema_dir.exists():
        schemas = sorted(
            f.name for f in schema_dir.iterdir() if f.is_file() and f.suffix in [".json", ".xsd"]
        )

    return ext, schemas

@studio_api.get("/partials/extension/{id}", response_class=HTMLResponse)
async def extension_detail(request: Request, id: str):
    data = get_extension_details(id)
    if not data:
        return HTMLResponse("Extension not found", status_code=404)
        
    ext, schemas = data
    progress = _evaluate_extension(ext)
    prompt_cards = [
        {
            **meta,
            "body": _build_ai_prompt(meta["id"], ext, progress) or "",
        }
        for meta in AI_PROMPTS_METADATA
    ]

    return templates.TemplateResponse(
        "extension.html",
        {
            "request": request,
            "extension": ext,
            "schemas": schemas,
            "progress": progress,
            "progress_items": progress["items"],
            "scripts": SCRIPT_COMMANDS_METADATA,
            "ai_prompts": prompt_cards,
            "ai_tools": detect_ai_tools(),
        },
    )


def run_cli_command(command: List[str]) -> Dict[str, Any]:
    """Execute repository CLI commands and capture output."""
    process = subprocess.run(
        command,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    return {
        "command": " ".join(command),
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
        "success": process.returncode == 0,
    }


def render_action_response(request: Request, title: str, result: Dict[str, Any]):
    status = "success" if result["success"] else "error"
    message = f"{title} {'completed' if result['success'] else 'failed'}"
    headers = {"HX-Trigger": json.dumps({"notify": {"message": message, "type": status}})}
    stdout = (result.get("stdout") or "").strip()
    stderr = (result.get("stderr") or "").strip()
    primary_output = stdout or stderr
    stderr_detail = stderr if (not result["success"] and stderr) else ""

    return templates.TemplateResponse(
        "action_result.html",
        {
            "request": request,
            "title": title,
            "result": result,
            "primary_output": primary_output,
            "has_output": bool(primary_output),
            "stderr_detail": stderr_detail,
        },
        headers=headers,
    )


def _build_script_command(script_id: str, ext: Dict[str, Any]) -> Optional[List[str]]:
    definition = SCRIPT_COMMAND_DEFS.get(script_id)
    if not definition:
        return None
    return definition["build"](ext)


def _build_ai_prompt(prompt_id: str, ext: Dict[str, Any], progress: Dict[str, Any]) -> Optional[str]:
    definition = AI_PROMPT_DEFS.get(prompt_id)
    if not definition:
        return None
    context = {
        "name": ext["name"],
        "carrier_id": ext["id"],
        "path": ext["path"],
        "features": ", ".join(ext["features"]),
        "progress_report": progress["report"],
    }
    return definition["template"].format(**context)


def _run_ai_prompt(prompt: str) -> Dict[str, Any]:
    tools = detect_ai_tools()
    tool = next((t for t in tools if t["preferred"]), tools[0] if tools else None)

    if tool and tool["id"] == "cursor-agent":
        return run_cli_command([tool["path"], "agent", "--print", prompt])
    if tool and tool["id"] == "claude":
        return run_cli_command([tool["path"], "-p", prompt])

    return {
        "command": "ai-prompt",
        "stdout": prompt,
        "stderr": "No AI CLI detected (cursor-agent or claude). Copy this prompt manually.",
        "success": False,
    }


@studio_api.post("/api/extensions/{id}/generate", response_class=HTMLResponse)
async def regenerate_schemas(request: Request, id: str):
    data = get_extension_details(id)
    if not data:
        raise HTTPException(status_code=404, detail="Extension not found")

    ext, _ = data
    command = ["./bin/run-generate-on", ext["path"]]
    result = run_cli_command(command)
    return render_action_response(request, "Schema generation", result)


@studio_api.post("/api/extensions/{id}/tests", response_class=HTMLResponse)
async def run_tests(request: Request, id: str):
    data = get_extension_details(id)
    if not data:
        raise HTTPException(status_code=404, detail="Extension not found")

    ext, _ = data
    tests_path = pathlib.Path(ext["path"]) / "tests"
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-v",
        "-f",
        str(tests_path),
    ]
    result = run_cli_command(command)
    return render_action_response(request, "Test suite", result)


@studio_api.post("/api/scripts", response_class=HTMLResponse)
async def run_script(
    request: Request,
    extension_id: str = Form(...),
    script_id: str = Form(...),
):
    data = get_extension_details(extension_id)
    if not data:
        raise HTTPException(status_code=404, detail="Extension not found")

    ext, _ = data
    command = _build_script_command(script_id, ext)
    if not command:
        raise HTTPException(status_code=404, detail="Unknown script")

    result = run_cli_command(command)
    label = SCRIPT_COMMAND_DEFS[script_id]["label"]
    return render_action_response(request, f"Script · {label}", result)


@studio_api.post("/api/ai/execute", response_class=HTMLResponse)
async def run_ai(
    request: Request,
    extension_id: str = Form(...),
    prompt_id: str = Form(...),
):
    data = get_extension_details(extension_id)
    if not data:
        raise HTTPException(status_code=404, detail="Extension not found")

    ext, _ = data
    tools = detect_ai_tools()
    progress = _evaluate_extension(ext)
    prompt = _build_ai_prompt(prompt_id, ext, progress)
    if not prompt:
        raise HTTPException(status_code=404, detail="Unknown prompt")

    result = _run_ai_prompt(prompt)
    title = f"AI prompt · {AI_PROMPT_DEFS[prompt_id]['label']} ({tools[0]['label'] if tools else 'manual'})"
    return render_action_response(request, title, result)


@app.command()
def start(
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(4002, help="Port to bind to"),
):
    """Launch the Karrio Studio server."""
    typer.echo(f"Starting Karrio Studio at http://{host}:{port}")
    uvicorn.run(studio_api, host=host, port=port)

if __name__ == "__main__":
    app()
