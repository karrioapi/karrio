# type: ignore
"""
Huey settings — auto-discovered by karrio.server.settings.__init__.py

Creates the HUEY Django setting and adds huey.contrib.djhuey to INSTALLED_APPS.
"""

import sys

import decouple
from karrio.server.huey.configuration import create_huey_instance
from karrio.server.settings.base import *

INSTALLED_APPS += ["huey.contrib.djhuey", "karrio.server.huey"]  # type: ignore

_WORKER_IMMEDIATE = decouple.config("WORKER_IMMEDIATE_MODE", default=False, cast=bool)
_DETACHED = decouple.config("DETACHED_WORKER", default=False, cast=bool)
_IS_WORKER = any(cmd in arg for arg in sys.argv for cmd in ("run_huey", "run-servicebus-worker"))

HUEY = create_huey_instance(
    work_dir=WORK_DIR,
    databases=DATABASES,
    worker_immediate_mode=_WORKER_IMMEDIATE,
    detached_worker=_DETACHED,
    is_worker_process=_IS_WORKER,
)
