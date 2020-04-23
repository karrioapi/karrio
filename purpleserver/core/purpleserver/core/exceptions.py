from rest_framework.exceptions import ValidationError as DRFValidationError
from purplship.core.errors import ValidationError as PurplShipValidationError


class ValidationError(DRFValidationError, PurplShipValidationError):
    pass
