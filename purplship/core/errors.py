"""PurplShip Custom Errors(Exception) definition modules"""


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


class RequiredFieldError(ValidationError):
    """Raised when one or many required fields are missing."""

    def __init__(self, field: str):
        super().__init__(f"<{field}> must be specified (required)")


class OriginNotServicedError(PurplShipError):
    """Raised when an origin is not supported by a shipping provider."""

    def __init__(self, origin: str, carrier_name: str):
        super().__init__(f"Origin country '{origin}' is not serviced by {carrier_name}")
