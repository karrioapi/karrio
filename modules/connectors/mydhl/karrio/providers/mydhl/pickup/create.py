import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.PickupDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = (
        _extract_details(response, settings)
        if "confirmation_number" in response
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    pickup = None  # parse carrier pickup type from "data"

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number="",  # extract confirmation number from pickup
        pickup_date=lib.fdate(""),  # extract tracking event date
    )


def pickup_request(
    payload: models.PickupRequest, settings: provider_utils.Settings
) -> lib.Serializable:

    # map data to convert karrio model to mydhl specific type
    request = None

    return lib.Serializable(request, lib.to_dict)
