from purplship.core.utils import Enum


class Option(Enum):
    boxknight_signature_required = "signature_required"


class Service(Enum):
    boxknight_sameday = "SAMEDAY"
    boxknight_nextday = "NEXTDAY"
    boxknight_scheduled = "SCHEDULED"
