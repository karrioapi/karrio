import karrio.schemas.colissimo.tracking_response as colissimo
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.colissimo.error as error
import karrio.providers.colissimo.utils as provider_utils
import karrio.providers.colissimo.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.Union[dict, typing.List[dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    responses = response if isinstance(response, list) else [response]
    messages = error.parse_laposte_error_response(responses, settings)
    tracking_details = [
        _extract_details(res["shipment"], settings)
        for res in responses
        if str(res.get("returnCode")).startswith("20")
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment = lib.to_object(colissimo.Shipment, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if shipment.event[0].code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.idShip,
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.date, "%Y-%m-%dT%H:%M:%S%z"),
                description=event.label,
                code=event.code,
                time=lib.flocaltime(event.date, "%Y-%m-%dT%H:%M:%S%z"),
            )
            for event in shipment.event
        ],
        estimated_delivery=lib.fdate(shipment.deliveryDate, "%Y-%m-%dT%H:%M:%S%z"),
        delivered=shipment.isFinal,
        info=models.TrackingInfo(
            carrier_tracking_link=shipment.url,
            expected_delivery=lib.fdate(shipment.estimDate, "%Y-%m-%dT%H:%M:%S%z"),
            shipment_service=shipment.product,
            shipping_date=lib.fdate(shipment.entryDate, "%Y-%m-%dT%H:%M:%S%z"),
            shipment_origin_country=getattr(
                shipment.contextData, "originCountry", None
            ),
            shipment_destination_country=getattr(
                shipment.contextData, "arrivalCountry", None
            ),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
