"""Shared logging-capture helper for telemetry tests.

Two project-specific noise sources need to be defeated in order to reliably
capture stdlib log records inside Django tests:

  1. Django's test runner calls `logging.disable(CRITICAL)` so non-critical
     records are dropped before reaching ANY handler — temporarily lift to
     NOTSET for the duration of the test and restore on cleanup.
  2. Loguru's root-level `InterceptHandler` makes `assertLogs` unreliable —
     attach directly to the named logger instead of going through the root.
"""

import logging
import unittest


def capture_records(
    test: unittest.TestCase,
    logger_name: str,
    level: int = logging.DEBUG,
) -> list[logging.LogRecord]:
    """Attach a list-backed handler to `logger_name` for the duration of
    `test` and return the list it appends to."""
    prior_disable_level = logging.root.manager.disable
    logging.disable(logging.NOTSET)
    test.addCleanup(logging.disable, prior_disable_level)

    records: list[logging.LogRecord] = []

    class _Cap(logging.Handler):
        def emit(self, r):
            records.append(r)

    handler = _Cap()
    handler.setLevel(level)
    target = logging.getLogger(logger_name)
    target.addHandler(handler)
    test.addCleanup(target.removeHandler, handler)
    return records
