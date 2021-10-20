from purplship.core.utils import Enum, Flag, Spec


class Service(Enum):
    ics_courier_nextday = 'ND'
    ics_courier_ground = 'GR'


class Option(Flag):
    ics_courier_cost_center = Spec.asValue("CostCenter")
    ics_courier_special_instruction = Spec.asValue("SpecialInstruction")
    ics_courier_no_signature_required = Spec.asFlag("NoSignatureRequired")
