
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_germany.error as error
import karrio.providers.dhl_germany.utils as provider_utils
import karrio.providers.dhl_germany.units as provider_units


def parse_tracking_response(
    responses: typing.List[typing.Tuple[str, lib.Element]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response_messages = []  # extract carrier response errors
    response_rates = []  # extract carrier response rates

    messages = error.parse_error_response(response_messages, settings)
    trackers = [_extract_details(rate, settings) for rate in response_rates]

    return trackers, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = None  # parse carrier tracking object type

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from tracking
        events=[
            models.TrackingEvent(
                date=lib.fdate(""), # extract tracking event date
                description="",  # extract tracking event description or code
                code="",  # extract tracking event code
                time=lib.ftime(""), # extract tracking event time
                location="",  # extract tracking event address
            )
            for event in []  # extract tracking events
        ],
        estimated_delivery=lib.fdate(""), # extract tracking estimated date if provided
        delivered=False,  # compute tracking delivered status
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = None  # map data to convert karrio model to dhl_germany specific type

    return lib.Serializable(request)
