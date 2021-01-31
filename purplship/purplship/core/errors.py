"""Purplship Custom Errors(Exception) definition modules"""
import warnings
from enum import Enum
from typing import Dict


class PurplShipError(Exception):
    """Base class for other exceptions."""

    code = "PURPLSHIP_INTERNAL_ERROR"


class PurplShipDetailedError(PurplShipError):
    """Base class for other exceptions."""

    def __init__(self, *args):
        self.details = None
        super().__init__(*args)


class ValidationError(PurplShipError):
    """Base class for other exceptions."""

    code = "PURPLSHIP_VALIDATING_ERROR"


class MethodNotSupportedError(PurplShipError):
    """Raised when a method from a base type is not implemented."""

    code = "PURPLSHIP_NON_SUPPORTED_ERROR"

    def __init__(self, method: str, base: str):
        super().__init__(f"{method} not supported by {base}")


class FieldErrorCode(Enum):
    required = dict(code="required", message="This field is required")
    invalid = dict(code="invalid", message="This field is invalid")
    exceeds = dict(code="exceeds", message="This field exceeds the max value")


class FieldError(PurplShipDetailedError):
    """Raised when one or many required fields are missing."""

    code = "PURPLSHIP_FIELD_ERROR"

    def __init__(self, fields: Dict[str, FieldErrorCode]):
        super().__init__("Invalid request payload")
        self.details = {name: code.value for name, code in fields.items()}


class OriginNotServicedError(PurplShipError):
    """Raised when an origin is not supported by a shipping provider."""

    code = "PURPLSHIP_ORIGIN_NOT_SERVICED_ERROR"

    def __init__(self, origin: str):
        super().__init__(f"Origin address '{origin}' is not serviced")


class DestinationNotServicedError(PurplShipError):
    """Raised when a destination is not supported by a shipping provider."""

    code = "PURPLSHIP_DESTINATION_NOT_SERVICED_ERROR"

    def __init__(self, origin: str):
        super().__init__(f"Destination address '{origin}' is not serviced")


class MultiParcelNotSupportedError(PurplShipError):
    """Raised when an origin is not supported by a shipping provider."""

    code = "PURPLSHIP_MULTI_PARCEL_NOT_SUPPORTED_ERROR"

    def __init__(self):
        super().__init__(f"Multi-parcel shipment not supported")
