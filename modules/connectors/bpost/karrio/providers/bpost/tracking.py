import karrio.schemas.bpost.tracking_info_v1 as bpost
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.bpost.error as error
import karrio.providers.bpost.utils as provider_utils
import karrio.providers.bpost.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(details, settings)
        for _, details in responses
        if "itemTracking" in getattr(details, "tag", None)
    ]

    return tracking_details, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(bpost.itemTrackingType, data)
    delivery = lib.fdate(details.deliveryTime, "%Y-%m-%dT%H:%M:%S%z")
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(details.stateInfo[0], "stateCode", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.itemCode,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.time, "%Y-%m-%dT%H:%M:%S%z"),
                description=event.stateDescription,
                code=event.stateCode,
                time=lib.flocaltime(event.time, "%Y-%m-%dT%H:%M:%S%z"),
            )
            for event in details.stateInfo
        ],
        estimated_delivery=delivery,
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(details.itemCode),
            customer_name=lib.failsafe(lambda: details.addressee.name),
            expected_delivery=delivery,
            package_weight=lib.failsafe(
                lambda: details.itemDetail.weightInGrams / 1000
            ),
            package_weight_unit=units.WeightUnit.KG,
            shipment_origin_country=lib.failsafe(
                lambda: details.sender.address.countryCode
            ),
            shipment_origin_postal_code=lib.failsafe(
                lambda: details.sender.address.postalCode
            ),
            shipment_destination_country=lib.failsafe(
                lambda: details.addressee.address.countryCode
            ),
            shipment_destination_postal_code=lib.failsafe(
                lambda: details.addressee.address.postalCode
            ),
        ),
        meta=dict(
            costCenter=details.costCenter,
            trackingId=details.trackingId,
            reference=details.customerReference,
            pickup_point=lib.text(
                getattr(details.pickupPoint, "houseNumber", "").strip(),
                getattr(details.pickupPoint, "streetName", "").strip(),
                getattr(details.pickupPoint, "postalCode", "").strip(),
                getattr(details.pickupPoint, "city", "").strip(),
            ),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
