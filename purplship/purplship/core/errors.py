"""Purplship Custom Errors(Exception) definition modules"""
import warnings
from enum import Enum
from typing import Dict


class DeprecatedClass:
    deprecation_message = "This class is deprecated and will be removed soon"

    def __init__(self, *args, **kwargs):
        warnings.warn(self.deprecation_message, DeprecationWarning)
        super().__init__(*args, **kwargs)


class FieldErrorCode(Enum):
    required = dict(code="required", message="This field is required")
    invalid = dict(code="invalid", message="This field is invalid")
    exceeds = dict(code="exceeds", message="This field exceeds the max value")


class ShippingSDKError(Exception):
    """Base class for other exceptions."""

    code = "SHIPPING_SDK_INTERNAL_ERROR"


class ShippingSDKDetailedError(ShippingSDKError):
    """Base class for other exceptions."""

    def __init__(self, *args):
        self.details = None
        super().__init__(*args)


class FieldError(ShippingSDKDetailedError):
    """Raised when one or many required fields are missing."""

    code = "SHIPPING_SDK_FIELD_ERROR"

    def __init__(self, fields: Dict[str, FieldErrorCode]):
        super().__init__("Invalid request payload")
        self.details = {name: code.value for name, code in fields.items()}


class ValidationError(ShippingSDKError):
    """Base class for other exceptions."""

    code = "SHIPPING_SDK_VALIDATING_ERROR"


class MethodNotSupportedError(ShippingSDKError):
    """Raised when a method from a base type is not implemented."""

    code = "SHIPPING_SDK_NON_SUPPORTED_ERROR"

    def __init__(self, method: str, base: str):
        super().__init__(f"{method} not supported by {base}")


class OriginNotServicedError(ShippingSDKError):
    """Raised when an origin is not supported by a shipping provider."""

    code = "SHIPPING_SDK_ORIGIN_NOT_SERVICED_ERROR"

    def __init__(self, origin: str):
        super().__init__(f"Origin address '{origin}' is not serviced")


class DestinationNotServicedError(ShippingSDKError):
    """Raised when a destination is not supported by a shipping provider."""

    code = "SHIPPING_SDK_DESTINATION_NOT_SERVICED_ERROR"

    def __init__(self, origin: str):
        super().__init__(f"Destination address '{origin}' is not serviced")


class MultiParcelNotSupportedError(ShippingSDKError):
    """Raised when an origin is not supported by a shipping provider."""

    code = "SHIPPING_SDK_MULTI_PARCEL_NOT_SUPPORTED_ERROR"

    def __init__(self):
        super().__init__(f"Multi-parcel shipment not supported")


"""Deprecated Custom Errors"""


class PurplShipError(Exception, DeprecatedClass):
    """Base class for other exceptions."""

    code = "SHIPPING_SDK_INTERNAL_ERROR"
    deprecation_message = "PurplShipError is deprecated and will be removed soon. use ShippingSDKError instead"


class PurplShipDetailedError(PurplShipError):
    """Base class for other exceptions."""

    def __init__(self, *args):
        self.details = None
        super().__init__(*args)
