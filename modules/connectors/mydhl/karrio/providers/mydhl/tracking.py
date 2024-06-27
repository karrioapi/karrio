import karrio.schemas.mydhl.tracking_request as mydhl
import karrio.schemas.mydhl.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages: typing.List[models.Message] = error.parse_error_response(
        response, settings
    )
    tracking_details = [
        _extract_details(details, settings)
        for _, details in response.get("shipments", [])
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(tracking.ShipmentType, data)
    last_event = next(iter(details.events), None)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(last_event, "typeCode", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.shipmentTrackingNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.date, "%Y-%m-%d"),
                time=lib.ftime(event.time, "%H:%M:%S"),
                description=event.description,
                code=event.typeCode,
                location=lib.failsafe(lambda: event.serviceArea[0].description, ""),
            )
            for event in details.events
        ],
        estimated_delivery=lib.fdate(details.estimatedDeliveryDate, "%Y-%m-%d"),
        delivered=(status == provider_units.TrackingStatus.delivered.name),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(
                details.shipmentTrackingNumber
            ),
            shipping_date=lib.fdate(details.shipmentTimestamp, "%Y-%m-%dT%H:%M:%S"),
            shipment_service=provider_units.ShippingService.map(
                details.productCode
            ).name_or_key,
            shipment_package_count=details.numberOfPieces,
            expected_delivery=lib.fdate(details.estimatedDeliveryDate, "%Y-%m-%d"),
            customer_name=lib.failsafe(lambda: details.shipperDetails.name),
            signed_by=next(_.signedBy for _ in details.events if any(_.signedBy or "")),
            package_weight=lib.to_decimal(details.totalWeight),
            package_weight_unit=lib.identity(
                units.WeightUnit.KG.name
                if details.unitOfMeasurements == "metric"
                else units.WeightUnit.LB.name
            ),
            shipment_origin_country=lib.failsafe(
                lambda: details.shipperDetails.postalAddress.countryCode
            ),
            shipment_origin_postal_code=lib.failsafe(
                lambda: details.shipperDetails.postalAddress.postalCode
            ),
            shipment_destination_country=lib.failsafe(
                lambda: details.receiverDetails.postalAddress.countryCode
            ),
            shipment_destination_postal_code=lib.failsafe(
                lambda: details.receiverDetails.postalAddress.postalCode
            ),
        ),
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to mydhl specific type
    request = mydhl.TrackingRequestType(
        shipmentTrackingNumber=payload.tracking_numbers,
        pieceTrackingNumber=[],
        shipmentReference=None,
        shipmentReferenceType=None,
        shipperAccountNumber=None,
        dateRangeFrom=None,
        dateRangeTo=None,
        trackingView="all-checkpoints",
        levelOfDetail="all",
        requestControlledAccessDataCodes=None,
    )

    return lib.Serializable(request, lib.to_dict)
