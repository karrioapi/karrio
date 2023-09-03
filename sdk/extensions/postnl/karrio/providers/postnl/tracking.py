import karrio.schemas.postnl.tracking_response as pnl
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.postnl.error as error
import karrio.providers.postnl.utils as provider_utils
import karrio.providers.postnl.units as provider_units


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
        _extract_details(res["CompleteStatus"]["Shipment"], settings)
        for _, res in responses
        if res.get("CompleteStatus", {}).get("Shipment") is not None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment = lib.to_object(pnl.ShipmentType, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if shipment.Status.StatusCode in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.MainBarcode,
        delivered=(status == "delivered"),
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.TimeStamp, "%d-%m-%Y %H:%M:%S"),
                time=lib.ftime(event.TimeStamp, "%d-%m-%Y %H:%M:%S"),
                description=event.Description,
                code=event.LocationCode,
                location=event.RouteName,
            )
            for event in shipment.Event
        ],
        estimated_delivery=lib.fdate(shipment.DeliveryDate, "%Y-%m-%d"),
        meta=dict(
            reference=shipment.Reference,
        ),
        info=models.TrackingInfo(
            customer_name=shipment.Customer.Name,
            shipment_service=shipment.ProductDescription,
            package_weight=shipment.Dimension.Weight,
            package_weight_unit=units.WeightUnit.kg.name,
            shipment_origin_country=lib.failsafe(
                lambda: shipment.Address[0].CountryCode
            ),
            shipment_origin_postal_code=lib.failsafe(
                lambda: shipment.Address[0].Zipcode
            ),
            shipment_destination_country=lib.failsafe(
                lambda: shipment.Address[-1].CountryCode
            ),
            shipment_destination_postal_code=lib.failsafe(
                lambda: shipment.Address[-1].Zipcode
            ),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
