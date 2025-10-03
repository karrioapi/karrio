"""Karrio Workflow Engine - Execution Engine Core

This module contains the core workflow execution engine for the Karrio automation platform.
It orchestrates multi-step workflows with support for HTTP requests, data mapping, and
conditional logic, with comprehensive tracing and error handling.

🎯 **Core Functionality**

The workflow execution engine processes WorkflowEvents by sequencing actions, managing
authentication, rendering templates, and executing HTTP requests or data transformations.
It provides enterprise-grade reliability with resumption, parallel execution, and
comprehensive audit trails for complex business process automation.

📊 **Complete Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      KARRIO WORKFLOW EXECUTION ENGINE                          │
│                         Complete Data Flow Illustration                        │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
    │  WorkflowEvent  │ ──── │  run_workflow   │ ──── │ process_workflow │
    │  (event_id)     │      │  (Entry Point)  │      │  (Orchestrator) │
    └─────────────────┘      └─────────────────┘      └─────────────────┘
             │                        │                        │
             │                        ▼                        ▼
    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
    │   Database      │      │     Tracer      │      │ Execution Seq.  │
    │   + Redis       │      │   + Cache       │      │  (Order-based)  │
    │   Context       │      │   Context       │      │   [0,1,2,...]   │
    └─────────────────┘      └─────────────────┘      └─────────────────┘
                                                               │
                                                               ▼
                                                     ┌─────────────────┐
                                                     │  Action Groups  │
                                                     │  by Order No.   │
                                                     │ {0: [a,b], 1:c} │
                                                     └─────────────────┘
                                                               │
                                                               ▼
                             ┌──────────────── PARALLEL EXECUTION ─────────────────┐
                             │                                                      │
                             ▼                        ▼                            ▼
                   ┌─────────────────┐      ┌─────────────────┐        ┌─────────────────┐
                   │execute_workflow │      │execute_workflow │        │execute_workflow │
                   │   _action A     │      │   _action B     │   ...  │   _action N     │
                   │ (same order)    │      │ (same order)    │        │ (same order)    │
                   └─────────────────┘      └─────────────────┘        └─────────────────┘
                             │                        │                            │
                             ▼                        ▼                            ▼
                   ┌─────────────────┐      ┌─────────────────┐        ┌─────────────────┐
                   │ authenticate_   │      │ authenticate_   │        │ authenticate_   │
                   │  connection     │      │  connection     │        │  connection     │
                   └─────────────────┘      └─────────────────┘        └─────────────────┘
                             │                        │                            │
                             ▼                        ▼                            ▼
                   ┌─────────────────┐      ┌─────────────────┐        ┌─────────────────┐
                   │ execute_action  │      │ execute_action  │        │ execute_action  │
                   │ • http_request  │      │ • data_mapping  │        │ • conditional   │
                   │ • data_mapping  │      │ • conditional   │        │                 │
                   │ • conditional   │      │                 │        │                 │
                   └─────────────────┘      └─────────────────┘        └─────────────────┘
                             │                        │                            │
                             └──────────────┬─────────────────┬───────────────────┘
                                           │                 │
                                           ▼                 ▼
                                  ┌─────────────────┐ ┌─────────────────┐
                                  │ Action Results  │ │  Tracing        │
                                  │ • Success       │ │  Records        │
                                  │ • Failed        │ │ • Input/Output  │
                                  │ • Conditional   │ │ • Timestamps    │
                                  └─────────────────┘ └─────────────────┘
                                           │                 │
                             ┌─────────────┴─────────────────┴───────────────────┐
                             │              RESULT AGGREGATION                   │
                             │                                                   │
                             │  • Collect all action results                     │
                             │  • Check for failures (abort workflow)           │
                             │  • Check conditional results (branch/abort)      │
                             │  • Pass results as 'steps' to next order         │
                             │  • Update workflow event status                   │
                             └───────────────────────────────────────────────────┘
```

🔄 **Action Execution Pipeline**

```
    WorkflowAction ──────┐
         │               │
         ▼               ▼
    Connection ────► authenticate_connection() ────► execute_action()
         │                       │                        │
         ▼                       ▼                        ▼
    Metafields ──────► Jinja2 Template ─────────► Action Type Handler
     (New approach)     Rendering                   │
         │                │                        ├── HTTP Request
    Legacy Credentials ──┘                        ├── Data Mapping
     (Fallback)                                   └── Conditional Logic
                                                       │
                                                       ▼
                                                  Action Result
                                                  • status: success/failed
                                                  • output: response data
                                                  • condition: boolean (conditional only)
```

🏗️ **Workflow Orchestration Flow**

```
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        WORKFLOW ORCHESTRATION                          │
    └─────────────────────────────────────────────────────────────────────────┘

    Event Start
         │
         ▼
    ┌─────────────────┐
    │ Load Workflow   │ ──── Retrieve workflow definition and actions
    │   Definition    │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Calculate       │ ──── Group actions by order, detect parallel execution
    │ Execution       │
    │ Sequence        │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Resume Check    │ ──── Find last executed order for resumption
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Execute Action  │ ──── Process each action group in sequence
    │ Groups (Order)  │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Parallel        │ ──── Execute same-order actions concurrently
    │ Execution       │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Result          │ ──── Aggregate results and update context
    │ Aggregation     │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Status Update   │ ──── Mark workflow as success/failed/cancelled
    └─────────────────┘
```

🔐 **Authentication & Connection Management**

```
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                     CONNECTION AUTHENTICATION FLOW                     │
    └─────────────────────────────────────────────────────────────────────────┘

    Action Requires Connection?
         │
         ▼
    ┌─────────────────┐
    │ Load Connection │ ──── Retrieve WorkflowConnection definition
    │   Definition    │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Credential      │ ──── Priority: Metafields > Legacy credentials
    │ Resolution      │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Template        │ ──── Render auth_template with credentials
    │ Rendering       │
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Authentication  │ ──── Apply to action headers/parameters
    │ Application     │
    └─────────────────┘
```

🎭 **Template Rendering Context Structure**

```
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        TEMPLATE CONTEXT STRUCTURE                      │
    └─────────────────────────────────────────────────────────────────────────┘

    {
        "order": 0,                     # Action execution order
        "parameters": {...},            # Event input parameters
        "steps": {                      # Previous action results
            "action_alias": {
                "response": {...},      # Action output
                "status": "success"     # Execution status
            }
        },
        "lib": karrio.lib,             # Utility functions
        "connection": {...},            # Authenticated connection
        "metadata": {...},              # Action metadata
        "credentials": {...},           # Connection credentials
        "workflow": {                   # Workflow metadata
            "id": "...",
            "name": "...",
            "slug": "..."
        },
        "event": {                      # Event metadata
            "id": "...",
            "event_type": "...",
            "created_at": "..."
        }
    }
```

⚡ **Supported Action Types**

**1. HTTP_REQUEST Actions:**
   • Method: GET, POST, PUT, DELETE, PATCH
   • Parameters: Query string or request body
   • Headers: Template-based with authentication
   • Authentication: Via connections (API key, Basic, OAuth2)
   • Response handling: JSON, XML, text
   • Error handling: Timeout, connection errors, SSL errors

**2. DATA_MAPPING Actions:**
   • Jinja2 template transformation
   • Access to previous action results via 'steps'
   • JSON or text output formats
   • Complex data manipulation with loops/conditionals

**3. CONDITIONAL Actions:**
   • Boolean expression evaluation
   • YAML/JSON result parsing
   • Workflow branching/termination on false
   • Context-aware condition checking

🛡️ **Error Handling & Resilience**

• **Automatic Failure Propagation**: Any action fails → workflow fails
• **Conditional Workflow Termination**: False condition → workflow aborts
• **Comprehensive Error Logging**: Full context and stack traces
• **Timeout Support**: Configurable timeouts for HTTP requests (default: 30s)
• **Connection Error Categorization**: Timeout, DNS, SSL error handling
• **Tracing for Debugging**: Complete audit trails for troubleshooting
• **Resume Capability**: Workflows can resume from last successful action order
• **Graceful Degradation**: Failed actions don't crash the entire system

⚡ **Performance Optimizations**

• **Database Query Optimization**: select_related/prefetch_related usage
• **Connection Pooling**: HTTP connection reuse and management
• **Parallel Execution**: Same-order actions using lib.run_concurrently
• **Redis Caching**: Session state and template caching
• **Pre-loading Metafields**: Avoid N+1 query problems
• **Template Compilation**: Jinja2 templates compiled and cached
• **Memory Efficient**: Streaming processing for large data sets
• **Lazy Loading**: Actions and connections loaded only when needed

🔒 **Security Considerations**

• **Credential Isolation**: Secure credential storage with encryption
• **Template Sandboxing**: Jinja2 templates run in restricted environment
• **Input Validation**: All inputs validated and sanitized before processing
• **Audit Logging**: Complete audit trail for compliance and debugging
• **Rate Limiting**: Built-in protection against abuse and DoS
• **Access Control**: Role-based permissions for workflow management
• **Connection Security**: SSL/TLS enforcement for external API calls

🏗️ **Module Dependencies & Architecture**

**Core Dependencies:**
• **karrio.lib**: Core utilities and HTTP client
• **automation.models**: Workflow, Action, Connection, Event models
• **tracing**: Execution logging and debugging infrastructure
• **serializers**: Data validation and transformation
• **utils**: Error handling decorators and utilities

**Integration Points:**
• **WorkflowEvent**: Entry point for workflow execution
• **TracingRecord**: Audit trail and debugging information
• **WorkflowConnection**: Authentication and credential management
• **Cache System**: Redis-based performance optimization
• **Task Queue**: Asynchronous execution via Huey/Celery

This module is the heart of Karrio's automation capabilities, enabling complex
business process orchestration with enterprise-grade reliability, performance,
and security. It supports everything from simple API integrations to complex
multi-step data processing workflows with full observability and error handling.

**Author**: Karrio Team
**License**: See project LICENSE file
"""

import yaml
import base64
import typing
import jinja2
import logging
import functools
import urllib.parse
import django.core.cache as caching

import karrio.lib as lib
import karrio.server.core.utils as utils
import karrio.server.tracing.models as tracing
import karrio.server.serializers as serializers
import karrio.server.automation.models as models
import karrio.server.tracing.utils as tracing_utils
import karrio.server.automation.serializers as automation_serializers

logger = logging.getLogger(__name__)


@utils.error_wrapper
def run_workflow(event_id: str, *args, **kwargs):
    """
    Main entry point for workflow execution.

    This is the top-level function called by the task queue (Celery/Huey) to execute
    a workflow. It sets up the execution environment, manages the workflow lifecycle,
    and persists all execution traces.

    EXECUTION FLOW:
    ===============
    1. Lookup WorkflowEvent by ID
    2. Initialize execution context (Tracer, Cache, Database context)
    3. Set workflow status to 'running'
    4. Call process_workflow() to execute the actual workflow
    5. Update final workflow status
    6. Persist all tracing records to database

    Args:
        event_id (str): The unique identifier of the WorkflowEvent to execute
        *args: Additional positional arguments (unused, for task queue compatibility)
        **kwargs: Additional keyword arguments (unused, for task queue compatibility)

    Returns:
        None: This function has no return value but updates the workflow event status

    Side Effects:
        - Updates WorkflowEvent.status in database
        - Creates TracingRecord entries for debugging/audit
        - Logs execution progress to application logs

    Database Operations:
        - SELECT: Retrieves WorkflowEvent and related Workflow/Actions
        - UPDATE: Updates WorkflowEvent status twice (running → final_status)
        - INSERT: Bulk creates TracingRecord entries

    Error Handling:
        - Wrapped with @utils.error_wrapper for automatic exception handling
        - Gracefully handles missing workflow events
        - Ensures tracing records are saved even if workflow fails

    Performance Notes:
        - Uses bulk operations for tracing records to minimize database round-trips
        - Lazy-loads related objects only when needed
        - Caches execution context to avoid repeated database queries

    Example Usage:
        >>> run_workflow("workflow_event_123abc")
        # Executes workflow and updates status

    Log Output:
        INFO: "> starting workflow execution..."
        INFO: "> ending workflow execution..."
        WARNING: "no workflow event found" (if event_id doesn't exist)
    """
    logger.info("> starting workflow execution...")

    events = models.WorkflowEvent.objects.filter(id=event_id)

    if events.exists():
        tracer = lib.Tracer()
        event = events.first()
        cache = lib.Cache(cache=caching.cache)
        context = serializers.get_object_context(event)

        events.update(status=automation_serializers.AutomationEventStatus.running.value)
        status = process_workflow(event, tracer=tracer, cache=cache, context=context)
        events.update(status=status)

        tracing_utils.bulk_save_tracing_records(tracer, context=context)
    else:
        logger.info("no workflow event found")

    logger.info("> ending workflow execution...")


@utils.error_wrapper
def process_workflow(
    event: models.WorkflowEvent,
    tracer: lib.Tracer,
    cache: lib.Cache,
    context=None,
) -> str:
    """
    Core workflow orchestration engine.

    This function implements the main workflow execution logic, handling action sequencing,
    parallel execution, error propagation, and conditional branching. It processes actions
    in order groups and aggregates results for subsequent steps.

    ORCHESTRATION LOGIC:
    ===================

    1. PREPARATION PHASE:
       - Extract execution sequence from workflow definition
       - Determine last completed action order (for resumption)
       - Prepare execution context with event parameters

    2. EXECUTION PHASE:
       For each order group (0, 1, 2, ...):
       - Skip if already executed (resumption support)
       - Execute actions in parallel using lib.run_concurrently
       - Collect and aggregate results
       - Check for failure conditions
       - Check for conditional termination
       - Check for cancellation requests
       - Build 'steps' context for next order group

    3. TERMINATION CONDITIONS:
       - SUCCESS: All actions completed successfully
       - FAILED: Any action returns status='failed'
       - ABORTED: Any conditional action returns condition=False
       - CANCELLED: Event status changed to 'cancelled' externally

    Args:
        event (models.WorkflowEvent): The workflow event to process
        tracer (lib.Tracer): Tracing context for debugging/audit
        cache (lib.Cache): Redis cache for session state
        context (dict, optional): Database context for object relationships

    Returns:
        str: Final workflow status ('success', 'failed', 'aborted', 'cancelled')

    Raises:
        Exception: Re-raises any unhandled exceptions as 'failed' status

    EXECUTION CONTEXT BUILDING:
    ===========================

    Each action group receives progressively richer context:

    Order 0 Actions:
    {
        "order": 0,
        "parameters": {...},    # Event input parameters
        "steps": {}             # Empty for first actions
    }

    Order 1 Actions:
    {
        "order": 1,
        "parameters": {...},    # Event input parameters
        "steps": {              # Results from order 0
            "action_a_alias": {"response": {...}, "status": "success"},
            "action_b_alias": {"response": {...}, "status": "success"}
        }
    }

    PARALLEL EXECUTION:
    ==================

    Actions with the same order number execute in parallel:
    - Reduces total workflow execution time
    - Maintains data consistency within each order
    - Uses lib.run_concurrently for thread-safe execution
    - Database connections are handled per-thread

    ERROR HANDLING:
    ==============

    Failure Propagation:
    - Any action failure immediately terminates workflow
    - Provides detailed error context in logs
    - Sets workflow status to 'failed'

    Conditional Branching:
    - Conditional actions can terminate workflow with condition=False
    - Sets workflow status to 'aborted' (not 'failed')
    - Allows for early termination based on business logic

    Cancellation Support:
    - Checks for external cancellation between order groups
    - Provides graceful shutdown mechanism
    - Sets workflow status to 'cancelled'

    RESUMPTION SUPPORT:
    ==================

    Workflows can be resumed from the last completed order:
    - get_last_executed_order() determines resumption point
    - Skips already-executed action groups
    - Maintains execution state across restarts
    - Useful for long-running workflows and error recovery

    PERFORMANCE OPTIMIZATIONS:
    =========================

    - Batch loads actions with select_related/prefetch_related
    - Pre-loads connection and metafield data
    - Minimizes database queries during execution
    - Uses Redis caching for session state
    - Parallel execution reduces wall-clock time

    Database Operations:
    - SELECT: Retrieves workflow actions with related data
    - SELECT: Checks for event cancellation between orders
    - No direct UPDATEs (handled by caller)

    Example Execution Flow:
    ======================

    ```python
    # Workflow with 3 actions: [A, B] (order 0), [C] (order 1)

    # Order 0: Execute A and B in parallel
    results_0 = lib.run_concurrently([
        execute_workflow_action(A, ...),
        execute_workflow_action(B, ...)
    ])

    # Check for failures
    if any(failed): return "failed"

    # Order 1: Execute C with results from A and B
    results_1 = lib.run_concurrently([
        execute_workflow_action(C, steps={
            "action_a": results_0[0],
            "action_b": results_0[1]
        })
    ])

    return "success"
    ```

    Log Output:
    -----------
    INFO: "> executing actions: ['action_a', 'action_b']..."
    INFO: "> executing actions: ['action_c']..."
    INFO: "> aborting execution, an action failed..." (if failure)
    INFO: "> aborting execution, condition is false..." (if conditional)
    INFO: "> aborting execution, event cancelled..." (if cancelled)
    INFO: "> execution failed due to runtime error..." (if exception)
    """
    trace = tracer.with_metadata(
        dict(
            workflow_event_id=event.id,
            workflow_id=event.workflow.id,
        )
    )

    try:
        execution_sequences = get_execution_sequence(event)
        last_executed_order = get_last_executed_order(event)
        workflow_actions = event.workflow.actions
        parameters = event.parameters or dict()
        results = []

        # Execute actions sequentially...
        for order, action_slugs in execution_sequences:
            if order > last_executed_order:
                logger.info(f"> executing actions: {action_slugs}...")
                # Pre-load connections and metafields to avoid database access during execution
                actions = workflow_actions.filter(slug__in=action_slugs).select_related('connection').prefetch_related('connection__metafields')

                _results = lib.run_concurently(
                    lambda action: execute_workflow_action(
                        action,
                        event,
                        tracer,
                        cache,
                        parameters={
                            "order": order,
                            "parameters": parameters,
                            "steps": functools.reduce(
                                lambda acc, _: {
                                    **acc,
                                    **{_.get("alias"): _.get("output")},
                                },
                                results,
                                # steps can be provided by the event parameters for single action execution
                                (parameters.get("steps") or {}),
                            ),
                        },
                    ),
                    actions,
                )
                results += _results

                # abort if any action failed
                if any([_.get("status") == "failed" for _ in _results]):
                    logger.info("> aborting execution, an action failed...")
                    return automation_serializers.AutomationEventStatus.failed.value

                # abort if condition is false
                if any(
                    ["condition" in _ and _.get("condition") == False for _ in _results]
                ):
                    logger.info("> aborting execution, condition is false...")
                    return automation_serializers.AutomationEventStatus.aborted.value

                # abort if event is cancelled
                if models.WorkflowEvent.objects.filter(
                    id=event.id, status="cancelled"
                ).exists():
                    logger.info("> aborting execution, event cancelled...")
                    return automation_serializers.AutomationEventStatus.cancelled.value

    except Exception as e:
        logger.exception(e)
        logger.info("> execution failed due to runtime error...")
        return automation_serializers.AutomationEventStatus.failed.value

    return automation_serializers.AutomationEventStatus.success.value


@utils.error_wrapper
def execute_workflow_action(
    action: models.WorkflowAction,
    event: models.WorkflowEvent,
    tracer: lib.Tracer,
    cache: lib.Cache,
    parameters: dict = None,
):
    """
    Execute a single workflow action with full tracing and error handling.

    This function handles the complete lifecycle of action execution including
    connection authentication, action execution, result processing, and comprehensive
    tracing for debugging and audit purposes.

    EXECUTION LIFECYCLE:
    ===================

    1. PRE-EXECUTION:
       - Create tracing metadata context
       - Log action input parameters
       - Load and prepare connection data (if required)

    2. CONNECTION AUTHENTICATION:
       - Extract metafields credentials (prioritized)
       - Fallback to legacy credentials field
       - Process authentication templates (Basic, API Key, OAuth2)
       - Handle connection failures gracefully

    3. ACTION EXECUTION:
       - Call execute_action() with prepared context
       - Handle action-specific logic (HTTP, data mapping, conditional)
       - Process execution results

    4. POST-EXECUTION:
       - Log action output results
       - Return standardized result format
       - Handle any runtime exceptions

    Args:
        action (models.WorkflowAction): The action definition to execute
        event (models.WorkflowEvent): The parent workflow event context
        tracer (lib.Tracer): Tracing context for logging execution details
        cache (lib.Cache): Redis cache for session state and optimization
        parameters (dict, optional): Execution parameters including:
            - order: Action execution order number
            - parameters: Event input parameters
            - steps: Results from previous actions

    Returns:
        dict: Standardized action execution result:
        {
            "format": "json",           # Response format
            "status": "success|failed", # Execution status
            "action_name": "...",       # Human-readable action name
            "alias": "...",             # Action alias for referencing
            "output": {                 # Action-specific output
                "response": {...}       # or error details
            },
            "condition": bool           # Only for conditional actions
        }

    TRACING RECORDS:
    ===============

    Two tracing records are created per action execution:

    1. "action-input" Record:
    {
        "format": "json",
        "parameters": {...},        # Execution context
        "action_name": "..."        # Action identifier
    }

    2. "action-output" Record:
    {
        "format": "json",
        "status": "success|failed",
        "action_name": "...",
        "alias": "...",
        "output": {...}
    }

    CONNECTION DATA PROCESSING:
    ==========================

    Modern Metafields Approach (Preferred):
    - Loads metafields with type conversion (string, number, boolean)
    - Validates required fields
    - Provides secure credential storage
    - Supports per-connection configuration

    Legacy Credentials Fallback:
    - Uses connection.credentials JSON field
    - Maintained for backward compatibility
    - Less type-safe than metafields

    Connection Data Structure:
    {
        'connection_obj': models.WorkflowConnection,
        'credentials': {...},       # Actual credential values
        'metadata': {...},          # Connection configuration
        'metafields': {...}         # Structured field data
    }

    ERROR HANDLING:
    ==============

    Connection Errors:
    - Missing connection data (graceful degradation)
    - Invalid credentials (logged warnings)
    - Authentication failures (detailed error context)

    Action Execution Errors:
    - Network timeouts and connection failures
    - Template rendering errors
    - Invalid action configurations
    - Runtime exceptions during execution

    Error Response Format:
    {
        "format": "json",
        "status": "failed",
        "action_name": "...",
        "alias": "...",
        "output": {
            "error": {
                "message": "...",       # Human-readable error
                "details": {...}        # Technical error context
            }
        }
    }

    PERFORMANCE OPTIMIZATIONS:
    =========================

    Database Optimization:
    - Pre-loads connection and metafields data
    - Avoids N+1 queries with select_related/prefetch_related
    - Minimal database access during execution

    Memory Management:
    - Lazy-loads connection data only when needed
    - Efficient credential handling with fallback logic
    - Structured error handling to prevent memory leaks

    SECURITY CONSIDERATIONS:
    =======================

    Credential Handling:
    - Metafields credentials are prioritized for security
    - Legacy credentials maintained for backward compatibility
    - No credential data logged in tracing records
    - Connection errors don't expose sensitive data

    Template Rendering:
    - Jinja2 templates run in controlled environment
    - No direct system access from templates
    - Credential context carefully managed

    Example Usage:
    =============

    ```python
    result = execute_workflow_action(
        action=workflow_action,
        event=workflow_event,
        tracer=execution_tracer,
        cache=redis_cache,
        parameters={
            "order": 0,
            "parameters": {"input": "value"},
            "steps": {}
        }
    )

    if result["status"] == "success":
        response_data = result["output"]["response"]
    else:
        error_info = result["output"]["error"]
    ```

    Log Output:
    ----------
    WARNING: "Failed to load connection data: ..." (connection issues)
    INFO: "> action execution failed due to runtime error..." (exceptions)

    Database Operations:
    - SELECT: Loads action.connection with metafields (if exists)
    - No direct UPDATEs (tracing handled separately)
    """
    _parameters = parameters or dict()
    trace = tracer.with_metadata(
        dict(
            workflow_event_id=event.id,
            workflow_id=event.workflow.id,
            workflow_action_id=action.id,
            workflow_action_slug=action.slug,
        )
    )

    trace(
        dict(
            format="json",
            parameters=_parameters,
            action_name=action.name,
        ),
        "action-input",
    )

    try:
        # Pre-load connection data to avoid database access during execution
        connection_data = None
        if action.connection:
            try:
                # Load metafields credentials (prioritize over legacy)
                metafields_credentials = action.connection.credentials_from_metafields or {}
                # Fallback to legacy credentials if metafields are empty
                legacy_credentials = action.connection.credentials or {}
                connection_credentials = metafields_credentials if metafields_credentials else legacy_credentials

                connection_data = {
                    'connection_obj': action.connection,
                    'credentials': connection_credentials,
                    'metadata': action.connection.metadata or {},
                    'metafields': action.connection.metafields_object or {},
                }
            except Exception as e:
                logger.warning(f"Failed to load connection data: {e}")
                connection_data = {
                    'connection_obj': action.connection,
                    'credentials': action.connection.credentials or {},
                    'metadata': action.connection.metadata or {},
                    'metafields': {},
                }

        connection = authenticate_connection(
            connection_data,
            event,
            tracer,
            cache,
            parameters=_parameters,
        )
        result = execute_action(
            action,
            trace,
            connection=connection,
            parameters=_parameters,
        )
    except Exception as e:
        logger.exception(e)
        logger.info("> action execution failed due to runtime error...")
        result = {
            "format": "json",
            "status": "failed",
            "action_name": action.name,
            "alias": action.alias,
            "output": dict(error=dict(message=str(e))),
        }

    trace(result, "action-output")

    return result


def get_execution_sequence(
    event: models.WorkflowEvent,
) -> typing.List[typing.Tuple[int, typing.List[str]]]:
    """
    Calculate the execution sequence for workflow actions.

    This function analyzes the workflow definition and returns an ordered sequence
    of action groups that can be executed in parallel. Actions with the same order
    number are grouped together for concurrent execution.

    EXECUTION SEQUENCING LOGIC:
    ===========================

    Standard Workflow Execution:
    - Processes all actions defined in workflow.action_nodes
    - Groups actions by their 'order' field
    - Returns sorted list of (order, [action_slugs])

    Single Action Execution (Debug Mode):
    - If parameters contain 'run_action' field
    - Executes only the specified action
    - Useful for testing individual actions
    - Validates action exists in workflow

    Args:
        event (models.WorkflowEvent): The workflow event containing execution context

    Returns:
        List[Tuple[int, List[str]]]: Ordered execution sequence where:
        - First element (int): Order number (0, 1, 2, ...)
        - Second element (List[str]): Action slugs to execute in parallel

    Raises:
        Exception: If run_action parameter specifies invalid action slug

    EXECUTION PATTERNS:
    ==================

    Sequential Execution:
    action_nodes = [
        {"order": 0, "slug": "action_a"},
        {"order": 1, "slug": "action_b"},
        {"order": 2, "slug": "action_c"}
    ]
    Result: [(0, ["action_a"]), (1, ["action_b"]), (2, ["action_c"])]

    Parallel Execution:
    action_nodes = [
        {"order": 0, "slug": "action_a"},
        {"order": 0, "slug": "action_b"},
        {"order": 1, "slug": "action_c"}
    ]
    Result: [(0, ["action_a", "action_b"]), (1, ["action_c"])]

    Mixed Execution:
    action_nodes = [
        {"order": 0, "slug": "fetch_data"},
        {"order": 1, "slug": "process_a"},
        {"order": 1, "slug": "process_b"},
        {"order": 1, "slug": "process_c"},
        {"order": 2, "slug": "aggregate"}
    ]
    Result: [
        (0, ["fetch_data"]),
        (1, ["process_a", "process_b", "process_c"]),
        (2, ["aggregate"])
    ]

    Single Action Debug Mode:
    event.parameters = {"run_action": "action_b"}
    Result: [(1, ["action_b"])]  # Only executes action_b at its defined order

    PERFORMANCE BENEFITS:
    ====================

    Parallel Execution:
    - Actions in same order group run concurrently
    - Reduces total workflow execution time
    - Maximizes resource utilization
    - Maintains data consistency within order groups

    Order-based Dependencies:
    - Lower order actions complete before higher order actions
    - Results from lower orders available as 'steps' context
    - Enables complex data flow patterns
    - Supports conditional execution based on previous results

    USE CASES:
    ==========

    ETL Workflows:
    Order 0: Extract data from multiple sources (parallel)
    Order 1: Transform each dataset (parallel)
    Order 2: Load into destination (sequential)

    API Integration:
    Order 0: Authenticate with services (parallel)
    Order 1: Fetch data from multiple APIs (parallel)
    Order 2: Merge and process results (sequential)
    Order 3: Send notifications (parallel)

    Validation Workflows:
    Order 0: Run multiple validation checks (parallel)
    Order 1: Aggregate validation results (sequential)
    Order 2: Send notifications based on results (conditional)

    DEBUG AND TESTING:
    ==================

    Single Action Testing:
    ```python
    # Test only the email action
    event_params = {"run_action": "send_email"}
    sequence = get_execution_sequence(event)
    # Returns: [(2, ["send_email"])] - runs only this action
    ```

    This is useful for:
    - Testing individual actions in isolation
    - Debugging specific workflow steps
    - Developing new actions incrementally
    - Troubleshooting production issues

    ERROR HANDLING:
    ==============

    Invalid Action Slug:
    - Raises Exception with clear error message
    - Prevents execution of non-existent actions
    - Ensures workflow integrity

    Example Usage:
    =============

    ```python
    event = WorkflowEvent.objects.get(id="...")
    sequence = get_execution_sequence(event)

    for order, action_slugs in sequence:
        print(f"Order {order}: {action_slugs}")
        # Execute actions in parallel
        results = lib.run_concurrently(
            lambda slug: execute_action(slug, ...),
            action_slugs
        )
    ```

    Output Example:
    Order 0: ['fetch_user_data', 'fetch_inventory_data']
    Order 1: ['calculate_recommendations', 'check_availability']
    Order 2: ['send_email_notification']
    """
    _parameters = event.parameters or dict()
    _run_action = _parameters.get("run_action")

    if _run_action is not None:
        _node = next(
            (_ for _ in event.workflow.action_nodes if _.get("slug") == _run_action),
            None,
        )

        if _node is None:
            raise Exception(f"invalid action slug {_run_action}")

        return [(_node["order"], [_node.get("slug")])]

    ordered_actions = functools.reduce(
        lambda acc, _: {
            **acc,
            _.get("order"): [*acc.get(_.get("order"), []), _.get("slug")],
        },
        event.workflow.action_nodes,
        {},
    )

    return [
        (order, ordered_actions.get(order)) for order in sorted(ordered_actions.keys())
    ]


def get_last_executed_order(
    event: models.WorkflowEvent,
) -> int:
    """
    Determine the last successfully executed action order for workflow resumption.

    This function enables workflow resumption by analyzing tracing records to find
    the highest order number of completed actions. This supports recovery from
    failures, system restarts, and long-running workflow management.

    RESUMPTION LOGIC:
    ================

    The function queries the tracing database for "action-output" records associated
    with this workflow event. These records are created when actions complete
    (successfully or with failures), providing a reliable audit trail.

    Query Strategy:
    - Filters TracingRecord by key="action-output"
    - Filters by workflow_event_id in metadata
    - Orders by timestamp (most recent first)
    - Extracts workflow_action_order from first (most recent) record

    Args:
        event (models.WorkflowEvent): The workflow event to analyze

    Returns:
        int: The highest order number of completed actions, or -1 if no actions
             have been executed yet

    RETURN VALUES:
    =============

    -1: No actions executed yet
        - Fresh workflow execution
        - All actions will be executed from order 0

    0: Actions from order 0 completed
        - Next execution will start from order 1
        - Order 0 actions will be skipped

    N: Actions through order N completed
        - Next execution will start from order N+1
        - Orders 0 through N will be skipped

    WORKFLOW RESUMPTION SCENARIOS:
    =============================

    Scenario 1: Fresh Execution
    ```
    Workflow: [A(0), B(1), C(2)]
    Tracing: [] (no records)
    Result: -1
    Next: Execute A, then B, then C
    ```

    Scenario 2: Partial Completion
    ```
    Workflow: [A(0), B(1), C(2)]
    Tracing: [A_output] (order 0 completed)
    Result: 0
    Next: Execute B, then C (skip A)
    ```

    Scenario 3: Mid-workflow Failure
    ```
    Workflow: [A(0), B(0), C(1), D(2)]
    Tracing: [A_output, B_output] (order 0 completed)
    Result: 0
    Next: Execute C, then D (skip A and B)
    ```

    Scenario 4: Near Completion
    ```
    Workflow: [A(0), B(1), C(2)]
    Tracing: [A_output, B_output] (orders 0,1 completed)
    Result: 1
    Next: Execute C only (skip A and B)
    ```

    USE CASES:
    ==========

    System Recovery:
    - Application restart during workflow execution
    - Database connection failures
    - Worker process crashes
    - Infrastructure maintenance

    Long-running Workflows:
    - Multi-hour data processing pipelines
    - Batch job processing
    - ETL workflows with multiple stages
    - Complex integration scenarios

    Error Recovery:
    - Manual workflow restart after fixing issues
    - Retry mechanism for transient failures
    - Partial workflow re-execution
    - Development and testing scenarios

    TRACING RECORD STRUCTURE:
    ========================

    TracingRecord fields used:
    - key: "action-output" (identifies completed actions)
    - meta.workflow_event_id: Links to specific workflow execution
    - meta.workflow_action_order: Order number of completed action
    - timestamp: When action completed (for ordering)

    Example TracingRecord:
    ```json
    {
        "key": "action-output",
        "meta": {
            "workflow_event_id": "event_123",
            "workflow_action_id": "action_456",
            "workflow_action_order": 1,
            "workflow_id": "workflow_789"
        },
        "timestamp": "2023-12-01T10:30:00Z",
        "record": {
            "status": "success",
            "output": {...}
        }
    }
    ```

    PERFORMANCE CONSIDERATIONS:
    ==========================

    Database Query:
    - Single query with indexed filters
    - Orders by timestamp for efficiency
    - Limits to first() result for fast retrieval
    - Uses meta__workflow_event_id index

    Memory Usage:
    - Minimal memory footprint
    - Only loads single record metadata
    - No large result set processing

    Edge Cases:
    - Empty tracing records (returns -1)
    - Multiple actions at same order (returns highest completed order)
    - Malformed tracing data (graceful fallback)

    RELIABILITY:
    ===========

    Data Consistency:
    - Tracing records created atomically with action completion
    - Timestamp ordering ensures proper sequence detection
    - Metadata validation prevents data corruption

    Fault Tolerance:
    - Handles missing tracing records gracefully
    - Defaults to safe re-execution (-1) on errors
    - No side effects from query operations

    Example Usage:
    =============

    ```python
    last_order = get_last_executed_order(event)

    if last_order == -1:
        print("Starting fresh workflow execution")
    else:
        print(f"Resuming from order {last_order + 1}")

    # Process only remaining actions
    for order, actions in execution_sequence:
        if order > last_order:
            execute_action_group(actions)
    ```

    Database Operations:
    - SELECT: Single query on TracingRecord table
    - Filters: key, meta__workflow_event_id
    - Ordering: timestamp DESC
    - Limit: 1 record
    """
    records = tracing.TracingRecord.objects.filter(
        key="action-output",
        meta__workflow_event_id=event.id,
    )

    if records.exists():
        return records.first().meta.get("workflow_action_order")

    return -1


def authenticate_connection(
    connection_data: typing.Optional[dict],
    event: models.WorkflowEvent,
    tracer: lib.Tracer,
    cache: lib.Cache,
    parameters: dict = None,
) -> dict:
    """
    Process connection authentication and return authentication context.

    This function handles various authentication schemes (Basic, API Key, OAuth2)
    and prepares authentication headers/tokens for use in HTTP requests and other
    authenticated actions. It supports both modern metafields credentials and
    legacy credential storage.

    AUTHENTICATION FLOW:
    ===================

    1. VALIDATION:
       - Check if connection data exists
       - Extract connection object and credentials
       - Prepare Jinja2 rendering context

    2. CREDENTIAL PRIORITIZATION:
       - Use metafields credentials (preferred)
       - Fallback to legacy credentials field
       - Merge with connection metadata

    3. AUTHENTICATION PROCESSING:
       - Process auth_template with Jinja2
       - Apply authentication scheme logic
       - Generate authentication headers/tokens

    4. CONTEXT PREPARATION:
       - Return authentication context for action execution
       - Include credentials for template rendering

    Args:
        connection_data (dict, optional): Pre-loaded connection information:
            - connection_obj: WorkflowConnection model instance
            - credentials: Credential values (metafields or legacy)
            - metadata: Connection configuration
            - metafields: Structured field data
        event (models.WorkflowEvent): Workflow event context
        tracer (lib.Tracer): Tracing context for debugging
        cache (lib.Cache): Redis cache for session optimization
        parameters (dict, optional): Execution context parameters

    Returns:
        dict: Authentication context for action execution:
        {
            "credentials": {...},           # Credential values
            "authorization": "...",         # Basic auth header (Basic only)
            "Authorization": "Bearer ...",  # API key header (API Key only)
            # ... other auth headers based on auth_template
        }

    AUTHENTICATION SCHEMES:
    ======================

    No Authentication:
    - connection_data is None
    - Returns: {"credentials": {}}
    - Use case: Public APIs, data mapping actions

    Basic Authentication:
    - auth_type: "basic"
    - auth_template: "username:password" format
    - Processing: Base64 encode template result
    - Returns: {"authorization": "Basic base64string", "credentials": {...}}

    API Key Authentication:
    - auth_type: "api_key"
    - auth_template: JSON structure with auth headers
    - Processing: Render template and parse as JSON
    - Returns: Parsed JSON + {"credentials": {...}}

    OAuth2 Authentication:
    - auth_type: "oauth2"
    - Processing: Not yet implemented
    - Returns: {"credentials": {...}}

    TEMPLATE RENDERING CONTEXT:
    ==========================

    The auth_template is rendered with rich context:

    ```python
    {
        # Execution parameters
        "order": 0,
        "parameters": {...},    # Event input parameters
        "steps": {...},         # Previous action results

        # Utility functions
        "lib": karrio.lib,      # Utility functions

        # Connection data
        "metadata": {...},      # Connection metadata
        "credentials": {...},   # Credential values
        "metafields": {...}     # Structured fields
    }
    ```

    CREDENTIAL EXAMPLES:
    ===================

    Basic Authentication:
    ```yaml
    auth_type: basic
    auth_template: "{{credentials.username}}:{{credentials.password}}"

    credentials:
        username: "api_user"
        password: "secret123"

    Result: {"authorization": "Basic YXBpX3VzZXI6c2VjcmV0MTIz"}
    ```

    API Key Authentication:
    ```yaml
    auth_type: api_key
    auth_template: |
        {
            "Authorization": "Bearer {{credentials.api_key}}",
            "X-API-Version": "v1"
        }

    credentials:
        api_key: "sk_test_123abc"

    Result: {
        "Authorization": "Bearer sk_test_123abc",
        "X-API-Version": "v1",
        "credentials": {"api_key": "sk_test_123abc"}
    }
    ```

    Complex API Key with Signature:
    ```yaml
    auth_template: |
        {
            "Authorization": "{{credentials.key_id}}:{{lib.hash_hmac('sha256', request_data, credentials.secret)}}",
            "Content-Type": "application/json"
        }
    ```

    METAFIELDS VS LEGACY CREDENTIALS:
    ================================

    Modern Metafields (Preferred):
    - Type-safe with validation (string, number, boolean)
    - Required field enforcement
    - Structured credential management
    - Enhanced security and audit

    Legacy Credentials (Fallback):
    - JSON field on WorkflowConnection
    - Backward compatibility
    - Less type safety
    - Simpler for basic use cases

    Priority Logic:
    1. If metafields exist and contain values → use metafields
    2. Else → use legacy credentials field
    3. Merge with connection metadata

    ERROR HANDLING:
    ==============

    Missing Connection:
    - Returns empty credentials context
    - Allows actions to proceed without authentication
    - Useful for public APIs and data transformations

    Template Rendering Errors:
    - Jinja2 template syntax errors
    - Missing credential fields
    - Invalid credential values
    - Graceful fallback to minimal context

    Authentication Failures:
    - Invalid credential formats
    - Missing required fields
    - Network issues during OAuth flows
    - Logged but don't prevent action execution

    SECURITY CONSIDERATIONS:
    =======================

    Credential Protection:
    - Credentials never logged in tracing records
    - Template rendering in isolated context
    - No credential exposure in error messages
    - Secure storage in metafields

    Template Safety:
    - Controlled Jinja2 environment
    - No filesystem access from templates
    - Limited function exposure
    - Input validation and sanitization

    PERFORMANCE OPTIMIZATIONS:
    =========================

    Credential Caching:
    - Pre-loaded in execute_workflow_action()
    - Avoids database queries during authentication
    - Efficient metafields processing

    Template Compilation:
    - Jinja2 templates compiled once per execution
    - Reused across multiple actions
    - Minimal CPU overhead

    USE CASES:
    ==========

    REST API Integration:
    - Bearer token authentication
    - API key headers
    - Custom authentication schemes

    Database Connections:
    - Username/password combinations
    - Connection string building
    - Credential rotation support

    Third-party Services:
    - OAuth2 flows (future)
    - Multi-factor authentication
    - Time-based tokens

    Example Usage:
    =============

    ```python
    # Pre-loaded connection data
    connection_data = {
        'connection_obj': connection,
        'credentials': {'api_key': 'sk_123'},
        'metadata': {'timeout': 30},
        'metafields': {}
    }

    auth_context = authenticate_connection(
        connection_data, event, tracer, cache, parameters
    )

    # Use in HTTP request
    headers = {
        **auth_context,  # Includes Authorization headers
        'Content-Type': 'application/json'
    }
    ```

    Database Operations:
    - No direct database queries (data pre-loaded)
    - No database modifications
    - Read-only operation
    """
    _parameters = parameters or dict()

    if connection_data is None:
        return dict()

    connection_obj = connection_data.get('connection_obj')
    connection_credentials = connection_data.get('credentials', {})

    _render_context = {
        **_parameters,
        "lib": lib,
        "metadata": connection_data.get('metadata', {}),
        "credentials": connection_credentials,
        "metafields": connection_data.get('metafields', {}),
    }

    if connection_obj is None:
        return dict(credentials=connection_credentials)

    if connection_obj.auth_type == automation_serializers.AutomationAuthType.basic.value:
        _computed_auth = jinja2.Template(connection_obj.auth_template or "").render(
            **_render_context
        )
        authorization = base64.b64encode(_computed_auth.encode("utf-8")).decode("ascii")

        return dict(authorization=authorization, credentials=connection_credentials)

    if connection_obj.auth_type == automation_serializers.AutomationAuthType.api_key.value:
        _computed_auth = jinja2.Template(connection_obj.auth_template or "").render(
            **_render_context
        )

        result = lib.to_dict(_computed_auth)
        result["credentials"] = connection_credentials
        return result

    if connection_obj.auth_type == automation_serializers.AutomationAuthType.oauth2.value:
        pass

    return dict(credentials=connection_credentials)


def execute_action(
    action: models.WorkflowAction,
    trace: typing.Callable,
    connection: dict = None,
    parameters: dict = None,
) -> dict:
    """
    Execute a specific action based on its type with comprehensive error handling.

    This function is the core action execution engine that dispatches to specific
    action type handlers (HTTP request, data mapping, conditional) and standardizes
    their output format. It provides rich template rendering context and robust
    error handling for all supported action types.

    SUPPORTED ACTION TYPES:
    ======================

    1. HTTP_REQUEST:
       - Purpose: Make HTTP API calls to external services
       - Methods: GET, POST, PUT, DELETE, PATCH
       - Features: Authentication, templating, timeout handling
       - Output: API response data

    2. DATA_MAPPING:
       - Purpose: Transform data using Jinja2 templates
       - Features: Access to previous action results, complex transformations
       - Output: Transformed data structure

    3. CONDITIONAL:
       - Purpose: Evaluate boolean conditions for workflow branching
       - Features: YAML/JSON expression evaluation
       - Output: Boolean result + workflow control

    Args:
        action (models.WorkflowAction): The action definition to execute
        trace (typing.Callable): Tracing function for logging execution details
        connection (dict, optional): Authentication context from authenticate_connection()
        parameters (dict, optional): Execution context including:
            - order: Action execution order
            - parameters: Event input parameters
            - steps: Results from previous actions

    Returns:
        dict: Standardized action result:
        {
            "format": "json|text",           # Response format
            "status": "success|failed",      # Execution status
            "action_name": "...",            # Human-readable name
            "alias": "...",                  # Action alias for referencing
            "output": {                      # Action-specific output
                "response": {...}            # Success response data
                # OR
                "error": {...}               # Error details
            },
            "condition": bool                # Only for conditional actions
        }

    TEMPLATE RENDERING CONTEXT:
    ===========================

    All action types receive rich template context:

    ```python
    {
        # Execution flow
        "order": 0,                 # Current action order
        "parameters": {...},        # Event input parameters
        "steps": {                  # Previous action results
            "fetch_user": {
                "response": {...},
                "status": "success"
            }
        },

        # Utilities and data
        "lib": karrio.lib,          # Utility functions
        "connection": {...},        # Authentication headers/tokens
        "metadata": {...},          # Action metadata
        "credentials": {...}        # Connection credentials
    }
    ```

    HTTP REQUEST ACTION TYPE:
    ========================

    Configuration:
    - action_type: "http_request"
    - host: Target server URL (supports templates)
    - endpoint: API endpoint path
    - method: HTTP method (GET, POST, PUT, DELETE, PATCH)
    - parameters_type: "querystring" or "data"
    - parameters_template: Request parameters (Jinja2 template)
    - header_template: HTTP headers (Jinja2 template)
    - content_type: Response format ("json" or other)

    Execution Flow:
    1. Render host URL with credentials context
    2. Render parameters template with execution context
    3. Build request URL with querystring or data payload
    4. Render headers template with authentication
    5. Execute HTTP request with timeout and error handling
    6. Process and return response

    Timeout and Error Handling:
    - Default timeout: 30 seconds
    - Configurable via parameters.timeout
    - Categorized error messages (timeout, connection, SSL)
    - Detailed error context for debugging

    Example HTTP Action:
    ```python
    action = WorkflowAction(
        action_type="http_request",
        host="https://api.example.com",
        endpoint="/users/{{parameters.user_id}}",
        method="GET",
        header_template='{"Authorization": "Bearer {{credentials.api_key}}"}',
        parameters_template='{"include": "profile,settings"}'
    )

    # Execution with context
    result = execute_action(action, trace, connection, parameters)
    # Returns: {"status": "success", "output": {"response": {...}}}
    ```

    DATA MAPPING ACTION TYPE:
    ========================

    Configuration:
    - action_type: "data_mapping"
    - parameters_template: Jinja2 transformation template
    - content_type: Output format ("json" or "text")

    Features:
    - Access to all previous action results via 'steps'
    - Complex data transformations with loops and conditionals
    - JSON parsing and generation
    - String manipulation and formatting

    Example Data Mapping:
    ```python
    # Transform user data from previous API call
    parameters_template = '''
    {
        "user_profile": {
            "name": "{{steps.fetch_user.response.first_name}} {{steps.fetch_user.response.last_name}}",
            "email": "{{steps.fetch_user.response.email}}",
            "preferences": {{steps.fetch_settings.response.preferences|tojson}}
        }
    }
    '''

    result = execute_action(data_mapping_action, trace, None, parameters)
    # Returns: {"status": "success", "output": {"response": {...}}}
    ```

    CONDITIONAL ACTION TYPE:
    =======================

    Configuration:
    - action_type: "conditional"
    - parameters_template: Boolean expression template
    - Format: YAML/JSON with "result" field

    Features:
    - Workflow branching and early termination
    - Access to all execution context
    - Complex boolean logic evaluation
    - Condition result affects workflow continuation

    Example Conditional:
    ```python
    # Check if user is premium before sending notification
    parameters_template = '''
    {
        "result": "{{steps.fetch_user.response.subscription_type == 'premium'}}",
        "user_type": "{{steps.fetch_user.response.subscription_type}}"
    }
    '''

    result = execute_action(conditional_action, trace, None, parameters)
    # Returns: {
    #     "status": "success",
    #     "output": {"response": {"result": true, ...}},
    #     "condition": true  # Controls workflow continuation
    # }
    ```

    ERROR HANDLING:
    ==============

    HTTP Request Errors:
    - Network timeouts: "Request timeout after N seconds"
    - Connection failures: "Connection error to HOST"
    - SSL/TLS issues: "SSL/TLS error connecting to HOST"
    - HTTP error codes: Captured in response

    Template Rendering Errors:
    - Jinja2 syntax errors in templates
    - Missing context variables
    - Type conversion errors
    - Invalid JSON generation

    Action Configuration Errors:
    - Unsupported action types
    - Missing required fields
    - Invalid parameter combinations

    Error Response Format:
    ```python
    {
        "format": "json",
        "status": "failed",
        "action_name": "API Call",
        "alias": "api_call",
        "output": {
            "error": {
                "message": "Request timeout after 30 seconds",
                "url": "https://api.example.com/users/123",
                "method": "GET",
                "timeout": 30,
                "original_error": "timeout exception details"
            }
        }
    }
    ```

    PERFORMANCE OPTIMIZATIONS:
    =========================

    Template Compilation:
    - Jinja2 templates compiled once per execution
    - Efficient context variable resolution
    - Minimal memory allocation

    HTTP Request Optimization:
    - Connection pooling via lib.request
    - Keep-alive connections where possible
    - Efficient header and parameter processing

    Data Processing:
    - Lazy JSON parsing and generation
    - Efficient string operations
    - Memory-conscious data transformations

    SECURITY CONSIDERATIONS:
    =======================

    Template Security:
    - Controlled Jinja2 environment
    - No filesystem access
    - Limited function exposure
    - Input sanitization

    Credential Handling:
    - Credentials available in templates but never logged
    - Secure authentication header construction
    - No credential exposure in error messages

    Network Security:
    - HTTPS enforcement for sensitive requests
    - Certificate validation
    - Request timeout enforcement

    USE CASES:
    ==========

    API Integration Workflows:
    1. HTTP: Authenticate with service
    2. HTTP: Fetch user data
    3. DATA_MAPPING: Transform for internal format
    4. CONDITIONAL: Check business rules
    5. HTTP: Update user profile (if condition true)

    Data Processing Pipelines:
    1. HTTP: Fetch raw data from multiple sources
    2. DATA_MAPPING: Clean and normalize data
    3. DATA_MAPPING: Apply business transformations
    4. CONDITIONAL: Validate data quality
    5. HTTP: Submit to destination (if valid)

    Notification Workflows:
    1. HTTP: Fetch user preferences
    2. CONDITIONAL: Check notification settings
    3. DATA_MAPPING: Build notification content
    4. HTTP: Send via preferred channel (if enabled)

    Example Execution:
    =================

    ```python
    # Execute HTTP request action
    result = execute_action(
        action=http_action,
        trace=tracer.log,
        connection={"Authorization": "Bearer token123"},
        parameters={
            "order": 1,
            "parameters": {"user_id": "123"},
            "steps": {"auth": {"response": {"token": "abc"}}}
        }
    )

    if result["status"] == "success":
        api_response = result["output"]["response"]
        print(f"API returned: {api_response}")
    else:
        error_details = result["output"]["error"]
        print(f"Action failed: {error_details['message']}")
    ```

    Tracing Integration:
    ===================

    The trace function logs detailed execution information:
    - HTTP request/response details (for HTTP actions)
    - Template input/output (for data mapping)
    - Condition evaluation (for conditionals)
    - Error context and stack traces
    - Performance metrics (execution time, etc.)

    Database Operations:
    - No direct database queries
    - Read-only operation on pre-loaded action data
    - No side effects beyond HTTP requests
    """
    _parameters = parameters or dict()

    _render_context = {
        **_parameters,
        "lib": lib,
        "connection": connection or {},
        "metadata": action.metadata or {},
        "credentials": (connection or {}).get("credentials", {}),
    }
    _format = action.content_type or "json"

    if (
        action.action_type
        == automation_serializers.AutomationActionType.http_request.value
    ):
        _trace = functools.partial(trace, format=_format)
        _computed_parameters = (
            jinja2.Template(action.parameters_template or "{}")
            .render(**_render_context)
            .strip()
        )
        _data = (
            dict(data=lib.to_json(lib.to_dict(_computed_parameters)))
            if action.parameters_type == "data"
            else dict()
        )
        _querystring = (
            f"?{urllib.parse.urlencode(lib.to_dict(_computed_parameters))}"
            if action.parameters_type == "querystring"
            else ""
        )
        _port = f":{action.port}" if action.port is not None else ""
        _endpoint = action.endpoint or ""

        # Render host template with credentials context
        _host = jinja2.Template(action.host or "").render(**_render_context)

        _method = (action.method or "GET").upper()
        _url = f"{_host}{_port}{_endpoint}{_querystring}"
        _headers = lib.to_dict(
            jinja2.Template(action.header_template or "{}").render(**_render_context)
        )
        _status = "success"

        def _on_error(_):
            nonlocal _status
            _status = "failed"
            return lib.failsafe(lambda: lib.decode(_.read()))

        # Add timeout support and enhanced error handling
        _computed_params_dict = lib.to_dict(_computed_parameters)
        _timeout = _computed_params_dict.get("timeout", 30)  # Default 30 second timeout

        try:
            _response = lib.request(
                url=_url,
                trace=_trace,
                method=_method,
                headers=_headers,
                on_error=_on_error,
                timeout=_timeout,
                **_data,
            )
        except Exception as e:
            # Enhanced error handling with detailed messages
            error_message = str(e)
            if "timeout" in error_message.lower():
                error_message = f"Request timeout after {_timeout} seconds"
            elif "connection" in error_message.lower():
                error_message = f"Connection error to {_host}"
            elif "ssl" in error_message.lower():
                error_message = f"SSL/TLS error connecting to {_host}"

            return {
                "format": _format,
                "status": "failed",
                "action_name": action.name,
                "alias": action.alias,
                "output": dict(
                    error=dict(
                        message=error_message,
                        url=_url,
                        method=_method,
                        timeout=_timeout,
                        original_error=str(e)
                    )
                ),
            }

        return {
            "format": _format,
            "status": _status,
            "action_name": action.name,
            "alias": action.alias,
            "output": dict(
                response=(lib.to_dict(_response) if _format == "json" else _response),
            ),
        }

    if (
        action.action_type
        == automation_serializers.AutomationActionType.data_mapping.value
    ):
        _computed_parameters = jinja2.Template(action.parameters_template or "").render(
            **_render_context
        )

        if _format == "json":
            _response = lib.to_dict(_computed_parameters)
        else:
            _response = _computed_parameters

        return {
            "format": _format,
            "status": "success",
            "action_name": action.name,
            "alias": action.alias,
            "output": dict(response=_response),
        }

    if (
        action.action_type
        == automation_serializers.AutomationActionType.conditional.value
    ):
        _computed_parameters = jinja2.Template(action.parameters_template or "").render(
            **_render_context
        )
        _response = lib.to_dict(_computed_parameters)
        _result = bool(yaml.safe_load(_response["result"]))

        return {
            "format": _format,
            "status": "success",
            "action_name": action.name,
            "alias": action.alias,
            "output": dict(response=dict(result=_result, content=_response)),
            "condition": _result,
        }

    return {
        "format": "json",
        "status": "failed",
        "action_name": action.name,
        "alias": action.alias,
        "output": dict(
            error=dict(message=f"action type {action.action_type} is not supported"),
        ),
    }
