"""Karrio Custom Errors(Exception) definition modules"""

import enum
import typing


class FieldErrorCode(enum.Enum):
    required = dict(code="required", message="This field is required")
    invalid = dict(code="invalid", message="This field is invalid")
    exceeds = dict(code="exceeds", message="This field exceeds the max value")


class ShippingSDKError(Exception):
    """Base class for other exceptions."""

    code = "SHIPPING_SDK_INTERNAL_ERROR"


class ShippingSDKDetailedError(ShippingSDKError):
    """Base class for other exceptions."""

    def __init__(self, *args, details=None):
        self.details = details
        super().__init__(*args)


class FieldError(ShippingSDKDetailedError):
    """Raised when one or many required fields are missing."""

    code = "SHIPPING_SDK_FIELD_ERROR"

    def __init__(self, fields: typing.Dict[str, FieldErrorCode]):
        super().__init__("Invalid request payload")
        self.details = {name: code.value for name, code in fields.items()}


class ParsedMessagesError(ShippingSDKDetailedError):
    """Raised when one or many required fields are missing."""

    code = "SHIPPING_SDK_FIELD_ERROR"

    def __init__(self, messages=[]):
        super().__init__("Invalid request payload")
        self.messages = messages


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
