import karrio.schemas.nationex.tracking_response as nationex
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.nationex.error as error
import karrio.providers.nationex.utils as provider_utils
import karrio.providers.nationex.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(res, settings, tracking_number=number)
            for number, res in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(res, settings)
        for _, res in responses
        if res.get("code") is None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment = lib.to_object(nationex.TrackingResponseType, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if shipment.ShipmentStatus in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=str(shipment.ShipmentId),
        delivered=status == "delivered",
        status=status,
        events=[
            models.TrackingEvent(
                code=event.ShipmentStatus,
                location=event.LastLocation,
                date=lib.fdate(event.StatusDate, "%Y-%m-%dT%H:%M:%SZ"),
                time=lib.flocaltime(event.StatusDate, "%Y-%m-%dT%H:%M:%SZ"),
                description=(
                    event.ShipmentStatusFr
                    if settings.language == "fr"
                    else event.ShipmentStatusEn
                ),
                latitude=None,
                longitude=None,
            )
            for event in shipment.StatusHistories
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(shipment.ShipmentId),
            shipping_date=lib.fdate(shipment.ExpeditionDate, "%Y-%m-%d"),
            shipment_package_count=shipment.TotalParcels,
            shipment_service=shipment.ShipmentType,
            package_weight=shipment.TotalWeight,
            shipment_origin_postal_code=getattr(shipment.Sender, "PostalCode", None),
            shipment_destination_postal_code=getattr(
                shipment.Destination, "PostalCode", None
            ),
            shipment_destination_country="CA",
            shipment_origin_country="CA",
            note=shipment.Note,
        ),
        meta=dict(
            reference=shipment.ReferenceNumber,
            accounty_number=str(shipment.BillingAccount),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
