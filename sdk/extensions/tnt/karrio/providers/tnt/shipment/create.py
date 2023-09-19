import karrio.schemas.tnt.shipping_request as tnt
import karrio.schemas.tnt.shipping_response as shipping
import karrio.schemas.tnt.shipping_common_definitions as common
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.utils as provider_utils
import karrio.providers.chronopost.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[lib.Message]]:
    response = _response.deserialize()
    shipment = _extract_detail(response, settings)

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_detail(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Optional[models.ShipmentDetails]:
    activity: shipping.document = lib.findElements(
        "document", response, element_type=shipping.document, first=True
    )

    if activity is None or activity.CREATE.SUCCESS != "Y":
        return None

    # label = parse_label_response(response)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=activity.CREATE.CONNUMBER,
        shipment_identifier=activity.CREATE.CONREF,
        docs=models.Documents(label=""),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = None

    return lib.Serializable(request)
