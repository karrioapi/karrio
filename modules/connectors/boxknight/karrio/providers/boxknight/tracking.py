import datetime
import karrio.schemas.boxknight.tracking_response as boxknight
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.boxknight.error as error
import karrio.providers.boxknight.utils as provider_utils
import karrio.providers.boxknight.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(res, settings, tracking_number=number)
            for number, res in responses
            if res.get("error") is not None
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(res, settings)
        for _, res in responses
        if res.get("error") is None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    order = lib.to_object(boxknight.TrackingResponse, data)
    delivered = order.orderStatus == "DELIVERY_COMPLETED"

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=order.id,
        events=[
            models.TrackingEvent(
                description=order.orderStatus,
                code=order.orderStatus,
                date=lib.fdate(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"),
                time=lib.flocaltime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"),
            )
        ],
        delivered=delivered,
        meta=dict(reference=order.refNumber),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(order.id),
            customer_name=getattr(order.recipient, "name", None),
            shipment_package_count=order.packageCount,
            shipment_service=order.service,
            shipment_origin_postal_code=getattr(
                order.originAddress, "postalCode", None
            ),
            shipment_origin_country=units.Country.map(
                getattr(order.originAddress, "country", None)
            ).name,
            shipment_destination_postal_code=getattr(
                order.recipientAddress, "postalCode", None
            ),
            shipment_destination_country=units.Country.map(
                getattr(order.recipientAddress, "country", None)
            ).name,
            shipping_date=lib.fdate(order.createdAt, "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [dict(order_id=number) for number in payload.tracking_numbers]

    return lib.Serializable(request)
