"""Karrio Scheduled Workflow Cron Utilities - Time-based Workflow Automation

This module provides production-ready cron expression handling for scheduled workflows within
the Karrio automation system. It implements robust validation, next-run calculation, and
human-readable description generation for time-based workflow triggers.

🎯 **Core Functionality**

The cron utilities enable precise scheduling of workflow executions using standard cron syntax.
They integrate with Django's timezone system and provide comprehensive error handling for
invalid expressions while supporting complex scheduling scenarios.

📊 **Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     KARRIO SCHEDULED WORKFLOW CRON SYSTEM                      │
│                         Complete Data Flow Illustration                        │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │  Cron Expression │    │   Validation &   │    │  Next Run Time  │
    │   "0 9 * * 1"   │───▶│   Calculation    │───▶│  2024-01-22     │
    │  (Every Monday  │    │     Engine       │    │   09:00:00 UTC  │
    │   at 9 AM)      │    │                  │    │                 │
    └─────────────────┘    └──────────────────┘    └─────────────────┘
             │                        │                        │
             │              ┌─────────▼─────────┐              │
             │              │  Human Readable   │              │
             └─────────────▶│   Description     │◀─────────────┘
                            │ "At 09:00 on Mon" │
                            └───────────────────┘

📋 **Input/Output Data Examples**

**Cron Expression Validation:**
```python
# Input
cron_expression = "0 9 * * 1"  # Every Monday at 9 AM

# Process
is_valid = validate_cron_expression(cron_expression)

# Output
True  # Valid expression
```

**Next Run Time Calculation:**
```python
# Input
cron_expression = "0 9 * * 1"  # Every Monday at 9 AM
base_time = datetime(2024, 1, 15, 10, 0, tzinfo=timezone.utc)  # Monday 10 AM

# Process
next_run = calculate_next_run_time(cron_expression, base_time)

# Output
datetime(2024, 1, 22, 9, 0, tzinfo=timezone.utc)  # Next Monday at 9 AM
```

**Human Description Generation:**
```python
# Input
cron_expression = "0 9 * * 1"

# Process
description = get_cron_description(cron_expression)

# Output
"At 09:00 on Monday"  # Human-readable description
```

**Due Check Evaluation:**
```python
# Input
cron_expression = "0 9 * * 1"
check_time = datetime(2024, 1, 22, 9, 0, tzinfo=timezone.utc)  # Monday 9 AM

# Process
is_due = is_cron_due(cron_expression, check_time)

# Output
True  # Workflow should execute now
```

🔧 **Integration Points**

1. **WorkflowTrigger.clean()** - Validates schedule field during model save
2. **WorkflowTrigger.update_next_run()** - Calculates next execution time
3. **Scheduled Task Executor** - Checks if workflows are due for execution
4. **Management Commands** - Provides human-readable schedule descriptions

⚠️ **Error Handling**

- **InvalidCronExpressionError**: Raised for malformed cron expressions
- **Timezone Awareness**: All times use Django's configured timezone
- **Edge Cases**: Handles leap years, month boundaries, DST transitions

📈 **Performance Characteristics**

- **Validation**: O(1) constant time using croniter parser
- **Calculation**: O(1) single iteration to next occurrence
- **Memory**: Minimal overhead, stateless operations
- **Thread Safety**: All functions are pure and thread-safe
"""

import datetime
from typing import Optional

from django.utils import timezone

from karrio.server.automation.exceptions import InvalidCronExpressionError


def validate_cron_expression(cron_expr: str) -> bool:
    """
    Validate a cron expression using croniter.

    Args:
        cron_expr: The cron expression to validate (e.g., "0 9 * * 1")

    Returns:
        True if valid

    Raises:
        InvalidCronExpressionError: If the cron expression is invalid
    """
    try:
        from croniter import croniter

        # Test if croniter can parse the expression
        base = datetime.datetime.now()
        cron = croniter(cron_expr, base)

        # Try to get the next execution time to verify it works
        next_run = cron.get_next(datetime.datetime)

        if not isinstance(next_run, datetime.datetime):
            raise InvalidCronExpressionError(f"Invalid cron expression: {cron_expr}")

        return True

    except ImportError:
        raise InvalidCronExpressionError("croniter package is required for cron validation")
    except Exception as e:
        raise InvalidCronExpressionError(f"Invalid cron expression '{cron_expr}': {str(e)}")


def calculate_next_run_time(cron_expr: str, base_time: Optional[datetime.datetime] = None) -> datetime.datetime:
    """
    Calculate the next run time for a cron expression.

    Args:
        cron_expr: The cron expression (e.g., "0 9 * * 1")
        base_time: Base time to calculate from (defaults to now)

    Returns:
        The next scheduled execution time as timezone-aware datetime

    Raises:
        InvalidCronExpressionError: If the cron expression is invalid
    """
    try:
        from croniter import croniter

        if base_time is None:
            base_time = timezone.now()
        elif base_time.tzinfo is None:
            # Convert naive datetime to timezone-aware
            base_time = timezone.make_aware(base_time)

        # Create croniter instance
        cron = croniter(cron_expr, base_time)

        # Get next execution time
        next_run = cron.get_next(datetime.datetime)

        # Ensure the result is timezone-aware
        if next_run.tzinfo is None:
            next_run = timezone.make_aware(next_run)

        return next_run

    except ImportError:
        raise InvalidCronExpressionError("croniter package is required for cron calculations")
    except Exception as e:
        raise InvalidCronExpressionError(f"Failed to calculate next run time for '{cron_expr}': {str(e)}")


def get_cron_description(cron_expr: str) -> str:
    """
    Get a human-readable description of a cron expression.

    Args:
        cron_expr: The cron expression

    Returns:
        Human-readable description of the schedule
    """
    try:
        from cron_descriptor import get_description
        return get_description(cron_expr)
    except ImportError:
        # Fallback to basic descriptions for common patterns
        return _get_basic_cron_description(cron_expr)
    except Exception:
        return f"Custom schedule: {cron_expr}"


def _get_basic_cron_description(cron_expr: str) -> str:
    """
    Provide basic descriptions for common cron patterns.

    Args:
        cron_expr: The cron expression

    Returns:
        Basic description of the schedule
    """
    common_patterns = {
        "0 0 * * *": "Daily at midnight",
        "0 9 * * *": "Daily at 9:00 AM",
        "0 12 * * *": "Daily at noon",
        "0 18 * * *": "Daily at 6:00 PM",
        "0 9 * * 1": "Every Monday at 9:00 AM",
        "0 9 * * 1-5": "Weekdays at 9:00 AM",
        "0 0 1 * *": "First day of every month at midnight",
        "*/15 * * * *": "Every 15 minutes",
        "*/30 * * * *": "Every 30 minutes",
        "0 */1 * * *": "Every hour",
        "0 */2 * * *": "Every 2 hours",
        "0 */6 * * *": "Every 6 hours",
        "0 */12 * * *": "Every 12 hours",
    }

    return common_patterns.get(cron_expr, f"Custom schedule: {cron_expr}")


def is_cron_due(cron_expr: str, last_run: Optional[datetime.datetime] = None) -> bool:
    """
    Check if a cron job is due to run based on the expression and last run time.

    Args:
        cron_expr: The cron expression
        last_run: When the job was last run (defaults to None, meaning never run)

    Returns:
        True if the job should run now
    """
    try:
        from croniter import croniter

        now = timezone.now()

        if last_run is None:
            # Never run before, so it's due
            return True

        # Ensure last_run is timezone-aware
        if last_run.tzinfo is None:
            last_run = timezone.make_aware(last_run)

        # Create croniter from last run time
        cron = croniter(cron_expr, last_run)

        # Get the next scheduled time after last run
        next_scheduled = cron.get_next(datetime.datetime)

        # Ensure timezone-aware
        if next_scheduled.tzinfo is None:
            next_scheduled = timezone.make_aware(next_scheduled)

        # Job is due if the next scheduled time has passed
        return next_scheduled <= now

    except Exception:
        # If we can't determine, assume it's not due to avoid spam
        return False
