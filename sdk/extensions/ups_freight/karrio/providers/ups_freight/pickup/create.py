
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils
import karrio.providers.ups_freight.units as provider_units


def parse_pickup_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response_messages = []  # extract carrier response errors
    response_pickup = None  # extract carrier response pickup

    messages = error.parse_error_response(response_messages, settings)
    pickup = _extract_details(response_pickup, settings)

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
        pickup_date=lib.fdate(""), # extract tracking event date
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings
) -> lib.Serializable:
    request = None  # map data to convert karrio model to ups_freight specific type

    return lib.Serializable(request)
