"""PurplShip Custom Errors(Exception) definition modules"""


class Error(Exception):
    """Base class for other exceptions."""

    pass


class MethodNotSupportedError(Error):
    """Raised when a method from a base type is not implemented."""

    def __init__(self, method: str, base: str):
        super().__init__(f"{method} not supported by {base}")


class OriginNotServicedError(Error):
    """Raised when an origin is not supported by a shipping provider."""

    def __init__(self, origin: str, carrier: str):
        super().__init__(f"Origin country '{origin}' is not serviced by {carrier}")
