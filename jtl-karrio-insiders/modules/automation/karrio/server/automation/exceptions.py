"""Karrio Scheduled Workflow Exceptions - Structured Error Handling

This module provides a comprehensive exception hierarchy for scheduled workflow operations
within the Karrio automation system. It implements typed error handling for cron validation,
scheduler operations, and workflow execution failures.

🎯 **Exception Hierarchy**

```
AutomationError (Base)
├── InvalidCronExpressionError    # Cron syntax validation failures
├── SchedulerError               # Task registration/management issues
└── WorkflowExecutionError       # Runtime execution problems
```

📊 **Error Categories & Use Cases**

**Cron Expression Errors:**
```python
# Invalid syntax
try:
    validate_cron_expression("invalid cron")
except InvalidCronExpressionError as e:
    # Handle malformed cron expressions
    print(f"Cron error: {e}")
    # Output: "Invalid cron expression 'invalid cron': ..."
```

**Scheduler Operation Errors:**
```python
# Task registration failures
try:
    scheduler.register_scheduled_workflow(trigger)
except SchedulerError as e:
    # Handle registration/Huey integration issues
    logger.error(f"Scheduler error: {e}")
```

**Workflow Execution Errors:**
```python
# Runtime execution problems
try:
    execute_scheduled_workflow(trigger_id)
except WorkflowExecutionError as e:
    # Handle workflow execution failures
    alert_operations_team(f"Execution failed: {e}")
```

🔧 **Integration Examples**

**Model Validation:**
```python
class WorkflowTrigger(models.Model):
    def clean(self):
        try:
            validate_cron_expression(self.schedule)
        except InvalidCronExpressionError as e:
            raise ValidationError({'schedule': str(e)})
```

**Service Error Handling:**
```python
class WorkflowScheduler:
    def register_scheduled_workflow(self, trigger):
        try:
            # Registration logic
            pass
        except Exception as e:
            raise SchedulerError(f"Failed to register trigger {trigger.id}: {e}")
```

⚠️ **Error Context & Debugging**

Each exception includes:
- **Descriptive Messages**: Clear explanation of what went wrong
- **Context Preservation**: Original error details when wrapping exceptions
- **Type Safety**: Structured hierarchy for proper exception handling
- **Integration**: Compatible with Django's validation and logging systems
"""


class AutomationError(Exception):
    """Base exception for automation module"""
    pass


class InvalidCronExpressionError(AutomationError):
    """Raised when a cron expression is invalid"""
    pass


class SchedulerError(AutomationError):
    """Raised when there's an error with the workflow scheduler"""
    pass


class WorkflowExecutionError(AutomationError):
    """Raised when there's an error executing a workflow"""
    pass
