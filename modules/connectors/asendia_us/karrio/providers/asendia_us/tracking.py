import karrio.schemas.asendia_us.tracking_response as asendia
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.asendia_us.error as error
import karrio.providers.asendia_us.utils as provider_utils
import karrio.providers.asendia_us.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    tracking_details = [
        _extract_details(detail, settings) for detail in response.get("data") or []
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = lib.to_object(asendia.DatumType, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if tracking.trackingMilestoneEvents[0].eventCode in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.trackingNumberVendor,
        events=[
            models.TrackingEvent(
                date=lib.fdate(
                    event.eventOn,
                    (
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                        if "." in event.eventOn
                        else "%Y-%m-%dT%H:%M:%S%z"
                    ),
                ),
                description=event.eventDescription,
                code=event.eventCode,
                time=lib.flocaltime(
                    event.eventOn,
                    (
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                        if "." in event.eventOn
                        else "%Y-%m-%dT%H:%M:%S%z"
                    ),
                ),
                location=lib.text(event.eventLocation),
            )
            for event in tracking.trackingMilestoneEvents
        ],
        delivered=status == "delivered",
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
