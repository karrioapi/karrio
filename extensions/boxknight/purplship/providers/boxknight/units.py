from enum import Enum


class Option(Enum):
    boxknight_signature_required = "SAMEDAY"


class Service(Enum):
    boxknight_sameday = "SAMEDAY"
    boxknight_nextday = "NEXTDAY"
    boxknight_scheduled = "SCHEDULED"
