from jstruct import struct
from canpar_lib.CanshipBusinessService import (
    GetLabelsAdvancedRq,
    getLabelsAdvanced
)
from purplship.core.utils import (
    create_envelope,
    Serializable,
    Envelope
)
from purplship.providers.canpar.utils import Settings


@struct
class LabelRequest:
    shipment_id: str
    thermal: bool = False


def get_label_request(payload: LabelRequest, settings: Settings) -> Serializable[Envelope]:

    request = create_envelope(
        body_content=getLabelsAdvanced(
            request=GetLabelsAdvancedRq(
                horizontal=False,
                id=payload.shipment_id,
                password=settings.password,
                thermal=payload.thermal,
                user_id=settings.username
            )
        )
    )

    return Serializable(request, Settings.serialize)
