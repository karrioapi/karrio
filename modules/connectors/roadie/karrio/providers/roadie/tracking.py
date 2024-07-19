import karrio.schemas.roadie.tracking_response as roadie
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.roadie.error as error
import karrio.providers.roadie.utils as provider_utils
import karrio.providers.roadie.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.Union[dict, typing.List[dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    responses = response if isinstance(response, list) else [response]
    messages = error.parse_error_response(responses, settings)

    tracking_details = [
        _extract_details(res, settings)
        for res in responses
        if res.get("errors") is None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment = lib.to_object(roadie.Shipment, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if shipment.events[0].name in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.tracking_number,
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.occurred_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                description=event.name,
                code=event.name,
                time=lib.flocaltime(event.occurred_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                latitude=getattr(event.location, "latitude", None),
                longitude=getattr(event.location, "longitude", None),
            )
            for event in shipment.events
        ],
        estimated_delivery=lib.fdate(
            getattr(shipment.deliver_between, "end", None), "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        delivered=status == "delivered",
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(
                shipment.tracking_number
            ),
            customer_name=getattr(shipment.delivery_location.contact, "name", None),
            shipping_date=lib.failsafe(
                lib.fdate(shipment.created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            ),
            signed_by=shipment.signatory_name,
            shipment_origin_country="US",
            shipment_destination_country="US",
            shipment_origin_postal_code=shipment.pickup_location.address.zip,
            shipment_destination_postal_code=shipment.delivery_location.address.zip,
            package_weight=sum([_.weight or 0.0 for _ in shipment.items], start=0.0),
            package_weight_unit=units.WeightUnit.LB.name,
            shipment_package_count=len(shipment.items),
        ),
        meta=dict(
            reference=shipment.reference_id,
            shipment_id=str(shipment.id),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
