
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [_extract_details(details, settings) for _, details in responses]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = None  # parse carrier tracking object type

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",
        events=[
            models.TrackingEvent(
                date=lib.fdate(""),
                description="",
                code="",
                time=lib.ftime(""),
                location="",
            )
            for event in []
        ],
        estimated_delivery=lib.fdate(""),
        delivered=False,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to mydhl specific type
    request = None

    return lib.Serializable(request, lib.to_dict)
