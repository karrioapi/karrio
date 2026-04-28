# type: ignore
import sys

import decouple

# Karrio Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = decouple.config(
    "TRACKING_PULSE", default=7200, cast=int
)  # value is seconds. so 10800 seconds = 3 Hours
TRACKER_BATCH_DELAY = decouple.config(
    "TRACKER_BATCH_DELAY", default=3, cast=int
)  # flat seconds between tracking batches (per-carrier)
# TRACKER_MAX_ACTIVE_DAYS is defined in constance.py (runtime-configurable via admin).
# The tracking task reads it from constance at runtime, falling back to settings.
# No need to duplicate here — constance.py is the canonical source.

# Check if worker is running in detached mode (separate from API server)
DETACHED_WORKER = decouple.config("DETACHED_WORKER", default=False, cast=bool)

WORKER_IMMEDIATE_MODE = decouple.config("WORKER_IMMEDIATE_MODE", default=False, cast=bool)

# Detect if running as a worker process (via run_huey or run-servicebus-worker)
IS_WORKER_PROCESS = any(cmd in arg for arg in sys.argv for cmd in ("run_huey", "run-servicebus-worker"))

# Task backend selection: "huey" (default), "servicebus", or "immediate"
# - "huey": Redis-backed task queue (existing behavior, backward-compatible)
# - "servicebus": Azure Service Bus with KEDA autoscaling
# - "immediate": synchronous execution (for local dev without Redis)
TASK_BACKEND = decouple.config("TASK_BACKEND", default="huey")


# ─────────────────────────────────────────────────────────────────────────────
# Task Backend Initialization
# ─────────────────────────────────────────────────────────────────────────────
# ImmediateBackend is set eagerly as a safe fallback. When TASK_BACKEND=huey,
# HueyConfig.ready() overrides it with HueyBackend after Django is fully loaded.
# This ensures tasks work even if the huey module isn't installed.

from karrio.server.core.backends.immediate import ImmediateBackend
from karrio.server.core.task_backend import set_backend

set_backend(ImmediateBackend())
