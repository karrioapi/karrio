import karrio.schemas.dhl_universal.tracking as dhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_universal.error as error
import karrio.providers.dhl_universal.utils as provider_utils
import karrio.providers.dhl_universal.units as provider_units

date_formats = [
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S%z",
]


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    errors = [e for e in response if "shipments" not in e]
    details = [
        _extract_detail(lib.to_object(dhl.Shipment, d["shipments"][0]), settings)
        for d in response
        if "shipments" in d
    ]

    return details, error.parse_error_response(errors, settings)


def _extract_detail(
    shipment: dhl.Shipment,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    latest_status = lib.failsafe(
        lambda: (
            shipment.status.statusCode
            or shipment.status.status
            or shipment.events[0].statusCode
        )
    ).lower()
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if latest_status in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )
    shorten_date = lambda _date: _date.split(".")[0] if _date else None

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=str(shipment.id),
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(shorten_date(event.timestamp), try_formats=date_formats),
                description=event.description or event.status or " ",
                location=(
                    event.location.address.addressLocality
                    if event.location is not None and event.location.address is not None
                    else None
                ),
                code=event.statusCode or "",
                time=lib.flocaltime(
                    shorten_date(event.timestamp), try_formats=date_formats
                ),
            )
            for event in shipment.events or []
        ],
        estimated_delivery=lib.fdate(
            shorten_date(shipment.estimatedTimeOfDelivery), try_formats=date_formats
        ),
        delivered=status == "delivered",
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(shipment.id),
            shipment_service=lib.failsafe(lambda: shipment.details.product.productName),
            customer_name=lib.failsafe(
                lambda: (
                    lib.text(
                        shipment.details.receiver.givenName,
                        shipment.details.receiver.familyName,
                    )
                    or lib.text(shipment.details.receiver.name)
                    or lib.text(shipment.details.receiver.organizationName)
                )
            ),
            shipment_destination_country=lib.failsafe(
                lambda: shipment.destination.address.countryCode
            ),
            shipment_destination_postal_code=lib.failsafe(
                lambda: shipment.destination.address.postalCode
            ),
            shipment_origin_country=lib.failsafe(
                lambda: shipment.origin.address.countryCode
            ),
            shipment_origin_postal_code=lib.failsafe(
                lambda: shipment.origin.address.postalCode
            ),
            package_weight=lib.failsafe(lambda: shipment.details.weight.value),
            package_weight_unit=lib.failsafe(lambda: shipment.details.weight.unitText),
            signed_by=lib.failsafe(
                lambda: (
                    lib.text(
                        shipment.details.proofOfDelivery.signed.givenName,
                        shipment.details.proofOfDelivery.signed.familyName,
                    )
                    or lib.text(shipment.details.proofOfDelivery.signed.name)
                )
            ),
        ),
        meta=dict(
            reference=lib.failsafe(lambda: shipment.details.references.number),
        ),
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    request = [
        dhl.TrackingRequest(
            trackingNumber=number,
            language="en",
        )
        for number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
