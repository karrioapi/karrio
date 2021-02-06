from purplship.core.utils import Enum, Spec


class Option(Enum):
    boxknight_signature_required = Spec.asFlag("signature_required")

    """ Unified Option type mapping """
    signature_confirmation = boxknight_signature_required


class Service(Enum):
    boxknight_sameday = "SAMEDAY"
    boxknight_nextday = "NEXTDAY"
    boxknight_scheduled = "SCHEDULED"
