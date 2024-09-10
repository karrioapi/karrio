import karrio.schemas.locate2u.tracking_response as locate2u
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.locate2u.error as error
import karrio.providers.locate2u.utils as provider_utils
import karrio.providers.locate2u.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
            if response.get("error") is not None
        ],
        [],
    )

    tracking_details = [
        _extract_details(response, settings)
        for _, response in responses
        if response.get("error") is None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = lib.to_object(locate2u.TrackingResponse, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if tracking.status in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=str(tracking.stopId),
        events=[
            models.TrackingEvent(
                date=lib.fdate(tracking.lastModifiedDate, "%Y-%m-%dT%H:%M:%S.%fZ"),
                description=tracking.status,
                code=tracking.status,
                time=lib.flocaltime(tracking.lastModifiedDate, "%Y-%m-%dT%H:%M:%S.%fZ"),
                latitude=tracking.location.latitude,
                longitude=tracking.location.longitude,
            )
        ],
        estimated_delivery=lib.fdate(tracking.arrivalDate, "%Y-%m-%dT%H:%M:%S%z"),
        delivered=(status == "delivered"),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
