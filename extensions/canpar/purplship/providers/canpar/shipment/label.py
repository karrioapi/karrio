from jstruct import struct
from pycanpar.CanshipBusinessService import (
    GetLabelsAdvancedRq,
    getLabelsAdvanced
)
from purplship.core.utils import (
    create_envelope,
    Serializable,
    Envelope
)
from purplship.providers.canpar.utils import Settings, default_request_serializer


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

    return Serializable(request, default_request_serializer)
