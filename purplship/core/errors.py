"""PurplShip Custom Errors(Exception) definition modules"""
import warnings
from enum import Enum
from typing import Dict


class PurplShipError(Exception):
    """Base class for other exceptions."""

    pass


class ValidationError(PurplShipError):
    """Base class for other exceptions."""

    pass


class MethodNotSupportedError(PurplShipError):
    """Raised when a method from a base type is not implemented."""

    def __init__(self, method: str, base: str):
        super().__init__(f"{method} not supported by {base}")


class ErrorCode(Enum):
    required = dict(code="required", message="This field is required")
    invalid = dict(code="invalid", message="This field is invalid")


class FieldError(ValidationError):
    """Raised when one or many required fields are missing."""

    def __init__(self, fields: Dict[str, ErrorCode]):
        self.details = {name: code.value for name, code in fields.items()}
        super().__init__("Invalid request payload")


class RequiredFieldError(ValidationError):
    """Raised when one or many required fields are missing."""

    def __init__(self, field: str):
        warnings.warn("deprecated use FieldError instead.", DeprecationWarning)
        super().__init__(f"<{field}> must be specified (required)")


class OriginNotServicedError(PurplShipError):
    """Raised when an origin is not supported by a shipping provider."""

    def __init__(self, origin: str, carrier_name: str):
        super().__init__(f"Origin country '{origin}' is not serviced by {carrier_name}")
