import karrio.schemas.zoom2u.tracking_response as locate2u
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.zoom2u.error as error
import karrio.providers.zoom2u.utils as provider_utils
import karrio.providers.zoom2u.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
            if response.get("message") is not None
        ],
        [],
    )

    tracking_details = [
        _extract_details(response, settings)
        for _, response in responses
        if response.get("message") is None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = lib.to_object(locate2u.TrackingResponseType, data)
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
        tracking_number=tracking.reference,
        events=[
            models.TrackingEvent(
                date=lib.fdate(tracking.statusChangeDateTime, "%Y-%m-%dT%H:%M:%S.%fZ"),
                description=tracking.status,
                code=tracking.status,
                time=lib.flocaltime(
                    tracking.statusChangeDateTime, "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            )
        ],
        delivered=(status == "delivered"),
        info=models.TrackingInfo(
            carrier_tracking_link=tracking.trackinglink,
        ),
        meta=dict(
            proofOfDeliveryPhotoUrl=data.get("proofOfDeliveryPhotoUrl"),
            signatureUrl=data.get("signatureUrl"),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
