import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hay_post.error as error
import karrio.providers.hay_post.units as provider_units
import karrio.providers.hay_post.utils as provider_utils
import karrio.schemas.hay_post.order_tracking_response as hay_post

from datetime import datetime


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    tracking_details = [
        _extract_details(response, settings) if response.get("key") is None else None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    detail = lib.to_object(hay_post.OrderTrackingResponseType, data)

    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if detail.order.stateId in status.value
        ),
        provider_units.TrackingStatus.delivered.name,
    )

    return models.TrackingDetails(
        tracking_number=detail.order.trackingId,
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        info=models.TrackingInfo(
            customer_name=f"{detail.customer.firstName} {detail.customer.lastName}",
            note=detail.order.comment,
            order_date=lib.fdate(detail.order.createDate, "%Y-%m-%dT%H:%M:%S"),
            order_id=str(detail.order.id),
            package_weight=str(detail.order.weight),
            shipment_pickup_date=lib.fdate(
                detail.order.createDate, "%Y-%m-%dT%H:%M:%S"
            ),
            shipment_service=detail.order.service.name,
            shipment_origin_country=detail.returnAddress.country.name,
            shipment_origin_postal_code=detail.returnAddress.postalCode,
            shipment_destination_country=detail.orderDestinationAddress.country.name,
            shipment_destination_postal_code=detail.orderDestinationAddress.country.name,
        ),
        events=[
            models.TrackingEvent(
                date=lib.fdate(detail.order.createDate, "%Y-%m-%dT%H:%M:%S"),
                description=(
                    detail.order.comment if detail.order.comment else "No description"
                ),
                code=detail.order.transactionId,
                time=lib.fdate(detail.order.createDate, "%Y-%m-%dT%H:%M:%S"),
                location=detail.orderDestinationAddress.address,
            )
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
