import karrio.schemas.amazon_shipping.tracking_response as amazon
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.amazon_shipping.error as error
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()
    errors: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, dict(tracking_number=id))
            for id, response in responses
            if "errors" in response
        ],
        [],
    )
    trackers = [
        _extract_details(response, settings)
        for _, response in responses
        if "errors" not in response
    ]

    return trackers, errors


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(amazon.TrackingResponse, data)
    delivered = details.summary.status == "Delivered"
    estimated_delivery = lib.fdate(details.promisedDeliveryDate, "%Y-%m-%dT%H:%M:%SZ")

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.trackingId,
        estimated_delivery=estimated_delivery,
        delivered=delivered,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventTime, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.eventCode,
                code=event.eventCode,
                time=lib.flocaltime(event.eventTime, "%Y-%m-%dT%H:%M:%SZ"),
                location=lib.join(
                    event.location.city,
                    event.location.stateOrRegion,
                    event.location.postalCode,
                    event.location.countryCode,
                    join=True,
                    separator=", ",
                ),
            )
            for event in details.eventHistory
        ],
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    return lib.Serializable(payload.tracking_numbers)
